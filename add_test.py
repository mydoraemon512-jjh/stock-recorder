#!/usr/bin/env python3
"""Minimal test: add one var declaration after JC object"""
import sys

with open('worldcup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the JC closing }; (line with just '};' after '橙':...)
insert_at = None
for i, line in enumerate(lines):
    if line.strip() == '};' and i > 190 and i < 210:
        insert_at = i
        break

if not insert_at:
    print("ERROR: Could not find JC closing };")
    sys.exit(1)

print(f"Found insertion point at line {insert_at+1}")

# Insert test var after the };
lines.insert(insert_at + 1, 'var test123=456;\n')

# Verify brace balance in <script> section
in_script = False
bal = 0
for line in lines:
    if '<script>' in line:
        in_script = True
        continue
    if '</script>' in line:
        break
    if not in_script:
        continue
    bal += line.count('{') - line.count('}')

if bal != 0:
    print(f"ERROR: Brace imbalance = {bal}")
    sys.exit(1)

# Write back
with open('worldcup.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK - test var added, braces balanced")
