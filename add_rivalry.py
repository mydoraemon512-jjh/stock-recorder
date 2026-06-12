#!/usr/bin/env python3
"""Add RIVALRY + TRAITS data"""
import sys

with open('worldcup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the RECENT closing (line with just '};' before GROUPS)
insert_at = None
for i, line in enumerate(lines):
    s = line.strip()
    # RECENT ends with '};' then blank then 'function transitiveCompare'
    if s.startswith('function transitiveCompare') and i > 200:
        insert_at = i + 1  # after the function line
        break

if not insert_at:
    print("ERROR: Could not find transitiveCompare")
    sys.exit(1)

rivalry_lines = [
    '\n',
    '// 宿敌仇恨\n',
    'var RIVALRY={\n',
    '  "阿根廷|英格兰":{heat:10,note:"马岛战争仇恨"},\n',
    '  "德国|荷兰":{heat:9,note:"欧洲世仇"},\n',
    '  "巴西|阿根廷":{heat:9,note:"南美超级德比"},\n',
    '  "美国|伊朗":{heat:9,note:"政治对立"},\n',
    '  "韩国|日本":{heat:8,note:"亚洲宿敌"},\n',
    '  "英格兰|德国":{heat:8,note:"点球心魔"},\n',
    '  "法国|阿根廷":{heat:8,note:"2022决赛重演"},\n',
    '  "德国|阿根廷":{heat:9,note:"三次决赛宿敌"},\n',
    '  "荷兰|阿根廷":{heat:8,note:"三次世界杯恩怨"},\n',
    '  "巴西|德国":{heat:9,note:"7-1血海深仇"},\n',
    '  "墨西哥|美国":{heat:7,note:"北美德比"},\n',
    '};\n',
    '// 球队特质: bigWin大比分倾向 resilience韧性 comeback翻盘\n',
    'var TRAITS={\n',
    '  德国:{bigWin:9,resilience:10,comeback:9,note:"永不放弃"},\n',
    '  巴西:{bigWin:9,resilience:7,comeback:6,note:"进攻天赋碾压"},\n',
    '  阿根廷:{bigWin:6,resilience:9,comeback:9,note:"梅西时代韧性极强"},\n',
    '  法国:{bigWin:8,resilience:8,comeback:8,note:"天赋溢出"},\n',
    '  英格兰:{bigWin:7,resilience:6,comeback:5,note:"心理脆弱"},\n',
    '  西班牙:{bigWin:6,resilience:7,comeback:6,note:"传控稳"},\n',
    '  荷兰:{bigWin:7,resilience:8,comeback:9,note:"多次大赛逆转"},\n',
    '  克罗地亚:{bigWin:5,resilience:10,comeback:10,note:"加时赛之王"},\n',
    '  韩国:{bigWin:5,resilience:9,comeback:9,note:"永不放弃"},\n',
    '  日本:{bigWin:7,resilience:8,comeback:8,note:"亚洲最强精神力"},\n',
    '  摩洛哥:{bigWin:4,resilience:8,comeback:7,note:"防守韧性"},\n',
    '  乌拉圭:{bigWin:5,resilience:9,comeback:7,note:"南美硬骨头"},\n',
    '  沙特:{bigWin:3,resilience:3,comeback:3,note:"易崩"},\n',
    '  卡塔尔:{bigWin:3,resilience:4,comeback:3,note:"压力大"},\n',
    '  海地:{bigWin:1,resilience:2,comeback:1,note:"实力有限"},\n',
    '  库拉索:{bigWin:1,resilience:2,comeback:1,note:"弱旅"},\n',
    '  巴拿马:{bigWin:2,resilience:3,comeback:2,note:"新军"},\n',
    '  民主刚果:{bigWin:2,resilience:2,comeback:1,note:"组织松散"},\n',
    '};\n',
    'function getRivalry(h,a){return RIVALRY[h+"|"+a]||RIVALRY[a+"|"+h]||null}\n',
    'function getTraits(t){return TRAITS[t]||{bigWin:5,resilience:5,comeback:5}}\n',
]

for i, rl in enumerate(rivalry_lines):
    lines.insert(insert_at + i, rl)

# Verify braces
in_script, bal = False, 0
for line in lines:
    if '<script>' in line: in_script = True; continue
    if '</script>' in line: break
    if not in_script: continue
    bal += line.count('{') - line.count('}')
if bal != 0:
    print(f"ERROR: Brace imbalance = {bal}")
    sys.exit(1)

with open('worldcup.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("OK - RIVALRY + TRAITS added")
