from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from generator.data_generator import DataGenerator
import time

class CameraSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.data_generator = DataGenerator()
        self.state = {
            "number": 0,
            "image_data": None,
            "number_detected": None,
            "processing_time": 0,
            "status": "capturing"  # Start in capturing state
        }
        self.priority = 1

    def capture_image(self):
        # Simulate capturing an image
        self.state["image_data"] = f"image_data_{time.time()}"
        print(f"[{self.name}] Captured image: {self.state['image_data']}")

    def process_image(self):
        # Simulate processing the image to detect a number
        self.state["number_detected"] = self.data_generator.generate_camera_value("camera_sensor")
        print(f"[{self.name}] Detected number: {self.state['number_detected']}")

    def timeAdvance(self):
        if self.state["status"] == "idle":
            return INFINITY
        elif self.state["status"] == "capturing":
            return 1.0  # Time to capture an image
        elif self.state["status"] == "processing":
            return 2.0  # Time to process the image
        return INFINITY

    def extTransition(self, inputs):
        # Handle external inputs (future manual interventions)
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        self.state["status"] = "capturing"
        return self.state

    def intTransition(self):
        if self.state["status"] == "capturing":
            self.capture_image()
            self.state["status"] = "processing"
        elif self.state["status"] == "processing":
            self.process_image()
            self.state["status"] = "capturing"  # Loop back to capturing for continuous processing
        return self.state

    def outputFnc(self):
        if self.state["status"] == "processing" and self.state["number_detected"] is not None:
            print(f"[{self.name}] Outputting detected number: {self.state['number_detected']}")
            return {self.outport: self.state["number_detected"]}
        return {}

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority