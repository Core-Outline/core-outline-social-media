import os
import subprocess
os.chdir(f"{os.getcwd()}")
latestCommit = subprocess.run(
    ['bash', '../app_container/scripts/dvc_upload.sh'], shell=False, capture_output=True)
print(latestCommit)
