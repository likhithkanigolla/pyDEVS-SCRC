from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from pypdevs.infinity import INFINITY
import time, random, json

class WaterQualityCamState:
    def __init__(self):
        self.data_aggregated = {}
        if random.random() < 0.8:  # 80% chance
            self.next_internal_time = 300.0
        else:  # 20% chance
            self.next_internal_time = 300.0 + random.uniform(-111, 334) #values based on the average of min and max value of 5 sensors


class WaterQualityCamNode(AtomicDEVS):
    def __init__(self, name, esp_pins):
        print(f"Initializing WaterQualityCamNode with name: {name}")
        AtomicDEVS.__init__(self, name)
        self.state = WaterQualityCamState()
        self.timeLast = 0.0  # Initialize timeLast
        self.pins = esp_pins
        
        # Define ports
        self.csi_inport = self.addInPort("csi_in")
        self.outport = self.addOutPort("out")
        self.priority = 3  # Priority for nodes

    def timeAdvance(self):
        # Calculate the remaining time until the next send event
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_internal_time}, timeLast: {self.timeLast}")
        return self.state.next_internal_time - self.timeLast if self.state.data_aggregated else INFINITY

    def extTransition(self, inputs):
        # Update the state based on inputs from CSI
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.csi_inport in inputs:
            self.state.data_aggregated['camera'] = inputs[self.csi_inport]
            print(f"[{self.name}] Aggregated camera data: {self.state.data_aggregated['camera']}")
        self.timeLast = self.state.next_internal_time  # Update timeLast
        return self.state

    def intTransition(self):
        # Schedule the next send time
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_internal_time  # Update timeLast
        self.state.next_internal_time += 1.0
        return self.state

    def outputFnc(self):
        # Only send data if there is aggregated data
        if self.state.data_aggregated:
            timestamp = str(int(time.time()))
            camera_value = str(self.state.data_aggregated.get('camera', ''))
            con_value = [timestamp, camera_value]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WC", "WM-WC-KH98-00", "V4.1.0", "WM-WC-V4.1.0"],
                    "con": con_value
                }
            }
            print(f"[{self.name}] Sending aggregated data: {data_to_send}")
            # Clear the aggregated data after sending
            self.state.data_aggregated = {}
            return {self.outport: data_to_send}
        else:
            print(f"[{self.name}] No data to send.")
        return {}

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority




