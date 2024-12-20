import pytest
import os
from src.factories.experiment_factory import ExperimentFactory
from src.models import ConstructionFile, PCR, Digest, Ligate, Transform, LabPacket, LabSheet, Inventory
from utils.saver import Serializer
from src.models.labplanner import Reagent


@pytest.fixture
def setup_experiment_factory():
    # Set up test data
    experiment_factory = ExperimentFactory()
    serializer = Serializer()

    # Example Steps
    pcr1 = PCR('PCR', 'pcrpdt', 'ca1067F', 'ca1067R', 'pSB1AK3-b0015', 1000)
    dig1 = Digest('Digest', 'pcrdig', 'pcrpdt', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
    dig2 = Digest('Digest', 'vectdig', 'pSB1A2-I13521', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
    lig = Ligate('Ligate', 'pSB1A2-Bca9128', ['pcrdig', 'vectdig'])
    trans = Transform('Transform', 'finalpdt', 'pSB1A2-Bca9128', 'Mach1', ['Amp'], 37)
    seqs = {'pSB1A2-I13521': 'randomsequencehere'}

    pcr2 = PCR('PCR', 'pcrOutput', 'oligoF', 'oligoR', 'template', 500)

    cf_list = [
        ConstructionFile(steps=[pcr1, dig1, dig2, lig, trans], sequences=seqs),
        ConstructionFile(steps=[pcr2], sequences=None)
    ]
    inventory = Inventory(boxes=[], construct_to_locations={}, loc_to_conc={}, loc_to_clone={}, loc_to_culture={})

    # Run the experiment factory to create the Experiment object
    experiment = experiment_factory.run("test_basic_ef", "B", cf_list, inventory)

    return {
        "experiment_factory": experiment_factory,
        "serializer": serializer,
        "experiment": experiment
    }

def test_experiment_serialization(setup_experiment_factory):
    data = setup_experiment_factory
    experiment = data["experiment"]

    # Ensure the experiment has a name for metadata serialization
    assert hasattr(experiment, "name") and experiment.name, "Experiment must have a valid name."

    # Serialize the experiment
    output_dir = "tests/output"
    os.makedirs(output_dir, exist_ok=True)
    data["serializer"].serialize_experiment(experiment, output_dir)

    # Verify metadata serialization
    experiment_dir = os.path.join(output_dir, experiment.name)
    metadata_file = os.path.join(experiment_dir, "metadata.txt")
    assert os.path.exists(metadata_file), "Expected metadata file does not exist."

    # Additional checks to ensure content in metadata file
    with open(metadata_file, "r") as f:
        metadata_content = f.read()
    assert f"Experiment Name: {experiment.name}" in metadata_content, "Experiment name is missing in metadata."

    # Verify LabPacket serialization
    lab_packet_dir = os.path.join(output_dir, experiment.name, "labpacket")
    assert os.path.exists(lab_packet_dir), "Expected LabPacket directory does not exist."

    # Verify Inventory serialization
    inventory_dir = os.path.join(output_dir, experiment.name, "inventory")
    assert os.path.exists(inventory_dir), "Expected Inventory directory does not exist."