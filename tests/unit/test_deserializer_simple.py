import os
import pytest
from utils.saver import Serializer
from src.utils.deserializer import Deserializer
from src.models.experiment import Experiment
from src.models.labplanner import *
from src.models.inventory import Inventory 

@pytest.fixture
def setup_experiment(mocker):
    # Create a mock ConstructionFile
    mock_cfs = [mocker.MagicMock(spec=ConstructionFile)]  # Minimal mock of ConstructionFile

    # Mock an Experiment object
    
    experiment = Experiment(
        name="test_experiment",
        cfs=mock_cfs,  # cfs comes before oligos, but not no handling built currently
        oligos=["Oligo1", "Oligo2"],
        nameToPoly={"PolyA": Polynucleotide(sequence="ATCG"), "PolyB": Polynucleotide(sequence="GCTA")},
        labPacket=LabPacket(labsheets=[]),  # Add mock LabSheets if necessary
        inventory=Inventory(boxes=[], construct_to_locations={}, loc_to_conc={}, loc_to_clone={}, loc_to_culture={})
    )
    return experiment


# def test_serialize_and_deserialize_experiment(setup_experiment):
#     serializer = Serializer()
#     deserializer = Deserializer()

#     # Serialize the experiment
#     output_dir = "tests/output/test_congruency"
#     os.makedirs(output_dir, exist_ok=True)
#     experiment = setup_experiment
#     serializer.serialize_experiment(experiment, output_dir)

#     # Update the expected directory for deserialization
#     nested_output_dir = os.path.join(output_dir, experiment.name)  # Includes the experiment name
#     deserialized_experiment = deserializer.deserialize_experiment(nested_output_dir)

#     # Verify congruency for non-cfs fields 
#     assert deserialized_experiment.name == experiment.name, "Experiment names do not match."
#     assert deserialized_experiment.oligos == experiment.oligos, "Oligos do not match."
#     assert deserialized_experiment.nameToPoly.keys() == experiment.nameToPoly.keys(), "Polynucleotide keys do not match."
#     assert all(
#         deserialized_experiment.nameToPoly[k].sequence == experiment.nameToPoly[k].sequence
#         for k in experiment.nameToPoly
#     ), "Polynucleotide sequences do not match."

#     # Verify LabPacket structure and content
#     assert deserialized_experiment.labPacket is not None, "LabPacket is missing."
#     assert isinstance(deserialized_experiment.labPacket.labsheets, list), "LabPacket labsheets should be a list."
#     assert len(deserialized_experiment.labPacket.labsheets) == len(experiment.labPacket.labsheets), "Mismatch in LabSheet count."

#     # Verify Inventory deserialized correctly
#     assert deserialized_experiment.inventory is not None, "Inventory is missing."
#     assert isinstance(deserialized_experiment.inventory.boxes, list), "Inventory boxes should be a list."
#     assert len(deserialized_experiment.inventory.boxes) == len(experiment.inventory.boxes), "Mismatch in Inventory box count."


def test_deserialize_labsheets():
    deserializer = Deserializer()

    # Set path to LabPacket directory
    lab_packet_dir = "tests/output/test_basic_ef/labpacket"

    # Deserialize the LabPacket
    lab_packet = deserializer.deserialize_lab_packet(lab_packet_dir)
    assert lab_packet is not None, "Failed to deserialize LabPacket."
    assert len(lab_packet.labsheets) > 0, "No LabSheets found in the LabPacket."

    # Verify each LabSheet
    for i, lab_sheet in enumerate(lab_packet.labsheets):
        assert hasattr(lab_sheet, "title"), f"LabSheet {i} is missing a title."
        assert hasattr(lab_sheet, "sheetType"), f"LabSheet {i} is missing a sheetType."
        assert hasattr(lab_sheet, "program"), f"LabSheet {i} is missing a program."
        assert hasattr(lab_sheet, "sources"), f"LabSheet {i} is missing sources."
        print(f"LabSheet {i}: Title = {lab_sheet.title}, Type = {lab_sheet.sheetType}")

    print("All LabSheets deserialized and validated successfully.")



