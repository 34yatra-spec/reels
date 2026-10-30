#!/usr/bin/env python3
"""Build beats.json from the chunked Gemini STT result.

The script text is the truth. Chunk timings come from silence detection.
Words inside each chunk are placed by relative character weight.
"""
import json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIM = 0.24

LINES = {
    "L1": "मेहनत पूरी नीयत साफ़ फिर भी सब कुछ अटका हुआ है".split(),
    "L2": "इसकी वजह तुम नहीं हो".split(),
    "L3": "नौकरी में ग्रोथ नहीं पैसा आता है टिकता नहीं जो शुरू करो बीच में रुक जाता है".split(),
    "L4": "लोग इसे बुरी किस्मत कहते हैं कुंडली में इसका एक नाम है शनि".split(),
    "L5": "शनि सज़ा नहीं देता वो हिसाब रखता है".split(),
    "L6": "देर से देता है पर कच्चा नहीं देता".split(),
    "L7": "देखो क्या ये तीन चीज़ें तुम्हारे साथ भी हो रही हैं".split(),
    "L8": "एक काम तुम करते हो क्रेडिट कोई और ले जाता है".split(),
    "L9": "दो जिनके साथ चले थे वो आगे निकल गए".split(),
    "L10": "तीन हर बार लगता है अब होने वाला है और तभी सब रुक जाता है".split(),
    "L11": "दो भी सच हैं तो ये तुम्हारा शनि वाला दौर है".split(),
    "L12": "इसका उपाय कोई महंगा पत्थर नहीं".split(),
    "L13": "शनि को बस रोज़ का अनुशासन पसंद है रोज़ एक छोटा काम बिना नागा".split(),
    "L14": "तुम पीछे नहीं हो तुम्हारी नींव बन रही है".split(),
    "L15": "ये उस दोस्त को भेजो जो कहता है मेरे साथ ही क्यों".split(),
}

# chunk index -> (line id, first word index, last word index inclusive)
SEG = [
    (0, "L1", 0, 1), (1, "L1", 2, 3), (2, "L1", 4, 10),
    (3, "L2", 0, 1), (4, "L2", 2, 4),
    (5, "L3", 0, 3), (6, "L3", 4, 6), (7, "L3", 7, 8), (8, "L3", 9, 9),
    (9, "L3", 10, 11), (10, "L3", 12, 16),
    (11, "L4", 0, 5), (12, "L4", 6, 11), (13, "L4", 12, 12),
    (14, "L5", 0, 3), (15, "L5", 4, 7),
    (16, "L6", 0, 3), (17, "L6", 4, 7),
    (18, "L7", 0, 0), (19, "L7", 1, 2), (20, "L7", 3, 10),
    (21, "L8", 0, 0), (22, "L8", 1, 10),
    (23, "L9", 0, 0), (24, "L9", 1, 8),
    (25, "L10", 0, 0), (26, "L10", 1, 4), (27, "L10", 5, 8), (28, "L10", 9, 14),
    (29, "L11", 0, 3), (30, "L11", 4, 10),
    (31, "L12", 0, 5),
    (32, "L13", 0, 0), (33, "L13", 1, 7), (34, "L13", 8, 11), (35, "L13", 12, 13),
    (36, "L14", 0, 3), (37, "L14", 4, 8),
    (38, "L15", 0, 7), (39, "L15", 8, 11),
]


def weight(tok):
    n = 0
    for ch in tok:
        o = ord(ch)
        if 0x0900 <= o <= 0x097F:
            cat = unicodedata.category(ch)
            if cat.startswith("M"):
                n += 0.5
            else:
                n += 1
    return max(n, 1.0)


def main():
    chunks = {c["i"]: c for c in json.load(open(os.path.join(ROOT, "audio/chunks.json")))}
    lines = {k: [] for k in LINES}
    for ci, lid, a, b in SEG:
        c = chunks[ci]
        s = c["start"] - TRIM
        e = c["end"] - TRIM
        words = LINES[lid][a:b + 1]
        ws = [weight(w) for w in words]
        total = sum(ws)
        t = s
        for w, wt in zip(words, ws):
            d = (e - s) * wt / total
            lines[lid].append({"text": w, "start": round(t, 3), "end": round(t + d, 3)})
            t += d
    out = {"audio": "assets/hi-voice.wav", "duration": 56.057, "lines": []}
    for lid in LINES:
        out["lines"].append({"id": lid, "words": lines[lid]})
    json.dump(out, open(os.path.join(ROOT, "beats.json"), "w"), ensure_ascii=False, indent=1)
    for lid in LINES:
        print(lid, " ".join(f'{w["text"]}@{w["start"]:.2f}' for w in lines[lid]))


if __name__ == "__main__":
    main()
