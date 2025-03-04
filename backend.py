import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from smbus2 import SMBus
import board
import adafruit_dht
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase (Replace with your actual service account key path)
cred = credentials.Certificate("path/to/your/firebase-key.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com/'  
})

# Initialize the RFID reader
reader = SimpleMFRC522()

# List of authorized UIDs
authorized_uids = [48069935880, 279458742619]  # Replace with your authorized UIDs

# Delay between reads (in seconds)
read_delay = 2  # Adjust this value as needed

# BH1750 address and command settings
BH1750_ADDR = 0x23  
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_HIGH_RES_MODE = 0x10

# Initialize I2C bus
bus = SMBus(1)  

# Initialize the DHT11 sensor
dht_device = adafruit_dht.DHT11(board.D4)  

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO18 for the LED (or any other available GPIO pin)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

def read_light_intensity():
    bus.write_byte(BH1750_ADDR, CONTINUOUS_HIGH_RES_MODE)
    time.sleep(0.2)  
    raw_data = bus.read_i2c_block_data(BH1750_ADDR, CONTINUOUS_HIGH_RES_MODE, 2)
    light_level = (raw_data[0] << 8) + raw_data[1]
    light_level = light_level / 1.2  
    return light_level

def send_to_firebase(data):
    ref = db.reference('/sensor_data')  
    ref.set(data)

def check_led_status():
    led_status_ref = db.reference('/led_status')
    led_status = led_status_ref.get()  
    return led_status

def set_led_state():
    led_status = check_led_status()
    if led_status == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)  
    else:
        GPIO.output(LED_PIN, GPIO.LOW)   

try:
    print("Hold a tag near the reader to check access...")

    while True:
        set_led_state()
        id, _ = reader.read()  

        if id in authorized_uids:
            print("Access granted!")
            access_status = "Granted"
        else:
            print("Access denied!")
            access_status = "Denied"

        light_level = read_light_intensity()
        print(f"Light Level: {light_level:.2f} lux")

        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            print(f"Temperature: {temperature:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
        except RuntimeError as e:
            print(f"Error reading DHT11 sensor: {e}")
            temperature = None
            humidity = None

        data = {
            "rfid_access": access_status,
            "light_level": light_level,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": time.time()
        }

        send_to_firebase(data)
        time.sleep(read_delay)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
