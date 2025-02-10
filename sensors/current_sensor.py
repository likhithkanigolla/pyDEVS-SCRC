from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class CurrentSensor(AtomicDEVS):
    def __init__(self, name):
        super(CurrentSensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"current": 0}
        self.priority = 1

    def intTransition(self):
        self.state["current"] = self.data_generator.generate_value("current_sensor")
        return self.state

    def extTransition(self, inputs):
        # if self.in_port in inputs:
        #     self.state = inputs[self.in_port]
        return self.state

    def outputFnc(self):
        return {self.outport: self.state["current"]}

    def timeAdvance(self):
        return 1.0
    
    def __lt__(self, other):
            return self.priority < other.priority