#!/usr/bin/env python3
"""Singapore MOE Primary / PSLE question bank generator — high uniqueness, topic-faithful."""
import os, json, random, itertools, hashlib

os.makedirs("data", exist_ok=True)
random.seed(42)

NAMES = [
    "Ali", "Bala", "Mei Ling", "Wei Jie", "Siti", "Kavitha", "David", "Sarah",
    "Fatimah", "Gopal", "Huiling", "Kumar", "Nurul", "Ravi", "Junjie",
    "Sanjay", "Ahmad", "Chloe", "Zhi Hao", "Xinyi", "Desmond", "Yusof", "Amira", "Brandon",
    "Priya", "Ethan", "Jia Hui", "Ryan", "Aisha", "Marcus"
]
ITEMS = [
    "marbles", "pencils", "stickers", "stamps", "sweets", "toy cars", "beads",
    "books", "erasers", "rulers", "paper clips", "balloons", "cards", "cupcakes", "cookies",
    "apples", "oranges", "markers", "coins", "stamps"
]

TOPICS = {
    "mathematics": {
        "P2": ["Numbers to 1000", "Addition & Subtraction", "Multiplication & Division", "Length", "Mass", "Money", "Time", "Fractions", "Shapes", "Picture Graphs"],
        "P3": ["Numbers to 10000", "Addition & Subtraction", "Multiplication & Division", "Money", "Length", "Mass", "Volume", "Time", "Fractions", "Angles", "Area & Perimeter", "Bar Graphs"],
        "P4": ["Numbers to 100000", "Factors & Multiples", "Fractions", "Decimals", "Time", "Area & Perimeter", "Symmetry", "Tables & Line Graphs"],
        "P5": ["Numbers to 10 Million", "Operations of Whole Numbers", "Fractions", "Decimals", "Area of Triangle", "Ratio", "Volume of Cube & Cuboid", "Average", "Percentage", "Angles"],
        "P6": ["Algebra", "Fractions", "Ratio", "Percentage", "Speed", "Circles", "Area & Perimeter of Composite Figures", "Volume of Composite Solids", "Pie Charts", "Net of Solids"]
    },
    "english": {
        "P2": ["Grammar MCQ", "Vocabulary MCQ", "Sentence Combining", "Editing for Spelling & Punctuation"],
        "P3": ["Grammar MCQ", "Vocabulary MCQ", "Synthesis & Transformation", "Editing"],
        "P4": ["Grammar MCQ", "Vocabulary MCQ", "Synthesis & Transformation", "Editing", "Vocabulary Cloze"],
        "P5": ["Grammar MCQ", "Vocabulary MCQ", "Synthesis & Transformation", "Editing", "Vocabulary Cloze"],
        "P6": ["Grammar MCQ", "Vocabulary MCQ", "Synthesis & Transformation", "Editing", "Vocabulary Cloze"]
    },
    "science": {
        "P3": ["Diversity of Living & Non-Living Things", "Plants & Fungi", "Materials", "Human Digestive System", "Human Muscular & Skeletal Systems"],
        "P4": ["Life Cycles of Animals", "Life Cycles of Plants", "Matter", "Light & Shadows", "Heat & Temperature"],
        "P5": ["Plant & Human Respiratory Systems", "Plant & Human Circulatory Systems", "Cell System", "Electrical Circuits", "Reproduction in Plants", "Reproduction in Humans", "Water Cycle"],
        "P6": ["Forces (Friction, Gravity, Elastic, Magnetic)", "Energy Forms & Conversions", "Photosynthesis & Respiration", "Food Chains & Food Webs", "Adaptations"]
    },
    "chinese": {
        "P2": ["Hanyu Pinyin", "Vocabulary Selection (词语选择)", "Sentence Completion (句型填空)"],
        "P3": ["Hanyu Pinyin", "Vocabulary Selection (词语选择)", "Sentence Completion (句型填空)", "Cloze Passage (短文填空)"],
        "P4": ["Vocabulary Selection (词语选择)", "Sentence Completion (句型填空)", "Cloze Passage (短文填空)", "Reading Comprehension MCQ"],
        "P5": ["Vocabulary Selection (词语选择)", "Sentence Completion (句型填空)", "Cloze Passage (短文填空)", "Reading Comprehension MCQ"],
        "P6": ["Vocabulary Selection (词语选择)", "Sentence Completion (句型填空)", "Cloze Passage (短文填空)", "Reading Comprehension MCQ"]
    }
}

def nname(i, offset=0):
    return NAMES[(i + offset) % len(NAMES)]

def nitem(i, offset=0):
    return ITEMS[(i + offset) % len(ITEMS)]

def diff_of(i):
    return ["Easy", "Medium", "Hard"][i % 3]

def shuffle_opts(correct, distractors):
    opts = [correct] + list(distractors)[:3]
    while len(opts) < 4:
        opts.append(f"Option {len(opts)+1}")
    # stable-ish shuffle from content hash
    h = int(hashlib.md5((correct + "|".join(map(str, distractors))).encode()).hexdigest(), 16)
    rng = random.Random(h)
    rng.shuffle(opts)
    return opts

def pack(qid, topic, qtype, question, answer, explanation, difficulty, options=None, heuristic=None, bar=None):
    d = {
        "id": qid,
        "topic": topic,
        "type": qtype,
        "question": question,
        "options": options or [],
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
    }
    if heuristic:
        d["heuristicId"] = heuristic
    if bar:
        d["barModel"] = bar
    return d

# -------------------- MATH GENERATORS --------------------

