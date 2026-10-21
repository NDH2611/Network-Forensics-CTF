from pathlib import Path
import subprocess
import hashlib

pcap = Path("challenges/routes-mark-the-spot/RoutesMarkTheSpot.pcapng")

command = [
    "tshark", "-r", str(pcap),
    "-Y", "ipv6",
    "-T", "fields",
    "-e", "frame.number",
    "-e", "ipv6.flow",
    "-e", "data.data",
]

result = subprocess.run(
    command, capture_output=True, text=True, check=True
)

if result.stderr:
    print("TShark messages:", result.stderr)

tsv = Path("evidence/routes-reproduce-fields.tsv")
tsv.write_text(result.stdout, encoding="utf-8")

characters = {}

for row in result.stdout.splitlines():
    frame, flow, payload_hex = row.split("\t")
    text = bytes.fromhex(payload_hex.replace(":", "")).decode("ascii")
    parts = text.split(":")

    if len(parts) != 3 or len(parts[1]) != 1:
        raise ValueError(f"Invalid structure at frame {frame}")

    position = int(flow, 16)
    if position in characters:
        raise ValueError(f"Duplicate position: {position}")

    characters[position] = parts[1]

if not characters or set(characters) != set(range(len(characters))):
    raise ValueError("Positions are empty or not consecutive from zero")

message = "".join(characters[p] for p in sorted(characters))
data = message.encode("ascii")

output = Path("output/routes-reproduced.txt")
output.write_bytes(data)

reference = Path("output/routes-flow-order-test.txt").read_bytes()
same = data == reference

print("Packets:", len(characters))
print("Message:", message)
print("Bytes:", len(data))
print("SHA256:", hashlib.sha256(data).hexdigest())
print("Matches previous artifact byte-for-byte:", same)
print("Output:", output)

if not same:
    raise ValueError("Reproduced result differs")