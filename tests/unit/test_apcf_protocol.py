import os
import pytest
from utils.saver import Serializer
from src.utils.deserializer import Deserializer
from src.factories.autoprotocol_factory import AutoprotocolFactory
from src.models import *

@pytest.fixture
def setup_experiment():
    # Mock an Experiment object
    experiment = Experiment(
        name="test_experiment",
        cfs=[ConstructionFile(steps=[])],  # cfs comes before oligos
        oligos=["Oligo1", "Oligo2"],
        nameToPoly={"PolyA": Polynucleotide(sequence="ATCG"), "PolyB": Polynucleotide(sequence="GCTA")},
        labPacket=LabPacket(labsheets=[]),  # Add mock LabSheets if necessary
        inventory=Inventory(boxes=[], construct_to_locations={}, loc_to_conc={}, loc_to_clone={}, loc_to_culture={})
    )
    return experiment

def test_deserialize_pcr_labsheet():
    deserializer = Deserializer()

    # Path to the PCR LabSheet
    labsheet_path = "tests/output/test_basic_ef/labpacket/0_test_basic_ef_ PCR.txt"

    # Deserialize the LabSheet
    lab_sheet = deserializer.deserialize_lab_sheet(labsheet_path)

    # Verify LabSheet structure
    assert lab_sheet.sheetType == PCR, "LabSheet type is not PCR."
    assert hasattr(lab_sheet, "reaction"), "LabSheet is missing reaction details."
    assert hasattr(lab_sheet, "program"), "LabSheet is missing program details."
    assert hasattr(lab_sheet, "protocol"), "LabSheet is missing protocol details."
    assert hasattr(lab_sheet, "instrument"), "LabSheet is missing instrument details."
    assert lab_sheet.sources, "LabSheet sources are missing."

    # Initialize AutoprotocolFactory and test processing
    factory = AutoprotocolFactory()
    factory._process_pcr(lab_sheet, None)  # Pass None for inventory for now
    print("Successfully processed PCR LabSheet into Autoprotocol.")