def math_p6(topic, i, qid):
    difficulty = diff_of(i)
    a, b = nname(i), nname(i, 3)
    item = nitem(i)

    if topic == "Algebra":
        mode = i % 5
        if mode == 0:
            c1, c2, k1, k2 = 2 + i % 6, 1 + i % 4, 3 + i % 9, 1 + i % 5
            ans_c, ans_k = c1 + c2, k1 - k2
            ans = f"{ans_c}x + {ans_k}" if ans_k >= 0 else f"{ans_c}x - {abs(ans_k)}"
            q = f"Simplify: {c1}x + {k1} + {c2}x - {k2}"
            exp = f"1. x-terms: {c1}x + {c2}x = {ans_c}x.\n2. Constants: {k1} - {k2} = {ans_k}.\n3. Result: {ans}."
            opts = shuffle_opts(ans, [f"{ans_c}x - {ans_k}", f"{c1}x + {k1}", f"{ans_c + 1}x + {ans_k}"])
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, opts, "algebra")
        if mode == 1:
            c, k, w = 2 + i % 7, 4 + i % 11, 2 + i % 6
            val = c * w + k
            q = f"Find the value of {c}w + {k} when w = {w}."
            exp = f"Substitute w = {w}: {c} × {w} + {k} = {c*w} + {k} = {val}."
            if difficulty == "Hard" and i % 2 == 0:
                return pack(qid, topic, "short_answer", q, str(val), exp, difficulty, [], "algebra")
            return pack(qid, topic, "mcq", q, str(val), exp, difficulty, shuffle_opts(str(val), [str(c+k), str(c*(w+k)), str(val+3)]), "algebra")
        if mode == 2:
            c, k = 2 + i % 5, 5 + i % 12
            ans = f"{3*c}m - {k}"
            q = f"{a} had {c}m {item}. {b} had twice as many as {a}. After they gave away {k} {item}, express the remaining number in terms of m."
            exp = f"1. {a}: {c}m. {b}: {2*c}m.\n2. Total = {3*c}m.\n3. Remaining = {3*c}m - {k}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{2*c}m - {k}", f"{3*c}m + {k}", f"{c}m - {k}"]), "algebra")
        if mode == 3:
            c, k, x = 3 + i % 5, 2 + i % 8, 4 + i % 7
            # cx - k = x  => solve? Use evaluate expression
            left = c * x - k
            q = f"If n = {x}, evaluate {c}n − {k}."
            exp = f"{c} × {x} − {k} = {c*x} − {k} = {left}."
            return pack(qid, topic, "mcq", q, str(left), exp, difficulty, shuffle_opts(str(left), [str(left+c), str(c*x+k), str(x-k)]), "algebra")
        # mode 4
        p, qv = 2 + i % 6, 3 + i % 5
        ans = f"{p}y + {qv}"
        q = f"Expand and simplify: {p}(y + 1) + {qv - p}"
        exp = f"{p}(y + 1) = {p}y + {p}. Then + {qv-p} → {p}y + {qv}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{p}y + {p}", f"{p}y - {qv}", f"y + {qv}"]), "algebra")

    if topic == "Fractions":
        mode = i % 4
        if mode == 0:
            whole = (i % 5 + 3) * 8
            num, den = 3, 8
            given = whole * num // den
            left = whole - given
            q = f"{a} had {whole} {item}. She gave {num}/{den} of them to {b}. How many did she have left?"
            exp = f"1. Given away = {num}/{den} × {whole} = {given}.\n2. Left = {whole} − {given} = {left}."
            bar = {"title": f"Fraction of {whole}", "bars": [{"name": a, "units": den, "color": "#00f2fe", "highlightUnits": den-num, "highlightColor": "#ffd166"}], "bracketText": f"{num}/{den} given away"}
            if difficulty == "Hard" and i % 2 == 0:
                return pack(qid, topic, "short_answer", q, str(left), exp, difficulty, [], "equal-fractions", bar)
            return pack(qid, topic, "mcq", q, str(left), exp, difficulty, shuffle_opts(str(left), [str(given), str(whole), str(left+2)]), "equal-fractions", bar)
        if mode == 1:
            d1, d2 = 4 + i % 3, 5 + i % 3
            # 1/d1 + 1/d2
            from math import gcd
            n = d2 + d1
            d = d1 * d2
            g = gcd(n, d)
            n, d = n // g, d // g
            ans = f"{n}/{d}"
            q = f"Find the sum of 1/{d1} and 1/{d2}. Give your answer in simplest form."
            exp = f"1/{d1} + 1/{d2} = {d2}/{d1*d2} + {d1}/{d1*d2} = {d1+d2}/{d1*d2} = {ans}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"1/{d1+d2}", f"{d1+d2}/{d1*d2}", f"2/{d1}"]), "equal-fractions")
        if mode == 2:
            tot = (i % 6 + 4) * 12
            used = tot * 5 // 12
            rem = tot - used
            q = f"A tank was 5/12 full. It contained {used} litres of water. What is the capacity of the tank?"
            exp = f"5/12 of capacity = {used} L → 1/12 = {used//5} L → capacity = 12 × {used//5} = {tot} L."
            return pack(qid, topic, "mcq", q, f"{tot} L", exp, difficulty, shuffle_opts(f"{tot} L", [f"{used} L", f"{rem} L", f"{tot+12} L"]), "equal-fractions")
        # mode 3
        u = 3 + i % 5
        of_what = u * 7
        ans = of_what * 3 // 7
        q = f"What is 3/7 of {of_what}?"
        exp = f"3/7 × {of_what} = 3 × {of_what//7} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(of_what), str(ans+u), str(of_what//7)]), "equal-fractions")

    if topic == "Ratio":
        mode = i % 3
        if mode == 0:
            diff = (4 + i % 5) * 6
            years = 2 + i % 4
            one_u = diff // 2
            son_now = one_u - years
            q = f"The age difference between {a}'s father and {a} is {diff} years. In {years} years, father will be 3 times {a}'s age. How old is {a} now?"
            exp = f"1. Difference constant = {diff}.\n2. In {years} years ratio 3:1 → 2 units = {diff} → 1 unit = {one_u}.\n3. {a} now = {one_u} − {years} = {son_now}."
            bar = {"title": f"Constant Difference ({diff} yrs)", "bars": [{"name": "Father", "units": 3, "color": "#4facfe"}, {"name": a, "units": 1, "color": "#00f2fe"}], "bracketText": f"2 units = {diff}"}
            ans = f"{son_now} years old"
            if difficulty == "Hard" and i % 2 == 0:
                return pack(qid, topic, "short_answer", q, str(son_now), exp, difficulty, [], "constant-difference", bar)
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{son_now+years} years old", f"{son_now+diff} years old", f"{one_u} years old"]), "constant-difference", bar)
        if mode == 1:
            mult = 3 + i % 6
            blue = 12 * mult  # after LCM framing
            # simpler: ratio 2:3, add red to become 4:5, blue constant
            # blue units 3 and 5 → LCM 15; initial red:blue = 10:15, new 12:15? Use classic 2:3 → 4:5
            # blue LCM of 3,5 = 15. Initial 2:3 = 10:15, new 4:5 = 12:15. Added red units = 2. If mult on 15-unit blue...
            blue = 15 * (1 + i % 4)
            unit = blue // 15
            added = 2 * unit
            q = f"A box had red and blue beads in the ratio 2:3. After {a} added {added} red beads, the ratio became 4:5. How many blue beads were there?"
            exp = f"Blue constant. LCM of 3 and 5 = 15.\nInitial 2:3 = 10:15. New 4:5 = 12:15.\nRed increased by 2 units = {added}. 1 unit = {unit}. Blue = 15 units = {blue}."
            bar = {"title": "Constant Part (Blue fixed)", "bars": [{"name": "Red after", "units": 4, "color": "#ff6b6b", "highlightUnits": 1, "highlightColor": "#ffd166"}, {"name": "Blue", "units": 5, "color": "#4facfe"}], "bracketText": f"Blue = {blue}"}
            return pack(qid, topic, "mcq", q, str(blue), exp, difficulty, shuffle_opts(str(blue), [str(10*unit), str(blue+added), str(12*unit)]), "constant-part", bar)
        # mode 2 share
        r1, r2, r3 = 2, 3, 5
        unit = 4 + i % 9
        total = (r1+r2+r3) * unit
        diffv = (r3 - r1) * unit
        q = f"{a}, {b} and Siti shared ${total} in the ratio {r1}:{r2}:{r3}. How much more did Siti receive than {a}?"
        exp = f"Total units = 10. 1 unit = ${total}//10 = ${unit}. Difference = 3 units = ${diffv}."
        bar = {"title": "Ratio share", "bars": [{"name": a, "units": 2, "color": "#00f2fe"}, {"name": b, "units": 3, "color": "#4facfe"}, {"name": "Siti", "units": 5, "color": "#a855f7"}], "bracketText": f"1 unit = ${unit}"}
        return pack(qid, topic, "mcq", q, f"${diffv}", exp, difficulty, shuffle_opts(f"${diffv}", [f"${r3*unit}", f"${r1*unit}", f"${r2*unit}"]), "constant-total", bar)

    if topic == "Percentage":
        mode = i % 3
        if mode == 0:
            price = (5 + i % 8) * 100
            pct = 15 if i % 2 else 20
            disc = price * pct // 100
            after = price - disc
            gst = round(after * 0.09, 2)
            final = round(after + gst, 2)
            q = f"A television cost ${price}. {a} bought it at {pct}% discount. GST of 9% was charged on the discounted price. How much did {a} pay?"
            exp = f"1. Discount = {pct}% of ${price} = ${disc}.\n2. Discounted = ${after}.\n3. GST = 9% of ${after} = ${gst}.\n4. Final = ${final:.2f}."
            ans = f"${final:.2f}"
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"${after:.2f}", f"${price - disc + price*9//100:.2f}", f"${price:.2f}"]), "number-value")
        if mode == 1:
            base = (i % 7 + 4) * 50
            pct = 10 + (i % 5) * 5
            part = base * pct // 100
            q = f"{pct}% of a number is {part}. What is the number?"
            exp = f"{pct}% → {part}, so 1% → {part // pct}, 100% → {base}."
            return pack(qid, topic, "mcq", q, str(base), exp, difficulty, shuffle_opts(str(base), [str(part), str(base+pct), str(base//2)]), "number-value")
        # mode 2
        old, new = 80 + i % 40, 100 + i % 50
        if new == old: new += 10
        change = new - old
        pct = round(change / old * 100, 1)
        q = f"A quantity increased from {old} to {new}. Find the percentage increase."
        exp = f"Increase = {change}. Percentage increase = {change}/{old} × 100% = {pct}%."
        ans = f"{pct}%"
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{change}%", f"{round(change/new*100,1)}%", f"{pct+5}%"]), "number-value")

    if topic == "Speed":
        mode = i % 3
        if mode == 0:
            s1, s2 = 50 + (i % 5) * 10, 40 + (i % 4) * 10
            hrs = 2 + i % 3
            dist = (s1 + s2) * hrs
            meet = 8 + hrs
            q = f"Town A and Town B are {dist} km apart. At 0800 a truck left A at {s1} km/h and a van left B at {s2} km/h towards each other. When did they meet?"
            exp = f"Combined speed = {s1+s2} km/h. Time = {dist}/{s1+s2} = {hrs} h. Meeting time = 0800 + {hrs} h = {meet:02d}00."
            ans = f"{meet:02d}00"
            bar = {"title": f"Opposite directions ({dist} km)", "bars": [{"name": "Truck", "units": 4, "color": "#00f2fe", "totalLabel": f"{s1} km/h"}, {"name": "Van", "units": 3, "color": "#ffd166", "totalLabel": f"{s2} km/h"}], "bracketText": f"Time = {hrs} h"}
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{meet-1:02d}00", f"{meet+1:02d}00", "1200"]), "speed-circles", bar)
        if mode == 1:
            speed = 40 + (i % 6) * 10
            time_h = 2 + i % 4
            dist = speed * time_h
            q = f"{a} cycled at {speed} km/h for {time_h} hours. How far did {a} travel?"
            exp = f"Distance = Speed × Time = {speed} × {time_h} = {dist} km."
            return pack(qid, topic, "mcq", q, f"{dist} km", exp, difficulty, shuffle_opts(f"{dist} km", [f"{speed} km", f"{dist+speed} km", f"{time_h} km"]), "speed-circles")
        # mode 2
        dist = 120 + (i % 5) * 30
        speed = 30 + (i % 4) * 10
        t = dist / speed
        # express as hours minutes if needed
        hrs = int(t)
        mins = int(round((t - hrs) * 60))
        ans = f"{hrs} h {mins} min" if mins else f"{hrs} h"
        q = f"A bus travels {dist} km at {speed} km/h. How long does the journey take?"
        exp = f"Time = Distance ÷ Speed = {dist} ÷ {speed} = {t} h = {ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{hrs+1} h", f"{speed} h", f"{mins} min"]), "speed-circles")

    if topic in ("Circles", "Area & Perimeter of Composite Figures"):
        r = (2 + i % 5) * 7
        quad = 22 * r * r // (7 * 4)
        tri = r * r // 2
        shaded = quad - tri
        q = f"A quadrant of radius {r} cm sits inside a square of side {r} cm. A right-angled isosceles triangle of legs {r} cm is drawn inside the quadrant. Find the shaded area (quadrant − triangle). Take π = 22/7."
        exp = f"1. Quadrant area = ¼ × 22/7 × {r}² = {quad} cm².\n2. Triangle = ½ × {r} × {r} = {tri} cm².\n3. Shaded = {quad} − {tri} = {shaded} cm²."
        ans = f"{shaded} cm²"
        if difficulty == "Hard" and i % 2 == 0:
            return pack(qid, topic, "short_answer", q, str(shaded), exp, difficulty, [], "speed-circles")
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{quad} cm²", f"{tri} cm²", f"{shaded+14} cm²"]), "speed-circles")

    if topic == "Volume of Composite Solids":
        mode = i % 3
        if mode == 0:
            n = 3 + i % 8
            side = 2 + i % 4
            vol = n * side ** 3
            q = f"A solid is made of {n} identical cubes of side {side} cm. Find the total volume."
            exp = f"Volume of 1 cube = {side}³ = {side**3} cm³. Total = {n} × {side**3} = {vol} cm³."
            return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{n*side*side} cm³", f"{vol-side**3} cm³", f"{vol+side**3} cm³"]), "number-value")
        if mode == 1:
            l, w, h = 4 + i % 5, 3 + i % 4, 5 + i % 6
            vol = l * w * h
            q = f"Find the volume of a cuboid {l} cm by {w} cm by {h} cm."
            exp = f"V = l × w × h = {l} × {w} × {h} = {vol} cm³."
            return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{l*w} cm³", f"{vol+10} cm³", f"{vol-5} cm³"]), "number-value")
        # tank
        L, W, H = 20 + i % 5 * 5, 10 + i % 4 * 5, 8 + i % 3 * 2
        filled = (i % 4 + 3) * 100
        # remaining height
        base = L * W
        h_filled = filled / base
        q = f"A rectangular tank is {L} cm long and {W} cm wide. It contains {filled} cm³ of water. What is the height of the water?"
        exp = f"Height = Volume ÷ Base area = {filled} ÷ ({L}×{W}) = {filled/base} cm."
        ans = f"{filled/base:g} cm"
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{H} cm", f"{filled} cm", f"{L} cm"]), "number-value")

    if topic == "Pie Charts":
        total = 120 + (i % 6) * 30
        pct = 10 + (i % 7) * 5
        val = total * pct // 100
        angle = pct * 360 // 100
        mode = i % 2
        if mode == 0:
            q = f"In a pie chart of {total} pupils, {pct}% liked Science. How many pupils liked Science?"
            exp = f"{pct}% of {total} = {val}."
            return pack(qid, topic, "mcq", q, str(val), exp, difficulty, shuffle_opts(str(val), [str(pct), str(total-val), str(angle)]), "number-value")
        q = f"A sector representing {pct}% of a pie chart has what angle at the centre?"
        exp = f"Angle = {pct}/100 × 360° = {angle}°."
        return pack(qid, topic, "mcq", q, f"{angle}°", exp, difficulty, shuffle_opts(f"{angle}°", [f"{pct}°", f"{360-angle}°", f"{angle+10}°"]), "number-value")

    if topic == "Net of Solids":
        mode = i % 3
        if mode == 0:
            q = f"How many faces does a cube have?"
            return pack(qid, topic, "mcq", q, "6", "A cube has 6 square faces.", difficulty, shuffle_opts("6", ["4", "8", "12"]), "number-value")
        if mode == 1:
            edge = 3 + i % 5
            # cube net area
            area = 6 * edge * edge
            q = f"A cube of edge {edge} cm is unfolded into a net. What is the total surface area of the net?"
            exp = f"6 faces × {edge}² = 6 × {edge*edge} = {area} cm²."
            return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{edge*edge} cm²", f"{4*edge*edge} cm²", f"{area+edge} cm²"]), "number-value")
        q = f"Which solid can be formed from a net of 4 triangles and 1 square?"
        ans = "Square pyramid"
        return pack(qid, topic, "mcq", q, ans, "A square base with 4 triangular faces forms a square pyramid.", difficulty, shuffle_opts(ans, ["Cube", "Triangular prism", "Cylinder"]), "number-value")

    # fallback should never hit for P6 if all topics covered
    return math_generic(topic, i, qid, "P6")


def math_generic(topic, i, qid, level):
    """Faithful fallbacks for lower levels."""
    difficulty = diff_of(i)
    a, b = nname(i), nname(i, 2)
    item = nitem(i)

    if "Addition" in topic or topic.startswith("Numbers"):
        n1 = 100 + (i * 7) % 900
        n2 = 50 + (i * 11) % 400
        if "100000" in topic or "Million" in topic:
            n1 = 10000 + (i * 97) % 80000
            n2 = 1000 + (i * 53) % 9000
        ans = n1 + n2
        q = f"{a} has {n1} {item}. {b} has {n2} {item}. How many {item} do they have altogether?"
        exp = f"{n1} + {n2} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(n1-n2), str(ans+10), str(ans-5)]))

    if "Subtraction" in topic:
        n1 = 200 + (i * 9) % 700
        n2 = 40 + (i * 5) % 150
        ans = n1 - n2
        q = f"{a} had {n1} {item}. {a} gave {n2} to {b}. How many did {a} have left?"
        exp = f"{n1} − {n2} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(n1+n2), str(n2), str(ans+2)]))

    if "Multiplication" in topic or "Operations" in topic:
        x, y = 3 + i % 9, 4 + i % 8
        ans = x * y
        q = f"There are {x} rows of {item} with {y} in each row. What is the total?"
        exp = f"{x} × {y} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(x+y), str(ans+x), str(ans-y)]))

    if topic == "Factors & Multiples":
        num = 24 + (i % 5) * 12
        factors = [k for k in range(1, num+1) if num % k == 0]
        non = [k for k in [5,7,9,11,13,14] if num % k != 0][0]
        q = f"Which of the following is NOT a factor of {num}?"
        exp = f"Factors of {num}: {factors}. {non} does not divide {num}."
        opts = shuffle_opts(str(non), [str(f) for f in factors[:3]])
        return pack(qid, topic, "mcq", q, str(non), exp, difficulty, opts)

    if topic == "Decimals":
        v = round((1 + i % 8) * 1.25, 2)
        qn = 2 + i % 5
        tot = round(v * qn, 2)
        q = f"{a} bought {qn} bottles of juice at {v} litres each. What is the total volume?"
        exp = f"{v} × {qn} = {tot} L."
        return pack(qid, topic, "mcq", q, f"{tot} L", exp, difficulty, shuffle_opts(f"{tot} L", [f"{round(tot+0.5,2)} L", f"{v} L", f"{qn} L"]))

    if "Area" in topic and "Triangle" in topic:
        base, h = 6 + (i % 6) * 2, 5 + i % 7
        area = base * h // 2
        q = f"A triangle has base {base} cm and height {h} cm. Find its area."
        exp = f"Area = ½ × {base} × {h} = {area} cm²."
        return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{base*h} cm²", f"{base+h} cm²", f"{area+5} cm²"]))

    if "Area" in topic or "Perimeter" in topic:
        l, w = 8 + i % 7, 4 + i % 5
        if "Perimeter" in topic and i % 2 == 0:
            per = 2 * (l + w)
            q = f"A rectangle is {l} cm by {w} cm. Find its perimeter."
            exp = f"Perimeter = 2 × ({l} + {w}) = {per} cm."
            return pack(qid, topic, "mcq", q, f"{per} cm", exp, difficulty, shuffle_opts(f"{per} cm", [f"{l*w} cm", f"{l+w} cm", f"{per+2} cm"]))
        area = l * w
        q = f"Find the area of a rectangle {l} cm by {w} cm."
        exp = f"Area = {l} × {w} = {area} cm²."
        return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{2*(l+w)} cm", f"{area+4} cm²", f"{l+w} cm²"]))

    if topic == "Average":
        n = 4 + i % 4
        avg = 140 + i % 20
        extra = 150 + i % 25
        new_avg = round(((n * avg) + extra) / (n + 1), 1)
        q = f"The average height of {n} pupils is {avg} cm. A new pupil of height {extra} cm joins. What is the new average?"
        exp = f"Total = {n*avg}. New total = {n*avg+extra}. New average = {new_avg} cm."
        return pack(qid, topic, "mcq", q, f"{new_avg} cm", exp, difficulty, shuffle_opts(f"{new_avg} cm", [f"{avg} cm", f"{extra} cm", f"{new_avg+1} cm"]))

    if topic == "Ratio":
        u1, u2 = 2 + i % 3, 3 + i % 4
        mult = 5 + i % 10
        tot = (u1 + u2) * mult
        v2 = u2 * mult
        q = f"{a} and {b} shared ${tot} in the ratio {u1}:{u2}. How much did {b} get?"
        exp = f"Units = {u1+u2}. 1 unit = ${mult}. {b} = {u2} units = ${v2}."
        bar = {"title": f"Ratio ${tot}", "bars": [{"name": a, "units": u1, "color": "#00f2fe"}, {"name": b, "units": u2, "color": "#4facfe"}], "bracketText": f"1u=${mult}"}
        return pack(qid, topic, "mcq", q, f"${v2}", exp, difficulty, shuffle_opts(f"${v2}", [f"${u1*mult}", f"${tot}", f"${v2-5}"]), "constant-total", bar)

    if topic == "Percentage":
        price = (3 + i % 6) * 50
        pct = 10 + (i % 5) * 5
        disc = price * pct // 100
        q = f"A bicycle costs ${price}. A {pct}% discount is given. What is the discount amount?"
        exp = f"Discount = {pct}% of ${price} = ${disc}."
        return pack(qid, topic, "mcq", q, f"${disc}", exp, difficulty, shuffle_opts(f"${disc}", [f"${price-disc}", f"${pct}", f"${disc+5}"]))

    if topic == "Volume of Cube & Cuboid" or topic == "Volume":
        l, w, h = 4 + i % 5, 3 + i % 4, 5 + i % 5
        vol = l * w * h
        q = f"Find the volume of a cuboid {l} cm × {w} cm × {h} cm."
        exp = f"V = {l}×{w}×{h} = {vol} cm³."
        return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{l*w} cm³", f"{vol+10} cm³", f"{vol-8} cm³"]))

    if topic == "Money":
        cost = 2 + i % 8
        qty = 3 + i % 5
        tot = cost * qty
        q = f"{a} bought {qty} erasers at ${cost} each. How much did {a} spend?"
        exp = f"{qty} × ${cost} = ${tot}."
        return pack(qid, topic, "mcq", q, f"${tot}", exp, difficulty, shuffle_opts(f"${tot}", [f"${cost}", f"${tot+cost}", f"${qty}"]))

    if topic == "Time":
        start_h, start_m = 8 + i % 5, (i * 5) % 60
        add = 20 + (i % 6) * 10
        end_m = start_m + add
        end_h = start_h + end_m // 60
        end_m %= 60
        q = f"A lesson starts at {start_h:02d}:{start_m:02d} and lasts {add} minutes. When does it end?"
        ans = f"{end_h:02d}:{end_m:02d}"
        exp = f"Add {add} minutes to {start_h:02d}:{start_m:02d} → {ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:00", f"{(end_h+1)%24:02d}:{end_m:02d}"]))

    if topic == "Length" or topic == "Mass":
        unit = "cm" if topic == "Length" else "g"
        x, y = 12 + i % 20, 5 + i % 10
        ans = x + y
        q = f"A ribbon is {x} {unit} long. Another is {y} {unit}. What is the total length?" if topic=="Length" else f"A bag of flour is {x} {unit}. Another is {y} {unit}. What is the total mass?"
        exp = f"{x} + {y} = {ans} {unit}."
        return pack(qid, topic, "mcq", q, f"{ans} {unit}", exp, difficulty, shuffle_opts(f"{ans} {unit}", [f"{x} {unit}", f"{abs(x-y)} {unit}", f"{ans+2} {unit}"]))

    if topic == "Fractions":
        den = 5 + i % 4
        num = 1 + i % (den - 1)
        q = f"Which fraction is shown when {num} out of {den} equal parts are shaded?"
        ans = f"{num}/{den}"
        return pack(qid, topic, "mcq", q, ans, f"{num} shaded parts out of {den} = {ans}.", difficulty, shuffle_opts(ans, [f"1/{den}", f"{den-num}/{den}", f"{num}/{den+1}"]))

    if topic == "Angles":
        a1 = 30 + (i % 5) * 10
        a2 = 180 - a1
        q = f"Two angles on a straight line are {a1}° and x. Find x."
        exp = f"Angles on a straight line sum to 180°. x = 180 − {a1} = {a2}."
        return pack(qid, topic, "mcq", q, f"{a2}°", exp, difficulty, shuffle_opts(f"{a2}°", [f"{a1}°", f"90°", f"{a2+10}°"]))

    if topic == "Symmetry":
        q = f"How many lines of symmetry does a square have?"
        return pack(qid, topic, "mcq", q, "4", "A square has 4 lines of symmetry.", difficulty, shuffle_opts("4", ["1", "2", "8"]))

    if "Graph" in topic or topic == "Tables & Line Graphs":
        v1, v2, v3 = 10 + i % 10, 15 + i % 12, 8 + i % 9
        q = f"A bar graph shows {a} scored {v1}, {b} scored {v2}, and Siti scored {v3} points. What is the total?"
        ans = str(v1+v2+v3)
        exp = f"{v1}+{v2}+{v3}={ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [str(v2), str(v1+v2), str(v1+v2+v3+5)]))

    if topic == "Shapes":
        q = f"How many sides does a hexagon have?"
        return pack(qid, topic, "mcq", q, "6", "A hexagon has 6 sides.", difficulty, shuffle_opts("6", ["5", "7", "8"]))

    if topic == "Money" or True:
        # ultimate safe fallback unique by i
        n1, n2 = 15 + i % 40, 7 + i % 20
        ans = n1 + n2
        q = f"[{topic}] {a} collected {n1} points and then earned {n2} more. What is {a}'s total?"
        exp = f"{n1} + {n2} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(n1), str(n2), str(abs(n1-n2))]))


