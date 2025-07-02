# Medic Demo

This repository contains a simple proof–of–concept for an emergency assistant.
The demo prompts the user for a description of the situation, records a short
audio sample and estimates a stress level from the recording.

> **Note**: This project is for demonstration purposes only. It relies on
> third–party libraries such as `sounddevice`, `soundfile`, `geocoder`, and
> `heartpy`. These packages may require additional system dependencies.

## Dependencies

Install the required libraries with:

```bash
pip install sounddevice soundfile geocoder heartpy
```

## Usage

```bash
python medic_demo.py
```

Pass `--help` to see command–line options such as the recording duration or
sample rate.

Follow the on-screen instructions. If the situation matches a predefined dangerous scenario, an alert sound is played and a stress score is calculated. The script then displays your estimated location and stress level.

The implementation can be extended to notify medical professionals or emergency contacts.
