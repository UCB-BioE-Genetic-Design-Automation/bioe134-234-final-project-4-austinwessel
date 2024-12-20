from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum, auto
from string import ascii_uppercase as alcU
from .inventory import *

@dataclass
class Polynucleotide:
    sequence: str
    ext5: Optional[str] = None
    ext3: Optional[str] = None
    is_double_stranded: bool = False
    is_circular: bool = False
    mod_ext5: str = 'hydroxyl'
    mod_ext3: str = 'hydroxyl'

@dataclass(frozen=True)
class Step:
    operation: str
    output: str

@dataclass(frozen=True)
class ConstructionFile:
    steps: List[Step]
    sequences: Dict[str, Polynucleotide]
    
@dataclass(frozen=True)
class PCR(Step):
    forward_oligo: str
    reverse_oligo: str
    template: str
    product_size: int = None

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'PCR')

@dataclass(frozen=True)
class Digest(Step):
    dna: str
    enzymes: list
    fragSelect: str
    product_size: int = None

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Digest')

@dataclass(frozen=True)
class Ligate(Step):
    dnas: list

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Ligate')

@dataclass(frozen=True)
class GoldenGate(Step):
    dnas: list
    enzyme: str

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Golden Gate')

@dataclass(frozen=True)
class Gibson(Step):
    dnas: list

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Gibson')

@dataclass(frozen=True)
class Transform(Step):
    dna: str
    strain: str
    antibiotics: list
    temperature: int = None

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Transform')

@dataclass(frozen=True)
class Pick(Step):

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Pick')

@dataclass(frozen=True)
class Miniprep(Step):
    
    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Miniprep')

@dataclass(frozen=True)
class Gel(Step):
    sample: str
    size: int

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Gel')

@dataclass(frozen=True)
class Zymo(Step):
    volume: float

    def __post_init__(self):
        object.__setattr__(self, 'operation', 'Zymo')

class Reagent(Enum):
    # Abstract Reagents
    mastermix = "mastermix"
    primer1 = "primer1"
    primer2 = "primer2"
    template = "template"
    frag1 = "frag1"
    frag2 = "frag2"
    frag3 = "frag3"
    frag4 = "frag4"
    dna = 'DNA'

    # Concrete Reagents
    ddH2O = "ddH2O"
    Phusion = "Phusion Polymerase"
    Q5_polymerase = "Q5 Polymerase"
    PrimeSTAR_GXL_DNA_Polymerase = "PrimeSTAR GXL DNA Polymerase"
    Gibson_Assembly_Master_Mix = "Gibson Assembly Master Mix"
    DpnI = "DpnI"
    BamHI = "BamHI"
    BglII = "BglII"
    BsaI = "BsaI"
    BsmBI = "BsmBI"
    T4_DNA_ligase = "T4 DNA Ligase"
    EcoRI = "EcoRI"
    SpeI = "SpeI"
    XhoI = "XhoI"
    XbaI = "XbaI"
    PstI = "PstI"
    Hindiii = "HindIII"
    T4_DNA_Ligase_Buffer_10x = "10x T4 DNA Ligase Buffer"
    NEB_Buffer_1_10x = "10x NEB Buffer 1"
    NEB_Buffer_2_10x = "10x NEB Buffer 2"
    NEB_Buffer_3_10x = "10x NEB Buffer 3"
    NEB_Buffer_4_10x = "10x NEB Buffer 4"
    Q5_Polymerase_Buffer_5x = "5x Q5 Polymerase Buffer"
    dNTPs_2mM = "2mM dNTPs"
    PrimeSTAR_GXL_Buffer_5x = "10x PrimeSTAR GXL Buffer"
    PrimeSTAR_dNTP_Mixture_2p5mM = "2.5mM PrimeSTAR GXL dNTPs"
    zymo_10b = "Zymo 10B competent cells"
    Zymo_5a = "Zymo 5A competent cells"
    JM109 = "JM109 competent cells"
    DH10B = "DH10B competent cells"
    MC1061 = "MC1061 competent cells"
    Ec100D_pir116 = "Ec100D pir116 competent cells"
    Ec100D_pir_plus = "Ec100D pir+ competent cells"
    lb_agar_50ug_ml_kan = "LB Agar + Kan Plate"
    lb_agar_100ug_ml_amp = "LB Agar + Amp Plate"
    lb_agar_100ug_ml_carb = "LB Agar + Carb Plate"
    lb_agar_100ug_ml_specto  = "LB Agar + Spec Plate"
    lb_agar_100ug_ml_cm = "LB Agar + Cm Plate"
    lb_agar_noAB = "LB Agar Plate"
    arabinose_10p = "10mM Arabinose solution"
    lb_specto = "LB + Spec Broth"
    lb_amp = "LB + Amp Broth"
    lb_carb = "LB + Carb Broth"
    lb_kan = "LB + Kan Broth"
    lb_cam = "LB + Cam Broth"
    lb = "LB Broth"

@dataclass(frozen=True)
class Recipe:
    mastermix: List[Tuple[Reagent, float]]  # The reagent and volume in microliters for the mastermix
    reaction: List[Tuple[Reagent, float]]   # The reagent and volume in microliters for the reaction

@dataclass(frozen=True)
class LabSheet:
    title: str  # Displayed at the top of the LabSheet
    sheetType: Step # what type of labsheet is it -- added
    steps: List[Step]  # ConstructionFile Steps executed on this sheet
    sources: List[Location]  # Samples to retrieve from Boxes
    destinations: List[Location]  # Samples to add new to Boxes
    program: str  # Program to run on a thermocycler
    protocol: str  # Specific protocol to use, e.g., PrimeStar or Phusion
    instrument: str  # Which instrument to put reactions/plates into
    notes: List[str]  # Any notes to display as alerts
    reaction: Recipe  # Ingredients for setting up the reaction
    
@dataclass(frozen=True)
class LabPacket:
    labsheets: List[LabSheet]