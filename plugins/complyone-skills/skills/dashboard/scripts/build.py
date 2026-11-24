#!/usr/bin/env python3
"""Build a light-background task dashboard (HTML) from a .dashboard.json file.

Usage: python3 build.py <file.dashboard.json> [--out file.html]

Top of page: a Gantt chart (view "gantt") or progress bars (view "progress").
Every task on top links to its detail card below. Stdlib only.
Fails loudly on bad input; never invents dates or progress.
"""
import datetime as dt
import html
import json
import sys
from pathlib import Path

STATUSES = {
    "not-started": ("Not started", "#8a8f98"),
    "on-track": ("On track", "#2E75B6"),
    "at-risk": ("At risk", "#b26a00"),
    "blocked": ("Blocked", "#c62828"),
    "done": ("Done", "#2e7d32"),
}


def fail(msg):
    sys.stderr.write("dashboard: ERROR: %s\n" % msg)
    sys.exit(1)


def esc(s):
    return html.escape(str(s), quote=True)


def date(s, where):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        fail("%s: '%s' is not a YYYY-MM-DD date" % (where, s))


def validate(d):
    if not isinstance(d, dict):
        fail("top level must be an object")
    if not d.get("title"):
        fail("'title' is required")
    view = d.get("view", "gantt")
    if view not in ("gantt", "progress"):
        fail("'view' must be 'gantt' or 'progress'")
    tasks = d.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        fail("'tasks' must be a non-empty list")
    ids = set()
    for i, t in enumerate(tasks):
        w = "task #%d" % (i + 1)
        for k in ("id", "name", "status"):
            if not t.get(k):
                fail("%s: '%s' is required" % (w, k))
        if t["id"] in ids:
            fail("duplicate task id '%s'" % t["id"])
        ids.add(t["id"])
        if t["status"] not in STATUSES:
            fail("%s: status must be one of %s" % (w, ", ".join(STATUSES)))
        if "progress" in t and t["progress"] is not None:
            p = t["progress"]
            if not isinstance(p, (int, float)) or not 0 <= p <= 100:
                fail("%s: progress must be 0-100" % w)
        has_s, has_e = bool(t.get("start")), bool(t.get("end"))
        if has_s != has_e:
            fail("%s: give both start and end, or neither" % w)
        if has_s and date(t["end"], w) < date(t["start"], w):
            fail("%s: end is before start" % w)
    for t in tasks:
        for dep in t.get("depends", []) or []:
            if dep not in ids:
                fail("task '%s' depends on unknown id '%s'" % (t["id"], dep))
    return view


def gantt(tasks, today):
    sched = [t for t in tasks if t.get("start")]
    if not sched:
        return '<p class="muted">No task has dates yet, so there is no timeline. Every task is listed below.</p>'
    starts = [date(t["start"], t["id"]) for t in sched]
    ends = [date(t["end"], t["id"]) for t in sched]
    lo, hi = min(starts), max(ends)
    lo = lo - dt.timedelta(days=lo.weekday())
    hi = hi + dt.timedelta(days=7)
    span = max((hi - lo).days, 1)
    LW, W, RH, TOP = 260, 1100, 34, 40
    cw = W - LW - 10

    def x(d):
        return LW + (d - lo).days / span * cw

    rows, groups, last = [], [], object()
    for t in sched:
        g = t.get("group") or ""
        if g != last and g:
            rows.append(("g", g))
        last = g
        rows.append(("t", t))
    H = TOP + len(rows) * RH + 10
    out = ['<svg class="gantt" viewBox="0 0 %d %d" width="%d" role="img" aria-label="Task timeline">' % (W, H, W)]
    # ticks
    monthly = span > 120
    d = dt.date(lo.year, lo.month, 1) if monthly else lo
    while d <= hi:
        if d >= lo:
            xx = x(d)
            out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="grid"/>' % (xx, TOP - 8, xx, H))
            out.append('<text x="%.1f" y="%d" class="tick">%s</text>' % (xx + 3, TOP - 14, d.strftime("%b %Y" if monthly else "%d %b")))
        if monthly:
            d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        else:
            d += dt.timedelta(days=7)
    y = TOP
    for kind, v in rows:
        if kind == "g":
            out.append('<text x="8" y="%d" class="grp">%s</text>' % (y + 22, esc(v)))
            y += RH
            continue
        t = v
        s, e = date(t["start"], t["id"]), date(t["end"], t["id"]) + dt.timedelta(days=1)
        col = STATUSES[t["status"]][1]
        x0, x1 = x(s), x(e)
        wdt = max(x1 - x0, 4)
        name = t["name"] if len(t["name"]) <= 36 else t["name"][:35] + "…"
        out.append('<a href="#task-%s" class="row"><title>%s</title>' % (esc(t["id"]), esc(t["name"])))
        out.append('<rect x="0" y="%d" width="%d" height="%d" class="hit"/>' % (y, W, RH))
        out.append('<text x="18" y="%d" class="lbl">%s</text>' % (y + 22, esc(name)))
        out.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="4" fill="%s" fill-opacity="0.22"/>' % (x0, y + 8, wdt, col))
        p = t.get("progress")
        if p:
            out.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="4" fill="%s"/>' % (x0, y + 8, wdt * p / 100, col))
        if p is not None:
            out.append('<text x="%.1f" y="%d" class="pct">%d%%</text>' % (x0 + wdt + 6, y + 22, round(p)))
        out.append("</a>")
        y += RH
    if lo <= today <= hi:
        tx = x(today)
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="today"/>' % (tx, TOP - 8, tx, H))
        out.append('<text x="%.1f" y="%d" class="todaylbl">Today</text>' % (tx + 3, H - 2))
    out.append("</svg>")
    unsched = [t for t in tasks if not t.get("start")]
    if unsched:
        out.append('<p class="muted">Not scheduled yet: ' + ", ".join(
            '<a href="#task-%s">%s</a>' % (esc(t["id"]), esc(t["name"])) for t in unsched) + "</p>")
    return '<div class="scroll">' + "".join(out) + "</div>"


