from src.models.inventory import *
from src.models.labplanner import *
from string import ascii_uppercase as alcU

class InventoryFactory:

    BOX_SIZE = 9
    NUM_MINIPREPS = 4

    def checkConc(self, construct, concentration, currSamples, oldInventory):
        '''
        Parameters:
            construct: construct of our desired sample
            concentration: concentration of our desired sample
            currSamples: a list of samples that have been generated recently
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            boolean value for if the desired sample exists
        '''

        # check if current samples contains the desired sample
        for sample in currSamples:
            if sample.construct == construct and sample.concentration == concentration:
                return True
        
        # check if the inventory exists
        if oldInventory == None:
            return False 
        
        # check if the construct exists
        if construct not in oldInventory.construct_to_locations:
            return False 
        
        locationsList = oldInventory.construct_to_locations[construct]
        for loc in locationsList:
            conc = oldInventory.loc_to_conc[loc]
            if conc == concentration:
                return True
        
        return False
    
    def checkConcCultClone(self, construct, concentration, culture, clone, oldInventory):
        '''
        Parameters:
            construct: construct of our desired sample
            concentration: concentration of our desired sample
            culture: culture of our desired sample
            clone: clone of our desired sample
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            boolean value for if the desired sample exists
        '''
        
        # check if the old inventory exists
        if oldInventory == None:
            return False
        
        if construct not in oldInventory.construct_to_locations:
            return False 
        
        # check for the sample in the locations list
        locationsList = oldInventory.construct_to_locations[construct]
        for loc in locationsList:
            locConc = oldInventory.loc_to_conc[loc]
            locClone = oldInventory.loc_to_clone[loc]
            locCult = oldInventory.loc_to_culture[loc]
            if locConc == concentration and locClone == clone and locCult == culture:
                return True
        
        return False
    
    def genNewPCRs(self, pcr, experimentID, currSamples, oldInventory):
        '''
        Parameters:
            pcr: a PCR object
            experimentID: the corresponding experiment ID
            currSamples: a list of Sample objects generated recently
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            newPCRs: a list of PCR samples generated
        '''

        newPCRs = []

        tempName = pcr.template
        containsTemp = self.checkConc(tempName, Concentration.dil20x, currSamples, oldInventory)
        if not containsTemp:
            template = Sample(tempName + 'dil', tempName + 'dil', Concentration.dil20x, tempName, None, None)
            newPCRs.append(template)

        oligoF = pcr.forward_oligo
        containsOligoF = self.checkConc(oligoF, Concentration.uM100, currSamples, oldInventory)
        if not containsOligoF:
            for100 = Sample(oligoF, None, Concentration.uM100, oligoF, None, None)
            newPCRs.append(for100)
        
        containsOligoFDil = self.checkConc(oligoF, Concentration.uM10, currSamples, oldInventory)
        if not containsOligoFDil:
            for10 = Sample('10uM-' + oligoF, '10uM-' + oligoF, Concentration.uM10, oligoF, None, None)
            newPCRs.append(for10)
        
        oligoR = pcr.reverse_oligo
        containsOligoR = self.checkConc(oligoR, Concentration.uM100, currSamples, oldInventory)
        if not containsOligoR:
            rev100 = Sample(oligoR, None, Concentration.uM100, oligoR, None, None)
            newPCRs.append(rev100)
        
        containsOligoRDil = self.checkConc(oligoR, Concentration.uM10, currSamples, oldInventory)
        if not containsOligoRDil:
            rev10 = Sample('10uM-' + oligoR, '10uM-' + oligoR, Concentration.uM10, oligoR, None, None)
            newPCRs.append(rev10)
        
        product = pcr.output
        containsPdt = self.checkConc(product, Concentration.zymo, currSamples, oldInventory)
        if not containsPdt:
            zymo = Sample('z' + experimentID, 'z' + experimentID + '-' + product, Concentration.zymo, product, None, None)
            newPCRs.append(zymo)
        
        return newPCRs

    def genNewDigests(self, digestion, experimentID, currSamples, oldInventory):
        '''
        Parameters:
            digestion: a Digest object
            experimentID: the corresponding experiment ID
            currSamples: a list of Sample objects generated recently
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            newDigests: a list of Digest samples generated
        '''
        newDigests = []
        product = digestion.output
        containsSample = self.checkConc(product, Concentration.zymo, currSamples, oldInventory)
        if not containsSample:
            zymo = Sample('d' + experimentID, 'd' + experimentID + '-' + product, Concentration.zymo, product, None, None)
            newDigests.append(zymo)
        return newDigests

    def genNewLigates(self, ligation, experimentID, currSamples, oldInventory):
        newLigates = []
        product = ligation.output
        containsSample = self.checkConc(product, Concentration.zymo, currSamples, oldInventory)
        if not containsSample:
            zymo = Sample('l' + experimentID, 'l' + experimentID + '-' + product, Concentration.zymo, product, None, None)
            newLigates.append(zymo)
        return newLigates

    def genNewMinipreps(self, transformation, experimentID, oldInventory):
        '''
        Parameters:
            transformation: a Transform object
            experimentID: the corresponding experiment ID
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            newMinipreps: a list of miniprep samples generated
        '''
        newMinipreps = []
        for i in range(InventoryFactory.NUM_MINIPREPS):
            containsSample = False
            product = transformation.output
            clone = experimentID + alcU[i]
            containsSample = self.checkConcCultClone(product, Concentration.miniprep, Culture.primary, clone, oldInventory)
            if not containsSample:
                mini = Sample(product + '-' + clone, product + '-' + clone, Concentration.miniprep, product, Culture.primary, clone)
                newMinipreps.append(mini)
        return newMinipreps
    
    def genNewSeqs(self, sequences, currSamples, oldInventory):
        '''
        Parameters:
            sequences: a list of genomic DNA or other sequences that possibly need to be ordered
            currSamples: a list of Sample objects generated recently
            oldInventory: an Inventory object containing all samples, possibly from pre-existing experiments
        Returns:
            newSeqs: a list of Samples generated
        '''
        newSeqs = []
        if not sequences:
            return []
        for seqName in sequences:
            containsSeq = self.checkConc(seqName, Concentration.gene, currSamples, oldInventory)
            if not containsSeq:
                seq = Sample(seqName, seqName, Concentration.gene, seqName, None, None)
                newSeqs.append(seq)
            containsSeq = self.checkConc(seqName, Concentration.dil20x, currSamples, oldInventory)
            if not containsSeq:
                seq = Sample(seqName + 'dil', seqName + 'dil', Concentration.dil20x, seqName, None, None)
                newSeqs.append(seq)
        return newSeqs
    
    def getNextLocation(self, currLoc):
        '''
        Parameter:
            currLoc: a list of [row, col]
        Return
            [row, col]: the next location for where a sample would go
        '''
        row = currLoc[0]
        col = currLoc[1]

        if row == col == InventoryFactory.BOX_SIZE - 1:
            return None
        if col == InventoryFactory.BOX_SIZE - 1:
            row += 1
            col = 0
        else:
            col += 1

        return [row, col]

    def assignSamples(self, experimentName, newSamples, oldInventory):
        '''
        Parameters:
            experimentName: the name of the experiment
            newSamples: a list of new samples to add to the inventory
            oldInventory: an existing Inventory object that needs to be updated
        Returns:
            boxes, cons_to_loc, loc_to_conc, loc_to_clone, loc_to_culture: lists and dictionaries for the construction of a new Inventory
        '''

        if oldInventory:
            boxes = oldInventory.boxes
            cons_to_loc = oldInventory.construct_to_locations
            loc_to_conc = oldInventory.loc_to_conc
            loc_to_clone = oldInventory.loc_to_clone
            loc_to_culture = oldInventory.loc_to_culture
        else:
            boxes = []
            cons_to_loc = {}
            loc_to_conc = {}
            loc_to_clone = {}
            loc_to_culture = {}

        boxIndex = 0
        samplesArrays = {}
        currIndex = [0, 0]

        samplesArrays[0] = [[None for _ in range(10)] for _ in range(10)]

        for sample in newSamples:

            samplesArrays[boxIndex][currIndex[0]][currIndex[1]] = sample
            loc = Location(experimentName + 'Box' + str(boxIndex), currIndex[0], currIndex[1], sample.label, sample.sidelabel)
            loc_to_conc[loc] = sample.concentration
            loc_to_clone[loc] = sample.clone
            loc_to_culture[loc] = sample.culture
            if sample.construct not in cons_to_loc:
                cons_to_loc[sample.construct] = {loc}
            else:
                cons_to_loc[sample.construct].add(loc)

            currIndex = self.getNextLocation(currIndex)
            if not currIndex:
                currIndex = [0, 0]
                boxIndex += 1
                samplesArrays[boxIndex] =  [[] for _ in range(10)]   

        for arrayIndex in samplesArrays:
            newBox = Box(experimentName + 'Box' + str(arrayIndex), 'materials for ' + experimentName, 'minus20', samplesArrays[arrayIndex])
            boxes.append(newBox)
            
        return boxes, cons_to_loc, loc_to_conc, loc_to_clone, loc_to_culture
    
    def run(self, experimentName, experimentID, cfList, oldInventory):
        '''
        Parameters:
            experimentName: name of the experiment
            experimentID: ID of the experiment
            cfList: a list of ConstructionFile objects
            oldInventory: a pre-existing Inventory object that possibly contains samples
        Returns:
            inventory: a new Inventory object with updated samples for the new experiments
        '''

        newSamples = []
        for cf in cfList:
            for step in cf.steps:
                if step.operation == 'PCR':
                    newSamples.extend(self.genNewPCRs(step, experimentID, newSamples, oldInventory))
                elif step.operation == 'Digest':
                    newSamples.extend(self.genNewDigests(step, experimentID, newSamples, oldInventory))
                elif step.operation == 'Ligate':
                    newSamples.extend(self.genNewLigates(step, experimentID, newSamples, oldInventory))
                elif step.operation == 'Transform':
                    newSamples.extend(self.genNewMinipreps(step, experimentID, oldInventory))
            newSamples.extend(self.genNewSeqs(cf.sequences, newSamples, oldInventory))

        boxes, cons_to_loc, loc_to_conc, loc_to_clone, loc_to_culture  = self.assignSamples(experimentName, newSamples, oldInventory)

        inventory = Inventory(boxes, cons_to_loc, loc_to_conc, loc_to_clone, loc_to_culture)
        return inventory
