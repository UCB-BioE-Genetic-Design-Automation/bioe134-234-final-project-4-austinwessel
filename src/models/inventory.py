from dataclasses import *
from enum import *

class Culture(Enum):
    library = "library"
    primary = "primary"
    secondary = "secondary"
    tertiary = "tertiary"

class Concentration(Enum):
    miniprep = "miniprep"   # A plasmid miniprep
    zymo = "zymo"           # A purified DNA product
    uM100 = "uM100"         # Oligo concentration for stocks
    uM10 = "uM10"           # Oligo concentration for PCR
    uM266 = "uM266"         # Oligo concentration for sequencing
    dil20x = "dil20x"       # A diluted plasmid or other DNA
    gene = "gene"           # A gene synthesis order

@dataclass(frozen=True)
class Sample:
    label: str              # What's written on the top of the tube
    sidelabel: str          # What's written on the side of the tube
    concentration: Concentration  # The amount or type of DNA present
    construct: str          # The name of the DNA matching the construction file
    culture: Culture        # For minipreps only, how many rounds of isolation
    clone: str              # Which isolate of several of the same construct

@dataclass(frozen=True)
class Location:
    boxname: str     # The name of the box a sample is in
    row: int         # The row within the box, starting with 0
    col: int         # The column within the box, starting with 0
    label: str       # What's written on the top of the tube
    sidelabel: str   # What's written on the side of the tube

@dataclass(frozen=True)
class Box:
    name: str                # name of the box, i.e., lysis1, and of the file
    description: str         # a description of the contents of the box
    location: str            # i.e., which freezer
    samples: list[list[Sample]]  # What's in each well, or None

@dataclass(frozen=True)
class Inventory:
    boxes: list[Box]                                   # all the boxes in the inventory
    construct_to_locations: dict[str, set[Location]]   # Quick lookup of samples by construct name
    loc_to_conc: dict[Location, Concentration]         # Quick lookup by Concentration
    loc_to_clone: dict[Location, str]                  # Quick lookup by Clone
    loc_to_culture: dict[Location, Culture]            # Quick lookup by Culture
