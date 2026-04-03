-- ============================================================
-- Snowflake Tasks to run the dbt pipeline
-- ============================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE ECOM_WH;
USE DATABASE ECOM_ANALYTICS;

-- ============================================================
-- Task 1: Scheduled – run dbt every 15 minutes via CRON
-- ============================================================
CREATE OR REPLACE TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_SCHEDULED
  WAREHOUSE = ECOM_WH
  SCHEDULE  = 'USING CRON */15 * * * * America/Los_Angeles'
  COMMENT   = 'Run ECOM_PIPELINE dbt project every 15 minutes'
AS
  EXECUTE DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE
    ARGS = 'run';

-- ============================================================
-- Task 2: Stream-driven – run dbt when RAW_ORDERS has new data
-- ============================================================
CREATE OR REPLACE TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_ON_NEW_ORDERS
  WAREHOUSE = ECOM_WH
  SCHEDULE  = '1 MINUTE'
  COMMENT   = 'Run ECOM_PIPELINE when new rows land in RAW_ORDERS'
  WHEN
    SYSTEM$STREAM_HAS_DATA('ECOM_ANALYTICS.RAW.RAW_ORDERS_STREAM')
AS
  EXECUTE DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE
    ARGS = 'run';

-- ============================================================
-- Resume tasks (tasks are created in SUSPENDED state)
-- ============================================================
ALTER TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_SCHEDULED RESUME;
ALTER TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_ON_NEW_ORDERS RESUME;

-- ============================================================
-- Verify
-- ============================================================
SHOW TASKS IN SCHEMA ECOM_ANALYTICS.PUBLIC;

-- ============================================================
-- Useful management commands (commented out)
-- ============================================================
-- ALTER TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_SCHEDULED SUSPEND;
-- ALTER TASK ECOM_ANALYTICS.PUBLIC.TASK_DBT_ON_NEW_ORDERS SUSPEND;
-- SELECT * FROM TABLE(ECOM_ANALYTICS.INFORMATION_SCHEMA.TASK_HISTORY()) ORDER BY SCHEDULED_TIME DESC LIMIT 10;
