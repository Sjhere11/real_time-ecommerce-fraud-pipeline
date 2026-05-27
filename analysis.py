import time
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Rich Terminal UI Imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

console = Console()

# Since analysis.py and creditcard.csv are in the same folder, look side-by-side
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "creditcard.csv")


def load_and_train():
    with console.status("[bold yellow]🔄 Stage 1/2: Ingesting Credit Card Dataset...", spinner="dots"):
        if not os.path.exists(CSV_PATH):
            console.print(f"[bold red]❌ Error: Cannot find '{CSV_PATH}'![/]")
            return None, None, None
        df = pd.read_csv(CSV_PATH)

    with console.status("[bold cyan]🔄 Stage 2/2: Training Live Core Model...", spinner="dots2"):
        X = df.drop(columns=['Class'])
        y = df['Class']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        # Hyperparameters balanced for streaming efficiency
        model = RandomForestClassifier(n_estimators=30, max_depth=8, class_weight='balanced', n_jobs=-1,
                                       random_state=42)
        model.fit(X_train, y_train)

    console.print("[bold green]✅ Model Synchronized! Ready to Ingest Transactions...[/]\n")
    return model, X_test, y_test


def build_dashboard(processed, flagged, amount_flagged, alert_records):
    # 1. Create the Metrics Table
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Processed Tx", justify="center")
    table.add_column("Fraud Intercepted 🛑", justify="center", style="bold red")
    table.add_column("Capital Flagged (USD)", justify="center", style="bold yellow")
    table.add_column("Anomalous Activity Rate", justify="center")

    rate = (flagged / processed * 100) if processed > 0 else 0
    table.add_row(f"{processed:,}", f"{flagged:,}", f"${amount_flagged:,.2f}", f"{rate:.4f}%")

    # 2. Extract trailing 12 alert strings
    log_display = "\n".join(alert_records[-12:])

    # 3. Combine them using a vertical layout inside a single Panel
    from rich.console import Group
    panel_content = Group(
        table,
        "\n",  # Spacer line
        Panel(log_display, title="🚨 Production Security Stream Logs", border_style="red")
    )

    return Panel(panel_content, title="⚡ LIVE PIPELINE INGESTION METRICS ⚡", border_style="cyan")


if __name__ == "__main__":
    model, X_test, y_test = load_and_train()

    if model is not None:
        total_processed = 0
        fraud_detected = 0
        total_usd_flagged = 0.0
        alert_log = ["[dim white]System Listening: Pipeline empty...[/]"]

        # Run full terminal override canvas
        with Live(build_dashboard(0, 0, 0, alert_log), refresh_per_second=5, screen=True) as live:
            for idx, row in X_test.iterrows():
                total_processed += 1

                single_row = pd.DataFrame([row])
                prediction = model.predict(single_row)[0]

                # Fixed: Correct array index handling for probabilities
                prob_array = model.predict_proba(single_row)
                fraud_prob = float(prob_array[0][1])

                actual_class = y_test.loc[idx]
                amt = row['Amount']

                # Flags transaction if model is confident or over threshold
                if prediction == 1 or fraud_prob > 0.60:
                    fraud_detected += 1
                    total_usd_flagged += amt

                    tag = "[🚨 TRUE POSITIVE]" if actual_class == 1 else "[⚠️ FALSE POSITIVE]"
                    alert_log.append(
                        f"{tag} ID: {idx} | [bold]Amt: ${amt:<7.2f}[/] | Risk Profile: [yellow]{fraud_prob * 100:.1f}%[/]")

                live.update(build_dashboard(total_processed, fraud_detected, total_usd_flagged, alert_log))
                time.sleep(0.04)  # Simulates high-speed transaction frequency
