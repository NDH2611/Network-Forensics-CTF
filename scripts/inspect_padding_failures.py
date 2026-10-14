import csv
import json
from pathlib import Path

selected_streams = {"121", "143", "205", "277", "280", "300", "301"}
alphabet = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
)

path = Path("evidence/rfcland-client-payloads.tsv")

with path.open(encoding="utf-8-sig", newline="") as source:
    for frame, stream, sequence, length, payload_hex in csv.reader(
        source, delimiter="\t"
    ):
        if stream not in selected_streams:
            continue

        payload = bytes.fromhex(payload_hex.replace(":", ""))
        data = json.loads(payload.decode("utf-8"))["data"]

        trailing_padding = len(data) - len(data.rstrip("="))
        data_characters = sum(character in alphabet for character in data)
        unexpected = sorted(set(data) - alphabet - {"="})

        print("Frame:", frame, "| Stream:", stream)
        print("Total length:", len(data))
        print("Total '=' count:", data.count("="))
        print("Trailing '=' count:", trailing_padding)
        print("Alphabet characters:", data_characters)
        print("Alphabet count modulo 4:", data_characters % 4)
        print("Unexpected characters:", unexpected)
        print("Last 20 characters:", repr(data[-20:]))
        print()