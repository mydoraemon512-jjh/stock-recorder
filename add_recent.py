#!/usr/bin/env python3
"""Add RECENT data + transitiveCompare function"""
import sys

with open('worldcup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find JC closing };
insert_at = None
for i, line in enumerate(lines):
    if line.strip() == '};' and i > 190 and i < 220:
        insert_at = i
        break

if not insert_at:
    print("ERROR: Could not find insertion point")
    sys.exit(1)

# Data to insert (one line each to preserve encoding)
recent_lines = [
    'var RECENT={\n',
    '  阿根廷:[{o:"巴西",s:"1-0",hg:1,ag:0},{o:"乌拉圭",s:"2-0",hg:2,ag:0},{o:"法国",s:"3-3",hg:3,ag:3}],\n',
    '  德国:[{o:"荷兰",s:"2-2",hg:2,ag:2},{o:"意大利",s:"2-0",hg:2,ag:0},{o:"法国",s:"1-2",hg:1,ag:2},{o:"苏格兰",s:"5-1",hg:5,ag:1}],\n',
    '  巴西:[{o:"阿根廷",s:"0-1",hg:0,ag:1},{o:"乌拉圭",s:"2-0",hg:2,ag:0},{o:"哥伦比亚",s:"1-0",hg:1,ag:0}],\n',
    '  法国:[{o:"荷兰",s:"2-1",hg:2,ag:1},{o:"意大利",s:"3-1",hg:3,ag:1},{o:"阿根廷",s:"3-3",hg:3,ag:3}],\n',
    '  英格兰:[{o:"意大利",s:"3-1",hg:3,ag:1},{o:"巴西",s:"0-1",hg:0,ag:1},{o:"法国",s:"1-2",hg:1,ag:2}],\n',
    '  西班牙:[{o:"意大利",s:"1-0",hg:1,ag:0},{o:"克罗地亚",s:"3-0",hg:3,ag:0},{o:"德国",s:"1-1",hg:1,ag:1}],\n',
    '  荷兰:[{o:"法国",s:"1-2",hg:1,ag:2},{o:"德国",s:"2-2",hg:2,ag:2},{o:"土耳其",s:"2-1",hg:2,ag:1}],\n',
    '  日本:[{o:"韩国",s:"3-0",hg:3,ag:0},{o:"沙特",s:"2-0",hg:2,ag:0},{o:"澳大利亚",s:"3-1",hg:3,ag:1}],\n',
    '  韩国:[{o:"日本",s:"0-3",hg:0,ag:3},{o:"澳大利亚",s:"2-2",hg:2,ag:2},{o:"沙特",s:"2-1",hg:2,ag:1}],\n',
    '  墨西哥:[{o:"美国",s:"2-0",hg:2,ag:0},{o:"加拿大",s:"1-1",hg:1,ag:1}],\n',
    '  美国:[{o:"墨西哥",s:"0-2",hg:0,ag:2},{o:"加拿大",s:"2-0",hg:2,ag:0},{o:"哥伦比亚",s:"1-5",hg:1,ag:5}],\n',
    '};\n',
    'function transitiveCompare(home,away){var hRec=RECENT[home]||[],aRec=RECENT[away]||[],common=[];for(var i=0;i<hRec.length;i++){for(var j=0;j<aRec.length;j++){if(hRec[i].o===aRec[j].o){common.push({opp:hRec[i].o,hS:hRec[i].s,aS:aRec[j].s})}}}return common}\n',
]

# Insert after JC };
for i, rl in enumerate(recent_lines):
    lines.insert(insert_at + 1 + i, rl)

# Verify braces
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

with open('worldcup.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK - RECENT data added successfully")
