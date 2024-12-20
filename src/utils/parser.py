from src.models.inventory import Inventory, Box, Sample, Concentration, Culture
from typing import List
import pickle


class Parser:
    '''
    This class contains utility functions for parsing serialized files.
    '''

    def parse_box_row_form(self, inpath: str) -> Box:
        '''
        Parses a previously serialized box file.
        
        Parameters:
            inpath: The path of the serialized box file to be parsed.
        
        Returns:
            A Box object.
        '''
        samples_array = [[None for _ in range(10)] for _ in range(10)]
        with open(inpath, 'r') as file:
            lines = file.readlines()
            name = lines[0].split()[1]
            description = lines[1].split()[1]
            location = lines[1].split()[1]

            for i in range(5, len(lines)):
                line_arr = lines[i].split()
                sidelabel = None if line_arr[2] == 'None' else line_arr[2]
                concentration = None if line_arr[3] == 'None' else Concentration(line_arr[3])
                culture = None if line_arr[5] == 'None' else Culture(line_arr[5])
                clone = None if line_arr[6] == 'None' else line_arr[6]
                sample = Sample(
                    label=line_arr[1],
                    sidelabel=sidelabel,
                    concentration=concentration,
                    construct=line_arr[4],
                    culture=culture,
                    clone=clone
                )
                row = ord(line_arr[0][0]) - 65
                col = int(line_arr[0][1])
                samples_array[row][col] = sample

        return Box(name, description, location, samples_array)

    def parse_inventory(self, indir: str) -> Inventory:
        '''
        Parses a previously serialized inventory directory.

        Parameters:
            indir: The directory containing serialized Inventory components.
        
        Returns:
            An Inventory object.
        '''
        boxes: List[Box] = []
        with open(f'{indir}/construct_to_locations', 'rb') as file:
            construct_to_locations = pickle.load(file)
        with open(f'{indir}/location_to_concentration', 'rb') as file:
            loc_to_conc = pickle.load(file)
        with open(f'{indir}/location_to_clone', 'rb') as file:
            loc_to_clone = pickle.load(file)
        with open(f'{indir}/location_to_culture', 'rb') as file:
            loc_to_culture = pickle.load(file)

        return Inventory(boxes, construct_to_locations, loc_to_conc, loc_to_clone, loc_to_culture)
