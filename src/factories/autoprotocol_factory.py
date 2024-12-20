import os
import json
from src.models import *
from src.utils.serialization import *
from autoprotocol.protocol import Protocol

class AutoprotocolFactory:
    """
    A factory to generate Autoprotocol instructions from a deserialized LabPacket.
    """

    def __init__(self):
        self.protocol = Protocol()

    def run(self, lab_packet, inventory):
        """
        Generate Autoprotocol instructions from a deserialized LabPacket and Inventory.

        Parameters:
            lab_packet: A deserialized LabPacket object containing LabSheets.
            inventory: A deserialized Inventory object.
        """
        if not lab_packet or not lab_packet.labsheets:
            raise ValueError("LabPacket is missing or contains no LabSheets.")

        for sheet in lab_packet.labsheets:
            self._process_lab_sheet(sheet, inventory)

    def _process_lab_sheet(self, lab_sheet, inventory):
        """
        Process an individual LabSheet to generate Autoprotocol steps.

        Parameters:
            lab_sheet: A deserialized LabSheet object.
            inventory: A deserialized Inventory object.
        """
        if lab_sheet.sheetType == PCR:
            self._process_pcr(lab_sheet, inventory)
        elif lab_sheet.sheetType == Digest:
            self._process_digest(lab_sheet, inventory)
        # Add more types as needed
        else:
            print(f"Warning: Unsupported LabSheet type: {lab_sheet.sheetType}")

    def _process_pcr(self, lab_sheet, inventory):
        """
        Generate Autoprotocol instructions for a PCR LabSheet.
        """
        for reagent in lab_sheet.reaction.reaction:
            self.protocol.transfer(
                source=reagent[0].value,  # Adjust to match LabSheet structure
                dest="destination_well",  # Replace with dynamic destination logic
                volume=f"{reagent[1]}:microliter"
            )
        self.protocol.thermocycle(
            groups=[
                {"cycles": 30, "steps": [
                    {"temperature": "95:celsius", "duration": "30:second"},
                    {"temperature": "55:celsius", "duration": "30:second"},
                    {"temperature": "72:celsius", "duration": "1:minute"}
                ]}
            ],
            volume="50:microliter"
        )

    def _process_digest(self, lab_sheet, inventory):
        """
        Generate Autoprotocol instructions for a Digest LabSheet.
        """
        # Example: Add Digest-specific instructions
        pass

    def export_protocol(self, output_path):
        """
        Export the generated protocol to a JSON file.

        Parameters:
            output_path: Path to save the Autoprotocol JSON.
        """
        with open(output_path, "w") as f:
            f.write(self.protocol.as_dict())
        print(f"Protocol exported to {output_path}")

