from pypdevs.DEVS import CoupledDEVS

from nodes.water_quality_node import WaterQualityNode
from nodes.water_level_node import WaterLevelNode
from nodes.water_quantity_node import WaterQuantityTypeOne
from nodes.water_quantity_node_cam import WaterQualityCamNode
from nodes.motor_controller_node import MotorControlNode

from sensors.ph_sensor import PHSensor
from sensors.temp_sensor import TempSensor
from sensors.tds_sensor import TDSSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.pulse_sensor import PulseSensor
from sensors.camera_sensor import CameraSensor
from sensors.current_sensor import CurrentSensor

from components.onem2m_interface import OneM2MInterface
from sink import Sink

esp_pins = {
    # ESP32 NodeMCU Pin Configuration
    "ADC": [32, 33, 34, 35, 36, 39],
    "DIGITAL_IO": [0, 2, 4, 12, 13, 14, 15],
    "PWM": [16, 17, 18, 19, 21, 23],
    "I2C": [22, 27],
    "SPI": [5, 18, 19, 23],
    "UART": [1, 3, 9, 10, 16, 17],
    "DAC": [25, 26],
    "TOUCH": [0, 2, 4, 12, 13, 14, 27],
    "RTC": [32, 33, 34, 35, 36, 39],
    "POWER": {"3V3": "External", "GND": "External"}
}

raspberry_pi_pins = {
    # Raspberry Pi GPIO Pin Configuration (Raspberry Pi 4 Model B)
    "GPIO": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    "I2C": [2, 3],  # SDA, SCL
    "SPI": [10, 11, 12, 13, 14, 15],  # MOSI, MISO, SCLK, CE0, CE1
    "UART": [14, 15],  # TX, RX
    "PWM": [18],  # PWM pin
    "ADC": None,  # Raspberry Pi does not have built-in ADC, requires external ADC like MCP3008
    "DIGITAL_IO": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],  # GPIO pins
    "DAC": None,  # Raspberry Pi does not have built-in DAC, requires external DAC like MCP4725
    "TOUCH": None,  # Raspberry Pi does not have built-in touch pins
    "RTC": None,  # External RTC module like DS3231 is needed
    "POWER": {"3V3": "External", "GND": "External"},
    "CSI": "Camera Serial Interface (CSI) Port",  # Special port for camera connection
}

class WaterQualityModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQualityModel")

        # Sensors
        ph_sensor = self.addSubModel(PHSensor("PHSensor"))
        temp_sensor = self.addSubModel(TempSensor("TempSensor"))
        tds_sensor = self.addSubModel(TDSSensor("TDSSensor"))

        # Node
        water_quality_node = self.addSubModel(WaterQualityNode("WaterQualityNode", esp_pins))

        # Interfaces and Sink
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors directly to the node's input ports
        self.connectPorts(temp_sensor.outport, water_quality_node.temp_inport)
        self.connectPorts(ph_sensor.outport, water_quality_node.ph_inport)
        self.connectPorts(tds_sensor.outport, water_quality_node.tds_inport)
        self.connectPorts(tds_sensor.outport, water_quality_node.turbudity_inport)

        # Connect node to the OneM2M interface
        self.connectPorts(water_quality_node.outport, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        self.connectPorts(onem2m_interface.outport, sink.inport)


class WaterLevelModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterLevelModel")
        
        ultrasonic_sensor = self.addSubModel(UltrasonicSensor("UltrasonicSensor"))
        temp_sensor = self.addSubModel(TempSensor("TempSensor"))
        
        water_level_node = self.addSubModel(WaterLevelNode("WaterLevelNode", esp_pins))
        
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))
        
        self.connectPorts(ultrasonic_sensor.outport, water_level_node.ultrasonic_inport)
        self.connectPorts(temp_sensor.outport, water_level_node.temp_inport)

        self.connectPorts(water_level_node.outport, onem2m_interface.inport)
        
        self.connectPorts(onem2m_interface.outport, sink.inport)

class WaterQuantityTypeOneModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQuantityTypeOneModel")
        
        pulse_sensor = self.addSubModel(PulseSensor("PulseSensor"))
        water_quantity_node = self.addSubModel(WaterQuantityTypeOne("WaterQuantityNode", esp_pins))
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))

        self.connectPorts(pulse_sensor.outport, water_quantity_node.pulse_inport)
        
        self.connectPorts(water_quantity_node.outport, onem2m_interface.inport)

        self.connectPorts(onem2m_interface.outport, sink.inport)
        
class WaterQualityCamNodeModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQualityCamNodeModel")

        camera_sensor = self.addSubModel(CameraSensor("CameraSensor"))
        water_quality_cam_node = self.addSubModel(WaterQualityCamNode("WaterQualityCamNode", raspberry_pi_pins))

        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))
        
        # Connecting the submodels
        self.connectPorts(camera_sensor.outport, water_quality_cam_node.csi_inport)
        self.connectPorts(water_quality_cam_node.outport, onem2m_interface.inport)
        self.connectPorts(onem2m_interface.outport, sink.inport)

class MotorControlNodeModel(CoupledDEVS):
    def __init__(self):
        super().__init__("MotorControlNodeModel")
        pulse_sensor = self.addSubModel(PulseSensor("PulseSensor"))
        motor_control_node = self.addSubModel(MotorControlNode("MotorControlNode", esp_pins))
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))

        self.connectPorts(pulse_sensor.outport, motor_control_node.pulse_inport)
        self.connectPorts(motor_control_node.outport, onem2m_interface.inport)
        self.connectPorts(onem2m_interface.outport, sink.inport)