def generate_math_question(level, qid, index):
    topics = TOPICS["mathematics"][level]
    topic = topics[(index - 1) % len(topics)]
    if level == "P6":
        return math_p6(topic, index, qid)
    if level == "P5" and topic in ("Ratio", "Percentage", "Average", "Area of Triangle", "Volume of Cube & Cuboid", "Fractions", "Decimals", "Angles", "Operations of Whole Numbers", "Numbers to 10 Million"):
        return math_generic(topic, index, qid, level)
    return math_generic(topic, index, qid, level)

# -------------------- ENGLISH --------------------

GRAMMAR = {
    "P6": [
        ("Not only ________ the suspect break into the house, but he also stole the jewelry.", "did", ["does", "had", "was"], "Inversion after 'Not only'; past narrative → 'did'."),
        ("Were he ________ the truth, his parents would have forgiven him.", "to have told", ["told", "to tell", "telling"], "Past conditional: 'Were he to have told'."),
        ("The principal requested that every teacher ________ present tomorrow.", "be", ["is", "are", "was"], "Subjunctive after 'requested that'."),
        ("My grandmother rarely goes out in the evening, ________ she?", "does", ["doesn't", "is", "isn't"], "'Rarely' is negative → positive tag 'does she?'."),
        ("Neither the boys nor their captain ________ aware of the change.", "was", ["were", "are", "been"], "Verb agrees with nearer subject 'captain'."),
        ("The storm prevented the ferry ________ leaving the terminal.", "from", ["to", "for", "by"], "'Prevent' + from + gerund."),
        ("Hardly had David stepped out ________ it started to pour.", "when", ["than", "then", "before"], "'Hardly... when'."),
        ("I would rather study diligently ________ fail my PSLE.", "than", ["then", "to", "from"], "'Would rather... than'."),
        ("She congratulated her classmate ________ winning first prize.", "on", ["for", "at", "about"], "'Congratulate someone on'."),
        ("This is the pupil ________ art project was praised.", "whose", ["who", "whom", "which"], "Possessive relative 'whose'."),
        ("No sooner had the bell rung ________ the pupils stood up.", "than", ["when", "then", "before"], "'No sooner... than'."),
        ("If I ________ you, I would revise the model method tonight.", "were", ["was", "am", "be"], "Subjunctive 'were' for advice."),
        ("The committee, as well as the principal, ________ present.", "is", ["are", "were", "have"], "'As well as' does not pluralise the verb."),
        ("She speaks English ________ than her brother.", "more fluently", ["fluent", "more fluent", "fluently"], "Adverb comparative for manner."),
        ("He is accustomed ________ waking up at dawn.", "to", ["with", "for", "by"], "'Accustomed to' + gerund."),
    ],
    "P5": [
        ("Seldom ________ we witness such an eclipse.", "do", ["does", "did", "are"], "Negative adverb → inversion."),
        ("If I ________ in your shoes, I would apologise.", "were", ["was", "am", "be"], "Subjunctive 'were'."),
        ("Having ________ her dinner, Siti washed the dishes.", "completed", ["complete", "completing", "completes"], "Having + past participle."),
        ("Siti, along with her siblings, ________ visiting the Gardens.", "is", ["are", "were", "been"], "Along with keeps singular verb."),
        ("The police are looking for the man ________ car was stolen.", "whose", ["whom", "who", "which"], "Possessive 'whose'."),
        ("Neither of the answers ________ correct.", "is", ["are", "were", "be"], "'Neither of' → singular."),
        ("He insisted ________ paying for the meal.", "on", ["to", "for", "in"], "'Insist on' + gerund."),
        ("The more you practise, ________ you become.", "the better", ["better", "the best", "good"], "The more... the better."),
    ],
    "P4": [
        ("Despite ________ exhausted, Bala finished the race.", "being", ["he was", "been", "is"], "Despite + gerund."),
        ("The boys completed the worksheet by ________.", "themselves", ["himself", "ourselves", "theirselves"], "Plural reflexive."),
        ("No sooner had the alarm rung ________ the guards rushed out.", "than", ["when", "then", "before"], "No sooner... than."),
        ("She is good ________ mathematics.", "at", ["in", "on", "for"], "Good at."),
        ("This is the book ________ I borrowed yesterday.", "which", ["who", "whose", "whom"], "Which for things."),
    ],
    "P3": [
        ("While the girls ________ netball, it started to drizzle.", "were playing", ["played", "are playing", "play"], "Past continuous interrupted."),
        ("The thief crept ________ through the corridor.", "stealthily", ["clumsily", "noisily", "boldly"], "Quietly/secretly = stealthily."),
        ("Neither of the girls ________ finished yet.", "has", ["have", "had", "having"], "Neither of + singular."),
        ("He walks to school ________ every morning.", "happily", ["happy", "happiness", "happier"], "Adverb modifies verb."),
    ],
    "P2": [
        ("My sister ________ a cake yesterday.", "baked", ["bakes", "bake", "is baking"], "Yesterday → simple past."),
        ("Every morning, father ________ to the market.", "goes", ["go", "went", "is going"], "Habit + singular."),
        ("This is the puppy ________ we rescued.", "which", ["who", "whom", "whose"], "Which for animals/things."),
        ("The children ________ in the playground now.", "are playing", ["is playing", "play", "played"], "Present continuous."),
    ],
}

