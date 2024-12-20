from dataclasses import *
from .labplanner import *
from .inventory import *


@dataclass(frozen=True)
class Experiment:
    name: str
    cfs: list[ConstructionFile]
    oligos: str
    nameToPoly: dict[str, Polynucleotide]
    labPacket: LabPacket
    inventory: Inventory