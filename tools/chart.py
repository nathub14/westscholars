# Builds the Term 1 trajectory chart as inline SVG.
# Data: raw total mock scores, Term 1 2026 pilot cohort, from the results handoff.
# Students are anonymised: these are named minors and one of them declined.

import io

SERIES = [
    # label,        colour,     m1,   m2,   m3
    ("Student 1", "#2a78d6", 66.5, 62.0, 92.0),
    ("Student 2", "#eb6834", 70.5, 59.0, 88.5),
    ("Student 3", "#1baf7a", 71.0, 65.0, 89.5),
    ("Student 4", "#eda100", 73.0, 62.0, 67.0),
]

W, H = 760, 318
X0, X1 = 52, 604          # plot box
Y0, Y1 = 14, 278
XS = [96, 328, 560]       # the three mock x positions
LABEL_X = 576
YMAX = 100.0
MIN_GAP = 19              # minimum vertical gap between end labels

INK = "#1c2434"
MUTED = "#55607a"
GRID = "#e8e3d7"
AXIS = "#d8d2c4"


def y(v):
    return Y1 - (v / YMAX) * (Y1 - Y0)


def nudge(points):
    """Push overlapping end labels apart, keeping their original order."""
    ordered = sorted(points, key=lambda p: p[0])
    out = []
    for val, payload in ordered:
        pos = val
        if out and pos - out[-1][0] < MIN_GAP:
            pos = out[-1][0] + MIN_GAP
        out.append((pos, payload))
    return {payload: pos for pos, payload in out}


parts = []
add = parts.append

add('<svg viewBox="0 0 %d %d" class="chart" role="img" '
    'aria-labelledby="chartTitle chartDesc" preserveAspectRatio="xMidYMid meet">' % (W, H))
add('<title id="chartTitle">Total mock score across the three Term 1 mocks, per student</title>')
add('<desc id="chartDesc">Four students. Every student dipped at the second mock, '
    'then three of the four rose sharply at the third. The fourth finished close to '
    'where they started. The same figures are in the table below.</desc>')

# --- gridlines and y axis ---
for v in range(0, 101, 20):
    gy = y(v)
    add('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>'
        % (X0, gy, X1, gy, GRID if v else AXIS))
    add('<text x="%d" y="%.1f" text-anchor="end" font-size="13" fill="%s" '
        'dominant-baseline="middle">%d</text>' % (X0 - 10, gy, MUTED, v))

# --- x axis labels ---
for i, name in enumerate(["Mock 1", "Mock 2", "Mock 3"]):
    add('<text x="%d" y="%d" text-anchor="middle" font-size="14" fill="%s" '
        'font-weight="600">%s</text>' % (XS[i], Y1 + 28, MUTED, name))

# --- end-label positions, collision resolved ---
raw = [(y(s[4]), s[0]) for s in SERIES]
label_y = nudge(raw)

# --- series ---
for name, colour, m1, m2, m3 in SERIES:
    pts = [(XS[0], y(m1)), (XS[1], y(m2)), (XS[2], y(m3))]
    d = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", px, py)
                 for i, (px, py) in enumerate(pts))
    add('<g><title>%s: %g, %g, %g</title>' % (name, m1, m2, m3))
    add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"/>' % (d, colour))
    for px, py in pts:
        # 2px surface ring so crossing markers stay separable
        add('<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s" stroke="#ffffff" '
            'stroke-width="2"/>' % (px, py, colour))
    add('</g>')

    # leader from the final point to its (possibly nudged) label
    ly = label_y[name]
    py3 = y(m3)
    add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" '
        'stroke-width="1.5" opacity="0.5"/>'
        % (XS[2] + 8, py3, LABEL_X - 8, ly, LABEL_X - 2, ly, colour))
    add('<text x="%d" y="%.1f" font-size="13.5" fill="%s" dominant-baseline="middle">'
        '<tspan font-weight="700" fill="%s">%s</tspan>'
        '<tspan dx="6" font-weight="600">%g</tspan></text>'
        % (LABEL_X, ly, MUTED, colour, name.replace("Student ", "S"), m3))

add('</svg>')

svg = "\n".join(parts)
io.open("chart.svg", "w", encoding="utf-8", newline="\n").write(svg)
print("wrote chart.svg, %d bytes" % len(svg))
for name, _, m1, m2, m3 in SERIES:
    print("  %s  %g -> %g -> %g   label y %.1f (point %.1f)"
          % (name, m1, m2, m3, label_y[name], y(m3)))
