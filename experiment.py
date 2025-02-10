from pypdevs.simulator import Simulator
from model import WaterQualityModel, WaterLevelModel, WaterQuantityTypeOneModel, WaterQualityCamNodeModel, MotorControlNodeModel
from generator.data_generator import DataGenerator
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'random'
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None

    logging.debug("Starting the model")
    
    model = WaterQualityModel()
    # model = WaterLevelModel()
    # model = WaterQuantityTypeOneModel()
    # model = WaterQualityCamNodeModel()
    # model = MotorControlNodeModel()
    
    logging.debug("Model Loaded")
    
    data_generator = DataGenerator(mode=mode, csv_file=csv_file)
    sim = Simulator(model)
    logging.debug("Simulator Loaded")
    
    sim.setClassicDEVS()
    logging.debug("Classic DEVS set")
    
    sim.setVerbose()
    logging.debug("Verbose mode set")
    
    # sim.setTerminationTime(86400)  # 24 hours
    sim.setTerminationTime(10) # 5 minutes
    logging.debug("Termination time set")
    
    logging.debug("Starting simulation")
    sim.simulate()
    logging.debug("Simulation finished")