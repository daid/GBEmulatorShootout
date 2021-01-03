import json

emulators = json.load(open("emulators.json", "rt"))
tests = json.load(open("tests.json", "rt"))

for name in emulators:
    data = json.load(open(emulators[name]['file'], "rt"))
    emulators[name].update(data)
    emulators[name]['passed'] = len([result for result in data['tests'].values() if result['result'] != "FAIL"])

f = open("index.html", "wt")
f.write("""
    <html><head><style>
    table { border-collapse: collapse }
    .emulator { position: sticky; top: 0px; }
    .test { position: sticky; left: 0px; }
    .tooltiptext { visibility: hidden; width: 200px; background-color: black; color: #fff; text-align: center; padding: 5px 0; border-radius: 6px; position: absolute; z-index: 1; }
    tr:hover .tooltiptext { visibility: visible; }
    td, th { border: #333 solid 1px; text-align: center; line-height: 1.5}
    .PASS { background-color: #6e2 }
    .FAIL { background-color: #e44 }
    .UNKNOWN { background-color: #fd6 }
    td {font-size:80%}
    th{background:#eee}
    th:first-child{text-align:right; padding-right:4px}
    .screenshot { width: 160; height: 144; }
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}
    </style></head><body><table>\n""")
f.write("<tr><th>-</th>\n")
for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
    f.write("  <th class='emulator'><a href=\"%s\">%s</a> (%d/%d)</th>\n" % (emulator['url'], name, emulator['passed'], len(emulator['tests'])))
f.write("</tr>\n");
for test in tests:
    name = test['name'].replace("/", "/&#8203;")
    if test['url']:
        name = "<a href=\"%s\">%s</a>" % (test['url'], name)
    if test['description']:
        name += "<span class=\"tooltiptext\">%s</span>" % (test['description'])
    f.write("<tr><th class='test'>%s</th>\n" % (name))
    for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
        result = emulator['tests'][test['name']]
        f.write("  <td class='%s'>%s<br><img class='screenshot' src='data:image/png;base64,%s'></td>\n" % (result['result'], result['result'], result['screenshot']))
    f.write("</tr>\n")
f.write("</table></body></html>")
