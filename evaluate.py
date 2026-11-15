"""Evaluate the fraud model used in analysis.py on the same 20% stratified hold-out.

Looks for creditcard.csv next to this file, or in a ./data folder.
Run: python evaluate.py
"""
import os

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = next((p for p in (os.path.join(BASE_DIR, "creditcard.csv"),
                             os.path.join(BASE_DIR, "data", "creditcard.csv")) if os.path.exists(p)), None)
if CSV_PATH is None:
    raise SystemExit("creditcard.csv not found: put it next to evaluate.py (or in ./data).")

df = pd.read_csv(CSV_PATH)
X, y = df.drop(columns=["Class"]), df["Class"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Same model settings as analysis.py
model = RandomForestClassifier(n_estimators=30, max_depth=8, class_weight="balanced",
                               n_jobs=-1, random_state=42).fit(X_tr, y_tr)
pred = model.predict(X_te)
score = model.predict_proba(X_te)[:, 1]

print("rows:", len(df), "| test rows:", len(X_te), "| frauds in test:", int(y_te.sum()))
print("precision:", round(precision_score(y_te, pred), 4))
print("recall   :", round(recall_score(y_te, pred), 4))
print("F1       :", round(f1_score(y_te, pred), 4))
print("PR-AUC   :", round(average_precision_score(y_te, score), 4))
print(confusion_matrix(y_te, pred))
