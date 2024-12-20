import json
import os
from src.utils.serialization import serialize

def write_experiment_output(experiment, base_dir):
    """
    Writes the full output of an Experiment to the specified base directory.

    Parameters:
        experiment: The Experiment object containing metadata, LabPacket, and Inventory.
        base_dir: The base directory to write all output files.
    """
    experiment_dir = os.path.join(base_dir, experiment.name)
    os.makedirs(experiment_dir, exist_ok=True)

    # Write metadata.txt
    write_metadata(experiment, os.path.join(experiment_dir, "metadata.txt"))

    # Write Experiment.json
    write_experiment_to_json(experiment, os.path.join(experiment_dir, "Experiment.json"))

    # Write LabPacket and LabSheets
    lab_packet_dir = os.path.join(experiment_dir, "LabPacket")
    write_labsheets_to_txt(experiment, lab_packet_dir)

    # Write Inventory folder
    inventory_dir = os.path.join(experiment_dir, "Inventory")
    write_inventory_to_json(experiment.inventory, inventory_dir)

def write_metadata(experiment, filepath):
    """
    Writes the metadata of an Experiment to a text file.

    Parameters:
        experiment: The Experiment object containing metadata.
        filepath: The path to save the metadata.txt file.
    """
    with open(filepath, "w") as f:
        f.write(f"Experiment Name: {experiment.name}\n")
        
        # Ensure oligos is iterable and safely handle None
        oligos = experiment.oligos if isinstance(experiment.oligos, (list, tuple)) else []
        f.write(f"Oligos: {', '.join(oligos)}\n")
        
        f.write("Polynucleotides:\n")
        for name, poly in experiment.nameToPoly.items():
            f.write(f"{name}: {poly.sequence}\n")


def write_experiment_to_json(experiment, filepath):
    """
    Serializes an Experiment object into a JSON file.

    Parameters:
        experiment: The Experiment object to serialize.
        filepath: The path to save the JSON file.
    """
    experiment_dict = serialize(experiment)
    with open(filepath, "w") as f:
        json.dump(experiment_dict, f, indent=4)

def write_labsheets_to_txt(experiment, outdir):
    """
    Saves all LabSheets in the Experiment's LabPacket as human-readable .txt files.

    Parameters:
        experiment: The Experiment object containing the LabPacket.
        outdir: The directory to save the LabSheet files.
    """
    os.makedirs(outdir, exist_ok=True)
    for i, lab_sheet in enumerate(experiment.labPacket.labsheets):
        filename = f"lab_sheet_{i}_{lab_sheet.title.replace(' ', '_')}.txt"
        filepath = os.path.join(outdir, filename)
        with open(filepath, "w") as f:
            f.write(format_lab_sheet(lab_sheet))

def format_lab_sheet(lab_sheet):
    """
    Formats a LabSheet object into a human-readable string.

    Parameters:
        lab_sheet: The LabSheet object to format.

    Returns:
        A formatted string representation of the LabSheet.
    """
    content = [f"LabSheet: {lab_sheet.title}\nType: {lab_sheet.sheetType}\n"]
    if lab_sheet.program:
        content.append(f"Program: {lab_sheet.program}\n")
    if lab_sheet.sources:
        content.append("Sources:\n")
        for source in lab_sheet.sources:
            content.append("\t" + ", ".join(source) + "\n")
    if lab_sheet.destinations:
        content.append("Destinations:\n")
        for dest in lab_sheet.destinations:
            content.append("\t" + ", ".join(dest) + "\n")
    if lab_sheet.notes:
        content.append("Notes:\n")
        for note in lab_sheet.notes:
            content.append("\t" + note + "\n")
    return "".join(content)

def write_inventory_to_json(inventory, outdir):
    """
    Serializes the Inventory object into JSON files within the specified directory.

    Parameters:
        inventory: The Inventory object to serialize.
        outdir: The directory to save the Inventory JSON files.
    """
    os.makedirs(outdir, exist_ok=True)
    inventory_dict = serialize(inventory)
    with open(os.path.join(outdir, "Inventory.json"), "w") as f:
        json.dump(inventory_dict, f, indent=4)
