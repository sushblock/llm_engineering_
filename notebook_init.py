import os
import sys
from dotenv import load_dotenv

def setup_path(root_markers=('cookbook', '.git', 'requirements.txt', '.env')):
    """
    Automatically:
      ✅ Detects your project root
      ✅ Adds it to sys.path
      ✅ Loads .env variables if present

    Parameters:
        root_markers (tuple): Folder/file names that mark the project root.
    Returns:
        str: Path to detected project root.
    """
    current_dir = os.getcwd()
    last_dir = None

    # Walk up directories to find a project root
    while current_dir != last_dir:
        if any(os.path.exists(os.path.join(current_dir, marker)) for marker in root_markers):
            project_root = current_dir
            break
        last_dir = current_dir
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    else:
        # fallback if no marker found
        project_root = os.getcwd()
        print("⚠️ Could not auto-detect project root, using current directory.")

    # Add project root to sys.path if not already there
    if project_root not in sys.path:
        sys.path.append(project_root)

    # Load environment variables from .env if it exists
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
        print(f"🔐 Loaded environment variables from: {env_path}")
    else:
        print("⚠️ No .env file found at project root.")

    print(f"📦 Project root added to sys.path:\n   {project_root}")
    return project_root
