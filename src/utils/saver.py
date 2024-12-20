import os
import json
from typing import Optional
from src.models.inventory import *
from src.models.labplanner import *
from src.models.experiment import *
from string import ascii_uppercase as alcU

class Saver:
    """
    assembles and saves Experiment objects, including LabPacket, LabSheets, Inventory, and metadata.
    """

    def save_experiment(self, experiment: Experiment, outdir: str = "data/outputs"):

        """Saves an Experiment object into LabSheets, Inventory, and metadata."""

        os.makedirs(outdir, exist_ok=True)
        experiment_dir = os.path.join(outdir, experiment.name)
        os.makedirs(experiment_dir, exist_ok=True)

        # LabPacket, Inventory, and metadata 
        self.save_metadata(experiment, experiment_dir)
        self.save_lab_packet(experiment.labPacket, os.path.join(experiment_dir, "labpacket"))
        self.save_inventory(experiment.inventory, os.path.join(experiment_dir, "inventory"))

        # Experiment as JSON
        self.save_experiment_to_json(experiment, os.path.join(experiment_dir, "experiment.json"))

    def save_metadata(self, experiment: Experiment, outdir: str):
        """
        saves metadata to a text file.
        """
        metadata_file = os.path.join(outdir, "metadata.txt")
        with open(metadata_file, "w") as f:
            f.write(f"Experiment Name: {experiment.name}\n")
            f.write(f"Oligos: {', '.join(experiment.oligos)}\n")
            f.write("Polynucleotides:\n")
            for name, poly in experiment.nameToPoly.items():
                f.write(f"{name}: {poly.sequence}\n")

    def save_lab_packet(self, lab_packet: LabPacket, outdir: str):
        """
        saves LabSheets in a LabPacket to individual files.
        """
        os.makedirs(outdir, exist_ok=True)
        for i, lab_sheet in enumerate(lab_packet.labsheets):
            outpath = os.path.join(outdir, f"{i}_{lab_sheet.title}.txt")
            self.save_lab_sheet(lab_sheet, outpath)

    def save_lab_sheet(self, lab_sheet: LabSheet, outpath: str):
        """
        saves a single LabSheet into a text file
        """
        with open(outpath, "w") as f:
            f.write(f"{lab_sheet.title}: {lab_sheet.sheetType}\n")
            if lab_sheet.program:
                f.write(f"Program: {lab_sheet.program}\n")
            if lab_sheet.sources:
                f.write("Sources:\n")
                for source in lab_sheet.sources:
                    f.write("\t".join(source) + "\n")
            if lab_sheet.destinations:
                f.write("Destinations:\n")
                for destination in lab_sheet.destinations:
                    f.write("\t".join(destination) + "\n")
            if lab_sheet.notes:
                f.write("Notes:\n")
                f.write("\n".join(lab_sheet.notes) + "\n")

    def save_inventory(self, inventory: Inventory, outdir: str):
        """
        Saves Inventory to JSON and row-formatted files.
        """
        os.makedirs(outdir, exist_ok=True)
        inventory_json = {"boxes": []}

        for i, box in enumerate(inventory.boxes):
            box_file = os.path.join(outdir, f"{i}_Box.txt")
            self.save_box_row_form(box, box_file)
            inventory_json["boxes"].append(box.to_dict())

        # Save additional Inventory mappings to JSON
        inventory_json.update({
            "construct_to_locations": {
                k: [str(loc) for loc in v] for k, v in inventory.construct_to_locations.items()
            },
            "loc_to_conc": {
                str(k): v.value for k, v in inventory.loc_to_conc.items()
            },
            "loc_to_clone": inventory.loc_to_clone,
            "loc_to_culture": {
                str(k): v.value for k, v in inventory.loc_to_culture.items()
            }
        })

        # Write inventory JSON
        inventory_json_file = os.path.join(outdir, "inventory.json")
        with open(inventory_json_file, "w") as f:
            json.dump(inventory_json, f, indent=4)


    def save_box_row_form(self, box: Box, outpath: str):
        """
        saves a Box to a TSV format.
        """
        with open(outpath, "w") as f:
            f.write(f">name {box.name}\n")
            f.write(f">description {box.description}\n")
            f.write(f">location {box.location}\n")
            f.write(">samples\n")
            f.write("Label\tSideLabel\tConcentration\tConstruct\tCulture\tClone\n")
            for row in box.samples:
                for sample in row:
                    if sample:
                        f.write(f"{sample.label}\t{sample.sidelabel}\t{sample.concentration.value}\t"
                                f"{sample.construct}\t{sample.culture.value}\t{sample.clone}\n")

 
    def save_experiment_to_json(self, experiment: Experiment, filepath: str):
        """
        Saves the entire Experiment object into a single JSON file.
        """
        experiment_dict = {
            "name": experiment.name,
            "oligos": experiment.oligos,
            "nameToPoly": {k: v.sequence for k, v in experiment.nameToPoly.items()},
            "labPacket": {"labsheets": [ls.to_dict() for ls in experiment.labPacket.labsheets]},
            "inventory": {"boxes": [box.to_dict() for box in experiment.inventory.boxes]}
        }

        with open(filepath, "w") as f:
            json.dump(experiment_dict, f, indent=4)