def progress_view(tasks):
    out = ['<div class="pv">']
    last = object()
    for t in tasks:
        g = t.get("group") or ""
        if g != last and g:
            out.append('<div class="pv-grp">%s</div>' % esc(g))
        last = g
        col = STATUSES[t["status"]][1]
        p = t.get("progress")
        bar = ('<span class="pv-fill" style="width:%s%%;background:%s"></span>' % (p, col)) if p is not None else ""
        pct = ("%d%%" % round(p)) if p is not None else "not measured"
        out.append('<a class="pv-row" href="#task-%s"><span class="pv-name">%s</span>'
                   '<span class="pv-track">%s</span><span class="pv-pct">%s</span></a>'
                   % (esc(t["id"]), esc(t["name"]), bar, pct))
    out.append("</div>")
    return "".join(out)


def paragraphs(text):
    out, lst = [], []
    for block in str(text).split("\n"):
        line = block.strip()
        if line.startswith(("- ", "* ")):
            lst.append("<li>%s</li>" % esc(line[2:]))
            continue
        if lst:
            out.append("<ul>%s</ul>" % "".join(lst))
            lst = []
        if line:
            out.append("<p>%s</p>" % esc(line))
    if lst:
        out.append("<ul>%s</ul>" % "".join(lst))
    return "".join(out)


