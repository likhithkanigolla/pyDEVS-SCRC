from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class PulseSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"pulse": 0}
        self.priority = 1

    def intTransition(self):
        self.state["pulse"] = self.data_generator.generate_value("pulse_sensor")
        return self.state
    
    def extTransition(self, inputs):
        return self.state
    
    def outputFnc(self):
        print(f"[{self.name}] Generating pulse value: {self.state['pulse']}")
        return {self.outport: self.state['pulse']}

    def timeAdvance(self):
        return 1.0
    
    def __lt__(self, other):
        return self.priority < other.priority