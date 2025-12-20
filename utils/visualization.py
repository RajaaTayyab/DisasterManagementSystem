"""
Console-based visualization utilities.

This module intentionally avoids graphical output and instead
provides structured textual summaries suitable for logs and reports.
"""

from typing import Dict


def print_simulation_header() -> None:
    print("=" * 70)
    print(" DISASTER MANAGEMENT & EMERGENCY RESPONSE SIMULATION ")
    print("=" * 70)


def print_step(step: int, current_time: float) -> None:
    print(f"\n--- Simulation Step {step} | Time={round(current_time, 2)} ---")


def print_metrics(summary: Dict[str, float]) -> None:
    print("\n=== SIMULATION SUMMARY ===")
    for key, value in summary.items():
        print(f"{key:25s}: {value}")
    print("=" * 70)
