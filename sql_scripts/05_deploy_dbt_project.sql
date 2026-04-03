-- ============================================================
-- Deploy dbt project as Snowflake-native DBT PROJECT object
-- ============================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE ECOM_WH;
USE DATABASE ECOM_ANALYTICS;

-- 1. Create an internal stage to hold the dbt project files
CREATE STAGE IF NOT EXISTS ECOM_ANALYTICS.PUBLIC.DBT_STAGING
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- 2. Upload dbt project files to the stage
--    Run these PUT commands from SnowSQL or the Snowflake CLI:
--
--    PUT 'file:///path/to/ecom_analytics/dbt_project.yml'                                  @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/profiles.yml'                                     @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/macros/generate_schema_name.sql'                  @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/macros AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/stg_customers.sql'                 @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/stg_orders.sql'                    @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/stg_order_items.sql'               @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/stg_products.sql'                  @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/_schema.yml'                       @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/staging/_sources.yml'                      @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/staging AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/intermediate/int_customer_orders.sql'      @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/intermediate AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/intermediate/int_order_items_enriched.sql' @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/intermediate AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/intermediate/_schema.yml'                  @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/intermediate AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/marts/dim_customers.sql'                   @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/marts AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/marts/dim_products.sql'                    @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/marts AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/marts/fct_orders.sql'                      @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/marts AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/marts/_schema.yml'                         @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/marts AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/metrics/customer_ltv.sql'                  @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/metrics AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/metrics/daily_revenue.sql'                 @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/metrics AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/metrics/product_performance.sql'           @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/metrics AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--    PUT 'file:///path/to/ecom_analytics/models/metrics/_schema.yml'                       @ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline/models/metrics AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- 3. Create the DBT PROJECT object from staged files
CREATE OR REPLACE DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE
  FROM '@ECOM_ANALYTICS.PUBLIC.DBT_STAGING/ecom_pipeline';

-- 4. Verify deployment
DESCRIBE DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE;
SHOW VERSIONS IN DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE;

-- 5. Execute the pipeline (run all models)
-- EXECUTE DBT PROJECT ECOM_ANALYTICS.PUBLIC.ECOM_PIPELINE
--   ARGS = 'run';
