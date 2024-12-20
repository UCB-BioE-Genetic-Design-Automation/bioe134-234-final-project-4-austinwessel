from src.models.experiment import *
from src.models.inventory import *
from src.models.labplanner import *

class LabPacketFactory:
    '''
    This class contains functions to construct a Lab Packet for some experiment, which can be eventually serialized.
    '''

    def pcrSheets(self, expName, pcrSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            pcrSteps: a list of Steps with the PCR operation
            inventory: a current Inventory object
        Returns:
            pcrLabSheets: a list containing LabSheet objects corresponding to PCR steps
        '''
        title = expName + ': PCR'
        program = 'PG3K55'
        protocol = 'PrimeSTAR'
        instrument = 'Thermocycler 2A'

        pcrLabSheets = []
        reactions = []
        reactions.append([Reagent.ddH2O, 32.0])
        reactions.append([Reagent.PrimeSTAR_dNTP_Mixture_2p5mM, 4.0])
        reactions.append([Reagent.primer1, 1.0])
        reactions.append([Reagent.primer2, 1.0])
        reactions.append([Reagent.template, 1.0])
        reactions.append([Reagent.PrimeSTAR_GXL_Buffer_5x, 10.0])
        reactions.append([Reagent.PrimeSTAR_GXL_DNA_Polymerase, 1.0])
    
        recipe = Recipe(None, reactions)

        notes = ['Never let enzymes warm up!  Only take the enzyme cooler out of the freezer\n'
                    + 'when you are actively using it, and only take the tubes out of it when actively\n'
                    + 'dispensing. Hold the enzyme tube by the top of the tube while dispensing\n'
                    + 'and do not place it in a rack.']
        
        sources = []
        destinations = []
        for step in pcrSteps:
            oligoF = step.forward_oligo
            chosenLoc = None
            locations = inventory.construct_to_locations[oligoF]
            for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.uM10:
                        chosenLoc = loc
                        break
            if chosenLoc == None:
                raise Exception("Null location for " + str(oligoF))
            sources.append((chosenLoc, oligoF, Concentration.uM10))

            oligoR = step.reverse_oligo
            chosenLoc = None
            locations = inventory.construct_to_locations[oligoR]
            for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.uM10:
                        chosenLoc = loc
                        break
            if chosenLoc == None:
                raise Exception("Null location for " + str(oligoR))
            sources.append((chosenLoc, oligoR, Concentration.uM10))

            template = step.template
            chosenLoc = None
            locations = inventory.construct_to_locations[template]
            for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.dil20x:
                        chosenLoc = loc
                        break
            if chosenLoc == None:
                raise Exception("Null location for " + str(template))
            sources.append((chosenLoc, template, Concentration.dil20x))

        pcrSheet = LabSheet(title, PCR, pcrSteps, sources, destinations, program, protocol, instrument, notes, recipe)
        pcrLabSheets.append(pcrSheet)

        return pcrLabSheets

    def digestSheets(self, expName, digestSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            digestSteps: a list of Steps with the Digest operation
            inventory: a current Inventory object
        Returns:
            digestLabSheets: a list containing LabSheet objects corresponding to digest steps
        '''

        digestLabSheets = []

        title = expName + ': Digestion'
        sources = []
        destinations = []
        program = 'main/dig'
        protocol = None
        instrument = 'Thermocycler 1A'
        notes = ['Never let enzymes warm up! Only take the enzyme cooler out of the freezer when you\n'
                 + 'are actively using it, and only take the tubes out of it when actively dispensing.']

        enzyme_to_steps = {}

        for step in digestSteps:
            tupStep = tuple(step.enzymes)
            if tupStep in enzyme_to_steps:
                enzyme_to_steps[tupStep].append(step)
            else:
                enzyme_to_steps[tupStep] = [step]
        
        for enzymeList in enzyme_to_steps:
            reaction = []
            reaction.append((Reagent.ddH2O, 33.5))
            reaction.append((Reagent.NEB_Buffer_2_10x, 5))
            reaction.append((Reagent.dna, 10))
            for enzyme in enzymeList:
                reaction.append((enzyme, 1))
            recipe = Recipe(None, reaction)

            for step in enzyme_to_steps[enzymeList]:
                dna = step.dna
                locations = inventory.construct_to_locations[dna]
                for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.zymo:
                        chosenLoc = loc
                        break
                if chosenLoc == None:
                    raise Exception('Null location for dna: ' + dna)
                sources.append((chosenLoc, dna))

                product = step.output
                locations = inventory.construct_to_locations[product]
                for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.zymo:
                        chosenLoc = loc
                        break
                if chosenLoc == None:
                    raise Exception('Null location for product: ' + product)
                destinations.append((chosenLoc, product))
        
            digestSheet = LabSheet(title, Digest, digestSteps, sources, destinations, program, protocol, instrument, notes, recipe)
            digestLabSheets.append(digestSheet)
    
        return digestLabSheets

    def ligateSheets(self, expName, ligateSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            ligateSteps: a list of Steps with the Ligate operation
            inventory: a current Inventory object
        Returns:
            ligateLabSheets: a list containing LabSheet objects corresponding to ligate steps
        '''

        ligateLabSheets = []

        title = expName + ': Ligation'
        sources = []
        destinations = []
        program = 'main/LIGATE'
        protocol = None
        instrument = 'Thermocycler 1A'
        notes = ['Never let enzymes warm up! Only take the enzyme cooler out of the freezer when you\n'
                 + 'are actively using it, and only take the tubes out of it when actively dispensing.']
        
        reaction = []
        reaction.append((Reagent.ddH2O, 7.5))
        reaction.append((Reagent.T4_DNA_Ligase_Buffer_10x, 1))
        reaction.append((Reagent.dna, 1))
        reaction.append((Reagent.T4_DNA_ligase, 0.5))
        recipe = Recipe(None, reaction)

        for step in ligateSteps:
            dnaList = step.dnas
            dnaLocs = []
            for dna in dnaList:
                locations = inventory.construct_to_locations[dna]
                for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.zymo:
                        chosenLoc = loc
                        break
                if chosenLoc == None:
                    raise Exception('Null location for dna: ' + dna)
                dnaLocs.append((chosenLoc, dna))
            sources.append(dnaLocs)

            product = step.output
            locations = inventory.construct_to_locations[product]
            for loc in locations:
                conc = inventory.loc_to_conc[loc]
                if conc == Concentration.zymo:
                    chosenLoc = loc
                    break
            if chosenLoc == None:
                raise Exception('Null location for product: ' + product)
            destinations.append((chosenLoc, product))
        
        ligateSheet = LabSheet(title, Ligate, ligateSteps, sources, destinations, program, protocol, instrument, notes, recipe)
        ligateLabSheets.append(ligateSheet)

        return ligateLabSheets

    def ggSheets(self, expName, ggSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            ggSteps: a list of Steps with the Golden Gate operation
            inventory: a current Inventory object
        Returns:
            ggLabSheets: a list containing LabSheet objects corresponding to Golden Gate steps
        '''

        ggLabSheets = []
        title = expName + ': Golden Gate Assembly'
        sources = []
        destinations = []
        programGG = 'main/GG1'
        protocolGG = 'Golden Gate Assembly'
        instrumentGG = 'Thermocycler 1A'
        notes = []

        enzyme_to_steps = {}

        for step in ggSteps:
            if step.enzyme in enzyme_to_steps:
                enzyme_to_steps[step.enzyme].append(step)
            else:
                enzyme_to_steps[step.enzyme] = [step]
        
        for enzyme in enzyme_to_steps:
            reaction = []
            reaction.append((Reagent.ddH2O, 6))
            reaction.append((Reagent.T4_DNA_Ligase_Buffer_10x, 1))
            reaction.append((Reagent.dna, 2))
            reaction.append((Reagent.T4_DNA_ligase, 0.5))
            reaction.append((enzyme, 1))
            recipe = Recipe(None, reaction)

            for step in enzyme_to_steps[enzyme]:
                dnas = step.dnas
                for dna in dnas:
                    locations = inventory.construct_to_locations[dna]
                    for loc in locations:
                        conc = inventory.loc_to_conc[loc]
                        if conc == Concentration.zymo:
                            chosenLoc = loc
                            break
                    if chosenLoc == None:
                        raise Exception('Null location for dna: ' + dna)
                    sources.append((chosenLoc, dna))
        
            ggLabSheet = LabSheet(title, GoldenGate, ggSteps, sources, destinations, programGG, protocolGG, instrumentGG, notes, recipe)
            ggLabSheets.append(ggLabSheet)

        return ggLabSheets
    
    def gibsonSheets(self, expName, gibsonSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            gibsonSteps: a list of Steps with the Gibson Assembly operation
            inventory: a current Inventory object
        Returns:
            gibLabSheets: a list containing LabSheet objects corresponding to Gibson Assembly steps
        '''

        gibLabSheets = []
        title = expName + ': Gibson Assembly'
        sources = []
        destinations = []
        programGib = 'main/GG1'
        protocolGib = 'Gibson Assembly'
        instrumentGib = 'Thermocycler 1A'
        notes = []

        reactionGib = []
        reactionGib.append((Reagent.ddH2O, 6))
        reactionGib.append((Reagent.Gibson_Assembly_Master_Mix, 10))
        reactionGib.append((Reagent.dna, 4))
        recipeGib = Recipe(None, reactionGib)

        for step in gibsonSteps:
            dnas = step.dnas
            for dna in dnas:
                locations = inventory.construct_to_locations[dna]
                for loc in locations:
                    conc = inventory.loc_to_conc[loc]
                    if conc == Concentration.zymo:
                        chosenLoc = loc
                        break
                if chosenLoc == None:
                    raise Exception('Null location for dna: ' + dna)
                sources.append((chosenLoc, dna))
        
        gibLabSheet = LabSheet(title, GoldenGate, gibsonSteps, sources, destinations, programGib, protocolGib, instrumentGib, notes, recipeGib)
        gibLabSheets.append(gibLabSheet)

        return gibLabSheets

    def transformSheets(self, expName, transformSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            transformSteps: a list of Steps with the Transform operation
            inventory: a current Inventory object
        Returns:
            allLabSheets: a list containing LabSheet objects corresponding to transform, pick, and miniprep steps
        '''

        allLabSheets = []

        title = expName + ': Transformation'
        sources = []
        destinationsTransform = []
        destinationsMiniprep = []
        program = ''
        protocol = ''
        instrument = ''
        recipe = None
        notes = ['Be gentle when mixing the cells or you will kill them. Never let cells warm up! They should never leave the cold block ']

        for step in transformSteps:
            dna = step.dna
            locations = inventory.construct_to_locations[dna]
            for loc in locations:
                conc = inventory.loc_to_conc[loc]
                if conc == Concentration.zymo:
                    chosenLoc = loc
                    break
            if chosenLoc == None:
                raise Exception('Null location for dna: ' + dna)
            sources.append((chosenLoc, dna))

            destinationsTransform.append((chosenLoc, dna, step.strain, step.antibiotics, step.temperature))
            
            product = step.output
            locations = inventory.construct_to_locations[product]
            for loc in locations:
                conc = inventory.loc_to_conc[loc]
                if conc == Concentration.miniprep:
                    chosenLoc = loc
                    destinationsMiniprep.append((chosenLoc, product, inventory.loc_to_clone[chosenLoc]))
            if chosenLoc == None:
                raise Exception('Null location for miniprep: ' + product)

        transformSheet = LabSheet(title, Transform, transformSteps, sources, destinationsTransform, program, protocol, instrument, notes, recipe)
        allLabSheets.append(transformSheet)

        title = expName + ': Pick'
        protocol = 'Pick 4 colonies into 4mL of 2YT + antibiotic in a 24-well block.'
        pickSheet = LabSheet(title, Pick, transformSteps, sources, destinationsTransform, program, protocol, instrument, notes, recipe)
        allLabSheets.append(pickSheet)

        title = expName + ': Miniprep'
        miniprepSheet = LabSheet(title, Miniprep, transformSteps, sources, destinationsMiniprep, program, protocol, instrument, notes, recipe)
        allLabSheets.append(miniprepSheet)
        return allLabSheets
    
    def gelSheets(self, expName, prevSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            prevSteps: a list of Steps that were completed prior to the Gel
            inventory: a current Inventory object
        Returns:
            gelSheets: a list containing LabSheet objects corresponding to Gel steps
        '''

        gelSheets = []
        title = expName + ': Gel'
        sources = ['Instrument from previous step.']
        destinations = []
        program = ''
        protocol = ''
        instrument = ''
        recipe = None
        notes = []

        for step in prevSteps:
            product = step.output
            locations = inventory.construct_to_locations[product]
            for loc in locations:
                conc = inventory.loc_to_conc[loc]
                if conc == Concentration.zymo:
                    chosenLoc = loc
                    break
            if chosenLoc == None:
                raise Exception('Null location for product: ' + product)
            destinations.append((chosenLoc, product, step.product_size))
    
        gelSheet = LabSheet(title, Gel, prevSteps, sources, destinations, program, protocol, instrument, notes, recipe)
        gelSheets.append(gelSheet)

        return gelSheets
        
    def zymoSheets(self, expName, prevSteps, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            prevSteps: a list of Steps that were completed prior to the Zymo
            inventory: a current Inventory object
        Returns:
            zymoSheets: a list containing LabSheet objects corresponding to Zymo steps
        '''

        zymoSheets = []
        zymoSteps = []
        title = expName + ': Zymo Cleanup'
        sources = ['Instrument from previous step.']
        destinations = []
        program = ''
        protocol = ''
        instrument = ''
        recipe = None
        notes = []

        for step in prevSteps:
            product = step.output
            if isinstance(step, PCR):
                zymoStep = Zymo('Zymo', product, 10)
            elif isinstance(step, Digest):
                zymoStep = Zymo('Zymo', product, 50)
            zymoSteps.append(zymoStep)
            
            locations = inventory.construct_to_locations[product]
            for loc in locations:
                conc = inventory.loc_to_conc[loc]
                if conc == Concentration.zymo:
                    chosenLoc = loc
                    break
            if chosenLoc == None:
                raise Exception('Null location for product: ' + product)
            destinations.append((chosenLoc, product))
        
        zymoSheet = LabSheet(title, Zymo, zymoSteps, sources, destinations, program, protocol, instrument, notes, recipe)
        zymoSheets.append(zymoSheet)
        return zymoSheets

    def run(self, expName, cfList, inventory):
        '''
        Parameters:
            expName: string for the corresponding experiment name
            cfList: a list of ConstructionFile objects corresponding to the experiment
            inventory: a current Inventory object
        Returns:
            labPacket: a LabPacket object
        '''

        pcrSteps = []
        digestSteps = []
        ligateSteps = []
        ggSteps = []
        gibsonSteps = []
        transformSteps = []
    
        for cf in cfList:
            for step in cf.steps:
                if step.operation == 'PCR':
                    pcrSteps.append(step)
                elif step.operation == 'Digest':
                    digestSteps.append(step)
                elif step.operation == 'Ligate':
                    ligateSteps.append(step)
                elif step.operation == 'Golden Gate':
                    ggSteps.append(step)
                elif step.operation == 'Gibson':
                    gibsonSteps.append(step)
                elif step.operation == 'Transform':
                    transformSteps.append(step)

        labSheets = []
        if pcrSteps:
            labSheets.extend(self.pcrSheets(expName, pcrSteps, inventory))
            labSheets.extend(self.zymoSheets(expName, pcrSteps, inventory))
            labSheets.extend(self.gelSheets(expName, pcrSteps, inventory))
        if digestSteps:
            labSheets.extend(self.digestSheets(expName, digestSteps, inventory))
            labSheets.extend(self.zymoSheets(expName, digestSteps, inventory))
        if ligateSteps:
            labSheets.extend(self.ligateSheets(expName, ligateSteps, inventory))
        if ggSteps:
            labSheets.extend(self.ggSheets(expName, ggSteps, inventory))
        if gibsonSteps:
            labSheets.extend(self.gibsonSheets(expName, gibsonSteps, inventory))
        if transformSteps:
            labSheets.extend(self.transformSheets(expName, transformSteps, inventory))

        labPacket = LabPacket(labSheets)
        return labPacket
