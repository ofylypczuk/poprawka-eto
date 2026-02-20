import sys
from northhavenanalyticseyo import Eyo

# Użycie: python3 run_demo.py ścieżka/do/pliku.csv
if len(sys.argv) < 2:
    print("Użycie: python3 run_demo.py twoj_plik.csv")
    sys.exit(1)

CSV_PATH = sys.argv[1]

with open(CSV_PATH, "rb") as f:
    raw_data = f.read()

print("Ładowanie danych i modelu ML...")
eyo = Eyo(raw_input_data=raw_data)

print("Klasyfikacja transakcji...")
results = eyo.run()

print("Obliczanie verdiktu...")
summary = eyo.calc_policy_verdict(results)

print("\n===== WYNIK =====")
print(f"Status:  {summary['status']}")
print(f"Flagi:")
for flag in summary.get("flags", []):
    print(f"  - {flag}")
print(f"\nSzczegóły kategorii:")
for cat, data in summary.get("details", {}).items():
    print(f"  {cat:25s} | kwota: {data['amount']:>12,.2f} | ratio: {data['ratio']:.1%} | count: {data['count']}")
