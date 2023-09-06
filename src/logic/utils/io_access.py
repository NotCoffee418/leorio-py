import os

# relative to src/utils/io_access.py


def get_path(*path_parts):
    """Get a path relative to the repo root by joining the path parts."""
    path = os.path.join(get_repo_root(), *path_parts)
    ensure_parent_dir_exists(path)
    return path


def get_repo_root():
    """Find the repository root directory"""
    current_path = os.path.abspath(__file__)
    while True:
        if os.path.basename(current_path) == "leorio-py":
            return current_path

        parent = os.path.dirname(current_path)

        if parent == current_path:
            raise Exception(
                "'leorio' directory not found in any parent directories.")

        current_path = parent


def ensure_parent_dir_exists(path):
    """Ensure the parent directory of the given path exists."""
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
