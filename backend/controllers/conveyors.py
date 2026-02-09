import serial
import json


class Conveyors:
    def __init__(self):
        self.serial = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            timeout=1
        )

    def deliver_product(self, board: int, stepper: int, steps: int, delay_us: int):
        msg = {
            "board": board,
            "stepper": stepper,
            "steps": steps,
            "delay_us": delay_us
        }

        data = json.dumps(msg) + "\n"
        self.serial.write(data.encode())

    def move_elevator(self, board:int|str):
        msg = {
            "board": 10,
            "stepper": 1,
            "delay_us": 800,
            "destination": board,
        }

        data = json.dumps(msg) + "\n"
        self.serial.write(data.encode())

    def move_elevators_conveyor(self):
        msg = {
            "board": 10,
            "stepper": 2,
            "delay_us": 800
        }

        data = json.dumps(msg) + "\n"
        self.serial.write(data.encode())




