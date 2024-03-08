from dataclasses import dataclass
from typing import Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEMITONES = {
    "A": 0,
    "A#": 1,
    "Bb": 1,
    "B": 2,
    "C": 3,
    "C#": 4,
    "Db": 4,
    "D": 5,
    "D#": 6,
    "Eb": 6,
    "E": 7,
    "F": 8,
    "F#": 9,
    "Gb": 9,
    "G": 10,
    "G#": 11,
    "Ab": 11,
}


class Note:
    def __init__(self, name: str, octave: int, shift_cents=0):
        assert name in SEMITONES
        self.name = name
        self.octave = octave
        self.semitone = SEMITONES[name]
        self.reference_pitch = 440
        self.frequency_Hz = (
            self.reference_pitch
            * 2 ** (self.semitone / 12)
            * 2 ** (octave - 4)
            * 2 ** (shift_cents / 1200)
        )


HARMONIC_SERIES_REFERENCE = {
    "1": Note("A", 1),
    "2": Note("A", 2),
    "3": Note("E", 2),
    "4": Note("A", 3),
    "5": Note("C#", 3, shift_cents=-12),
    "6": Note("E", 3),
    "7": Note("G", 3, shift_cents=-30),
    "8": Note("A", 4),
    "9": Note("B", 4),
    "10": Note("C#", 4, shift_cents=-12),
    "11": Note("D#", 4, shift_cents=-49),
    "12": Note("E", 4),
    "13": Note("F", 4, shift_cents=41),
    "14": Note("G", 4, shift_cents=-30),
    "15": Note("G#", 4, shift_cents=-12),
    "16": Note("A", 5),
}


class HarmonicSeries:
    def __init__(self, first_partial: Note):
        self.first_partial = first_partial
        reference_note = HARMONIC_SERIES_REFERENCE["1"]
        frequency_ratio = first_partial.frequency_Hz / reference_note.frequency_Hz
        self.frequencies = [
            note.frequency_Hz * frequency_ratio
            for note in HARMONIC_SERIES_REFERENCE.values()
        ]


class Spectrum:
    def __init__(self, note: Note, partial_number: int, quality_factor: float):
        self.quality_factor = quality_factor
        self.partial_number = partial_number
        self.note = note

        reference_note = HARMONIC_SERIES_REFERENCE[str(partial_number)]
        frequency_ratio = note.frequency_Hz / reference_note.frequency_Hz
        harmonic_frequencies = np.array(
            [
                note.frequency_Hz * frequency_ratio
                for note in HARMONIC_SERIES_REFERENCE.values()
            ]
        )

        self.harmonics_df = pd.DataFrame()
        self.harmonics_df["frequency_Hz"] = harmonic_frequencies
        self.harmonics_df["amplitude_dB"] = self.get_amplitudes(
            harmonic_frequencies, LPF_dB_per_octave=0, BPF_dB_per_octave=5
        )
        self.harmonics_df["partial_number"] = list(range(1, 1 + len(self.harmonics_df)))
        self.harmonics_df["quality_factor"] = quality_factor

    def get_amplitudes(self, frequencies, LPF_dB_per_octave=0, BPF_dB_per_octave=0):
        result = -LPF_dB_per_octave * np.log2(frequencies)
        result += (
            -BPF_dB_per_octave * np.log2(self.note.frequency_Hz / frequencies) ** 2
        )
        return result

    def generate_spectrum(self):
        df = pd.DataFrame()
        df["frequency_Hz"] = np.linspace(100, 2e3, 5000)
        df["total_susceptibility"] = 0
        for i, partial in self.harmonics_df.iterrows():
            key = f"partial {int(partial.partial_number)}"
            df[key] = 10 ** (partial.amplitude_dB / 10) * susceptibility(
                df.frequency_Hz,
                partial.frequency_Hz,
                partial.quality_factor,
            )
            df["total_susceptibility"] += df[key]

        df["spectrum_dB"] = dB(np.abs(df["total_susceptibility"]) ** 2)
        return df

    def plot(self):
        df = self.generate_spectrum()
        fig, ax = plt.subplots()
        ax.plot(df.frequency_Hz, df.spectrum_dB)
        ax.set_xscale("log")
        ax.plot(
            self.note.frequency_Hz,
            np.interp(self.note.frequency_Hz, df.frequency_Hz, df.spectrum_dB),
            "o",
        )
        plt.show()


def resonance_function(x, f0, Q):
    result = (1 - (x / f0) ** 2) ** 2 + x**2 / (f0**2 * Q**2)
    result *= Q**2
    result = 1 / result
    return result


def susceptibility(f, f0, Q):
    gamma = f0 / Q
    result = 1/(f0**2 - f**2 - 1j * gamma * f)
    return result * f0 * gamma


def dB(x):
    return 10 * np.log10(x)


if __name__ == "__main__":
    sp = Spectrum(Note("F", 4), 8, 100)
    sp.plot()
    ...
