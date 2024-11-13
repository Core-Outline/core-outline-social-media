from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path('./', '.env')
load_dotenv(dotenv_path=env_path)

env_var = os.environ


snowflake_username = env_var['SNOWFLAKE_USERNAME']
snowflake_password = env_var['SNOWFLAKE_PASSWORD']
snowflake_database = env_var['SNOWFLAKE_DATABASE']
snowflake_account= env_var['SNOWFLAKE_ACCOUNT']
snowflake_warehouse= env_var['SNOWFLAKE_WAREHOUSE']
snowflake_schema= env_var['SNOWFLAKE_SCHEMA']