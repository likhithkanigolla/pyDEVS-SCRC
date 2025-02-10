from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class TurbiditySensor(AtomicDEVS):
    def __init__(self, name):
        super(TurbiditySensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"turbidity": 0}
        self.priority = 1
    
    def intTransition(self):
        self.state["turbidity"] = self.data_generator.generate_value("turbidity_sensor")
        return self.state
    
    def extTransition(self, inputs):
        return self.state
    
    def outputFnc(self):
        print(f"[{self.name}] Generating turbidity value: {self.state['turbidity']}")
        return {self.outport: self.state['turbidity']}
    
    def timeAdvance(self):
        return 5.0
    
    def __lt__(self, other):
        return self.priority < other.priority
    