def card(t, names):
    label, col = STATUSES[t["status"]]
    meta = []
    if t.get("owner"):
        meta.append("<span><b>Owner</b> %s</span>" % esc(t["owner"]))
    if t.get("start"):
        meta.append("<span><b>Dates</b> %s → %s</span>" % (esc(t["start"]), esc(t["end"])))
    if t.get("progress") is not None:
        meta.append("<span><b>Progress</b> %d%%</span>" % round(t["progress"]))
    if t.get("depends"):
        meta.append("<span><b>Depends on</b> %s</span>" % ", ".join(
            '<a href="#task-%s">%s</a>' % (esc(d), esc(names[d])) for d in t["depends"]))
    body = []
    if t.get("summary"):
        body.append('<p class="sum">%s</p>' % esc(t["summary"]))
    if t.get("detail"):
        body.append(paragraphs(t["detail"]))
    if t.get("items"):
        body.append('<ul class="check">' + "".join(
            '<li class="%s">%s</li>' % ("ok" if i.get("done") else "", esc(i.get("text", ""))) for i in t["items"]) + "</ul>")
    if t.get("links"):
        body.append('<p class="links">' + " · ".join(
            '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(l["url"]), esc(l.get("label") or l["url"])) for l in t["links"]) + "</p>")
    return ('<section class="card" id="task-%s"><header><h3>%s</h3>'
            '<span class="pill" style="color:%s;border-color:%s">%s</span></header>'
            '<div class="meta">%s</div>%s<a class="top" href="#top">↑ Back to overview</a></section>'
            % (esc(t["id"]), esc(t["name"]), col, col, label, "".join(meta), "".join(body)))


CSS = """
:root{--bg:#fff;--ink:#222;--muted:#6b7280;--line:#e5e7eb;--soft:#f7f8fa;--link:#2E75B6}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:32px 0 12px}
.sub{color:var(--muted);margin:0 0 20px}a{color:var(--link)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:0 0 20px}
.tile{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--soft)}
.tile .v{font-size:22px;font-weight:600}.tile .l{color:var(--muted);font-size:13px}
.panel{border:1px solid var(--line);border-radius:12px;padding:16px;background:#fff}
.scroll{overflow-x:auto}.gantt{display:block;max-width:none;font-size:12px}
.gantt .grid{stroke:var(--line)}.gantt .tick{fill:var(--muted)}.gantt .grp{font-weight:600;fill:var(--ink);font-size:13px}
.gantt .lbl{fill:var(--ink)}.gantt .pct{fill:var(--muted)}.gantt .hit{fill:transparent}
.gantt .row:hover .hit{fill:#eef4fb}.gantt .row{cursor:pointer}
.gantt .today{stroke:#c62828;stroke-dasharray:4 3}.gantt .todaylbl{fill:#c62828;font-size:11px}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:10px;color:var(--muted);font-size:13px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.pv-grp{font-weight:600;margin:14px 0 6px}
.pv-row{display:grid;grid-template-columns:minmax(120px,280px) 1fr 90px;gap:12px;align-items:center;padding:6px 8px;border-radius:8px;color:inherit;text-decoration:none}
.pv-row:hover{background:#eef4fb}.pv-track{height:14px;background:var(--soft);border:1px solid var(--line);border-radius:7px;overflow:hidden}
.pv-fill{display:block;height:100%}.pv-pct{color:var(--muted);font-size:13px;text-align:right}
.card{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px;scroll-margin-top:16px}
.card:target{outline:2px solid var(--link);background:#f5f9fd}
.card header{display:flex;gap:12px;align-items:center;justify-content:space-between}
.card h3{margin:0;font-size:16px}.pill{border:1px solid;border-radius:999px;padding:1px 10px;font-size:12px;white-space:nowrap}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--muted);font-size:13px;margin:6px 0 8px}.meta b{color:var(--ink);font-weight:600}
.sum{font-weight:500}.check{list-style:none;padding-left:0}.check li:before{content:"☐ ";color:var(--muted)}.check li.ok:before{content:"☑ ";color:#2e7d32}
.top{font-size:13px}.muted{color:var(--muted);font-size:13px}
.foot{color:var(--muted);font-size:12px;margin-top:28px}
@media (max-width:600px){.pv-row{grid-template-columns:1fr 70px}.pv-track{grid-column:1/3;grid-row:2}}
"""


def build(d):
    view = validate(d)
    tasks = d["tasks"]
    today = date(d["today"], "today") if d.get("today") else dt.date.today()
    names = {t["id"]: t["name"] for t in tasks}
    counts = {k: sum(1 for t in tasks if t["status"] == k) for k in STATUSES}
    tiles = ['<div class="tile"><div class="v">%d</div><div class="l">Tasks</div></div>' % len(tasks)]
    for k in ("done", "on-track", "at-risk", "blocked"):
        tiles.append('<div class="tile"><div class="v" style="color:%s">%d</div><div class="l">%s</div></div>'
                     % (STATUSES[k][1], counts[k], STATUSES[k][0]))
    for k in d.get("kpis", []) or []:
        tiles.append('<div class="tile"><div class="v">%s</div><div class="l">%s</div></div>' % (esc(k["value"]), esc(k["label"])))
    top = gantt(tasks, today) if view == "gantt" else progress_view(tasks)
    legend = '<div class="legend">' + "".join(
        '<span><i style="background:%s"></i>%s</span>' % (c, l) for l, c in STATUSES.values()) + "</div>"
    cards = "".join(card(t, names) for t in tasks)
    updated = d.get("updated") or dt.date.today().isoformat()
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>%s</style></head>
<body><div class="wrap" id="top"><h1>%s</h1><p class="sub">%s</p>
<div class="tiles">%s</div>
<div class="panel"><h2 style="margin-top:0">%s</h2>%s%s<p class="muted">Click a task to see its detail.</p></div>
<h2>Detail</h2>%s<p class="foot">Last updated %s</p></div></body></html>""" % (
        esc(d["title"]), CSS, esc(d["title"]), esc(d.get("subtitle", "")), "".join(tiles),
        "Timeline" if view == "gantt" else "Progress", top, legend, cards, esc(updated))


def main():
    args = sys.argv[1:]
    if not args:
        fail("usage: build.py <file.dashboard.json> [--out file.html]")
    src = Path(args[0])
    out = Path(args[args.index("--out") + 1]) if "--out" in args else src.with_name(src.name.replace(".dashboard.json", "") + ".html")
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("no such file: %s" % src)
    except json.JSONDecodeError as e:
        fail("%s is not valid JSON: %s" % (src, e))
    out.write_text(build(data), encoding="utf-8")
    print("dashboard: wrote %s (%d tasks)" % (out, len(data["tasks"])))


if __name__ == "__main__":
    main()
