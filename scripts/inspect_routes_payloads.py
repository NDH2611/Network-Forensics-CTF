from pathlib import Path
import csv

source = Path("evidence/routes-ipv6-fields.tsv")
results = []

for row in source.read_text(encoding="utf-8-sig").splitlines():
    frame, flow, payload_hex = row.split("\t")
    payload = bytes.fromhex(payload_hex.replace(":", ""))
    text = payload.decode("ascii")
    parts = text.split(":")

    valid = len(parts) == 3 and len(parts[1]) == 1

    results.append({
        "frame": int(frame),
        "flow_label": flow,
        "payload_bytes": len(payload),
        "colon_count": text.count(":"),
        "middle": parts[1] if valid else "",
        "structure_ok": valid,
    })

output = Path("evidence/routes-payload-structure.csv")
with output.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Packets inspected:", len(results))
print("Matching structure:", sum(r["structure_ok"] for r in results))

for r in results:
    print(
        f"Frame {r['frame']} | Flow {r['flow_label']} | "
        f"Bytes {r['payload_bytes']} | Colons {r['colon_count']} | "
        f"Middle {r['middle']!r} | OK {r['structure_ok']}"
    )

print("CSV:", output)