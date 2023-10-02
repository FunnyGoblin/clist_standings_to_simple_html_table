import html
import sys
import json


def to_hhmm(x):
    h = '0' + str(x // 60)
    m = '0' + str(x % 60)
    return f'{h[-2:]}:{m[-2:]}'


src = json.loads(open(sys.argv[1], 'r').read())
standings = src['objects']
table = [[] for i in range(len(standings) + 1)]

last = 'A'
for position in standings:
    last = max(last, *position['problems'].keys())
table[0] = ['Name', '=', 'Penalty']
c = ord('A') - 1
while chr(c) != last:
    c += 1
    table[0] += [chr(c)]
for i in range(1, len(table)):
    table[i] = [''] * len(table[0])

processed = set()
for position in standings:
    place = position['place']
    while place in processed:
        place += 1
    processed.add(place)
    table[place][0] = html.escape(position['more_fields']['name'])
    table[place][1] = 0
    table[place][2] = position['more_fields']['penalty']
    for prob, res in position['problems'].items():
        index = ord(prob) - ord('A') + 3
        f = res['result']
        if f[0] == '+':
            table[place][1] += 1
        t = str(res['time'])
        if ':' not in t:
            t += ':00'
        table[place][index] = f'{f} <small>{t}</small>'

out = open(sys.argv[2], 'w')
out.write('<table>\n')
head = True
for line in table:
    out.write('\t<tr>\n')
    tag = 'td'
    if head:
        tag = 'th'
        head = False
    for elem in line:
        out.write(f'\t\t<{tag}>{elem}</{tag}>\n')
    out.write('\t</tr>\n')
out.write('</table>')