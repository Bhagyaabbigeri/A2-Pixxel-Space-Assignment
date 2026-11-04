# Pixxel Space Mission Operations — Assignment A2 (Power and Eclipse)

This repository contains the telemetry analysis scripts, data cleaning logs, and deliverables for **Question A2: Power and eclipse** of the Pixxel Mission Operations assignment.

## Repository contents

- **`a2_eda.py`**: Python script used to analyze `telemetry_48h.csv`, compute orbital periods, eclipse durations, eclipse fractions, and state-of-charge depths, and track the power-positive status of KESTREL-4.
- **`data_cleaning_log.md`**: Log of data cleaning steps, including handling duplicate timestamps and telemetry gaps.
- **`a2_report.md`**: Final textual report submitted in the Pixxel portal.

## How to run the analysis script

1. Ensure `telemetry_48h.csv` is in the repository root.
2. Run the analysis script with Python:

   ```bash
   python a2_eda.py
   ```
