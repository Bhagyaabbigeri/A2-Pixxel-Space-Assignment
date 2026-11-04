### 1. Orbit Period
- **Columns & Rows Used:** `timestamp_utc` (Column A) and `eclipse` (Column C).
- **Step-by-Step Analysis:** Manually audited across 30 eclipse entry events (starting at **Excel Row 273** where `eclipse` flips from 0 to 1). Measuring the time between consecutive shadow entries across 48 hours yielded 29 full orbit intervals.
- **Quantitative Results:** Mean orbital period = **95.11 minutes** (Min = 95.00 min, Max = 95.17 min, std dev = 0.078 min), confirming nominal Low Earth Orbit behavior matching textbook predictions.

### 2. Eclipse Duration & Fraction
- **Columns & Rows Used:** `timestamp_utc` (Column A) and `eclipse` (Column C).
- **Mean Duration:** **34.85 minutes** (Range: 34.83 to 35.00 min, measured precisely from shadow entry at **Excel Row 273** to shadow exit at **Excel Row 482** where `eclipse` returns to 0).
- **Eclipse Fraction:** Eclipse duration divided by mean orbit period = 34.85 / 95.11 = **0.3664** (**36.64%** of each orbit spent in darkness).

### 3. State-of-Charge Depth per Eclipse
- **Columns & Rows Used:** `batt_soc_pct` (Column F) and `batt_current_a` (Column E).
- **Definition & Result:** Battery state of charge at shadow entry minus the lowest SoC reached before recharging resumes (`batt_current_a > 0`). Mean depth = **9.32%** (Range: 6.69% to 10.99%).
- **Stability:** Drain depth per eclipse is stable (~9%), but baseline SoC is unstable. It decays from ~99.7% down to **77.48%** at orbit 30 because a stuck heater (`heater_a` = 0.9 A starting at **Excel Row 7086**) prevents full recharge.

### 4. Power-Positive Definition
A LEO satellite is power-positive when orbital generation equals or exceeds consumption, ensuring the battery fully recovers its state of charge (net SoC change >= 0) before each eclipse.

### 5. Losing Power-Positive
- **Evidence & Threshold:** Monitor entry SoC. If entry SoC drops below 98.0% for 3 consecutive orbits, it confirms a sustained energy deficit.
- **Application:** **KESTREL-4 is NOT power-positive.** Entry SoC dropped to **98.36%** at Orbit 14 (**Excel Row 7696**, `2026-09-14 21:57:40 UTC`), followed by 96.92% and 95.77%, confirming persistent loss of power-positive operation.

### Deliverable Summary Table
| Metric | Value | Range / Spread |
| :--- | :--- | :--- |
| **Orbit Period** | **95.11 min** | Min: 95.00 min, Max: 95.17 min |
| **Eclipse Duration** | **34.85 min** | Min: 34.83 min, Max: 35.00 min |
| **Eclipse Fraction** | **0.3664 (36.64%)** | — |
| **SoC Depth per Eclipse** | **9.32%** | Min: 6.69%, Max: 10.99% |

*Data cleaning: 4 duplicate timestamps sorted; 1,510 s telemetry gap near Sept 15 20:11 UTC.*

## Decision record
- **AI assistance:** Used AI to parse telemetry columns and structure script logic.
- **What I kept:** Period/eclipse math and power-positive definition.
- **What I changed:** Cross-checked manual CSV row transitions (Excel rows 273, 482, 7086, 7696), identified stuck heater at Orbit 13, and set 3-orbit threshold at Orbit 14.