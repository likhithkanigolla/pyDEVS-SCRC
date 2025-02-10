from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class PHSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.inport = self.addInPort("in_port") 
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"ph": 0}
        self.priority = 1
    
    def intTransition(self):
        self.state["ph"] = self.data_generator.generate_value("ph_sensor")
        return self.state
    
    def extTransition(self, inputs):
        return self.state

    def outputFnc(self):
        print(f"[{self.name}] Generating PH value: {self.state['ph']}")
        return {self.outport: self.state['ph']}

    def timeAdvance(self):
        return 5.0  
    
    def __lt__(self, other):
        return self.priority < other.priority