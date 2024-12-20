import pytest
from .cleanup_test_output import cleanup_output_folder

# housekeeping function to keep tests/output from overflowing with LabPackets etc.
# also to test reproducibility of results and creation of folder structure
# Uncomment to enable

@pytest.fixture(scope="session", autouse=True)
def run_cleanup_before_tests():
    cleanup_output_folder()