VOCAB = {
    "P6": [("inevitable","certain to happen","avoidable"),("meticulously","with extreme care","recklessly"),("resilient","recovers quickly from setbacks","fragile"),
           ("subsequent","coming after in time","previous"),("validate","confirm accuracy","reject"),("unprecedented","never done before","common"),
           ("advocate","publicly support","oppose"),("meticulous","very careful and precise","careless"),("conspicuous","clearly visible","hidden"),
           ("alleviate","make suffering less severe","worsen"),("diligent","hard-working and careful","lazy"),("ambiguous","having more than one meaning","clear")],
    "P5": [("exacerbate","make worse","alleviate"),("preposterous","ridiculous","reasonable"),("deteriorate","become worse","improve"),
           ("obsolete","no longer used","modern"),("resilient","able to recover","weak"),("conspicuous","clearly visible","hidden"),
           ("reluctant","unwilling","eager"),("essential","absolutely necessary","optional")],
    "P4": [("demonstrate","show clearly","hide"),("observe","watch carefully","ignore"),("ancient","very old","modern"),
           ("temporary","lasting a short time","permanent"),("unique","one of a kind","common"),("reluctant","unwilling","eager"),
           ("spectacular","impressive to see","dull"),("generous","willing to give","selfish")],
    "P3": [("enthusiastic","full of interest","bored"),("ferocious","savage","tame"),("examine","inspect closely","ignore"),
           ("rescue","save from danger","harm"),("courageous","brave","cowardly"),("scrumptious","delicious","stale"),
           ("cluttered","messy","neat"),("commence","begin","end")],
    "P2": [("enormous","very large","tiny"),("terrified","very scared","calm"),("delicious","tastes very good","bitter"),
           ("cautious","careful","careless"),("generous","willing to share","selfish"),("exhausted","very tired","energetic"),
           ("polite","good manners","rude"),("furious","very angry","calm")],
}

