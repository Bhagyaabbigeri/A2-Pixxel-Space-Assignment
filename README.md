# KESTREL-4 Power & Eclipse Analysis (Assignment A2)

This repository contains the exploratory data analysis script, data-cleaning documentation, and technical report for **Assignment A2: Power and Eclipse** of the Pixxel Mission Operations assessment. It evaluates 48 hours of **KESTREL-4** housekeeping telemetry (`2026-09-14 00:00:00 UTC` to `2026-09-16 00:00:00 UTC`, 10-second nominal cadence) to characterize orbital eclipse timing, battery State of Charge (SoC) depth-of-discharge, and spacecraft power-positive stability.

## 1. Repository Structure

* **a2_eda.py** — Python analysis script that cleans raw telemetry in memory, detects shadow entry/exit transitions, calculates orbital and eclipse durations, and tracks orbit-over-orbit battery SoC trends.
* **A2-MD.md** — Complete written submission for Question A2 covering orbital timing, eclipse energy balance, and power-margin degradation.
* **data_cleaning_log.md** — Step-by-step log of raw CSV data-quality issues identified and resolved in code prior to orbital and power calculations.
* **telemetry_48h.csv** — Raw 48-hour KESTREL-4 housekeeping dataset (17,134 rows across 22 telemetry channels).
* **README.md** — Project overview, key engineering results, and reproduction instructions.

## 2. Key Orbital & Power Findings

| Metric | Nominal Baseline (Pre-19:40 UTC Sept 14) | Degraded Regime (Post-19:40 UTC Sept 14) | Unit |
| :--- | :--- | :--- | :--- |
| Mean Orbit Period | 95.11 (range 95.00 to 95.17, std 0.08) | 95.11 | min |
| Mean Eclipse Duration | 34.85 (range 34.83 to 35.00, std 0.05) | 34.85 | min |
| Eclipse Fraction | 36.64 | 36.64 | % |
| Eclipse SoC Drop (DoD) | 9.19 mean (8.57 to 10.54) | 9.42 mean (6.53 to 10.89) | % |
| Peak Sunlit SoC Recovery | ~99.7 | Drains ~1.2 per orbit down to 68.33 | % |

* **Nominal Power-Positive Operation (`2026-09-14 00:00:00Z` to `19:39:50Z`):** During the first 12 orbits, solar array current averages 2.05 A in sunlight (0.00 A in eclipse) and the regulated bus holds at 27.88 V to 28.05 V. The battery discharges from ~99.7% at shadow entry to ~90.0% at shadow exit and recharges back to ~99.7% before the next eclipse.
* **Loss of Power-Positive Balance (`2026-09-14 19:40:00Z` Onward):** At Excel Row 7086 (`2026-09-14T19:40:00Z`), the battery heater (`heater_a`) latches ON at 0.9 A (~25 W continuous load) even though battery temperature is 19.45 °C (above the ~17.9 °C thermostat shutoff threshold). This constant parasitic load prevents full sunlit recharging, causing peak SoC to decay by ~1.2% per orbit and cross the 70.0% yellow low limit at `2026-09-15T21:42:00Z` (Row 16308), reaching a minimum of 68.33% (`2026-09-15T23:18:20Z`).

## 3. Data-Cleaning Pipeline (In-Memory)

To comply with mission data integrity rules, the raw `telemetry_48h.csv` file is never modified by hand. Instead, `a2_eda.py` performs the following cleaning steps in memory (detailed in `data_cleaning_log.md`):

1. **Timestamp Deduplication:** Removes 4 duplicate timestamp pairs between `2026-09-14 02:58:20Z` and `03:01:30Z` (Excel Rows 1072–1073, 1082–1083, 1088–1089, and 1094–1095) using `keep='first'` so time derivatives do not divide by zero.
2. **Chronological Sorting:** Fixes out-of-order logging between `2026-09-14 03:02:50Z` and `03:03:50Z` (Excel Rows 1104–1108, where `03:03:20Z–03:03:40Z` was recorded before `03:03:00Z–03:03:10Z`), restoring a continuous 10-second cadence.
3. **Telemetry Gap Masking:** Identifies the 1,510-second (25 min 10 s) downlink gap on `2026-09-15` between `20:11:50Z` (Row 15917) and `20:37:00Z` (Row 15918) and excludes that incomplete orbit from mean period and eclipse duration statistics rather than distorting slopes with linear interpolation.
4. **Transient Spike & Flatline Filtering:** Accounts for single-sample ADC bit-flips (such as `bus_voltage_v = 26.88 V` at Row 15246) and the 3-hour `batt_temp_c` sensor flatline at 18.40 °C (`2026-09-15 11:00:00Z` to `13:59:50Z`, Rows 12606–13685).

## 4. Prerequisites & Execution

Install the required Python packages:

```bash
pip install pandas numpy
