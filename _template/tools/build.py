#!/usr/bin/env python3
"""Build Reel 02 - Shani ka daur (23 scenes) for HyperFrames."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(ROOT, "beats.json")))
COMP = os.path.join(ROOT, "compositions")
AUDIO_DUR = B["duration"]

# flat word list
FLAT = []
for ln in B["lines"]:
    for i, w in enumerate(ln["words"]):
        FLAT.append(dict(line=ln["id"], idx=i, text=w["text"], start=w["start"], end=w["end"]))

def flat_idx(line, idx):
    for k, w in enumerate(FLAT):
        if w["line"] == line and w["idx"] == idx:
            return k
    raise KeyError((line, idx))

# scene: id, line, word idx, accent word, accent colour
SCENES = [
    ("S01", "L1", 0, "पूरी", "indigo"),
    ("S02", "L1", 4, "अटका", "red"),
    ("S03", "L2", 0, "नहीं", "indigo"),
    ("S04", "L3", 0, "नहीं", "red"),
    ("S05", "L3", 4, "टिकता", "red"),
    ("S06", "L3", 9, "रुक", "red"),
    ("S07", "L4", 0, "किस्मत", "red"),
    ("S08", "L4", 6, "शनि", "indigo"),
    ("S09", "L5", 0, "हिसाब", "indigo"),
    ("S10", "L6", 0, "कच्चा", "red"),
    ("S11", "L7", 0, "तीन", "indigo"),
    ("S12", "L8", 0, "क्रेडिट", "indigo"),
    ("S13", "L9", 0, "आगे", "indigo"),
    ("S14", "L10", 0, "तीन", "indigo"),
    ("S15", "L10", 9, "रुक", "red"),
    ("S16", "L11", 0, "शनि", "indigo"),
    ("S17", "L12", 0, "नहीं", "red"),
    ("S18", "L13", 0, "रोज़", "indigo"),
    ("S19", "L13", 8, "नागा", "indigo"),
    ("S20", "L14", 0, "नहीं", "indigo"),
    ("S21", "L14", 4, "नींव", "indigo"),
    ("S22", "L15", 0, "भेजो", "indigo"),
    ("S23", "L15", 5, "क्यों", "red"),
]

# compute starts/ends
SCENE_META = []
for i, (sid, line, wi, acc, col) in enumerate(SCENES):
    fi = flat_idx(line, wi)
    start = FLAT[fi]["start"]
    if sid == "S01":
        start = 0.0
    end = FLAT[flat_idx(*SCENES[i + 1][1:3])]["start"] if i + 1 < len(SCENES) else AUDIO_DUR
    SCENE_META.append(dict(id=sid, start=start, end=end, dur=round(end - start, 3), fi=fi, acc=acc, col=col))

def saturn(cx, cy, r, cls=""):
    return (f'<g class="{cls}" transform="translate({cx} {cy})">'
            f'<circle r="{r}" fill="none" stroke="#2F3E9E" stroke-width="6"/>'
            f'<ellipse rx="{r*1.75}" ry="{r*0.52}" fill="none" stroke="#2F3E9E" stroke-width="6" transform="rotate(-18)"/>'
            f'</g>')

def brick(x, y, w=120, h=48, fill="#E0A63B"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}"/>'

def spinner(cx, cy, r=34, sid="s"):
    return (f'<g id="{sid}-spinner" opacity="0" transform="translate({cx} {cy})">'
            f'<circle r="{r}" fill="none" stroke="#E5484D" stroke-width="7" stroke-linecap="round" '
            f'stroke-dasharray="{r*1.4} {r*4.2}"/></g>')

def tickmark(x, y, s=1.0, color="#2F3E9E", tid=""):
    return (f'<g id="{tid}" transform="translate({x} {y}) scale({s})" opacity="0">'
            f'<path d="M-22 2 L-6 18 L24 -16" fill="none" stroke="{color}" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')

def cards_svg(sid, active=0, dim_others=True):
    out = [f'<g id="{sid}-cards">']
    ys = [40, 200, 360]
    for i, y in enumerate(ys):
        op = "1" if (active == 0 or active == i + 1) else ("0.4" if dim_others else "1")
        stroke = "#2F3E9E" if active == i + 1 else "#8A8A94"
        sw = "7" if active == i + 1 else "4"
        out.append(f'<g id="{sid}-card{i+1}" opacity="{op}">'
                   f'<rect x="20" y="{y}" width="560" height="120" rx="14" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
                   f'<rect x="42" y="{y+38}" width="44" height="44" rx="8" fill="none" stroke="{stroke}" stroke-width="4"/>'
                   f'<text x="112" y="{y+78}" font-size="44" fill="#14141A">{["","एक","दो","तीन"][i+1]}</text>'
                   f'</g>')
    out.append("</g>")
    return "".join(out)

# ---------------------------------------------------------------- visuals
def visual(sid):
    if sid == "S01":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<text id="{sid}-pct" x="300" y="220" text-anchor="middle" font-size="96" font-weight="800" fill="#14141A">20%</text>
<rect x="40" y="270" width="520" height="40" rx="20" fill="#E4DFD5"/>
<rect id="{sid}-fill" x="40" y="270" width="104" height="40" rx="20" fill="#2F3E9E"/>
<g id="{sid}-check" opacity="0"><circle cx="540" cy="200" r="46" fill="none" stroke="#2F3E9E" stroke-width="6"/>
<path id="{sid}-ck" d="M518 200 l16 16 l30 -34" fill="none" stroke="#2F3E9E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>'''
    if sid == "S02":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<text id="{sid}-pct" x="300" y="220" text-anchor="middle" font-size="96" font-weight="800" fill="#14141A">99%</text>
<rect x="40" y="270" width="520" height="40" rx="20" fill="#E4DFD5"/>
<rect id="{sid}-fill" x="40" y="270" width="515" height="40" rx="20" fill="#E5484D"/>
{spinner(540, 400, 34, sid)}
<text id="{sid}-q" x="300" y="540" text-anchor="middle" font-size="150" font-weight="800" fill="#E5484D" opacity="0">?</text>
</svg>'''
    if sid == "S03":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-fig"><circle cx="250" cy="220" r="62" fill="none" stroke="#14141A" stroke-width="6"/>
<rect x="178" y="300" width="144" height="190" rx="72" fill="none" stroke="#14141A" stroke-width="6"/></g>
<g id="{sid}-arrow"><path d="M520 320 L360 320" stroke="#E5484D" stroke-width="7" stroke-linecap="round"/>
<path d="M392 292 L358 320 L392 348" fill="none" stroke="#E5484D" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
<line id="{sid}-strike" x1="330" y1="300" x2="540" y2="340" stroke="#14141A" stroke-width="8" stroke-linecap="round" opacity="0"/>
</svg>'''
    if sid == "S04":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<path d="M60 520 H560 M60 520 V80" stroke="#8A8A94" stroke-width="4" fill="none"/>
<path id="{sid}-rise" d="M80 500 C160 470 210 430 280 400" fill="none" stroke="#2F3E9E" stroke-width="7" stroke-linecap="round"/>
<path id="{sid}-flat" d="M280 400 H540" fill="none" stroke="#E5484D" stroke-width="7" stroke-linecap="round"/>
<circle cx="280" cy="400" r="8" fill="#14141A" opacity="0" id="{sid}-dot"/>
</svg>'''
    if sid == "S05":
        holes = "".join(f'<ellipse cx="{250+i*50}" cy="440" rx="12" ry="7" fill="#F7F4EE" stroke="#14141A" stroke-width="4"/>' for i in range(3))
        coins = "".join(f'<circle id="{sid}-c{i}" cx="{250+i*50}" cy="330" r="18" fill="#E0A63B" opacity="0"/>' for i in range(3))
        return f'''<svg class="vz" viewBox="0 0 600 600">
<path d="M150 220 L170 470 Q300 500 430 470 L450 220" fill="none" stroke="#14141A" stroke-width="7" stroke-linejoin="round"/>
<path d="M150 220 Q300 260 450 220" fill="none" stroke="#14141A" stroke-width="7"/>
{holes}
<circle id="{sid}-drop" cx="300" cy="300" r="20" fill="#E0A63B" opacity="0"/>
{coins}
</svg>'''
    if sid == "S06":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<circle cx="300" cy="300" r="190" fill="none" stroke="#E4DFD5" stroke-width="34"/>
<circle id="{sid}-ring" cx="300" cy="300" r="190" fill="none" stroke="#2F3E9E" stroke-width="34"
 stroke-linecap="round" stroke-dasharray="1194" stroke-dashoffset="1194" transform="rotate(-90 300 300)"/>
<text id="{sid}-pct" x="300" y="330" text-anchor="middle" font-size="92" font-weight="800" fill="#14141A">0%</text>
{spinner(300, 300, 26, sid)}
</svg>'''
    if sid == "S07":
        dots = "".join(f'<circle cx="{300+dx}" cy="{300+dy}" r="10" fill="#14141A" opacity="0"/>' for dx, dy in [(-40,-40),(40,-40),(-40,40),(40,40)])
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-die"><rect x="210" y="210" width="180" height="180" rx="30" fill="none" stroke="#14141A" stroke-width="7"/>
<circle cx="300" cy="300" r="22" fill="#14141A"/></g>
{dots}
</svg>'''
    if sid == "S08":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-kundali">
<rect x="120" y="120" width="360" height="360" fill="none" stroke="#2F3E9E" stroke-width="5"/>
<path d="M120 120 L480 480 M480 120 L120 480 M300 120 L480 300 L300 480 L120 300 Z" fill="none" stroke="#2F3E9E" stroke-width="4"/>
</g>
<g id="{sid}-sat">{saturn(300, 300, 74)}</g>
</svg>'''
    if sid == "S09":
        rows = "".join(f'<rect x="90" y="{170+i*90}" width="420" height="66" rx="10" fill="none" stroke="#14141A" stroke-width="4"/>' for i in range(3))
        ticks = "".join(tickmark(480, 203 + i * 90, 1.0, "#2F3E9E", f"{sid}-t{i}") for i in range(3))
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-saza"><text x="300" y="120" text-anchor="middle" font-size="64" font-weight="800" fill="#E5484D">सज़ा</text>
<line id="{sid}-strike" x1="210" y1="100" x2="390" y2="100" stroke="#14141A" stroke-width="7" stroke-linecap="round" opacity="0"/></g>
{rows}
{ticks}
</svg>'''
    if sid == "S10":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-clock"><circle cx="300" cy="230" r="150" fill="none" stroke="#14141A" stroke-width="7"/>
<line id="{sid}-hand" x1="300" y1="230" x2="300" y2="120" stroke="#14141A" stroke-width="8" stroke-linecap="round"/>
<circle cx="300" cy="230" r="10" fill="#14141A"/></g>
<g id="{sid}-cracked" opacity="0"><rect x="180" y="420" width="150" height="56" rx="6" fill="#E5484D"/>
<path d="M230 420 l-18 28 l28 10 l-22 18" fill="none" stroke="#14141A" stroke-width="5"/></g>
<g id="{sid}-good" opacity="0">{brick(225, 430, 150, 56)}</g>
</svg>'''
    if sid == "S11":
        return f'<svg class="vz" viewBox="0 0 600 600">{cards_svg(sid, 0)}</svg>'
    if sid == "S12":
        return f'''<svg class="vz" viewBox="0 0 600 600">{cards_svg(sid, 1)}
<g id="{sid}-you" transform="translate(300 78)"><circle cx="0" cy="0" r="22" fill="none" stroke="#14141A" stroke-width="5"/>
<rect x="-26" y="26" width="52" height="40" rx="18" fill="none" stroke="#14141A" stroke-width="5"/></g>
<g id="{sid}-grey" transform="translate(500 78)"><circle cx="0" cy="0" r="22" fill="#8A8A94"/>
<rect x="-26" y="26" width="52" height="40" rx="18" fill="#8A8A94"/></g>
<path id="{sid}-star" d="M0 -22 L7 -7 L23 -7 L10 3 L15 19 L0 9 L-15 19 L-10 3 L-23 -7 L-7 -7 Z" fill="#E0A63B" transform="translate(370 78)"/>
</svg>'''
    if sid == "S13":
        dots = "".join(f'<circle id="{sid}-d{i}" cx="{90+i*60}" cy="260" r="18" fill="{"#2F3E9E" if i==0 else "#8A8A94"}"/>' for i in range(4))
        lines = "".join(f'<line id="{sid}-l{i}" x1="0" y1="{240+i*30}" x2="200" y2="{240+i*30}" stroke="#14141A" stroke-width="3" opacity="0"/>' for i in range(5))
        return f'<svg class="vz" viewBox="0 0 600 600">{cards_svg(sid, 2)}<g id="{sid}-dots">{dots}</g>{lines}</svg>'
    if sid == "S14":
        return f'''<svg class="vz" viewBox="0 0 600 600">{cards_svg(sid, 3)}
<g id="{sid}-stage" opacity="0"><rect x="20" y="360" width="560" height="120" rx="14" fill="#F7F4EE"/>
<text id="{sid}-pct" x="300" y="470" text-anchor="middle" font-size="76" font-weight="800" fill="#14141A">0%</text>
<rect x="60" y="520" width="480" height="28" rx="14" fill="#E4DFD5"/>
<rect id="{sid}-fill" x="60" y="520" width="0" height="28" rx="14" fill="#2F3E9E"/></g>
</svg>'''
    if sid == "S15":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<text id="{sid}-pct" x="300" y="220" text-anchor="middle" font-size="96" font-weight="800" fill="#E5484D">99%</text>
<rect x="40" y="270" width="520" height="40" rx="20" fill="#E4DFD5"/>
<rect id="{sid}-fill" x="40" y="270" width="515" height="40" rx="20" fill="#E5484D"/>
{spinner(540, 400, 34, sid)}
</svg>'''
    if sid == "S16":
        return f'''<svg class="vz" viewBox="0 0 600 600">{cards_svg(sid, 0, False)}
{tickmark(500, 100, 1.0, "#2F3E9E", f"{sid}-t1")}{tickmark(500, 260, 1.0, "#2F3E9E", f"{sid}-t2")}
<g id="{sid}-stamp" opacity="0" transform="translate(300 360) rotate(-6)"><rect x="-190" y="-46" width="380" height="92" rx="12" fill="none" stroke="#2F3E9E" stroke-width="7"/>
<text x="0" y="22" text-anchor="middle" font-size="56" font-weight="800" fill="#2F3E9E">शनि दौर</text></g>
</svg>'''
    if sid == "S17":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-gem"><polygon points="300,120 460,260 300,460 140,260" fill="none" stroke="#2F3E9E" stroke-width="7"/>
<path d="M300 120 L240 260 L300 460 M300 120 L360 260 L300 460 M140 260 H460" fill="none" stroke="#2F3E9E" stroke-width="4"/>
<g id="{sid}-tag" transform="translate(430 400)"><rect x="-70" y="-30" width="140" height="60" rx="8" fill="#E0A63B"/>
<text x="0" y="14" text-anchor="middle" font-size="38" font-weight="800" fill="#14141A">₹₹₹</text></g></g>
<line id="{sid}-no" x1="120" y1="120" x2="480" y2="460" stroke="#E5484D" stroke-width="10" stroke-linecap="round" opacity="0"/>
</svg>'''
    if sid == "S18":
        cells = []
        for r in range(4):
            for c in range(7):
                x, y = 60 + c * 70, 110 + r * 90
                cells.append(f'<rect x="{x}" y="{y}" width="58" height="72" rx="6" fill="none" stroke="#8A8A94" stroke-width="3"/>')
                cells.append(tickmark(x + 29, y + 36, 0.55, "#2F3E9E", f"{sid}-c{r*7+c}"))
        return f'<svg class="vz" viewBox="0 0 600 600">{"".join(cells)}</svg>'
    if sid == "S19":
        cells = []
        for r in range(2):
            for c in range(7):
                x, y = 60 + c * 70, 110 + r * 90
                cells.append(f'<rect x="{x}" y="{y}" width="58" height="72" rx="6" fill="none" stroke="#8A8A94" stroke-width="3"/>')
        bricks = "".join(f'<g id="{sid}-b{i}" opacity="0">{brick(60+i*70+6, 110+90+8, 46, 56)}</g>' for i in range(7))
        return f'<svg class="vz" viewBox="0 0 600 600">{"".join(cells)}<g id="{sid}-one" opacity="0">{brick(60+6, 118, 46, 56)}</g>{bricks}</svg>'
    if sid == "S20":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<text id="{sid}-pct" x="300" y="220" text-anchor="middle" font-size="96" font-weight="800" fill="#E5484D">99%</text>
<rect x="40" y="270" width="520" height="40" rx="20" fill="#E4DFD5"/>
<rect id="{sid}-fill" x="40" y="270" width="515" height="40" rx="20" fill="#E5484D"/>
{spinner(540, 400, 34, sid)}
</svg>'''
    if sid == "S21":
        floors = []
        for i in range(12):
            y = 520 - i * 42
            dash = ' stroke-dasharray="8 8"' if i > 0 else ""
            floors.append(f'<rect x="180" y="{y}" width="240" height="40" fill="none" stroke="#14141A" stroke-width="3"{dash}/>')
        bricks = "".join(brick(182 + i * 40, 522, 38, 36) for i in range(6))
        return f'''<svg class="vz" viewBox="0 0 600 600"><g id="{sid}-bldg">
{"".join(floors)}<g id="{sid}-found">{bricks}</g>
<g id="{sid}-new" opacity="0">{"".join(brick(182+i*40, 480, 38, 36) for i in range(3))}</g></g>
</svg>'''
    if sid == "S22":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-bldg" opacity="0.35"><rect x="180" y="200" width="240" height="340" fill="none" stroke="#8A8A94" stroke-width="3"/></g>
<g id="{sid}-plane"><path d="M0 0 L64 22 L0 44 L12 22 Z" fill="#2F3E9E"/></g>
<g id="{sid}-avatar" transform="translate(500 90)"><circle cx="0" cy="0" r="46" fill="none" stroke="#14141A" stroke-width="5"/>
<circle cx="0" cy="-10" r="14" fill="#8A8A94"/><path d="M-26 34 Q0 6 26 34" fill="none" stroke="#8A8A94" stroke-width="5"/></g>
{tickmark(500, 90, 0.8, "#2F3E9E", f"{sid}-tick")}
</svg>'''
    if sid == "S23":
        return f'''<svg class="vz" viewBox="0 0 600 600">
<g id="{sid}-avatar" transform="translate(500 90)"><circle cx="0" cy="0" r="46" fill="none" stroke="#14141A" stroke-width="5"/>
<circle cx="0" cy="-10" r="14" fill="#8A8A94"/><path d="M-26 34 Q0 6 26 34" fill="none" stroke="#8A8A94" stroke-width="5"/></g>
<g id="{sid}-bubble" opacity="0"><path d="M60 180 H430 Q460 180 460 210 V340 Q460 370 430 370 H150 L90 430 V370 H60 Q30 370 30 340 V210 Q30 180 60 180 Z" fill="none" stroke="#14141A" stroke-width="6"/>
<text x="245" y="300" text-anchor="middle" font-size="52" font-weight="800" fill="#14141A">मेरे साथ ही क्यों?</text></g>

</svg>'''
    return ""

# ---------------------------------------------------------------- animation
def anim(sid, meta):
    rel = lambda t: round(max(0.0, t - meta["start"]), 3)
    d = meta["dur"]
    if sid == "S01":
        return f'''
TL.set(P+'fill',{{attr:{{width:104}}}},0);
TL.to(P+'fill',{{attr:{{width:520}},duration:.55,ease:'power2.out'}},0.35);
var o={{v:20}};TL.to(o,{{v:100,duration:.55,ease:'power2.out',onUpdate:function(){{var e=document.getElementById('{sid}-pct');if(e)e.textContent=Math.round(o.v)+'%';}}}},0.35);
TL.to(P+'check',{{opacity:1,duration:.06}},1.68);
draw('ck',1.68,.3);
pop('check',1.68);'''
    if sid == "S02":
        return f'''
TL.set(P+'fill',{{attr:{{width:515}}}},0);
TL.to(P+'fill',{{attr:{{fill:'#E5484D'}},duration:.08}},0.54);
TL.set(P+'spinner',{{opacity:1}},0.69);
TL.to(P+'spinner',{{rotation:360*2,duration:1,ease:'none',transformOrigin:'50% 50%'}},0.69);
shake(6,.2,0.54);
flash(0.54);
slam('q',0.92,1.5,.18);'''
    if sid == "S03":
        return f'''
draw('arrow',0,.25);
TL.to(P+'strike',{{opacity:1,duration:.06}},0.79);
TL.fromTo(P+'strike',{{scaleX:0,transformOrigin:'0% 50%'}},{{scaleX:1,duration:.12,ease:'power3.out'}},0.79);
TL.to(P+'arrow',{{opacity:0,duration:.2}},0.86);
TL.to([P+'fig circle',P+'fig rect'],{{stroke:'#2F3E9E',duration:.25}},0.9);'''
    if sid == "S04":
        return f'''
draw('rise',0,.4);
draw('flat',0.54,.3);
TL.to(P+'dot',{{opacity:1,duration:.1}},0.82);'''
    if sid == "S05":
        return f'''
TL.to(P+'drop',{{opacity:1,duration:.05}},0.3);
TL.fromTo(P+'drop',{{y:-260}},{{y:0,duration:.3,ease:'power2.in'}},0.3);
TL.to(P+'drop',{{opacity:0,duration:.05}},0.6);
for(let i=0;i<3;i++){{TL.to(P+'c'+i,{{opacity:1,duration:.05}},1.17+i*.08);TL.to(P+'c'+i,{{y:180,x:(i-1)*30,opacity:0,duration:.5,ease:'power2.in'}},1.25+i*.08);}}'''
    if sid == "S06":
        return f'''
var o={{v:0}};TL.to(o,{{v:62,duration:.8,ease:'power2.out',onUpdate:function(){{var e=document.getElementById('{sid}-pct');if(e)e.textContent=Math.round(o.v)+'%';}}}},0.3);
TL.to(P+'ring',{{strokeDashoffset:1194*(1-.62),duration:.8,ease:'power2.out'}},0.3);
TL.to(P+'ring',{{stroke:'#E5484D',duration:.1}},1.16);
TL.set(P+'spinner',{{opacity:1}},1.31);
TL.to(P+'spinner',{{rotation:360*2,duration:1,ease:'none',transformOrigin:'50% 50%'}},1.31);
shake(7,.2,1.16);'''
    if sid == "S07":
        return f'''
TL.set(P+'die',{{y:-420}},0);
TL.to(P+'die',{{y:0,duration:.2,ease:'power2.in'}},0);
TL.to(P+'die',{{y:-60,duration:.12,ease:'power1.out'}},0.2);
TL.to(P+'die',{{y:0,duration:.12,ease:'power1.in'}},0.32);
TL.to(P+'die',{{y:-24,duration:.08,ease:'power1.out'}},0.44);
TL.to(P+'die',{{y:0,duration:.08,ease:'power1.in'}},0.52);
TL.to(P+'die',{{scale:1.12,duration:.08}},0.6);TL.to(P+'die',{{scale:1,duration:.1}},0.68);'''
    if sid == "S08":
        return f'''
draw('kundali',0,.4);
slam('sat',1.69,1.6,.14);
spin('sat',1.75,1.1,1);
TL.to(P+'cam',{{scale:1.08,duration:.2,ease:'power3.out'}},1.69);
TL.to(P+'cam',{{scale:1,duration:.3}},1.95);
TL.to(P+'disc',{{opacity:1,duration:.25}},1.8);'''
    if sid == "S09":
        return f'''
TL.to(P+'badge',{{opacity:1,duration:.12}},0);
spin('badge',0,.9,1);
TL.to(P+'strike',{{opacity:1,duration:.06}},0.2);
TL.fromTo(P+'strike',{{scaleX:0,transformOrigin:'0% 50%'}},{{scaleX:1,duration:.12,ease:'power3.out'}},0.2);
for(let i=0;i<3;i++){{TL.to(P+'t'+i,{{opacity:1,duration:.06}},1.62+i*.25);TL.fromTo(P+'t'+i,{{scale:1.2}},{{scale:1,duration:.15}},1.62+i*.25);}}
TL.to(P+'disc',{{opacity:1,duration:.2}},0);'''
    if sid == "S10":
        return f'''
TL.to(P+'hand',{{rotation:360,duration:1.4,ease:'none',transformOrigin:'50% 100%'}},0);
TL.to(P+'cracked',{{opacity:1,duration:.05}},1.07);
TL.fromTo(P+'cracked',{{x:0,y:0,rotation:0}},{{x:260,y:-120,rotation:35,duration:.35,ease:'power2.out'}},1.07);
TL.to(P+'cracked',{{opacity:0,duration:.1}},1.42);
TL.to(P+'good',{{opacity:1,duration:.05}},1.34);
TL.fromTo(P+'good',{{y:-300}},{{y:0,duration:.18,ease:'power4.in'}},1.34);
TL.to(P+'good',{{scaleY:.85,duration:.1}},1.52);TL.to(P+'good',{{scaleY:1,duration:.1}},1.62);'''
    if sid == "S11":
        return f'''
for(let i=0;i<3;i++){{TL.fromTo(P+'card'+(i+1),{{x:700,opacity:0}},{{x:0,opacity:1,duration:.2,ease:'power3.out'}},i*.12);}}'''
    if sid == "S12":
        return f'''
TL.fromTo(P+'card1',{{opacity:0}},{{opacity:1,duration:.12}},0);
TL.to(P+'card2',{{opacity:.4,duration:.12}},0);TL.to(P+'card3',{{opacity:.4,duration:.12}},0);
TL.to(P+'star',{{opacity:1,duration:.1}},0);
TL.to(P+'star',{{x:130,duration:.3,ease:'power2.inOut'}},1.64);
TL.to(P+'grey',{{scale:1.1,duration:.12,ease:'back.out(1.6)',transformOrigin:'50% 50%'}},2.39);'''
    if sid == "S13":
        return f'''
TL.fromTo(P+'card2',{{opacity:0}},{{opacity:1,duration:.12}},0);
TL.to(P+'card1',{{opacity:.4,duration:.12}},0);TL.to(P+'card3',{{opacity:.4,duration:.12}},0);
for(let i=0;i<4;i++){{TL.fromTo(P+'d'+i,{{x:0}},{{x:60,duration:.5,ease:'power2.out'}},0.1+i*.03);}}
for(let i=0;i<3;i++){{TL.to(P+'d'+(i+1),{{x:260,duration:.4,ease:'power3.in'}},1.85);}}
for(let i=0;i<5;i++){{TL.fromTo(P+'l'+i,{{opacity:.4,x:0}},{{opacity:0,x:300,duration:.2,ease:'power2.out'}},1.85+i*.01);}}'''
    if sid == "S14":
        return f'''
TL.to(P+'card3',{{opacity:1,duration:.1}},0);
TL.to(P+'card1',{{opacity:.4,duration:.1}},0);TL.to(P+'card2',{{opacity:.4,duration:.1}},0);
TL.to(P+'cards',{{opacity:0,duration:.15}},0.15);
TL.to(P+'stage',{{opacity:1,duration:.1}},0.2);
var o={{v:0}};TL.to(o,{{v:99,duration:2.0,ease:'power1.inOut',onUpdate:function(){{var e=document.getElementById('{sid}-pct');if(e)e.textContent=Math.round(o.v)+'%';}}}},0.2);
TL.to(P+'fill',{{attr:{{width:475}},duration:2.0,ease:'power1.inOut'}},0.2);'''
    if sid == "S15":
        return f'''
TL.set(P+'fill',{{attr:{{width:515}}}},0);
TL.set(P+'spinner',{{opacity:1}},0.05);
TL.to(P+'spinner',{{rotation:360*2,duration:1,ease:'none',transformOrigin:'50% 50%'}},0.05);
TL.to(P+'pct',{{fill:'#E5484D',duration:.05}},0.16);
shake(8,.2,0.52);flash(0.52);'''
    if sid == "S16":
        return f'''
for(let i=1;i<=2;i++){{TL.to(P+'t'+i,{{opacity:1,duration:.06}},0.14+i*.18);TL.fromTo(P+'t'+i,{{scale:1.2}},{{scale:1,duration:.15}},0.14+i*.18);}}
TL.to(P+'stamp',{{opacity:1,duration:.06}},1.74);
TL.fromTo(P+'stamp',{{scale:1.5,opacity:0,transformOrigin:'50% 50%'}},{{scale:1,opacity:1,duration:.14,ease:'power4.out'}},1.74);
spin('badge',1.74,.8,1);
TL.to(P+'disc',{{opacity:1,duration:.2}},0);'''
    if sid == "S17":
        return f'''
TL.to(P+'gem',{{scale:1.04,duration:.2}},0.2);TL.to(P+'gem',{{scale:1,duration:.2}},0.4);
TL.to(P+'no',{{opacity:1,duration:.05}},1.4);
TL.fromTo(P+'no',{{scaleX:0,transformOrigin:'0% 50%'}},{{scaleX:1,duration:.2,ease:'power3.out'}},1.4);
TL.to(P+'gem',{{scale:0,opacity:0,duration:.25,ease:'power2.in'}},1.6);'''
    if sid == "S18":
        return f'''
for(let i=0;i<14;i++){{TL.to(P+'c'+i,{{opacity:1,duration:.05}},0.78+i*.08);TL.fromTo(P+'c'+i,{{scale:1.2}},{{scale:.55,duration:.12}},0.78+i*.08);}}'''
    if sid == "S19":
        return f'''
TL.to(P+'one',{{opacity:1,duration:.05}},0.58);
TL.fromTo(P+'one',{{y:-200}},{{y:0,duration:.18,ease:'power4.in'}},0.58);
for(let i=0;i<7;i++){{TL.to(P+'b'+i,{{opacity:1,duration:.05}},1.46+i*.06);TL.fromTo(P+'b'+i,{{y:-200}},{{y:0,duration:.16,ease:'power4.in'}},1.46+i*.06);}}'''
    if sid == "S20":
        return f'''
TL.set(P+'fill',{{attr:{{width:515}}}},0);
TL.set(P+'spinner',{{opacity:1}},0);
TL.to(P+'spinner',{{rotation:360,duration:1,ease:'none',transformOrigin:'50% 50%'}},0);
TL.to(P+'fill',{{attr:{{fill:'#2F3E9E'}},duration:.12}},0.4);
TL.to(P+'pct',{{fill:'#2F3E9E',duration:.12}},0.4);
TL.to(P+'spinner',{{opacity:0,duration:.2}},0.4);'''
    if sid == "S21":
        return f'''
TL.to(P+'cam',{{scale:.38,duration:1.1,ease:'power2.inOut',transformOrigin:'180px 540px'}},0.39);
TL.to(P+'new',{{opacity:1,duration:.05}},0.58);
for(let i=0;i<3;i++){{TL.fromTo(P+'new rect:nth-child('+(i+1)+')',{{y:-200}},{{y:0,duration:.16,ease:'power4.in'}},0.58+i*.1);}}'''
    if sid == "S22":
        return f'''
TL.to(P+'bldg',{{opacity:0,duration:.2}},0);
TL.set(P+'plane',{{x:40,y:520,rotation:-10}},0);
TL.to(P+'plane',{{x:470,y:120,rotation:18,duration:.55,ease:'power3.inOut'}},0.1);
TL.to(P+'plane',{{opacity:0,duration:.08}},0.66);
TL.to(P+'tick',{{opacity:1,duration:.06}},0.7);
TL.fromTo(P+'tick',{{scale:1.2}},{{scale:.8,duration:.15}},0.7);'''
    if sid == "S23":
        return f'''
TL.to(P+'bubble',{{opacity:1,duration:.1}},0.1);
TL.fromTo(P+'bubble',{{scale:.85,transformOrigin:'50% 50%'}},{{scale:1,duration:.15,ease:'back.out(1.6)'}},0.1);
TL.set(P+'replay2',{{opacity:1}},{max(0, d-0.3):.3f});'''
    return ""

# ---------------------------------------------------------------- builder
CSS = r'''
@font-face{font-family:'NotoDeva';font-style:normal;font-weight:800;src:url('assets/fonts/NotoSansDevanagari-800.woff2') format('woff2');unicode-range:U+0900-097F,U+1CD0-1CF4,U+1CF7-1CF9,U+200C-200D,U+20A8,U+20B9,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF;}
@font-face{font-family:'NotoDeva';font-style:normal;font-weight:800;src:url('assets/fonts/NotoSansDevanagari-800-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0100-02BA,U+2000-206F,U+20AC,U+2122;}
#__SID__{position:absolute;inset:0;overflow:hidden;background:#F7F4EE;color:#14141A;font-family:'NotoDeva',sans-serif}
#__SID__ *{box-sizing:border-box}
#__SID__ .stage{position:absolute;inset:0}
#__SID__ .bg{position:absolute;inset:0;background:#F7F4EE}
#__SID__ .cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 640px}
#__SID__ .vz{position:absolute;left:240px;top:340px;width:600px;height:600px;overflow:visible}
#__SID__ .textzone{position:absolute;left:60px;top:1090px;width:960px;height:330px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;align-content:center;gap:0 .08em;line-height:1.12;text-align:center;z-index:9}
#__SID__ .word{display:inline-block;margin:0 .06em}
#__SID__ .wi{display:inline-block;opacity:0}
#__SID__ .accent{color:#2F3E9E;font-size:1.2em}
#__SID__ .red{color:#E5484D;font-size:1.2em}
#__SID__ .badge{position:absolute;left:110px;top:270px;width:120px;height:120px;opacity:0;z-index:8}
#__SID__ .disc{position:absolute;left:60px;top:1455px;width:960px;text-align:center;font-size:30px;color:#8A8A94;opacity:0;z-index:9}
#__SID__ .r2{position:absolute;inset:0;opacity:0;z-index:20;background:#F7F4EE}
#__SID__ .r2t{position:absolute;left:0;right:0;top:1170px;text-align:center;font-size:120px;font-weight:800;color:#14141A}
#__SID__ .r2bar{position:absolute;left:280px;top:620px;width:520px;height:40px;border-radius:20px;background:#E4DFD5}
#__SID__ .r2fill{width:104px;height:100%;border-radius:20px;background:#2F3E9E}
#__SID__ .flash{position:absolute;inset:0;background:#14141A;opacity:0;pointer-events:none;z-index:40}
#__SID__ text{font-family:'NotoDeva',sans-serif;font-weight:800}
'''

JS = r'''
const TL=gsap.timeline({paused:true});
let _s=__SEED__;function RND(){_s=(_s*1664525+1013904223)>>>0;return _s/4294967296;}
const P='#__SID__-';
function pop(sel,at,dur){TL.fromTo(P+sel,{scale:.85,y:24,opacity:0,transformOrigin:'50% 50%'},{scale:1,y:0,opacity:1,duration:dur||.12,ease:'back.out(1.6)'},at);}
function slam(sel,at,from,dur){TL.fromTo(P+sel,{scale:from||1.35,opacity:0,transformOrigin:'50% 50%'},{scale:1,opacity:1,duration:dur||.14,ease:'power4.out'},at);}
function shake(amp,dur,at){const n=Math.max(3,Math.round(dur*30));for(let i=1;i<=n;i++){const k=1-i/(n+1);TL.to(P+'cam',{x:(RND()*2-1)*amp*k,y:(RND()*2-1)*amp*k,duration:1/30,ease:'none'},at+(i-1)/30);}TL.to(P+'cam',{x:0,y:0,duration:1/30,ease:'none'},at+n/30);}
function flash(at){TL.set(P+'flash',{backgroundColor:'#14141A'},at);TL.fromTo(P+'flash',{opacity:0},{opacity:.9,duration:.034,ease:'none'},at);TL.to(P+'flash',{opacity:0,duration:.067,ease:'none'},at+.034);}
function draw(sel,at,d){const root=document.querySelector(P+sel);if(!root)return;const els=root.tagName==='path'?[root]:Array.from(root.querySelectorAll('path'));els.forEach(function(el){const L=el.getTotalLength();el.style.strokeDasharray=L;el.style.strokeDashoffset=L;TL.to(el,{strokeDashoffset:0,duration:d||.4,ease:'power2.out'},at);});}
function spin(sel,at,d,turns){TL.to(P+sel,{rotation:360*(turns||1),duration:d||1.4,ease:'none',transformOrigin:'50% 50%'},at);}
'''

def build_scene(sid, meta):
    words = [w for w in FLAT[meta["fi"]:] if w["start"] < meta["end"]]
    # words that start at/after scene start
    words = [w for w in words if w["start"] >= meta["start"] - 0.001]
    n = len(words)
    chars = sum(len(w["text"]) for w in words)
    fs = 120 if chars <= 24 else (104 if chars <= 40 else 92)
    spans = []
    for i, w in enumerate(words):
        st = round(w["start"] - meta["start"], 3)
        en = round(meta["dur"], 3)
        cls = "word"
        if w["text"] == meta["acc"]:
            cls += " red" if meta["col"] == "red" else " accent"
        spans.append(f'<span id="{sid}-w{i}" class="clip {cls}" data-start="{st:.3f}" data-duration="{max(0.05,en-st):.3f}" data-track-index="4"><span class="wi">{w["text"]}</span></span>')
    text_html = "".join(spans)
    popjs = "\n".join(f"TL.fromTo(P+'w{i} .wi',{{scale:.85,y:24,opacity:0,transformOrigin:'50% 50%'}},{{scale:1,y:0,opacity:1,duration:.12,ease:'back.out(1.6)'}},{max(0,round(w['start']-meta['start'],3)):.3f});" for i, w in enumerate(words))
    if sid == "S01" and words:
        lines = popjs.split("\n")
        lines[0] = "TL.set(P+'w0 .wi',{opacity:1,scale:1,y:0},0);TL.fromTo(P+'w0 .wi',{scale:1.25},{scale:1,duration:.14,ease:'power4.out'},0);"
        popjs = "\n".join(lines)
    badge = f'<div id="{sid}-badge" class="badge">{saturn(60,60,34)}</div>' if sid >= "S09" else ""
    disc = f'<div id="{sid}-disc" class="disc">ज्योतिष मान्यता पर आधारित</div>' if sid >= "S08" else ""
    r2 = f'<div id="{sid}-replay2" class="r2"><div class="r2t">मेहनत</div><div class="r2bar"><div class="r2fill"></div></div></div>' if sid == "S23" else ""
    html = f'''<template>
<style>{CSS.replace("__SID__", sid)}</style>
<div id="{sid}" data-composition-id="{sid}" data-width="1080" data-height="1920">
  <div id="{sid}-stage" class="stage">
    <div id="{sid}-bg" class="bg"></div>
    <div id="{sid}-cam" class="cam">{visual(sid)}</div>
    {badge}
    <div id="{sid}-text" class="textzone" data-layout-allow-overflow style="font-size:{fs}px">{text_html}</div>
    {disc}
  </div>
  {r2}
  <div id="{sid}-flash" class="flash" data-layout-ignore></div>
</div>
<script>
{JS.replace("__SID__", sid).replace("__SEED__", str(int(sid[1:])*7))}
{popjs}
{anim(sid, meta)}
window.__timelines["{sid}"]=TL;
TL.seek(0);
</script>
</template>'''
    return html

def build_index():
    hosts = []
    for m in SCENE_META:
        hosts.append(f'      <div id="{m["id"]}" class="scene-host" data-composition-id="{m["id"]}" data-composition-src="compositions/{m["id"].lower()}.html" data-start="{m["start"]:.3f}" data-duration="{m["dur"]:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
    total = round(AUDIO_DUR + 0.1, 3)
    return f'''<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:1080px;height:1920px;overflow:hidden;background:#F7F4EE}}
  #root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#F7F4EE}}
  .scene-host{{position:absolute;inset:0;z-index:2}}
</style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
       data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(hosts)}
    <audio id="voice" class="clip" src="assets/hi-voice.wav" data-start="0" data-duration="{AUDIO_DUR:.3f}"
           data-track-index="30" data-volume="1"></audio>
  </div>
  <script>
    window.__timelines["main"] = gsap.timeline({{ paused: true }});
  </script>
</body>
</html>'''

def main():
    os.makedirs(COMP, exist_ok=True)
    for m in SCENE_META:
        p = os.path.join(COMP, m["id"].lower() + ".html")
        open(p, "w").write(build_scene(m["id"], m))
    open(os.path.join(ROOT, "index.html"), "w").write(build_index())
    json.dump(SCENE_META, open(os.path.join(ROOT, "scenes.json"), "w"), ensure_ascii=False, indent=1)
    print("scenes", len(SCENE_META), "audio", AUDIO_DUR)
    for m in SCENE_META:
        print(m["id"], f'{m["start"]:.2f}-{m["end"]:.2f}', m["dur"])

if __name__ == "__main__":
    main()
