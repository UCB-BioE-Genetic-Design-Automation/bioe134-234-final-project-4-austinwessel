from src.models.experiment import *
from src.factories.inventory_factory import *
from src.models.labplanner import *
from src.factories.lab_packet_factory import LabPacketFactory
from src.factories.oligo_list_factory import *

class ExperimentFactory:
    '''
    This class is written with the structure of the original ExperimentFactory class in Java.
    '''
    inventoryFactory = InventoryFactory()
    labPacketFactory = LabPacketFactory()

    def run(self, experimentName, experimentID, cfList, oldInventory):
        '''
        Parameters:
            experimentName: a string of the experiment name
            experimentID: a string of the ID number of the experiment
            cflist: a list of ConstructionFile objects for the corresponding experiment
            oldInventory: an Inventory object for the existing (old) inventory
        Returns: 
            experiment: an Experiment object
        '''
        self.sequences = {}
        for cf in cfList:
            if cf.sequences:
                self.sequences.update(cf.sequences)
        self.oligoList = None
        self.inventory = self.inventoryFactory.run(experimentName, experimentID, cfList, oldInventory)
        self.packet = self.labPacketFactory.run(experimentName, cfList, self.inventory)
        
        experiment = Experiment(experimentName, cfList, self.oligoList, self.sequences, self.packet, self.inventory)

        return experiment
