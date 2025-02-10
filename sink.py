from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class Sink(AtomicDEVS):
    def __init__(self, name="Sink"):
        super().__init__(name)
        self.inport = self.addInPort("in")

    def extTransition(self, inputs):
        print(f"[{self.name}] Received data: {inputs[self.inport]}")
        return self.state

    def timeAdvance(self):
        return INFINITY

    def outputFnc(self):
        return {}