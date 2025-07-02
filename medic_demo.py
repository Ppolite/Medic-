import random
from dataclasses import dataclass

import geocoder
import heartpy as hp
import sounddevice as sd
import soundfile as sf

# Predefined dangerous situations and stress thresholds
DANGEROUS_SITUATIONS = {
    "fire": 8,
    "earthquake": 9,
    "flood": 7,
    "gas leak": 6,
    "gunshots": 10,
    "explosion": 9,
}

# Example medical professional locations (city -> coordinates)
MEDICAL_PROFESSIONALS = {
    "nurse": [
        ("New York", (40.7128, -74.0060)),
        ("Los Angeles", (34.0522, -118.2437)),
    ],
    "doctor": [
        ("Chicago", (41.8781, -87.6298)),
        ("Houston", (29.7604, -95.3698)),
    ],
    "paramedic": [
        ("Philadelphia", (39.9526, -75.1652)),
        ("Phoenix", (33.4484, -112.0740)),
    ],
}


@dataclass
class StressResult:
    heart_rate: float
    breathing_rate: float
    stress_score: float


def play_alert(filename: str = "alert_sound.wav") -> None:
    """Play an alert sound."""
    data, sr = sf.read(filename, dtype="float32")
    sd.play(data, sr)
    sd.wait()


def record_audio(duration: int = 30, sample_rate: int = 22050):
    """Record audio from the microphone."""
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording.squeeze(), sample_rate


def compute_stress(signal, sample_rate: int, baseline_hr: int = 70, baseline_br: int = 15) -> StressResult:
    """Compute stress level from an audio signal."""
    filtered = hp.filter_signal(signal, cutoff=[0.8, 3.5], sample_rate=sample_rate, order=3, filtertype="bandpass")
    wd, measures = hp.process(filtered, sample_rate, report_time=False)
    heart_rate = measures["bpm"]
    breathing_rate = 60 / (wd["resp_rate_ts"][1] - wd["resp_rate_ts"][0])
    stress_score = 0.5 * (heart_rate / 80) + 0.5 * (breathing_rate / 20)
    stress_score *= (1 + (heart_rate - baseline_hr) / baseline_hr) * (1 + (breathing_rate - baseline_br) / baseline_br)
    return StressResult(heart_rate, breathing_rate, stress_score)


def get_user_location():
    """Attempt to obtain the user's city and coordinates via IP lookup."""
    g = geocoder.ip("me")
    return g.city, g.latlng


def send_help_request(professional: str, city: str) -> None:
    """Placeholder for notifying a medical professional."""
    print(f"Requesting help from a {professional} near {city}...")


def main() -> None:
    user_input = input("What's happening? ").strip().lower()
    if user_input in DANGEROUS_SITUATIONS:
        play_alert()

        signal, sr = record_audio()
        result = compute_stress(signal, sr)
        city, latlng = get_user_location()
        print(f"Detected heart rate: {result.heart_rate:.1f} bpm")
        print(f"Detected breathing rate: {result.breathing_rate:.1f} bpm")
        print(f"Stress level: {result.stress_score:.2f}")
        print(f"Approximate location: {city} {latlng}")

        # Choose a professional to notify (placeholder logic)
        role = random.choice(list(MEDICAL_PROFESSIONALS.keys()))
        send_help_request(role, city)
    else:
        print("Situation not recognized as dangerous. Stay alert and safe.")


if __name__ == "__main__":
    main()
