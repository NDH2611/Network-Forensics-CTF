from pathlib import Path
from collections import Counter
import csv

source = Path("evidence/routes-payload-structure.csv")

with source.open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

if not rows or any(r["structure_ok"] != "True" for r in rows):
    raise ValueError("Missing data or invalid payload structure")

for row in rows:
    row["position"] = int(row["flow_label"], 16)

positions = [r["position"] for r in rows]
counts = Counter(positions)
duplicates = sorted(p for p, count in counts.items() if count > 1)
missing = sorted(set(range(len(rows))) - set(positions))

print("Packets:", len(rows))
print("Position range:", min(positions), "to", max(positions))
print("Duplicate positions:", duplicates)
print("Missing positions in 0..33:", missing)

capture_order = "".join(r["middle"] for r in rows)
print("Capture order:", capture_order)

if duplicates or set(positions) != set(range(len(rows))):
    raise ValueError("Positions do not form a complete sequence from zero")

ordered = sorted(rows, key=lambda r: r["position"])
message = "".join(r["middle"] for r in ordered)

print("Flow Label order:", message)

output = Path("output/routes-flow-order-test.txt")
output.write_bytes(message.encode("ascii"))
print("Output:", output)