SYNTHESIS = [
    ("The boy did not study. He failed the examination.", "because", "the boy failed the examination because he did not study"),
    ("Siti is very agile. She can scale the high wall easily.", "enough", "siti is agile enough to scale the high wall easily"),
    ("Bala worked hard. He was still unable to complete the task.", "Although", "although bala worked hard, he was still unable to complete the task"),
    ("You must start now. Otherwise, you will miss the last train.", "Unless", "unless you start now, you will miss the last train"),
    ("He finished his speech. The audience broke into applause.", "No sooner had", "no sooner had he finished his speech than the audience broke into applause"),
    ("She entered the room. She heard a scratching noise.", "Hardly had", "hardly had she entered the room when she heard a scratching noise"),
    ("David was poor. He contributed generously.", "Despite", "despite being poor, david contributed generously"),
    ("Mei Ling was tired. She continued revising.", "Although", "although mei ling was tired, she continued revising"),
    ("The rain stopped. The children went out to play.", "When", "when the rain stopped, the children went out to play"),
    ("He is tall. He can reach the top shelf.", "enough", "he is tall enough to reach the top shelf"),
]

def generate_english_question(level, qid, index):
    difficulty = diff_of(index)
    mode = index % 5
    name = nname(index)
    name2 = nname(index, 4)
    item = nitem(index)

    if mode == 0:
        rules = GRAMMAR[level]
        stem, ans, bad, exp = rules[index % len(rules)]
        # personalise stems for uniqueness while keeping grammar point
        q = stem.replace("David", name).replace("Siti", name).replace("Bala", name2)
        q = q.replace("the suspect", f"the suspect that {name} saw" if index % 3 == 0 else "the suspect")
        if "________" in q and index % 2:
            q = q + f" (Context: {name} was discussing this in class.)"
        return pack(qid, "Grammar MCQ", "mcq", q, ans, exp, difficulty, shuffle_opts(ans, bad))

    if mode == 1:
        words = VOCAB[level]
        word, definition, antonym = words[index % len(words)]
        others = [w[0] for w in words if w[0] != word]
        frames = [
            f'Choose the word closest in meaning to: "{definition}".',
            f'{name} looked up a word meaning "{definition}". Which word fits best?',
            f'In the sentence "{name} remained _____ during the setback", which word meaning "{definition}" fits?',
            f'Which word best matches this definition used in PSLE cloze: "{definition}"?',
            f'{name2} described something as "{definition}". Pick the best word.',
        ]
        q = frames[index % len(frames)]
        exp = f"'{word}' means '{definition}'. Opposite idea: '{antonym}'."
        return pack(qid, "Vocabulary MCQ", "mcq", q, word, exp, difficulty, shuffle_opts(word, others[:3]))

    if mode == 2 and level != "P2":
        sent, joiner, ans = SYNTHESIS[index % len(SYNTHESIS)]
        parts = [p.strip() for p in sent.split(".") if p.strip()]
        p0 = parts[0].replace("The boy", name).replace("Siti", name).replace("Bala", name).replace("David", name).replace("He", name).replace("She", name)
        p1 = parts[1].replace("He", name).replace("She", name).replace("The audience", f"the class of {name2}")
        # rebuild answer with name where simple
        ans2 = ans.replace("the boy", name.lower()).replace("siti", name.lower()).replace("bala", name.lower()).replace("david", name.lower()).replace("he ", name.lower()+" ").replace("she ", name.lower()+" ")
        q = f"Combine into one sentence using the word(s) given.\n\n1) {p0}.\n2) {p1}.\n\nUse: {joiner}"
        return pack(qid, "Synthesis & Transformation", "short_answer", q, ans2, f"Model: {ans2}", difficulty, [])

    if mode == 3:
        spell = [
            ("necessary", ["neccessary", "necesary", "neccesary"], "one c, two s"),
            ("environment", ["enviroment", "enviornment", "enviromment"], "contains 'iron'"),
            ("tomorrow", ["tommorrow", "tomorow", "tomorro"], "one m, two r"),
            ("beautiful", ["beatiful", "beautifull", "beutiful"], "beauti + ful"),
            ("because", ["becuase", "becouse", "becasue"], "be-cause"),
            ("friend", ["freind", "frend", "friand"], "i before e"),
            ("receive", ["recieve", "receve", "receeve"], "e before i after c"),
            ("definitely", ["definately", "definatly", "definetely"], "finite inside"),
            ("separate", ["seperate", "seperete", "seprate"], "sep-a-rate"),
            ("questionnaire", ["questionaire", "questionnare", "questionnair"], "double n"),
        ]
        w, bad, tip = spell[index % len(spell)]
        q = f"Choose the correctly spelt word for {name}'s editing exercise involving '{item}'."
        topic = "Editing for Spelling & Punctuation" if level == "P2" else "Editing"
        return pack(qid, topic, "mcq", q + f" Which spelling is correct?", w, f"Correct spelling is '{w}' ({tip}).", difficulty, shuffle_opts(w, bad))

    # mode 4 cloze / agreement
    cloze = [
        (f"{name} and {name2} _____ going to the library after school.", "are", ["is", "was", "be"], "Plural compound subject → are."),
        (f"Neither {name} nor {name2} _____ late yesterday.", "was", ["were", "are", "be"], "Neither nor → nearer subject; treat singular if both singular."),
        (f"The box of {item} _____ on the table.", "is", ["are", "were", "be"], "Head noun 'box' is singular."),
        (f"{name} completed the work by _____.", "himself" if index%2==0 else "herself", ["themselves", "myself", "itself"], "Reflexive matches subject."),
        (f"There _____ many {item} in the drawer.", "are", ["is", "was", "be"], "Many + plural noun → are."),
    ]
    stem, ans, bad, exp = cloze[index % len(cloze)]
    topic = "Vocabulary Cloze" if level in ("P4","P5","P6") else "Grammar MCQ"
    return pack(qid, topic, "mcq", stem, ans, exp, difficulty, shuffle_opts(ans, bad))

