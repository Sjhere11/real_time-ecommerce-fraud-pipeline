# ⚡ Real-Time E-Commerce Fraud Ingestion & ML Pipeline

A high-performance, low-latency data engineering and machine learning backend pipeline designed to ingest streaming transaction vectors and perform immediate anomaly inference within milliseconds.

---

## 🏗️ System Architecture & Workflow

Instead of approaching the 150MB dataset via typical static notebooks, this project abstracts real-world financial data distribution patterns to simulate an live, enterprise-level streaming payment gateway engine:

```text
[ Streaming Source Vector ] ──► [ Feature Scaling Engine ] ──► [ Real-Time Inference Brain ]
                                                                        │
                                                                        ▼
                                                       [ Live Rich Terminal Analytical HUD ]
```

- **Data Processing Vector:** Loops systematically over test frames to cleanly replicate high-throughput transaction frequency streams.
- **Dynamic Preprocessing Matrix:** Integrates algorithmic feature scaling to accurately parse structural data dimensions.
- **Balanced Anomaly Evaluator:** Handles severe transaction classification imbalance using class-weight optimization vectors to guarantee robust structural predictions.

---

## 🖥️ Live Terminal Interface View

The pipeline shifts past structural overhead constraints by implementing a clean, responsive console dashboard framework using `Rich` to handle continuous live tracking updates without frontend browser lag:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               ⚡ LIVE PIPELINE INGESTION METRICS (BACKEND ACTIVE) ⚡                     │
│                        Status: Ingesting Stream • 25 Tx/sec                            │
└────────────────────────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────┐┌────────────────────────────────────────────────┐
│ 📊 Pipeline Performance Metrics      ││ 🚨 Production Security Stream Logs             │
│                                      ││                                                │
│ Processed Tx:         142,450        ││ [🚨 TRUE POSITIVE] ID: 10421 | Risk: 98.4%      │
│ Fraud Intercepted 🛑:  244           ││ [🚨 TRUE POSITIVE] ID: 10589 | Risk: 91.1%      │
│ Capital Flagged:      $32,410.50     ││ [⚠️ FALSE POSITIVE] ID: 11043 | Risk: 67.8%     │
│ Anomalous Act. Rate:  0.171%         ││ [🚨 TRUE POSITIVE] ID: 11201 | Risk: 94.3%      │
└──────────────────────────────────────┘└────────────────────────────────────────────────┘
```

---

## 🛠️ Infrastructure Core
- **Engine Core:** Python 3.x
- **Scientific Computations & Parsing:** Pandas, NumPy
- **Machine Learning Vectors:** Scikit-Learn (LogisticRegression Engine)
- **UI Terminal Controls:** Rich Frame Ingestion Engine

---

## 🚀 Execution & Initialization

To initialize and deploy this backend framework on your localized system configuration:

1. Clone the repository assets:
   ```bash
   git clone https://github.com/Sjhere11/real_time-ecommerce-fraud-pipeline.git
   cd real_time-ecommerce-fraud-pipeline/data
   ```

2. Provision the system operational dependency libraries:
   ```bash
   pip install pandas scikit-learn rich
   ```

3. Initialize the real-time core ingestion file:
   ```bash
   python analysis.py
   ```
