python -m venv snf
snf\Scripts\activate


pip install pipx
pipx install snowflake-cli --force

pipx ensurepath

snow --version

New-Item -ItemType Directory -Path "C:\temp" -Force
$env:TEMP = "C:\temp"
irm https://ai.snowflake.com/static/cc-scripts/install.ps1 | iex

cortex --version

EKJGUYM-FL96854.snowflakecomputing.com

to remove old connection

Remove-Item "$env:USERPROFILE\.snowflake\connections.toml"



cd /path/to/your/project

git init
git add .
git commit -m "Initial commit: E-Commerce Realtime Pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main