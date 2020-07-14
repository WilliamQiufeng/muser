import importlib.util
import io
import os
import sys
import subprocess

args = [sys.executable, "-m", "pip", "install", "dulwich"]
subprocess.check_call(args)
from dulwich import porcelain

repo_path: str = input(
    "Where do you want to install the game [path/n/empty]: ")
if repo_path.strip() == "" or repo_path == "n":
    repo_path = "muser"
repo = None
if os.path.exists(repo_path):
    print("Repo already exists. Opening...")
    repo = porcelain.open_repo(repo_path)
else:
    print("Repo doesn't exist. Cloning...")
    os.mkdir(repo_path)
    repo = porcelain.clone("https://github.com/Qiufeng54321/muser", repo_path)
print("Fetching Repo...")
porcelain.fetch(repo)
print("Pulling Repo...")
porcelain.pull(repo)
print("Running game_setup.py...")

sys.path.append("muser/muser/")
spec = importlib.util.spec_from_file_location(
    "game_setup", os.path.join(repo_path, "muser", "game_setup.py"))
game_setup_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_setup_module)

print("Finished.")
