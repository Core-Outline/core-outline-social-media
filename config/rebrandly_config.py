from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path('./', '.env')
load_dotenv(dotenv_path=env_path)

env_var = os.environ

rebrandly_api = env_var['REBRANDLY_API']
rebrandly_base_url = env_var['REBRANDLY_BASE_URL']