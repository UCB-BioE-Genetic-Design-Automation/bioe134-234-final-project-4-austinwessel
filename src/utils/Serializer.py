from string import ascii_uppercase as alcU
from src.models import *
from src.models.labplanner import *
import pickle

class Serializer:
    '''
    A class holding all serialization functions.
    '''
    def serializeLabSheet(self, labSheet, outpath):
        '''
        Parameters:
            labSheet: a LabSheet object to be serialized
            outpath: the path for the serialized LabSheet
        Returns:
            None
        '''
        with open(outpath, 'w+') as f:
            f.write(labSheet.title + '\n')
            f.write('Reaction:\n')
            if labSheet.reaction:
                for reagent in labSheet.reaction.reaction: 
                    f.write(str(reagent[1]) + 'uL ' + reagent[0].value + '\n')
                f.write('\n')
            
            if labSheet.sheetType == PCR:
                f.write('Program: ' + labSheet.program + '\n' + 'Protocol: ' + labSheet.protocol + '\n' + 'Instrument: ' + labSheet.instrument + '\n\n')
                f.write('Sources: \n')
                f.write('Label \t Construct \t Concentration \t Location \n')
                for source in labSheet.sources:
                    f.write(source[0].label + '\t' + source[1] + '\t' + source[2].value + '\t' +
                            source[0].boxname + '/' + alcU[source[0].row] + str(source[0].col) + '\n')
            
            if labSheet.sheetType == Digest:
                f.write('Program: ' + labSheet.program + '\n' + 'Instrument: ' + labSheet.instrument + '\n\n')
                f.write('Samples: \n')
                f.write('Source-Label \t Source-DNAs \t Source-Location \t Product-Label \t Product-DNA \t Product-Location \n')
                for i in range(len(labSheet.sources)):
                    f.write(labSheet.sources[i][0].label + '\t' + labSheet.sources[i][1] + '\t' + labSheet.sources[i][0].boxname + '/' + alcU[labSheet.sources[i][0].row] + str(labSheet.sources[i][0].col) + '\t' +
                        labSheet.destinations[i][0].label + '\t' + labSheet.destinations[i][1] + '\t' + labSheet.destinations[i][0].boxname + '/' + alcU[labSheet.destinations[i][0].row] + str(labSheet.destinations[i][0].col) + '\n')

            if labSheet.sheetType == Ligate:
                f.write('Program: ' + labSheet.program + '\n' + 'Instrument: ' + labSheet.instrument + '\n\n')
                f.write('Samples: \n')
                for i in range(len(labSheet.sources)):
                    f.write('Source-Labels \t Source-DNAs \t Source-Location \n')
                    for source in labSheet.sources[i]:
                        f.write(source[0].label + '\t' + source[1] +  '\t'  + source[0].boxname + '/' + alcU[source[0].row] + str(source[0].col) + '\n')
                    
                    f.write('\nProduct-Label \t Product-DNA \t Product-Location \n')
                    f.write(labSheet.destinations[i][0].label + '\t' + labSheet.destinations[i][1] + '\t' + labSheet.destinations[i][0].boxname + '/' + alcU[labSheet.destinations[i][0].row] + str(labSheet.destinations[i][0].col) + '\n')
                
            if labSheet.sheetType == Zymo:
                f.write('Sources: \n')
                for source in labSheet.sources:
                    f.write(source + '\t')
                f.write('\n')
                f.write('Samples: \n')
                f.write('Product-Label \t Product \t Elution Volume \t Product-Location \n')
                for i in range(len(labSheet.steps)):
                    dest = labSheet.destinations[i]
                    f.write(dest[0].label + '\t' + dest[1] + '\t' + str(labSheet.steps[i].volume) + 'uL' + '\t' +
                            dest[0].boxname + '/' + alcU[dest[0].row] + str(dest[0].col) + '\n')

            if labSheet.sheetType == Gel:
                f.write('Sources: \n')
                for source in labSheet.sources:
                    f.write(source + '\t')
                f.write('\n')
                f.write('Samples: \n')
                f.write('Label \t Size \t Product \n')
                for i in range(len(labSheet.steps)):
                    dest = labSheet.destinations[i]
                    f.write(dest[0].label + '\t' + str(dest[2]) + '\t' + dest[1] + '\n')

            if labSheet.sheetType == GoldenGate:
                f.write('Samples: \n')
                f.write('Label \t Frag1 \t Product \n')
                for source in labSheet.sources:
                    f.write(source[0].label + '\t' + source[1] +  '\t'  + source[0].boxname + '/' + alcU[source[0].row] + str(source[0].col) + '\n')

            if labSheet.sheetType == Gibson:
                f.write('Samples: \n')
                f.write('Label \t Frag1 \t Product \n')
                for source in labSheet.sources:
                    f.write(source[0].label + '\t' + source[1] +  '\t'  + source[0].boxname + '/' + alcU[source[0].row] + str(source[0].col) + '\n')

            if labSheet.sheetType == Transform:
                f.write('Sources: \n')
                f.write('Label \t Construct \t Location \n')
                for source in labSheet.sources:
                    f.write(source[0].label + '\t' + source[1] + '\t' + source[0].boxname + '/' + 
                            alcU[source[0].row] + str(source[0].col) + '\n')
                
                f.write('Samples: \n')
                f.write('Label \t Construct \t Strain \t Antibiotic \t Incubate \n')
                for dest in labSheet.destinations:
                    f.write(dest[0].label + '\t' + dest[1] + '\t' + dest[2] + '\t')
                    for antibiotic in dest[3]:
                        f.write(antibiotic + '\t')
                    f.write(str(dest[4]) + '\n')

            if labSheet.sheetType == Pick:
                f.write('Samples: \n')
                f.write('Label \t Construct \t Strain \t Antibiotic \t Incubate \n')
                for dest in labSheet.destinations:
                    f.write(dest[0].label + '\t' + dest[1] + '\t' + dest[2] + '\t')
                    for antibiotic in dest[3]:
                        f.write(antibiotic + '\t')
                    f.write(str(dest[4]) + '\n')
                
                f.write('\n')
                f.write('Protocol: ' + labSheet.protocol)

            if labSheet.sheetType == Miniprep:
                f.write('Samples: \n')
                f.write('Label \t Location \n')
                for dest in labSheet.destinations:
                    f.write(dest[0].label + '\t' + 
                            dest[0].boxname + '/' + alcU[dest[0].row] + str(dest[0].col) + '\n')

            f.write('\n')
            f.write('Notes: \n')
            for note in labSheet.notes:
                f.write(note + '\n')

    def serializeLabPacket(self, labPacket, outdir):
        '''
        Parameters:
            labPacket: a LabPacket object to be serialized
            outdir: the directory for the serialized LabPacket
        Returns:
            None
        '''
        for i in range(len(labPacket.labsheets)):
            self.serializeLabSheet(labPacket.labsheets[i], outdir + '/' + f'{i} ' + labPacket.labsheets[i].title + '.txt')
        
    def serializeBoxRowForm(self, box, outpath):
        '''
        Parameters:
            box: a Box object to be serialized
            outpath: the path for the serialized box
        Returns:
            None
        '''
        with open(outpath, 'w+') as f:
            f.write(f'>name {box.name}\n')
            f.write(f'>description {box.description}\n')
            f.write(f'>location {box.location}\n')
            f.write(f'>samples\n')
            f.write(f'>label\tsidelabel\tconcentration\tconstruct\tculture\tclone\n')
            for i in range(len(box.samples)):
                for j in range(len(box.samples[i])):
                    if box.samples[i][j]:
                        f.write(str(alcU[i]) + str(j) + '\t')
                        concentration = box.samples[i][j].concentration
                        if concentration:
                            concentration = box.samples[i][j].concentration.value
                        culture = box.samples[i][j].culture
                        if culture:
                            culture = box.samples[i][j].culture.value
                        f.write(f'{box.samples[i][j].label}\t{box.samples[i][j].sidelabel}\t{concentration}\t' +
                                f'{box.samples[i][j].construct}\t{culture}\t {box.samples[i][j].clone}')
                        f.write('\n')
    
    def serializeInventory(self, inventory, outdir):
        '''
        Parameters:
            inventory: an Inventory object to be serialized
            outdir: the directory for the serialized inventory
        Returns:
            None
        '''
        for i in range(len(inventory.boxes)):
            self.serializeBoxRowForm(inventory.boxes[i], f'{outdir}/{i}-Box.txt')

        with open(f'{outdir}/construct_to_locations', 'ab') as consToLoc:
            pickle.dump(inventory.construct_to_locations, consToLoc)
        
        with open(f'{outdir}/location_to_concentration', 'ab') as locToConc:
            pickle.dump(inventory.loc_to_conc, locToConc)

        with open(f'{outdir}/location_to_clone', 'ab') as locToClone:
            pickle.dump(inventory.loc_to_clone, locToClone)

        with open(f'{outdir}/location_to_culture', 'ab') as locToCulture:
            pickle.dump(inventory.loc_to_culture, locToCulture)
