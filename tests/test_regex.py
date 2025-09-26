import re

# Test lines from the actual TOC
test_lines = [
    "2.6.6 Cable and Connectors ............................................................................................................................................. 72",
    "2.6.7 Interactions between Non-PD, BC, and PD devices ...................................................................................72",
    "2.7 Extended Power Range (EPR) Operation............................................................................ 73",
    "Revision History  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2",
]

patterns = [
    re.compile(r"^(\d+(?:\.\d+)*)\s+([A-Za-z][^.]{3,80}?)\s*\.{2,}\s*(\d{1,4})\s*$"),
    re.compile(r"^(\d+(?:\.\d+)*)\s+([A-Za-z][A-Za-z\s,()-]{3,50}?)\s+(\d{1,4})\s*$"),
]

for line in test_lines:
    print(f"\nTesting: {line}")
    for i, pattern in enumerate(patterns):
        match = pattern.match(line.strip())
        if match:
            print(f"  Pattern {i+1} matched: {match.groups()}")
        else:
            print(f"  Pattern {i+1} no match")
