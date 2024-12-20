import os
import pytest
from utils.saver import Serializer

# Mock Experiment class for testing
class MockExperiment:
    def __init__(self, name, oligos, nameToPoly):
        self.name = name
        self.oligos = oligos
        self.nameToPoly = nameToPoly

# Test function
def test_serialize_metadata_creates_file(tmpdir):
    """
    Test if serialize_metadata creates a metadata file in the specified directory.
    """
    # Create mock data for the test
    experiment_name = "Test Experiment"
    oligos = ["Oligo1", "Oligo2"]
    nameToPoly = {
        "PolyA": type("MockPoly", (object,), {"sequence": "ATCGATCG"}),
        "PolyB": type("MockPoly", (object,), {"sequence": "CGTACGTA"}),
    }

    # Create a mock Experiment object
    experiment = MockExperiment(name=experiment_name, oligos=oligos, nameToPoly=nameToPoly)

    # Create a Serializer instance
    serializer = Serializer()

    # Use pytest's tmpdir fixture to create a temporary directory
    output_dir = tmpdir.mkdir("experiment_outputs")

    # Call the function to test
    serializer.save_metadata(experiment, str(output_dir))

    # Assert that the metadata file was created
    metadata_file = os.path.join(output_dir, "metadata.txt")
    assert os.path.exists(metadata_file), "Metadata file was not created!"

    # Optional: Print the contents of the file for debugging (can be removed in production)
    with open(metadata_file, "r") as f:
        print(f.read())
