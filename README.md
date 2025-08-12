# Smart Balcony

## Simulation

### Purpose

Provide an end‑to‑end dry‑run of the Smart Balcony control logic without any physical hardware attached. The script mimics soil‑moisture depletion, publishes readings over MQTT, and toggles a virtual pump when the threshold is crossed.

### Files

* **configuration.yaml** – Home Assistant snippet that defines the MQTT sensor (`balcony/moisture`) and binary sensor (`balcony/pump_status`).
* **smart\_text.py** – Python 3.11 script that performs the simulation loop.

### Key Parameters (inside *smart\_text.py*)

* `broker_ip`, `broker_port`, `username`, `password` – MQTT connection details.
* `threshold` – Moisture percentage below which the pump turns on (default 50).
* Simulation timing – two‑second steps, sixty‑second total run, five‑second pump burst.
* Moisture loss – random one to five percent per step; pump adds twenty‑five percent back.

### Run Instructions

```bash
python -m venv .venv
source .venv/bin/activate
pip install paho-mqtt
# edit smart_text.py to set broker_ip
python simulation/smart_text.py
```

Check the console output and verify that Home Assistant entities update in real time.

### Expected Behaviour

```
[0s]  Moisture: 100.00
[2s]  Moisture: 96.37
...
[18s] Moisture: 48.21   # below threshold
[18s] Pump ON
[23s] Pump OFF – Moisture: 73.21
```

The loop ends automatically after sixty seconds and the MQTT client disconnects cleanly.

---

## Hardware

### Objective

Translate the simulated logic into a working prototype that senses real soil moisture with an Arduino and actuates a watering valve (MG90S servo) from a Raspberry Pi based on those readings.

### Bill of Materials

* Raspberry Pi 3 Model B v1.2
* Arduino Uno
* Capacitive soil‑moisture sensor
* MG90S micro‑servo (drives a pump or valve)
* Breadboard, jumper wires, USB A‑B cable
* Five‑volt two‑ampere power supply (recommended for servo)

### Wiring Summary

**Sensor to Arduino**

```
Sensor VCC : 5 V
Sensor GND : GND
Sensor AO  : A0
```

**Servo to Raspberry Pi**

```
Orange (signal) : GPIO 18 (pin 12)
Red (VCC)       : 5 V rail (pin 2 or external)
Brown (GND)     : Pi GND (pin 6)
```

Arduino connects to the Raspberry Pi over USB and usually appears as `/dev/ttyACM0`.

### Source Code

* **code\_test.py** – Reads serial moisture values, decides whether watering is needed, and commands the servo.
* **motor\_test.py** – Use to calibrate PWM duty‑cycle versus servo angle.
* **test\_sensor.py** – Prints raw ADC values for wet and dry soil to help set a reliable threshold.

### Arduino Sketch (not included here)

* Initialise serial communication at nine‑thousand six‑hundred baud.
* Read `analogRead(A0)` once per second.
* Send the integer value to the Pi with `Serial.println()`.

### Pi‑side Software Setup

```bash
sudo apt update
sudo apt install python3-pip
pip install pyserial RPi.GPIO
python hardware/code_test.py  # start the controller
```

### Calibration and Validation

1. Run **test\_sensor.py** with the probe in air (dry) and in saturated soil (wet) and note both readings.
2. Edit the threshold constant in **code\_test.py** (for example 700).
3. Execute **motor\_test.py** to confirm the servo travels the full range without jitter.
4. Water a plant until the sensor reports "wet," then let it dry naturally; the servo should trigger when the reading falls below the threshold.

### Troubleshooting

* **No serial data** – Confirm that the Arduino enumerates as `/dev/ttyACM0` with `ls /dev/ttyACM*`.
* **Servo stutters** – Use an external five‑volt supply and share ground between the Pi and the servo.
* **MQTT entities unavailable** – Ensure the simulation script is not running and that Home Assistant’s MQTT integration is enabled with matching topics.
