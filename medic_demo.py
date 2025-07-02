"""Minimal emergency assistant demo script."""

import argparse
import random
from dataclasses import dataclass
from typing import Iterable, Tuple

import geocoder
import heartpy as hp
import sounddevice as sd
import soundfile as sf

# Predefined dangerous situations and stress thresholds
DANGEROUS_SITUATIONS: dict[str, int] = {
    "fire": 8,
    "earthquake": 9,
    "flood": 7,
    "gas leak": 6,
    "gunshots": 10,
    "explosion": 9,
}

# Example medical professional locations (city -> coordinates)
MEDICAL_PROFESSIONALS: dict[str, Iterable[Tuple[str, Tuple[float, float]]]] = {
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
    """Container for vital measurements and computed stress."""

    heart_rate: float
    breathing_rate: float
    stress_score: float


def play_alert(filename: str = "alert_sound.wav") -> None:
    """Play an alert sound if the file exists."""
    try:
        data, sr = sf.read(filename, dtype="float32")
    except Exception as exc:  # pragma: no cover - demo only
        print(f"Unable to play alert sound: {exc}")
        return
    sd.play(data, sr)
    sd.wait()


def record_audio(duration: int = 30, sample_rate: int = 22050) -> Tuple[Iterable[float], int]:
    """Record audio from the microphone."""
    print(f"Recording {duration}s of audio...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording.squeeze(), sample_rate


def compute_stress(
    signal: Iterable[float],
    sample_rate: int,
    baseline_hr: int = 70,
    baseline_br: int = 15,
) -> StressResult:
    """Estimate a stress score using HeartPy."""

    filtered = hp.filter_signal(
        signal, cutoff=[0.8, 3.5], sample_rate=sample_rate, order=3, filtertype="bandpass"
    )
    wd, measures = hp.process(filtered, sample_rate, report_time=False)
    heart_rate = measures["bpm"]
    breathing_rate = 60 / (wd["resp_rate_ts"][1] - wd["resp_rate_ts"][0])
    stress_score = 0.5 * (heart_rate / 80) + 0.5 * (breathing_rate / 20)
    stress_score *= (1 + (heart_rate - baseline_hr) / baseline_hr) * (
        1 + (breathing_rate - baseline_br) / baseline_br
    )
    return StressResult(heart_rate, breathing_rate, stress_score)


def get_user_location() -> Tuple[str | None, Tuple[float, float] | None]:
    """Attempt to obtain the user's city and coordinates via IP lookup."""
    try:
        g = geocoder.ip("me")
    except Exception as exc:  # pragma: no cover - network
        print(f"Location lookup failed: {exc}")
        return None, None
    return g.city, g.latlng


def send_help_request(professional: str, city: str | None) -> None:
    """Placeholder for notifying a medical professional."""
    where = city or "your area"
    print(f"Requesting help from a {professional} near {where}...")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--duration", type=int, default=30, help="record duration in seconds")
    parser.add_argument("-r", "--sample-rate", type=int, default=22050, help="audio sample rate")
    parser.add_argument("-a", "--alert", default="alert_sound.wav", help="path to alert sound file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    user_input = input("What's happening? ").strip().lower()
    if user_input in DANGEROUS_SITUATIONS:
        play_alert(args.alert)

        signal, sr = record_audio(args.duration, args.sample_rate)
        result = compute_stress(signal, sr)
        city, latlng = get_user_location()
        print(f"Detected heart rate: {result.heart_rate:.1f} bpm")
        print(f"Detected breathing rate: {result.breathing_rate:.1f} bpm")
        print(f"Stress level: {result.stress_score:.2f}")
        print(f"Approximate location: {city} {latlng}")

        role = random.choice(list(MEDICAL_PROFESSIONALS.keys()))
        send_help_request(role, city)
    else:
        print("Situation not recognized as dangerous. Stay alert and safe.")


if __name__ == "__main__":
    main()
