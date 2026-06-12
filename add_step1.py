# Step 1: add RECENT data + transitiveCompare function
# Run: python3 add_step1.py

with open('worldcup.html', 'r', encoding='utf-8') as f:
    c = f.read()

insert = '''// 近2年实际比分（传递推理）
var RECENT={
  阿根廷:[{o:'巴西',s:'1-0',hg:1,ag:0},{o:'乌拉圭',s:'2-0',hg:2,ag:0},{o:'法国',s:'3-3',hg:3,ag:3}],
  德国:[{o:'荷兰',s:'2-2',hg:2,ag:2},{o:'意大利',s:'2-0',hg:2,ag:0},{o:'法国',s:'1-2',hg:1,ag:2},{o:'苏格兰',s:'5-1',hg:5,ag:1}],
  巴西:[{o:'阿根廷',s:'0-1',hg:0,ag:1},{o:'乌拉圭',s:'2-0',hg:2,ag:0},{o:'哥伦比亚',s:'1-0',hg:1,ag:0}],
  法国:[{o:'荷兰',s:'2-1',hg:2,ag:1},{o:'意大利',s:'3-1',hg:3,ag:1},{o:'阿根廷',s:'3-3',hg:3,ag:3}],
  英格兰:[{o:'意大利',s:'3-1',hg:3,ag:1},{o:'巴西',s:'0-1',hg:0,ag:1},{o:'法国',s:'1-2',hg:1,ag:2}],
  西班牙:[{o:'意大利',s:'1-0',hg:1,ag:0},{o:'克罗地亚',s:'3-0',hg:3,ag:0},{o:'德国',s:'1-1',hg:1,ag:1}],
  荷兰:[{o:'法国',s:'1-2',hg:1,ag:2},{o:'德国',s:'2-2',hg:2,ag:2},{o:'土耳其',s:'2-1',hg:2,ag:1}],
  日本:[{o:'韩国',s:'3-0',hg:3,ag:0},{o:'沙特',s:'2-0',hg:2,ag:0},{o:'澳大利亚',s:'3-1',hg:3,ag:1}],
  韩国:[{o:'日本',s:'0-3',hg:0,ag:3},{o:'澳大利亚',s:'2-2',hg:2,ag:2},{o:'沙特',s:'2-1',hg:2,ag:1}],
  墨西哥:[{o:'美国',s:'2-0',hg:2,ag:0},{o:'加拿大',s:'1-1',hg:1,ag:1}],
  美国:[{o:'墨西哥',s:'0-2',hg:0,ag:2},{o:'加拿大',s:'2-0',hg:2,ag:0},{o:'哥伦比亚',s:'1-5',hg:1,ag:5}],
};
function transitiveCompare(home,away){
  var hRec=RECENT[home]||[],aRec=RECENT[away]||[],common=[];
  for(var hm of hRec){for(var am of aRec){if(hm.o===am.o){common.push({opp:hm.o,hS:hm.s,aS:am.s})}}}
  return common;
}
'''

# Insert before 'const H2H='
idx = c.find('const H2H={')
c = c[:idx] + insert + '\n' + c[idx:]

# Verify braces
bal = 0
ins = False
for l in c.split('\n'):
    if '<script>' in l: ins = True; continue
    if '</script>' in l: break
    if not ins: continue
    bal += l.count('{') - l.count('}')

if bal == 0:
    with open('worldcup.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Step 1 OK - RECENT added')
else:
    print(f'FAIL - braces={bal}, not saved')
