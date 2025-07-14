import re
import shutil
import os

def clean_collection_name(name: str) -> str:
    name = name.strip().replace(" ", "-")
    name = re.sub(r"[^a-zA-Z0-9._-]", "", name)
    name = re.sub(r"^[^a-zA-Z]+", "", name)
    name = re.sub(r"[^a-zA-Z0-9]+$", "", name)
    return name if len(name) >= 3 else f"col-{name}"

def clean_pycache():
    pycache_path = os.path.join(os.path.dirname(__file__), "__pycache__")
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path, ignore_errors=True)
