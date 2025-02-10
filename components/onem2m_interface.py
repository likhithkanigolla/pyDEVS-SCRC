from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class OneM2MInterfaceState:
    def __init__(self):
        self.processing_time = 0.0
        self.data_to_send = None

class OneM2MInterface(AtomicDEVS):
    def __init__(self, name, simulated_delay=1.0):
        super().__init__(name)
        self.simulated_delay = float(simulated_delay)  # Ensure simulated_delay is a float
        self.state = OneM2MInterfaceState()
        self.timeLast = 0.0
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")
        self.priority = 4  # Example priority attribute

    def timeAdvance(self):
        if self.state.data_to_send is None:
            return INFINITY
        return self.state.processing_time - self.timeLast

    def extTransition(self, inputs):
        self.state.data_to_send = inputs[self.inport]
        self.state.processing_time = self.timeLast + self.simulated_delay
        return self.state

    def outputFnc(self):
        sensor_data = self.state.data_to_send
        transformed_data = {
            "m2m:sgn": {
                "m2m:nev": {
                    "m2m:rep": {
                        "m2m:cin": {
                            "con": sensor_data["m2m:cin"]["con"],
                            "ri": "cin7124901579521707503",
                            "pi": "cnt8702778900039637980",
                            "rn": "cin_UKmyMwKBXt",
                            "ct": "20231207T061300,532674",
                            "lt": "20231207T061300,532674",
                            "ty": 4,
                            "cs": len(sensor_data["m2m:cin"]["con"]),
                            "st": 0,
                            "cnf": "text/plain:0",
                            "con": sensor_data["m2m:cin"]["con"]
                        }
                    },
                    "m2m:rss": 1
                },
                "m2m:sud": 'false',
                "m2m:sur": "/in-cse/sub-632211058"
            }
        }
        self.state.data_to_send = None
        print(f"OneM2M Interface simulated sending: {transformed_data}")
        return {self.outport: transformed_data}

    def intTransition(self):
        self.timeLast = self.state.processing_time
        self.state.processing_time = INFINITY
        return self.state

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority