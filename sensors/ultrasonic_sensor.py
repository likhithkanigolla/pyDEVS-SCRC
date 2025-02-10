from pypdevs.DEVS import AtomicDEVS
from generator.data_generator import DataGenerator

class UltrasonicSensor(AtomicDEVS):
    def __init__(self, name):
        super(UltrasonicSensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {"distance": 0}
        self.priority = 1

    def intTransition(self):
        self.state["distance"] = self.data_generator.generate_value("ultrasonic_sensor")
        return self.state

    def extTransition(self, inputs):
        return self.state

    def outputFnc(self):
        print(f"[self.name]Generating Distance: {self.state['distance']}")
        return {self.outport: self.state["distance"]}

    def timeAdvance(self):
        return 1.0
    
    def __lt__(self, other):
            return self.priority < other.priority