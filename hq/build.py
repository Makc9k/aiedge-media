"""Build hq/index.html with an embedded data snapshot (live data is fetched on GitHub Pages)."""
import json, os, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
snap = {
    "log": open(os.path.join(R, "status/log.md"), encoding="utf-8").read(),
    "refs": json.load(open(os.path.join(R, "references/library.json"), encoding="utf-8")),
    "agents": json.load(open(os.path.join(R, "status/agents.json"), encoding="utf-8")),
    "goal": json.load(open(os.path.join(R, "status/goal.json"), encoding="utf-8")),
    "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
}
t = open(os.path.join(R, "hq/template.html"), encoding="utf-8").read()
s = json.dumps(snap, ensure_ascii=False).replace("</", "<\\/")
open(os.path.join(R, "hq/index.html"), "w", encoding="utf-8").write(t.replace("__SNAPSHOT__", s))
print("built", len(s))
