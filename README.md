# Real-Time E-Commerce Fraud Pipeline

Streams held-out credit-card transactions through a class-weighted Random Forest and shows fraud alerts on a live terminal dashboard built with `Rich`.

**Stack:** Python, pandas, scikit-learn (`RandomForestClassifier`), Rich

## Results

Evaluated on a stratified 20% hold-out: 56,962 transactions, 98 of them fraud.

| Metric (fraud class) | Value |
|---|---|
| Precision | 0.593 |
| Recall | 0.847 |
| F1 | 0.698 |
| PR-AUC | 0.804 |

| | Predicted legit | Predicted fraud |
|---|---|---|
| **Actual legit** | 56,807 | 57 |
| **Actual fraud** | 15 | 83 |

The model catches 83 of 98 frauds (84.7%) and raises 57 false alarms (precision 59.3%). Accuracy is not reported on purpose: only 0.17% of transactions are fraud, so predicting "legit" every time would already score 99.8%.

Setup: 80/20 stratified split, `random_state=42`, `RandomForestClassifier(n_estimators=30, max_depth=8, class_weight="balanced")`. Reproduce with `python evaluate.py`.

## Dataset

[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (ULB, Kaggle): 284,807 transactions, about 0.17% fraud, with anonymised features `V1`-`V28` plus `Time`, `Amount` and the `Class` label. The CSV is about 150 MB and is not in this repo: download it and put `creditcard.csv` next to `analysis.py`.

## How it works

```text
creditcard.csv ──► 80/20 stratified split ──► Random Forest (class-weighted, trained on 80%)
                                                      │
                          20% hold-out replayed row by row, scored per transaction
                                                      ▼
                                       Rich live terminal dashboard
```

- `analysis.py` trains the model, then replays the hold-out set one transaction at a time (0.04 s delay, so at most about 25 transactions per second) and flags a transaction when the model predicts fraud.
- The dashboard shows processed count, frauds flagged, USD value flagged, flag rate, and the latest alerts marked true or false positive using the known label.
- `evaluate.py` trains the same model and prints precision, recall, F1, PR-AUC and the confusion matrix.

### Dashboard layout (illustrative mock-up, numbers differ from a real run)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      ⚡ LIVE PIPELINE INGESTION METRICS ⚡                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────┐┌────────────────────────────────────────────────┐
│ Processed Tx:         142,450        ││ [🚨 TRUE POSITIVE] ID: 10421 | Risk: 98.4%      │
│ Fraud Intercepted:    244            ││ [🚨 TRUE POSITIVE] ID: 10589 | Risk: 91.1%      │
│ Capital Flagged:      $32,410.50     ││ [⚠️ FALSE POSITIVE] ID: 11043 | Risk: 67.8%     │
│ Anomalous Act. Rate:  0.171%         ││ [🚨 TRUE POSITIVE] ID: 11201 | Risk: 94.3%      │
└──────────────────────────────────────┘└────────────────────────────────────────────────┘
```

## Run it

```bash
git clone https://github.com/Sjhere11/real_time-ecommerce-fraud-pipeline.git
cd real_time-ecommerce-fraud-pipeline
pip install pandas scikit-learn rich
# put creditcard.csv next to analysis.py, then:
python evaluate.py     # metrics, about 30 seconds
python analysis.py     # live dashboard, about 40 minutes for the full hold-out; Ctrl+C to stop
```

## Limitations

- One random split and no cross-validation. The 0.5 decision threshold is not tuned, so precision and recall can be traded against each other.
- The "stream" is a simulation: it replays the test set with a fixed delay. The transactions-per-second figure is the replay rate, not measured throughput or latency.
- Features `V1`-`V28` are anonymised, so the model cannot be explained in business terms.
