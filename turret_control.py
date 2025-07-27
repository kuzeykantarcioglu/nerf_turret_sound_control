import numpy as np
import pyaudio
import time
from scipy.signal import hamming
from scipy.fftpack import fft
import lgpio  # For GPIO control on Raspberry Pi

# GPIO Pin Configuration
STEP_PIN = 17        # Stepper motor step pin
DIR_PIN = 27         # Stepper motor direction pin
SOLENOID_PIN = 22    # Solenoid control pin

# Frequency Ranges for Notes (in Hz)
NOTES = {
    'G': (690, 710),
    'B': (820, 840),
    'D': (515, 535),
}

# Initialize GPIO with lgpio
chip = lgpio.gpiochip_open(0)  # Open GPIO chip
if chip < 0:
    raise RuntimeError("Failed to open GPIO chip")

lgpio.gpio_claim_output(chip, STEP_PIN)  # Claim STEP_PIN as output
lgpio.gpio_claim_output(chip, DIR_PIN)  # Claim DIR_PIN as output
lgpio.gpio_claim_output(chip, SOLENOID_PIN)  # Claim SOLENOID_PIN as output

lgpio.gpio_write(chip, STEP_PIN, 0)  # Set initial state to LOW
lgpio.gpio_write(chip, DIR_PIN, 0)
lgpio.gpio_write(chip, SOLENOID_PIN, 0)

# Helper Functions for Motor and Solenoid Control
def rotate_motor(clockwise=True):
    """Rotate the motor in the specified direction."""
    lgpio.gpio_write(chip, DIR_PIN, 1 if clockwise else 0)
    for _ in range(200):  # Adjust for the desired rotation
        lgpio.gpio_write(chip, STEP_PIN, 1)
        time.sleep(0.001)
        lgpio.gpio_write(chip, STEP_PIN, 0)
        time.sleep(0.001)

def fire_solenoid(active):
    """Activate or deactivate the solenoid."""
    lgpio.gpio_write(chip, SOLENOID_PIN, 1 if active else 0)

def get_note_from_frequency(freq):
    """Map a frequency to a note based on predefined ranges."""
    for note, (low, high) in NOTES.items():
        if low <= freq <= high:
            return note
    return None

# Note Detection Function
def detect_note():
    NUM_SAMPLES = 2048
    SAMPLING_RATE = 48000
    MIN_FREQUENCY = 60
    MAX_FREQUENCY = 1000

    pa = pyaudio.PyAudio()
    device_index = None

    # Find USB Microphone Device
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if "USB Audio" in info['name']:  # Match USB microphone name
            device_index = i
            break

    if device_index is None:
        raise ValueError("USB Microphone not found!")

    # Open audio stream
    try:
        _stream = pa.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=SAMPLING_RATE,
                          input=True,
                          frames_per_buffer=NUM_SAMPLES,
                          input_device_index=device_index)
    except Exception as e:
        print(f"Could not open audio stream: {e}")
        pa.terminate()
        return None

    try:
        while True:
            data = _stream.read(NUM_SAMPLES, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            normalized_data = audio_data / 32768.0
            window = hamming(NUM_SAMPLES)
            fft_data = np.abs(fft(window * normalized_data))[:NUM_SAMPLES // 2]

            # Detect peak frequency
            peak_index = np.argmax(fft_data[1:]) + 1
            if peak_index != len(fft_data) - 1:
                y0, y1, y2 = np.log(fft_data[peak_index - 1:peak_index + 2])
                x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
                frequency = (peak_index + x1) * SAMPLING_RATE / NUM_SAMPLES
            else:
                frequency = peak_index * SAMPLING_RATE / NUM_SAMPLES

            if MIN_FREQUENCY <= frequency <= MAX_FREQUENCY:
                print(f"Detected frequency: {frequency:.2f} Hz")
                note = get_note_from_frequency(frequency)
                if note:
                    return note
            time.sleep(0.01)
    except Exception as e:
        print(f"An error occurred during note detection: {e}")
    finally:
        _stream.stop_stream()
        _stream.close()
        pa.terminate()
    return None

# Main Loop
try:
    print("Starting sound-controlled turret. Press Ctrl+C to stop.")
    while True:
        note = detect_note()
        if note == 'G':  # Rotate clockwise
            print("Note G detected: Rotating clockwise.")
            rotate_motor(clockwise=True)
        elif note == 'B':  # Rotate counterclockwise
            print("Note B detected: Rotating counterclockwise.")
            rotate_motor(clockwise=False)
        elif note == 'D':  # Fire the Nerf gun
            print("Note D detected: Firing solenoid.")
            fire_solenoid(active=True)
            time.sleep(1)  # Fire for 1 second
            fire_solenoid(active=False)
        else:
            print("No note detected or unrecognized note.")
except KeyboardInterrupt:
    print("Shutting down turret.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    lgpio.gpiochip_close(chip)  # Clean up GPIO resources


