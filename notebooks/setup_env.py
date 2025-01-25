import os

def setup_environment(expected_dir: str = "WFC-RI") -> None:
    """
    Ensures the working directory is set to the expected parent directory.
    """
    if not os.getcwd().endswith(expected_dir):
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        os.chdir(parent_dir)