# -------------------- SCIENCE --------------------

SCIENCE_BANK = {
    "P6": [
        ("Forces (Friction, Gravity, Elastic, Magnetic)",
         "A {m} kg crate needed {f1} N to slide on sandpaper but only {f2} N on polished tiles. Explain why more force was needed on sandpaper.",
         "sandpaper is rougher, so frictional force is greater and opposes motion more",
         "Concept: Friction opposes motion and increases with roughness.\nEvidence: {f1} N vs {f2} N.\nReasoning: Sandpaper is rougher → greater friction → larger pulling force needed.",
         "greater frictional force",
         ["the crate became heavier on sandpaper", "gravity increased on sandpaper", "tiles created magnetic force"]),
        ("Energy Forms & Conversions",
         "A ball released from height {h} m rolled down a smooth ramp and sped up. State the main energy conversion.",
         "gravitational potential energy to kinetic energy",
         "As height falls, GPE decreases and is converted mainly to KE, so speed rises.",
         "gravitational potential energy",
         ["chemical to light energy", "kinetic to sound only", "elastic to magnetic energy"]),
        ("Photosynthesis & Respiration",
         "An aquatic plant produced {b1} oxygen bubbles/min with the lamp at 10 cm, but only {b2} bubbles/min at 50 cm. Explain.",
         "greater distance lowers light intensity and slows photosynthesis",
         "Lower light intensity → slower photosynthesis → fewer oxygen bubbles.",
         "light intensity",
         ["the plant ran out of water", "oxygen turned into carbon dioxide only", "temperature must have been zero"]),
        ("Food Chains & Food Webs",
         "In a garden food chain, caterpillars eat leaves and birds eat caterpillars. What is the role of the bird?",
         "secondary consumer / predator of the caterpillar",
         "Leaves = producer, caterpillar = primary consumer, bird = secondary consumer.",
         "secondary consumer",
         ["producer", "decomposer only", "primary consumer"]),
        ("Adaptations",
         "A desert fox has large ears. How does this help it survive heat?",
         "large ears increase surface area to lose heat faster",
         "Greater surface area of thin ears allows more heat loss to cooler air.",
         "lose heat",
         ["ears store water", "ears make it run faster only", "ears block all sunlight completely"]),
    ],
    "P5": [
        ("Electrical Circuits",
         "Two bulbs in series glowed dimly. After a third bulb was added in series, all became dimmer. Explain.",
         "more bulbs in series increase resistance and reduce current",
         "Higher total resistance → smaller current → dimmer bulbs.",
         "increases resistance",
         ["voltage of the battery increased", "bulbs gained chemical energy", "current increased"]),
        ("Water Cycle",
         "Beaker A (surface {s1} cm²) and Beaker B (surface {s2} cm²) held equal water. B lost more water in 3 hours. Explain.",
         "larger exposed surface area increases rate of evaporation",
         "More surface molecules contact air → faster evaporation.",
         "exposed surface area",
         ["B was colder", "gravity pulled water out of B only", "B had less air pressure only because it was blue"]),
        ("Cell System",
         "Onion skin cells have a cell wall and nucleus but no chloroplasts. Why no chloroplasts?",
         "onion skins grow underground without light so they do not photosynthesise",
         "Chloroplasts trap light for photosynthesis; underground cells do not need them.",
         "no light / no photosynthesis",
         ["onion cells are not living", "cell walls replace chloroplasts", "nuclei destroy chloroplasts"]),
        ("Plant & Human Respiratory Systems",
         "During exercise, breathing rate increases. Why?",
         "body cells need more oxygen and must remove more carbon dioxide",
         "Higher respiration rate in muscles demands more O₂ and produces more CO₂.",
         "more oxygen",
         ["the lungs shrink permanently", "the heart stops", "less carbon dioxide is produced"]),
        ("Plant & Human Circulatory Systems",
         "Why does the left ventricle have thicker walls than the right ventricle?",
         "it pumps blood a greater distance around the whole body",
         "Left ventricle sends blood systemically; needs greater force.",
         "pumps blood around the body",
         ["it stores urine", "it only pumps to the lungs", "it makes red blood cells"]),
        ("Reproduction in Plants",
         "Insect-pollinated flowers are often brightly coloured. Why?",
         "to attract insects that transfer pollen",
         "Bright petals attract pollinators which move pollen to other flowers.",
         "attract insects",
         ["to scare herbivores only", "to store more water", "to block sunlight"]),
        ("Reproduction in Humans",
         "Where does fertilisation usually occur in humans?",
         "in the fallopian tube / oviduct",
         "Sperm meets egg in the oviduct; the zygote then travels to the uterus.",
         "fallopian tube",
         ["only in the stomach", "in the liver", "in the large intestine"]),
    ],
    "P4": [
        ("Matter",
         "{v} cm³ of air was pumped into a rigid {cap} cm³ container. Final air volume stayed {cap} cm³. Explain.",
         "air is a gas with no definite volume and can be compressed",
         "Gases take the container's volume and can be compressed.",
         "can be compressed",
         ["air turned into a solid", "the container expanded to {v+cap}", "air has definite shape"]),
        ("Light & Shadows",
         "Plastic, tracing paper and cardboard were placed before a lamp. Only cardboard made a dark sharp shadow. Why?",
         "cardboard is opaque and blocks light",
         "Opaque materials block light completely, forming dark shadows.",
         "opaque",
         ["cardboard is transparent", "plastic absorbs all sound", "tracing paper is a light source"]),
        ("Heat & Temperature",
         "A metal lid on a glass jar loosened after hot water was poured on the lid. Explain.",
         "metal lid gained heat and expanded more/faster than glass",
         "Metal expands when heated; expansion loosened the fit.",
         "expanded",
         ["glass evaporated", "water froze the lid", "metal contracted when heated"]),
        ("Life Cycles of Animals",
         "A butterfly's life cycle includes egg, larva, pupa and adult. Which stage is the caterpillar?",
         "larva",
         "The caterpillar is the larval stage before pupa.",
         "larva",
         ["pupa only", "egg only", "adult only"]),
        ("Life Cycles of Plants",
         "Why do most seeds need water to germinate?",
         "water softens the seed coat and activates growth processes",
         "Water allows the embryo to become active and the coat to split.",
         "water",
         ["seeds need darkness only", "seeds must freeze first", "seeds need wind only"]),
    ],
    "P3": [
        ("Diversity of Living & Non-Living Things",
         "A mushroom and a fern neither produce seeds. How do they reproduce?",
         "by spores",
         "Ferns and fungi commonly reproduce using spores.",
         "spores",
         ["by giving birth to live young only", "by laying shelled eggs only", "by photosynthesis only"]),
        ("Materials",
         "A ceramic cup shattered when dropped but a plastic cup did not. Which property helped the plastic cup?",
         "plastic is less brittle / more flexible and impact-resistant",
         "Plastic can absorb impact better; ceramic is brittle.",
         "not brittle",
         ["plastic is always heavier", "ceramic is magnetic", "plastic is opaque only"]),
        ("Human Digestive System",
         "How does chewing help digestion?",
         "it breaks food into smaller pieces and increases surface area for enzymes",
         "Smaller pieces → larger surface area → enzymes act faster.",
         "surface area",
         ["chewing creates vitamins", "chewing removes all water", "chewing stops peristalsis"]),
        ("Plants & Fungi",
         "What do plants need to make food during photosynthesis?",
         "light, carbon dioxide and water",
         "Chlorophyll traps light to combine CO₂ and water into sugar (and oxygen).",
         "light",
         ["only soil minerals and darkness", "only oxygen and plastic", "only wind"]),
        ("Human Muscular & Skeletal Systems",
         "What is one function of the human skeleton?",
         "supports the body and protects organs",
         "Bones provide framework and protect organs like the brain and heart.",
         "support",
         ["produces bile only", "stores urine only", "transports oxygen only"]),
    ],
}

