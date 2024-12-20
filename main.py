import sys
import os
from src.models import *
from src.factories import *
from src.utils import *


def main():
    # Example PCR, Digest, Ligate, Transform operations
    pcr1 = PCR('PCR', 'pcrpdt', 'ca1067F', 'ca1067R', 'pSB1AK3-b0015', 1000)
    dig1 = Digest('Digest', 'pcrdig', 'pcrpdt', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
    dig2 = Digest('Digest', 'vectdig', 'pSB1A2-I13521', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
    lig = Ligate('Ligate', 'pSB1A2-Bca9128', ['pcrdig', 'vectdig'])
    trans = Transform('Transform', 'finalpdt', 'pSB1A2-Bca9128', 'Mach1', ['Amp'], 37)
    seqs = {'pSB1A2-I13521': 'randomsequencehere'}

    pcr2 = PCR('PCR', 'pcrOutput', 'oligoF', 'oligoR', 'template', 500)

    # Construction file list
    cf_list = [ConstructionFile([pcr1, dig1, dig2, lig, trans], seqs), ConstructionFile([pcr2], None)]

    # Initialize utilities
    serializer = Saver()  #previously serializer = Serializer(), likely not working 
    parser = Parser()
    experiment_factory = ExperimentFactory()

    # Run Experiment
    experiment_name = "TestExperiment"
    experiment_id = "TestID"
    output_dir = "data/output"

    experiment = experiment_factory.run(experiment_name, experiment_id, cf_list, None)

    # Serialize LabPacket and Inventory
    serializer.save_lab_packet(experiment.labPacket, f"{output_dir}/labpacket")
    serializer.save_inventory(experiment.inventory, f"{output_dir}/inventory")

    # Parse inventory for demonstration purposes
    parsed_inventory = parser.parse_inventory(f"{output_dir}/inventory")
    box = parser.parse_box_row_form(f"{output_dir}/inventory/0-Box.txt")
 #   serializer.serialize_box_row_form(box, f"{output_dir}/test_box_serialized.txt")   

    print(f"LabPacket and Inventory serialized to {output_dir}")

if __name__ == "__main__":
    main()

# Example PCR, Digest, Ligate, Transform operations
pcr1 = PCR('PCR', 'pcrpdt', 'ca1067F', 'ca1067R', 'pSB1AK3-b0015', 1000)
dig1 = Digest('Digest', 'pcrdig', 'pcrpdt', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
dig2 = Digest('Digest', 'vectdig', 'pSB1A2-I13521', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
lig = Ligate('Ligate', 'pSB1A2-Bca9128', ['pcrdig', 'vectdig'])
trans = Transform('Transform', 'finalpdt', 'pSB1A2-Bca9128', 'Mach1', ['Amp'], 37)
seqs = {'pSB1A2-I13521': 'randomsequencehere'}

pcr2 = PCR('PCR', 'pcrOutput', 'oligoF', 'oligoR', 'template', 500)

# Construction file list
cf_list = [ConstructionFile([pcr1, dig1, dig2, lig, trans], seqs), ConstructionFile([pcr2], None)]
cf_pcr = [ConstructionFile([pcr1], seqs)]

# Initialize utilities
serializer = Saver()
parser = Parser()
experiment_factory = ExperimentFactory()

# Run Experiment
experiment_name = "main_just_pcr"
experiment_id = "m_ID"
output_dir = "data/output"

experiment = experiment_factory.run(experiment_name, experiment_id, cf_pcr, None)

# Serialize LabPacket and Inventory
serializer.save_lab_packet(experiment.labPacket, f"{output_dir}/labpacket")
serializer.save_inventory(experiment.inventory, f"{output_dir}/inventory")

# Parse inventory for demonstration purposes
parsed_inventory = parser.parse_inventory(f"{output_dir}/inventory")
box = parser.parse_box_row_form(f"{output_dir}/inventory/0-Box.txt")
serializer.serialize_box_row_form(box, f"{output_dir}/test_box_serialized.txt")

print(f"LabPacket and Inventory serialized to {output_dir}")
