import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def get_project_path(*parts):
    return os.path.abspath(os.path.join(PROJECT_ROOT, *parts))


def ensure_project_dir(*parts):
    path = get_project_path(*parts)
    os.makedirs(path, exist_ok=True)
    return path


def get_project_file(*parts):
    return get_project_path(*parts)