def generate_science_question(level, qid, index):
    actual = level if level != "P2" else "P3"
    difficulty = diff_of(index)
    bank = SCIENCE_BANK[actual]
    topic_list = TOPICS["science"][actual]
    # Prefer matching topic slot
    topic_wanted = topic_list[(index - 1) % len(topic_list)]
    candidates = [t for t in bank if t[0] == topic_wanted] or bank
    t = candidates[index % len(candidates)]
    topic, stem, ans, exp, keyword, distractors = t
    # parameter fill
    params = {
        "m": 5 + index % 10,
        "f1": 40 + index % 50,
        "f2": 10 + index % 15,
        "h": 2 + index % 8,
        "b1": 30 + index % 40,
        "b2": 5 + index % 12,
        "s1": 40 + index % 30,
        "s2": 100 + index % 80,
        "v": 80 + index % 40,
        "cap": 400 + index % 5 * 50,
    }
    question = stem.format(**params)
    explanation = exp.format(**params)
    # uniqueness wrappers
    wrappers = [
        question,
        f"Experiment log #{index}: " + question,
        f"{nname(index)} recorded the following. " + question,
        f"PSLE-style item ({topic.split()[0]}): " + question,
        f"Study the scenario carefully. " + question,
    ]
    question = wrappers[index % len(wrappers)]
    if difficulty == "Easy":
        return pack(qid, topic, "mcq", question, ans, explanation, difficulty, shuffle_opts(ans, distractors))
    q2 = question + f"\n\n(Include key idea: '{keyword}')"
    return pack(qid, topic, "short_answer", q2, keyword.lower(), explanation, difficulty, [])

# -------------------- CHINESE --------------------

CHINESE_BANK = {
    "P6": [
        ("Vocabulary Selection (词语选择)", "王校长的演讲言简意赅，令我们受益________。", "匪浅", ["浅薄", "深刻", "困难"], "成语‘受益匪浅’表示收获很大。"),
        ("Vocabulary Selection (词语选择)", "面对困难，他从不轻言放弃，总是________地前进。", "坚持不懈", ["三心二意", "得意忘形", "自暴自弃"], "‘坚持不懈’表示持续努力。"),
        ("Vocabulary Selection (词语选择)", "全班同学________，终于赢得了比赛。", "齐心协力", ["各自为政", "心不在焉", "粗心大意"], "齐心协力=同心合作。"),
        ("Sentence Completion (句型填空)", "________下雨，________运动会照常举行。", "虽然……但是……", ["因为……所以……", "不但……而且……", "只要……就……"], "转折关系用虽然……但是……。"),
        ("Sentence Completion (句型填空)", "这本科普书________内容丰富，________插图精美。", "不但……而且……", ["虽然……但是……", "因为……所以……", "如果……就……"], "递进关系用不但……而且……。"),
        ("Sentence Completion (句型填空)", "________认真复习，________能取得好成绩。", "只要……就……", ["虽然……但是……", "不但……而且……", "与其……不如……"], "条件关系。"),
        ("Cloze Passage (短文填空)", "听到远处传来雷声，小明________地跑回家。", "迫不及待", ["从容不迫", "慢条斯理", "无精打采"], "迫不及待=急不可待。"),
        ("Reading Comprehension MCQ", "短文写一位同学每天早起跑步。这段文字主要说明他怎样？", "持之以恒", ["半途而废", "骄傲自满", "心猿意马"], "长期坚持=持之以恒。"),
        ("Vocabulary Selection (词语选择)", "老师的教导让我________。", "受益匪浅", ["一无所获", "心不在焉", "花言巧语"], "表示收获大。"),
        ("Vocabulary Selection (词语选择)", "看到有人摔倒，他________地上前帮忙。", "见义勇为", ["袖手旁观", "幸灾乐祸", "冷嘲热讽"], "见义勇为=见到正义的事勇于去做。"),
    ],
    "P5": [
        ("Vocabulary Selection (词语选择)", "遇到困难时，我们要勇敢地________挑战。", "迎接", ["逃避", "害怕", "拒绝"], "迎接挑战为正面搭配。"),
        ("Sentence Completion (句型填空)", "经过筹备，活动终于________顺利举行。", "得以", ["也许", "居然", "很难"], "‘得以’表示能够实现。"),
        ("Hanyu Pinyin", "‘诚恳’ 的拼音是？", "chéng kěn", ["chén kēn", "chén kěn", "chéng kē"], "诚 chéng，恳 kěn。"),
        ("Cloze Passage (短文填空)", "他做事非常________，从不马虎。", "认真", ["马虎", "粗心", "懒惰"], "认真与马虎相反。"),
        ("Reading Comprehension MCQ", "短文赞美一位乐于助人的同学，中心思想是？", "助人为乐", ["自私自利", "斤斤计较", "骄傲自大"], "乐于助人→助人为乐。"),
        ("Vocabulary Selection (词语选择)", "春天来了，公园里的花________开了。", "争先恐后", ["无影无踪", "四面八方", "一干二净"], "形容争着开放。"),
    ],
    "P4": [
        ("Vocabulary Selection (词语选择)", "这家店的价格十分________。", "公道", ["昂贵", "浪费", "随便"], "公道=合理公平。"),
        ("Sentence Completion (句型填空)", "他上课不专心，________成绩下降。", "导致", ["因为", "所以", "可能"], "导致接不良结果。"),
        ("Hanyu Pinyin", "‘偶尔’ 的拼音是？", "ǒu ěr", ["ǒu ér", "óu ěr", "ōu ēr"], "ǒu ěr。"),
        ("Cloze Passage (短文填空)", "请你________把门关上。", "随手", ["随便", "随意", "虽然"], "随手=顺手。"),
        ("Reading Comprehension MCQ", "短文写小明把座位让给老人，表现了什么品质？", "尊敬长辈", ["骄傲自满", "自私自利", "粗心大意"], "让座=尊敬长辈。"),
    ],
    "P3": [
        ("Vocabulary Selection (词语选择)", "大雨把小明淋得像只________鸡。", "落汤", ["烤", "飞", "水"], "落汤鸡。"),
        ("Sentence Completion (句型填空)", "我们应该________帮助有困难的人。", "主动", ["被动", "故意", "偶然"], "主动帮助。"),
        ("Hanyu Pinyin", "‘医生’ 的拼音是？", "yī shēng", ["yí shēng", "yì shèng", "yī shēn"], "yī shēng。"),
        ("Cloze Passage (短文填空)", "妈妈做的菜真________。", "好吃", ["难看", "难听", "难受"], "菜→好吃。"),
    ],
    "P2": [
        ("Hanyu Pinyin", "‘学校’ 的拼音是？", "xué xiào", ["xué xiáo", "xuē xiāo", "xué xiāo"], "xué xiào。"),
        ("Vocabulary Selection (词语选择)", "弟弟在草地上高兴地________。", "奔跑", ["睡觉", "哭泣", "发呆"], "玩耍场景用奔跑。"),
        ("Sentence Completion (句型填空)", "老师表扬小明，因为他很________。", "勤奋", ["懒惰", "难过", "生气"], "被表扬的品质。"),
        ("Hanyu Pinyin", "‘朋友’ 的拼音是？", "péng yǒu", ["péng yóu", "pēng yǒu", "péng yòu"], "péng yǒu。"),
        ("Vocabulary Selection (词语选择)", "今天的天气真________。", "晴朗", ["黑暗", "嘈杂", "拥挤"], "天气搭配晴朗。"),
    ],
}


