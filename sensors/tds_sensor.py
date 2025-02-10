from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class TDSSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"tds": 0}
        self.priority = 1
        
    def intTransition(self):
        self.state["tds"] = self.data_generator.generate_value("tds_sensor")
        return self.state
    
    def extTransition(self, inputs):
        return self.state

    def outputFnc(self):
        print(f"[{self.name}] Generating TDS value: {self.state['tds']}")
        return {self.outport: self.state['tds']}
    
    def timeAdvance(self):
        return 5.0 

    def __lt__(self, other):
        return self.priority < other.priority