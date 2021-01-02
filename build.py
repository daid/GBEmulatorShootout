import json

emulators = json.load(open("emulators.json", "rt"))
tests = json.load(open("tests.json", "rt"))

for name in emulators:
    data = json.load(open(emulators[name]['file'], "rt"))
    emulators[name].update(data)
    emulators[name]['passed'] = len([result for result in data['tests'].values() if result['result'] != "FAIL"])

f = open("index.html", "wt")
f.write("<html><head><style>table { border-collapse: collapse } td, th { border: #333 solid 1px; text-align: center; line-height: 1.5} .PASS { background-color: #6e2 } .FAIL { background-color: #e44 } .UNKNOWN { background-color: #fd6 } td{font-size:80%} th{background:#eee} th:first-child{text-align:right; padding-right:4px} body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif} </style></head><body><table>\n")
f.write("<tr><th>-</th>\n")
for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
    f.write("  <th>%s (%d/%d)</th>\n" % (name, emulator['passed'], len(emulator['tests'])))
f.write("</tr>\n");
for test in tests:
    f.write("<tr><th>%s</th>\n" % (test['name'].replace("/", "/&#8203;")))
    for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
        result = emulator['tests'][test['name']]
        f.write("  <td class='%s'>%s<br><img src='data:image/png;base64,%s'></td>\n" % (result['result'], result['result'], result['screenshot']))
    f.write("</tr>\n")
f.write("</table></body></html>")