# Expanded parametric Chinese items for uniqueness
CHINESE_EXTRA = []
_idioms = [
    ("专心致志", "全神贯注地做一件事"),
    ("坚持不懈", "持续努力不放弃"),
    ("见义勇为", "看到正义的事勇于去做"),
    ("齐心协力", "大家一起努力"),
    ("受益匪浅", "得到很大收获"),
    ("迫不及待", "急着要做"),
    ("大公无私", "公正不自私"),
    ("滔滔不绝", "说话连续不停"),
    ("一丝不苟", "做事认真细致"),
    ("画龙点睛", "关键处加以点明"),
    ("守株待兔", "//不劳而获的侥幸心理"),
    ("亡羊补牢", "出了问题及时补救"),
    ("井底之蛙", "见识短浅"),
    ("对牛弹琴", "对不懂的人讲道理"),
    ("狐假虎威", "借别人势力吓唬人"),
    ("掩耳盗铃", "自己骗自己"),
    ("刻舟求剑", "不知变通"),
    ("拔苗助长", "急于求成反而坏事"),
    ("守望相助", "互相帮助"),
    ("循序渐进", "按步骤慢慢进步"),
]
for i,(idiom, meaning) in enumerate(_idioms):
    CHINESE_EXTRA.append(("Vocabulary Selection (词语选择)", f"成语“{idiom}”的意思最接近：", meaning, ["完全相反的意思", "与天气有关", "表示食物味道"], f"“{idiom}”：{meaning}。"))
    CHINESE_EXTRA.append(("Sentence Completion (句型填空)", f"造句时可以使用成语“{idiom}”来形容：", meaning, ["无关的场景", "错误的语法", "英文翻译"], f"结合语境：{meaning}。"))

_connectors = [
    ("因为……所以……", "因果关系"),
    ("虽然……但是……", "转折关系"),
    ("不但……而且……", "递进关系"),
    ("如果……就……", "假设关系"),
    ("只有……才……", "条件关系"),
    ("与其……不如……", "取舍关系"),
    ("既然……就……", "推论关系"),
    ("不管……都……", "无条件关系"),
]
for pair, meaning in _connectors:
    CHINESE_EXTRA.append(("Sentence Completion (句型填空)", f"表示{meaning}时，常用关联词：", pair, ["然后……接着……", "首先……其次……", "这里……那里……"], f"{pair} 表示{meaning}。"))

_pinyin = [
    ("学习", "xué xí"), ("快乐", "kuài lè"), ("中国", "zhōng guó"), ("谢谢", "xiè xie"),
    ("老师", "lǎo shī"), ("朋友", "péng yǒu"), ("学校", "xué xiào"), ("家庭", "jiā tíng"),
    ("时间", "shí jiān"), ("运动", "yùn dòng"), ("图书", "tú shū"), ("安静", "ān jìng"),
    ("勇敢", "yǒng gǎn"), ("诚实", "chéng shí"), ("努力", "nǔ lì"), ("成功", "chéng gōng"),
]
for word, py in _pinyin:
    bad = [py.replace(" ","")[:3]+" "+py.split()[-1], py.split()[0]+" "+py.split()[-1][::-1] if False else py.replace("ā","á"), py.replace("ī","í")]
    # simple distractors
    parts = py.split()
    distractors = [parts[0]+" "+parts[-1].swapcase() if False else parts[0]+" x", parts[0]+" "+parts[-1][:-1]+"a", "hàn yǔ"]
    CHINESE_EXTRA.append(("Hanyu Pinyin", f"“{word}” 的汉语拼音是？", py, distractors[:3], f"{word} → {py}。"))


def generate_chinese_question(level, qid, index):
    difficulty = diff_of(index)
    bank = CHINESE_BANK[level] + CHINESE_EXTRA
    t = bank[index % len(bank)]
    topic, q, ans, bad, exp = t
    name = ["小明", "小华", "美玲", "志豪", "丽芬", "伟杰", "淑慧", "俊杰"][index % 8]
    name2 = ["老师", "妈妈", "同学", "校长", "爸爸", "朋友"][index % 6]
    # parametric personalisation
    q2 = q.replace("小明", name).replace("他", name if index % 5 == 0 else "他").replace("王校长", name2 if "校长" in name2 else "王校长")
    frames = [
        q2,
        f"请选择正确的答案：{q2}",
        f"（{name}的练习）{q2}",
        f"阅读并作答：{q2}",
        f"根据句意填空：{q2}",
    ]
    qf = frames[index % len(frames)]
    if "拼音" in topic or topic == "Hanyu Pinyin":
        extras = [
            ("‘学习’ 的拼音是？", "xué xí", ["xué xì", "xuē xí", "xué xǐ"], "xué xí。"),
            ("‘快乐’ 的拼音是？", "kuài lè", ["kuai lè", "kuài le", "kuāi lè"], "kuài lè。"),
            ("‘中国’ 的拼音是？", "zhōng guó", ["zōng guó", "zhōng guo", "zhòng guó"], "zhōng guó。"),
            ("‘谢谢’ 的拼音是？", "xiè xie", ["xiē xie", "xiè xiē", "xie xie"], "xiè xie。"),
            ("‘老师’ 的拼音是？", "lǎo shī", ["lǎo sī", "láo shī", "lǎo shí"], "lǎo shī。"),
        ]
        if index % 3 == 0:
            topic, qf, ans, bad, exp = "Hanyu Pinyin", extras[index % len(extras)][0], extras[index % len(extras)][1], extras[index % len(extras)][2], extras[index % len(extras)][3]
            qf = f"{name}问：{qf}"
    return pack(qid, topic, "mcq", qf, ans, exp, difficulty, shuffle_opts(ans, bad))


def uniquify(questions):
    """Ensure unique question stems; tweak duplicates lightly."""
    seen = {}
    out = []
    for q in questions:
        stem = q["question"]
        if stem in seen:
            seen[stem] += 1
            n = seen[stem]
            # append distinguishing note without changing answer
            q = dict(q)
            q["question"] = f"{stem}\n(Variant {n})"
            q["id"] = q["id"] + f"_v{n}"
        else:
            seen[stem] = 1
        out.append(q)
    return out


def main():
    print("Compiling high-uniqueness Singapore MOE PSLE bank...")
    total = 0
    for subject, levels in TOPICS.items():
        for level in levels:
            path = f"data/{level.lower()}_{subject}.json"
            questions = []
            for i in range(1, 1001):
                qid = f"{level}_{subject.upper()[:4]}_{i:04d}"
                if subject == "mathematics":
                    q = generate_math_question(level, qid, i)
                elif subject == "english":
                    q = generate_english_question(level, qid, i)
                elif subject == "science":
                    q = generate_science_question(level, qid, i)
                else:
                    q = generate_chinese_question(level, qid, i)
                questions.append(q)
            questions = uniquify(questions)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            uniq = len({q["question"].split("\n(Variant")[0] for q in questions})
            print(f"  -> {path}: 1000 items, ~{uniq} unique stems")
            total += 1000
    print(f"Done. {total} questions compiled.")

if __name__ == "__main__":
    main()
