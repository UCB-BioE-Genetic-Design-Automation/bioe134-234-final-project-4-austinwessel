import os
import pickle
from src.models.inventory import *
from src.models.labplanner import *
from src.models.experiment import *
from .parser import Parser

class Deserializer:
    """
    A class holding all deserialization functions for Experiment objects.

    + using methods in utils/parser.py to deserialize inventory
    """
    def __init__(self):
        self.parser = Parser()

    def deserialize_experiment(self, indir: str) -> Experiment:
        """
        Reconstructs an Experiment object, including its LabPacket, Inventory, and associated metadata.

        Parameters:
            indir: The directory containing serialized Experiment data.

        Returns:
            Experiment: The reconstructed Experiment object.
        """
        if not os.path.exists(indir):
            raise FileNotFoundError(f"Input directory does not exist: {indir}")

        # Reconstruct metadata
        metadata = self.deserialize_metadata(indir)

        # Reconstruct LabPacket
        lab_packet_dir = os.path.join(indir, "labpacket")
        lab_packet = self.deserialize_lab_packet(lab_packet_dir)

        # Reconstruct Inventory
        inventory_dir = os.path.join(indir, "inventory")
        inventory = self.deserialize_inventory(inventory_dir)

        # Return the reconstructed Experiment
        return Experiment(
            name=metadata["name"],
            cfs = [],                           #cfs defaults to empty since no deserialization capabilites currently
            oligos=metadata["oligos"],
            nameToPoly=metadata["nameToPoly"],
            labPacket=lab_packet,
            inventory=inventory
        )

    def deserialize_metadata(self, indir: str) -> dict:
        """
        Reconstructs metadata from a metadata.txt file.

        Parameters:
            indir: The directory containing the metadata.txt file.

        Returns:
            dict: Metadata extracted from the file.
        """
        metadata_file = os.path.join(indir, "metadata.txt")
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

        metadata = {"name": None, "oligos": [], "nameToPoly": {}}
        with open(metadata_file, "r") as f:
            lines = f.readlines()

        # Parse metadata
        metadata["name"] = lines[0].split(": ")[1].strip()

        # Safely parse oligos: Handle cases where it's serialized as a string or list
        oligos_raw = lines[1].split(": ")[1].strip()
        if oligos_raw.startswith("[") and oligos_raw.endswith("]"):
            # Likely a list representation: eval to convert back to a list
            metadata["oligos"] = eval(oligos_raw)
        else:
            # Handle as a comma-separated string
            metadata["oligos"] = oligos_raw.split(",")

        metadata["nameToPoly"] = {
            line.split(": ")[0]: Polynucleotide(sequence=line.split(": ")[1].strip())
            for line in lines[3:]
        }

        return metadata

    def deserialize_lab_packet(self, indir: str) -> LabPacket:
        """
        Reconstructs a LabPacket object from serialized LabSheets.

        Parameters:
            indir: The directory containing serialized LabSheet files.

        Returns:
            LabPacket: The reconstructed LabPacket object.
        """
        if not os.path.exists(indir):
            raise FileNotFoundError(f"LabPacket directory not found: {indir}")

        lab_sheets = []
        for filename in sorted(os.listdir(indir)):
            filepath = os.path.join(indir, filename)
            lab_sheets.append(self.deserialize_lab_sheet(filepath))

        return LabPacket(labsheets=lab_sheets)

    def deserialize_lab_sheet(self, filepath: str) -> LabSheet:
        """
        Reconstructs a LabSheet object from a serialized file.

        Parameters:
            filepath: Path to the serialized LabSheet file.

        Returns:
            LabSheet: The reconstructed LabSheet object.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"LabSheet file not found: {filepath}")

        with open(filepath, "r") as f:
            lines = f.readlines()

        # Parse LabSheet content dynamically based on its type
        title = lines[0].strip()
        sheet_type = self.identify_sheet_type(title)  # Custom function to map titles to types

        # Reconstruct attributes based on sheet type
        if sheet_type == PCR:
            program = lines[2].split(": ")[1]
            protocol = lines[3].split(": ")[1]
            instrument = lines[4].split(": ")[1]

            sources_start = lines.index("Sources:") + 2
            sources = []
            for line in lines[sources_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                sources.append({
                    "label": parts[0],
                    "construct": parts[1],
                    "concentration": parts[2],
                    "location": parts[3]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                program=program,
                protocol=protocol,
                instrument=instrument,
                sources=sources
            )

        elif sheet_type == Digest:
            program = lines[2].split(": ")[1]
            instrument = lines[3].split(": ")[1]

            samples_start = lines.index("Samples:") + 2
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "source_label": parts[0],
                    "source_dnas": parts[1],
                    "source_location": parts[2],
                    "product_label": parts[3],
                    "product_dna": parts[4],
                    "product_location": parts[5]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                program=program,
                instrument=instrument,
                samples=samples
            )

        elif sheet_type == Ligate:
            program = lines[2].split(": ")[1]
            instrument = lines[3].split(": ")[1]

            # Parse Sources
            sources_start = lines.index("Samples:") + 1
            sources = []
            i = sources_start
            while i < len(lines) and "Product-Label" not in lines[i]:
                if lines[i].startswith("Source-Labels"):
                    source_block = []
                    i += 1  # Move past the header
                    while i < len(lines) and lines[i].strip():
                        parts = lines[i].split("\t")
                        source_block.append({
                            "label": parts[0],
                            "dna": parts[1],
                            "location": parts[2]
                        })
                        i += 1
                    sources.append(source_block)
                i += 1

            # Parse Destinations
            destinations_start = lines.index("Product-Label") + 1
            destinations = []
            for line in lines[destinations_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                destinations.append({
                    "label": parts[0],
                    "dna": parts[1],
                    "location": parts[2]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                program=program,
                instrument=instrument,
                sources=sources,
                destinations=destinations
            )
        
        elif sheet_type == Zymo:
            # Parse Sources
            sources_start = lines.index("Sources:") + 1
            sources = []
            for source in lines[sources_start:]:
                if not source.strip():
                    break
                sources.append(source.strip())

            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "product_label": parts[0],
                    "product": parts[1],
                    "elution_volume": parts[2],
                    "product_location": parts[3]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                sources=sources,
                samples=samples
            )
        
        elif sheet_type == Gel:
            # Parse Sources
            sources_start = lines.index("Sources:") + 1
            sources = []
            for source in lines[sources_start:]:
                if not source.strip():
                    break
                sources.append(source.strip())

            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "size": parts[1],
                    "product": parts[2]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,                     
                sources=sources,
                samples=samples
            )
        
        elif sheet_type == GoldenGate:
            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "frag1": parts[1],
                    "product": parts[2]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                samples=samples
            )
        
        elif sheet_type == Gibson:
            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "frag1": parts[1],
                    "product": parts[2]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                samples=samples
            )
        
        elif sheet_type == Transform:
            # Parse Sources
            sources_start = lines.index("Sources:") + 1
            sources = []
            for line in lines[sources_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                sources.append({
                    "label": parts[0],
                    "construct": parts[1],
                    "location": parts[2]
                })

            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "construct": parts[1],
                    "strain": parts[2],
                    "antibiotic": parts[3:-1],  # Antibiotics are a list
                    "incubate": parts[-1]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                sources=sources,
                samples=samples
            )
        
        elif sheet_type == Pick:
            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "construct": parts[1],
                    "strain": parts[2],
                    "antibiotic": parts[3:-1],  # Antibiotics are a list
                    "incubate": parts[-1]
                })

            # Parse Protocol
            protocol_start = lines.index("Protocol:") + 1
            protocol = lines[protocol_start] if protocol_start < len(lines) else None

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                samples=samples,
                protocol=protocol
            )
        
        elif sheet_type == Miniprep:
            # Parse Samples
            samples_start = lines.index("Samples:") + 1
            samples = []
            for line in lines[samples_start:]:
                if not line.strip():
                    break
                parts = line.split("\t")
                samples.append({
                    "label": parts[0],
                    "location": parts[1]
                })

            return LabSheet(
                title=title,
                sheetType=sheet_type,
                samples=samples
            )

        else:
            raise ValueError(f"Unknown LabSheet type: {sheet_type}")
        
    def identify_sheet_type(self, title: str) -> type:
        """
        Identifies the LabSheet type based on the title or other distinguishing features.

        Parameters:
            title: The title of the LabSheet.

        Returns:
            type: The type of the LabSheet (e.g., PCR, Digest).
        """
        if "PCR" in title:
            return PCR
        elif "Digest" in title:
            return Digest
        elif "Ligate" in title:
            return Ligate
        elif "Zymo" in title:
            return Zymo
        elif "Gel" in title:
            return Gel
        elif "GoldenGate" in title:
            return GoldenGate
        elif "Gibson" in title:
            return Gibson
        elif "Transform" in title:
            return Transform
        elif "Pick" in title:
            return Pick
        elif "Miniprep" in title:
            return Miniprep
        else:
            raise ValueError(f"Cannot identify sheet type from title: {title}")



    def deserialize_inventory(self, indir: str) -> Inventory:
        """
        Reconstructs an Inventory object from serialized files.

        Parameters:
            indir: The directory containing serialized inventory files.

        Returns:
            Inventory: The reconstructed Inventory object.
        """
        if not os.path.exists(indir):
            raise FileNotFoundError(f"Inventory directory not found: {indir}")
        
        # Use the parser to reconstruct the Inventory
        inventory = self.parser.parse_inventory(indir)

        # Parse Boxes
        for filename in sorted(os.listdir(indir)):
            if filename.endswith("-Box.txt"):
                filepath = os.path.join(indir, filename)
                box = self.parser.parse_box_row_form(filepath)
                inventory.boxes.append(box)

        return inventory
