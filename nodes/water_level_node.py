from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time, random

class WaterLevelNodeState:
    def __init__(self):
        self.data_aggregated = {}
        if random.random() < 0.8:  # 80% chance
            self.next_internal_time = 1.0
        else:  # 20% chance
            self.next_internal_time = 1.0 + random.uniform(-0.1, 0.3)

class WaterLevelNode(AtomicDEVS):
    def __init__(self, name, esp_pins):
        print(f"[{name}] Initializing WaterLevelNode.")
        AtomicDEVS.__init__(self, name)
        self.state = WaterLevelNodeState()
        self.timeLast = 0.0
        self.priority = 3
        self.pins = esp_pins
        
        # Access the first SPI pin for the ultrasonic and temp input ports
        self.ultrasonic_inport = self.addInPort(f"ultrasonic_in_{self.pins['UART'][0]}")
        self.temp_inport = self.addInPort(f"temp_in_{self.pins['SPI'][0]}")  # Use another SPI pin if required
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_internal_time}, timeLast: {self.timeLast}")
        return self.state.next_internal_time - self.timeLast if self.state.data_aggregated else INFINITY
    
    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.ultrasonic_inport in inputs:
            self.state.data_aggregated['ultrasonic'] = inputs[self.ultrasonic_inport]
            print(f"[{self.name}] Aggregated ultrasonic data: {self.state.data_aggregated['ultrasonic']}")
        if self.temp_inport in inputs:
            self.state.data_aggregated['temperature'] = inputs[self.temp_inport]
            print(f"[{self.name}] Aggregated temperature data: {self.state.data_aggregated['temperature']}")
        self.timeLast = self.state.next_internal_time  # Update timeLast
        return self.state
    
    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_internal_time  # Update timeLast
        self.state.next_internal_time += 1.0
        return self.state
    
    def outputFnc(self):
        if self.state.data_aggregated:
            timestamp = str(int(time.time()))
            temp_value = str(self.state.data_aggregated.get('temperature', ''))
            distance_value = str(self.state.data_aggregated.get('ultrasonic', ''))
            con_value = [timestamp, temp_value, distance_value]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WL", "WM-WL-KH98-00", "V2.1.0", "WM-WD-V2.1.0"],
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