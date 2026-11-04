### 1. Orbit Period
- **Columns & Rows Used:** `timestamp_utc` (Column A) and `eclipse` (Column C).
- **Step-by-Step Analysis:** I tracked every time the satellite entered Earth's shadow (`eclipse` flipping from 0 to 1, starting at **Excel Row 273** at `00:45:10 UTC`). Measuring the time between 30 consecutive shadow entries across 48 hours yielded 29 full orbit intervals, avoiding the 1,510-second telemetry gap near Orbit 28.
- **Quantitative Results:** Mean orbital period = **95.11 minutes** (Min = 95.00 min, Max = 95.17 min, std dev = 0.078 min), matching standard ~520 km Low Earth Orbit behavior.

### 2. Eclipse Duration & Fraction
- **Columns & Rows Used:** `timestamp_utc` (Column A) and `eclipse` (Column C).
- **Mean Duration:** **34.85 minutes** (Range: 34.83 to 35.00 min, measured from shadow entry at **Excel Row 273** to shadow exit at **Excel Row 482** where `eclipse` returns to 0).
- **Eclipse Fraction:** Dividing mean eclipse duration by mean orbit period (`34.85 / 95.11`) gives **0.3664**, meaning **36.64%** of each orbit is spent in darkness on battery power.

### 3. State-of-Charge Depth per Eclipse
- **Columns & Rows Used:** `batt_soc_pct` (Column F), `batt_current_a` (Column E), and `heater_a` (Column O).
- **Definition & Result:** Battery state of charge at shadow entry minus the lowest SoC reached before recharging resumes (`batt_current_a > 0`). Mean depth = **9.32%** (Range: 6.69% to 10.99%).
- **Stability:** The ~9.3% drain per eclipse is stable, but the starting SoC before each eclipse is unstable. From Orbit 1 to 13, it recharges to ~99.7%. However, at Orbit 13 (**Excel Row 7086**, `20:16:00 UTC`), the heater (`heater_a`) gets stuck ON at **0.9 A**, preventing full recharge in sunlight and dragging minimum SoC down to **77.48%** by Orbit 30.

### 4. Power-Positive Definition
A LEO satellite is power-positive when solar energy generated during sunlight (~60.26 min) equals or exceeds total energy consumed by the bus, heaters, and payload across the full 95.11-minute orbit, ensuring the battery fully recovers its state of charge (net SoC change >= 0%) before the next eclipse.

### 5. Losing Power-Positive
- **Evidence & Threshold:** Monitor `batt_soc_pct` at consecutive shadow entries. If entry SoC drops below **98.5% for 3 consecutive orbits**, it confirms a sustained energy deficit rather than a single heavy imaging pass.
- **Application:** **KESTREL-4 is NOT power-positive.** After the heater sticks ON at Row 7086, entry SoC drops to **98.36%** at Orbit 14 (**Excel Row 7696**, `2026-09-14 21:57:40 UTC`), followed by **96.92%** (Orbit 15) and **95.77%** (Orbit 16), confirming persistent loss of power-positive operation.

### Deliverable Summary Table
| Metric | Value | Range / Spread |
| :--- | :--- | :--- |
| **Orbit Period** | **95.11 min** | Min: 95.00 min, Max: 95.17 min |
| **Eclipse Duration** | **34.85 min** | Min: 34.83 min, Max: 35.00 min |
| **Eclipse Fraction** | **0.3664 (36.64%)** | — |
| **SoC Depth per Eclipse** | **9.32%** | Min: 6.69%, Max: 10.99% |

*Data cleaning: 4 duplicate timestamps sorted; 1,510 s telemetry gap near Sept 15 20:11 UTC.*