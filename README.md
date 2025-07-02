# Medic Demo

This repository contains a simple proof-of-concept for an emergency assistant. The demo prompts the user for a description of the situation, records a short audio sample, and estimates a stress level from the recording.

> **Note**: This project is only a demonstration. It relies on third-party libraries such as `sounddevice`, `soundfile`, `librosa`, and `heartpy`. These packages may require additional system dependencies.

## Usage

```bash
python medic_demo.py
```

Follow the on-screen instructions. If the situation matches a predefined dangerous scenario, an alert sound is played and a stress score is calculated. The script then displays your estimated location and stress level.

The implementation can be extended to notify medical professionals or emergency contacts.
