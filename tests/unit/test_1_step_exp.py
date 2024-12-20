import pytest
import os
from src.factories.experiment_factory import ExperimentFactory
from src.models import ConstructionFile, PCR, LabPacket, LabSheet, Inventory
from utils.serialization import *
from src.utils.write_out import write_experiment_output

@pytest.fixture
def setup_experiment_factory():
    # Set up test data
    experiment_factory = ExperimentFactory()


    # Example Experiment with 1 PCR step, to generate 3 lab sheets
    pcr1 = PCR('PCR', 'pcrpdt', 'ca1067F', 'ca1067R', 'pSB1AK3-b0015', 1000)
    cf_list = [ConstructionFile(steps=[pcr1], sequences={})]
    inventory = Inventory(boxes=[], construct_to_locations={}, loc_to_conc={}, loc_to_clone={}, loc_to_culture={})

    # Run the experiment factory to create the Experiment object
    experiment = experiment_factory.run("test_1_step_exp", "A", cf_list, inventory)

    return experiment

def test_one_step_experiment_output(setup_experiment_factory, tmpdir):
    """
    Tests the writing of a 1-step Experiment output to the specified directory.
    """
    experiment = setup_experiment_factory  # Use the Experiment object directly
    output_dir = tmpdir.mkdir("output")
    print(serialize(experiment.cfs[0].steps[0]))


    # Write experiment output in one step
    write_experiment_output(experiment, str(output_dir))

    # Validate experiment directory
    experiment_dir = os.path.join(output_dir, experiment.name)
    assert os.path.exists(experiment_dir), "Experiment directory was not created."

    # Validate metadata.txt
    metadata_file = os.path.join(experiment_dir, "metadata.txt")
    assert os.path.exists(metadata_file), "metadata.txt was not created."

    # Validate Experiment.json
    experiment_json_file = os.path.join(experiment_dir, "Experiment.json")
    assert os.path.exists(experiment_json_file), "Experiment.json was not created."

    # Validate LabPacket directory
    lab_packet_dir = os.path.join(experiment_dir, "LabPacket")
    assert os.path.exists(lab_packet_dir), "LabPacket directory was not created."
    assert len(os.listdir(lab_packet_dir)) == len(experiment.labPacket.labsheets), "LabSheets were not saved correctly."

    # Validate Inventory directory
    inventory_dir = os.path.join(experiment_dir, "Inventory")
    assert os.path.exists(inventory_dir), "Inventory directory was not created."
    inventory_json_file = os.path.join(inventory_dir, "Inventory.json")
    assert os.path.exists(inventory_json_file), "Inventory.json was not created."


