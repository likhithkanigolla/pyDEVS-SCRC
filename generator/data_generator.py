import json
import random
import logging
import csv
import sys
import os
import joblib

class DataGenerator:
    def __init__(self, mode='random', config_file='generator/sensors_config.json', csv_file=None):
        if mode == 'csv' and csv_file is None:
            raise ValueError("CSV mode requires a valid CSV file path")
        elif mode == 'csv':
            self.generator = CSVDataGenerator(csv_file)
        elif mode == 'random':
            self.generator = RandomDataGenerator(config_file)
        else:
            raise ValueError(f"Unsupported mode: {mode}")


    def generate_value(self, sensor_name):
        return self.generator.generate_value(sensor_name)

    def generate_pulse_value(self, sensor_name):
        return self.generator.generate_pulse_value(sensor_name)

    def generate_camera_value(self, sensor_name):
        return self.generator.generate_camera_value(sensor_name)

class RandomDataGenerator:
    def __init__(self, config_file):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        with open(config_file, 'r') as file:
            self.config = json.load(file)
        logging.info('Loaded configuration from %s', config_file)

    def generate_value(self, sensor_name):
        logging.debug('Generating value for sensor: %s', sensor_name)
        sensor_config = self.config[sensor_name]
        min_value = sensor_config['min']
        max_value = sensor_config['max']
        step = sensor_config['step']
        
        if 'current_value' not in sensor_config:
            sensor_config['current_value'] = random.uniform(min_value, max_value)
            logging.debug('Initial value for %s: %f', sensor_name, sensor_config['current_value'])
        else:
            change = random.choice([-1, 1]) * step
            sensor_config['current_value'] += change
            logging.debug('Updated value for %s: %f', sensor_name, sensor_config['current_value'])
            if sensor_config['current_value'] > max_value:
                sensor_config['current_value'] = max_value
                logging.debug('Value for %s capped to max: %f', sensor_name, max_value)
            elif sensor_config['current_value'] < min_value:
                sensor_config['current_value'] = min_value
                logging.debug('Value for %s capped to min: %f', sensor_name, min_value)

        return sensor_config['current_value']
    
    def generate_pulse_value(self, sensor_name):
        sensor_config = self.config[sensor_name]
        sensor_config['current_value'] = random.choice([0, 1])
        return sensor_config['current_value']
    
    def generate_camera_value(self, sensor_name):
        logging.debug('Generating camera value for sensor: %s', sensor_name)
        sensor_config = self.config[sensor_name]
        if 'current_value' not in sensor_config:
            sensor_config['current_value'] = 1
            logging.debug('Initial camera value for %s: %f', sensor_name, sensor_config['current_value'])
        else:
            sensor_config['current_value'] += 1
            logging.debug('Updated camera value for %s: %f', sensor_name, sensor_config['current_value'])
        return sensor_config['current_value']

class CSVDataGenerator:
    def __init__(self, csv_file):
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.data = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append({sensor_name: float(value) for sensor_name, value in row.items() if value})
        self.index = 0
        logging.info('Loaded data from %s', csv_file)

    def get_next_row(self):
        if self.index < len(self.data):
            row = self.data[self.index]
            self.index = (self.index + 1) % len(self.data)
            logging.debug('Read row %d: %s', self.index, row)
            return row
        else:
            raise ValueError("No more data available")

    def generate_value(self, sensor_name):
        row = self.get_next_row()
        if sensor_name in row:
            value = row[sensor_name]
            logging.debug('Generated value for %s: %f', sensor_name, value)
            return value
        else:
            raise ValueError(f"No data for sensor: {sensor_name}")

    def generate_pulse_value(self, sensor_name):
        return self.generate_value(sensor_name)

    def generate_camera_value(self, sensor_name):
        return self.generate_value(sensor_name)