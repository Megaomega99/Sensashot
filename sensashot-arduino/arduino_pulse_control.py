import serial
import time
import subprocess
import os
import requests
import zipfile
import platform

class ArduinoCliManager:
    def __init__(self):
        self.cli_path = self._setup_arduino_cli()

    def _setup_arduino_cli(self):
        """Download and setup arduino-cli if not present"""
        cli_path = os.path.join(os.getcwd(), "arduino-cli.exe")

        if not os.path.exists(cli_path):
            print("Downloading arduino-cli...")
            url = "https://github.com/arduino/arduino-cli/releases/latest/download/arduino-cli_Windows_64bit.zip"

            try:
                response = requests.get(url)
                with open("arduino-cli.zip", "wb") as f:
                    f.write(response.content)

                with zipfile.ZipFile("arduino-cli.zip", 'r') as zip_ref:
                    zip_ref.extract("arduino-cli.exe", ".")

                os.remove("arduino-cli.zip")
                print("Arduino CLI downloaded successfully")
            except Exception as e:
                print(f"Error downloading arduino-cli: {e}")
                return None

        return cli_path

    def setup_arduino_environment(self, board="arduino:avr:uno"):
        """Setup Arduino environment"""
        if not self.cli_path:
            return False

        try:
            # Initialize config
            subprocess.run([self.cli_path, "config", "init"], check=True, capture_output=True)

            # Update core index
            subprocess.run([self.cli_path, "core", "update-index"], check=True, capture_output=True)

            # Install Arduino AVR core
            subprocess.run([self.cli_path, "core", "install", "arduino:avr"], check=True, capture_output=True)

            print("Arduino environment setup complete")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting up Arduino environment: {e}")
            return False

    def compile_and_upload(self, sketch_path, port, board="arduino:avr:uno"):
        """Compile and upload Arduino sketch"""
        if not self.cli_path:
            print("Arduino CLI not available")
            return False

        try:
            # Compile
            print("Compiling sketch...")
            subprocess.run([
                self.cli_path, "compile",
                "--fqbn", board,
                sketch_path
            ], check=True, capture_output=True)

            # Upload
            print(f"Uploading to {port}...")
            subprocess.run([
                self.cli_path, "upload",
                "--fqbn", board,
                "--port", port,
                sketch_path
            ], check=True, capture_output=True)

            print("Upload successful!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error during compile/upload: {e}")
            return False

class ArduinoPulseController:
    def __init__(self, port='COM5', baudrate=9600):
        """
        Initialize Arduino connection

        Args:
            port (str): Arduino COM port (Windows) or device path (Linux/Mac)
            baudrate (int): Communication speed
        """
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"Connected to Arduino on {port}")
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            self.arduino = None

    def send_pulse(self, pin_number):
        """
        Send 200ms pulse to specified Arduino pin

        Args:
            pin_number (int): Arduino pin number (3, 5, 6, or 9)
        """
        if self.arduino is None:
            print("Arduino not connected")
            return

        if pin_number not in [3, 5, 6, 9]:
            print("Invalid pin. Use pins 3, 5, 6, or 9")
            return

        try:
            # Send command to Arduino
            command = f"PULSE_{pin_number}\n"
            self.arduino.write(command.encode())
            print(f"200ms pulse sent to pin {pin_number}")

            # Wait for Arduino response
            response = self.arduino.readline().decode().strip()
            if response:
                print(f"Arduino response: {response}")

        except Exception as e:
            print(f"Error sending pulse: {e}")

    def close(self):
        """Close Arduino connection"""
        if self.arduino:
            self.arduino.close()
            print("Arduino connection closed")

def main():
    print("=== Arduino Pulse Controller Setup ===")

    # Ask user if they want to upload the sketch
    upload_sketch = input("Do you want to upload the Arduino sketch? (y/n): ").lower().strip()

    if upload_sketch == 'y':
        print("\n--- Setting up Arduino CLI and uploading sketch ---")
        cli_manager = ArduinoCliManager()

        if cli_manager.cli_path:
            # Setup Arduino environment
            if cli_manager.setup_arduino_environment():
                # Upload the sketch
                sketch_path = os.path.join(os.path.dirname(__file__), "arduino_sketch")
                if cli_manager.compile_and_upload(sketch_path, "COM5"):
                    print("Sketch uploaded successfully!")
                    time.sleep(3)  # Wait for Arduino to restart after upload
                else:
                    print("Failed to upload sketch")
                    return
            else:
                print("Failed to setup Arduino environment")
                return
        else:
            print("Failed to setup Arduino CLI")
            return

    print("\n--- Starting Arduino communication ---")
    # Initialize controller
    controller = ArduinoPulseController()

    if controller.arduino is None:
        print("Failed to connect to Arduino. Please check connection and port.")
        return

    print("\nArduino Pulse Controller")
    print("Press 1-4 to send pulses to pins 3,5,6,9 respectively")
    print("Press 'q' to quit")

    # Pin mapping: user input -> Arduino pin
    pin_mapping = {
        '1': 3,
        '2': 5,
        '3': 6,
        '4': 9
    }

    try:
        while True:
            user_input = input("\nEnter command (1-4 or q): ").strip()

            if user_input.lower() == 'q':
                break
            elif user_input in pin_mapping:
                pin = pin_mapping[user_input]
                controller.send_pulse(pin)
            else:
                print("Invalid input. Use 1-4 or 'q' to quit")

    except KeyboardInterrupt:
        print("\nProgram interrupted")

    finally:
        controller.close()

if __name__ == "__main__":
    main()