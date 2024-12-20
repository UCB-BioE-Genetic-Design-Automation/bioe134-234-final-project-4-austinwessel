## adapted from @jessicajxlin BioE140L-LabPlanner

everything beneath this these 3 text blocks is largley the same

### changes
- added pytest in tests/unit to confirm preexisting functionality and more features 
--- the first 3 files are not tests but related to the cleanup of the tests/data that would pile up quickly while making test_Experiments
- in utils, serialization.py and write_out.py were the closest i got to my goal(s)


### goals and how they shifted
- originally wanted to minimally change this working project and only extend it in the direction of using Autoprotocol's protocol methods to make JSON styled robotic instructions 
- first approach was to inverse 'Serializer.py' with 'deserializer.py' to try to get a set of deserialized lab instructions from LabSheets. having both would also satisfy some good testing as we could use them to validate each other.
- second approach was to pass over a complete Experiment instance along with a metadata.txt file associated with that instance, then trying to shape that into JSON, but the Experiment -> metadata -> JSON translations had too many formatting issues. along the way the issue of ConstructionFiles and their parsing would surface a lot. 
- third approach nuked a lot of the capabilities of main.py, since the preexisting Serializer.py is getting replaced by serialization.py and write_out.py. serialization.py handles the dataclass -> dict and dict -> dataclass, although not in class methods yet. write_out.py handles all of the output of human_readable.txt files associated with an Experiment as well as the JSON format required by autoprotocol's api by importing serialization.py's serialize and deserialize functions. They need to be tested to handle all of the dataclasses or enum classes found in this file to be foolproof.

### State
- Not working due to multiple util files that approximate the same things that could and should be unified into at least 2 maybe 3 files
- autoprotocol_factory, my original goal of extending somewhat, is largely unchanged, as well as oligo_list_factory
- some of the tests that do exist probably deserved to be deleted since the rely on methods from my first and second approaches
- no functional c9 wrapper




# BioE140L-LabPlanner

## File Directory

The descriptions here contain a general overview of the files. Each function should have a docstring with the specific inputs/outputs in the file itself.

### Model Files

`Autoprotocol.py`, `Inventory.py`, `Experiment.py`, `LabPlanner.py` each contain basic classes with their associated fields. These files were left mostly unmodified, with the few exceptions below:
* Gel, Zymo, Pick, and Miniprep steps were added to the LabPlanner file; even though these steps might not be explicitly included in construction files, these steps were added in the code for consistency/ease of use in other functions.

### Factory Files

`ExperimentFactory.py`: This file contains the ExperimentFactory class. This class uses both the other factories to generate a new `Experiment` object when its `run` function is called.

`InventoryFactory.py`: This file contains the InventoryFactory class. When the `run` function is called, a new inventory is generated taking into account the old inventory; overall, this function generates new samples for each step while checking the previous inventory, and assigns them to new boxes.

`LabPacketFactory.py`: This file contains the LabPacketFactory class. `LabSheet` objects are generated for each of the PCR, Ligate, Digest, Golden Gate, Gibson, and Transform, Zymo, Gel, Pick, and Miniprep steps, and compiled into a LabPacket.

`OligoListFactory.py`: This file contains the OligoListFactory class, but remains incomplete. 


### Other Files

`Parser.py`: This file is intended to contain functions for parsing various files. Currently, it parses boxes written in row form, as well as inventories.

`Serializer.py`: This file contains functions for serializing different objects. Currently, it contains functions for serializing lab sheets/packets and boxes. 

`main.py`: This file contains the code to be run. [See Instructions for Use].

## Instructions for Use

Code to be run should be written in `main.py`. `ConstructionFile` objects are created and a list of this `ConstructionFiles` is passed to the `ExperimentFactory`, which is created and run. The corresponding lab sheets and inventory are serialized, with the files being written to `out-inventory` and `out-labpacket` directories. For the inventory serialization, only the box is human-readable, and the dictionaries are not human-readable, but instead kept for easier parsing.

The box is re-serialized into `out-inventory` as `test.txt`, and the re-serialization of the box after parsing, when compared to the initial serialization, should be the same, demonstrating that the parsing and serialization functions for the box are accurate.

## Limitations & Future Work

1. CF parser and simulator integration. Currently, the construction file steps are encoded explicitly in `main.py`, as opposed to being parsed from a construction file. Future integration with an existing parser, or future work in writing a parser would be necessary.
2. Incomplete code. I chose to prioritize other factories to encode the essential functions of the original Lab Planner. Some of the factories/classes are incomplete, as listed below:
  * OligoListFactory.
  * Autoprotocol.
  * Mastermixes.
4. Testing. Basic testing has been done on the existing parsers/serializers, as well as the lab packet and inventory construction. Further testing would need to be done on other steps, as well as on a longer list of construction files.
