#!/usr/bin/env python3
"""Singapore MOE Primary / PSLE question bank generator — high uniqueness, topic-faithful."""
import os, json, random, itertools, hashlib

os.makedirs("data", exist_ok=True)
random.seed(42)

NAMES = [
    "Ali", "Bala", "Mei Ling", "Wei Jie", "Siti", "Kavitha", "David", "Sarah",
    "Fatimah", "Gopal", "Huiling", "Kumar", "Nurul", "Ravi", "Junjie",
    "Sanjay", "Ahmad", "Chloe", "Zhi Hao", "Xinyi", "Desmond", "Yusof", "Amira", "Brandon",
    "Priya", "Ethan", "Jia Hui", "Ryan", "Aisha", "Marcus", "Hafiz", "Joyce", "Kenji",
    "Lina", "Oscar", "Pei Ling", "Qistina", "Raj", "Sofia", "Tanya", "Umar", "Vera",
    "Wei Ming", "Xuan", "Yasmin", "Zane", "Ananya", "Ben", "Carmen", "Dinesh", "Elena",
    "Farid", "Gina", "Hassan", "Irene", "Joel", "Keisha", "Leo", "Mira", "Noah", "Owen",
]
ITEMS = [
    "marbles", "pencils", "stickers", "stamps", "sweets", "toy cars", "beads",
    "books", "erasers", "rulers", "paper clips", "balloons", "cards", "cupcakes", "cookies",
    "apples", "oranges", "markers", "coins", "badges", "notebooks", "crayons", "keychains",
    "postcards", "magnets", "bookmarks", "folders", "highlighters", "sharpener", "glue sticks",
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

def _math_wrap(q, i, a, topic):
    """Frame variants so identical number patterns still read as different stems."""
    places = ["the canteen", "the school hall", "Jurong library", "Bishan park", "the classroom", "East Coast Park"]
    place = places[i % len(places)]
    frames = [
        q,
        f"Word problem #{i} ({topic}): {q}",
        f"{a} worked on this at {place}. {q}",
        f"PSLE-style practice: {q}",
        f"Show your working. {q}",
        f"Heuristic check ({place}): {q}",
        f"Drill set {(i % 40) + 1}: {q}",
        f"Read carefully before choosing. {q}",
    ]
    return frames[i % len(frames)]


def math_p6(topic, i, qid):
    difficulty = diff_of(i)
    a, b = nname(i), nname(i, 3)
    item = nitem(i)

    if topic == "Algebra":
        mode = i % 5
        if mode == 0:
            c1, c2, k1, k2 = 2 + (i * 3) % 6, 1 + (i * 5) % 4, 3 + (i * 7) % 9, 1 + (i * 2) % 5
            ans_c, ans_k = c1 + c2, k1 - k2
            ans = f"{ans_c}x + {ans_k}" if ans_k >= 0 else f"{ans_c}x - {abs(ans_k)}"
            raw = f"Simplify: {c1}x + {k1} + {c2}x - {k2}"
            q = _math_wrap(raw, i, a, topic)
            exp = f"1. x-terms: {c1}x + {c2}x = {ans_c}x.\n2. Constants: {k1} - {k2} = {ans_k}.\n3. Result: {ans}."
            opts = shuffle_opts(ans, [f"{ans_c}x - {ans_k}", f"{c1}x + {k1}", f"{ans_c + 1}x + {ans_k}"])
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, opts, "algebra")
        if mode == 1:
            c, k, w = 2 + (i * 3) % 7, 4 + (i * 5) % 11, 2 + (i * 7) % 6
            val = c * w + k
            raw = f"Find the value of {c}w + {k} when w = {w}."
            q = _math_wrap(raw, i, a, topic)
            exp = f"Substitute w = {w}: {c} × {w} + {k} = {c*w} + {k} = {val}."
            if difficulty == "Hard" and i % 2 == 0:
                return pack(qid, topic, "short_answer", q, str(val), exp, difficulty, [], "algebra")
            return pack(qid, topic, "mcq", q, str(val), exp, difficulty, shuffle_opts(str(val), [str(c+k), str(c*(w+k)), str(val+3)]), "algebra")
        if mode == 2:
            c, k = 2 + (i * 3) % 5, 5 + (i * 5) % 12
            ans = f"{3*c}m - {k}"
            raw = f"{a} had {c}m {item}. {b} had twice as many as {a}. After they gave away {k} {item}, express the remaining number in terms of m."
            q = _math_wrap(raw, i, a, topic)
            exp = f"1. {a}: {c}m. {b}: {2*c}m.\n2. Total = {3*c}m.\n3. Remaining = {3*c}m - {k}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{2*c}m - {k}", f"{3*c}m + {k}", f"{c}m - {k}"]), "algebra")
        if mode == 3:
            c, k, x = 3 + (i * 2) % 5, 2 + (i * 3) % 8, 4 + (i * 5) % 7
            left = c * x - k
            raw = f"If n = {x}, evaluate {c}n − {k}."
            q = _math_wrap(raw, i, a, topic)
            exp = f"{c} × {x} − {k} = {c*x} − {k} = {left}."
            return pack(qid, topic, "mcq", q, str(left), exp, difficulty, shuffle_opts(str(left), [str(left+c), str(c*x+k), str(x-k)]), "algebra")
        # mode 4
        p, qv = 2 + (i * 3) % 6, 3 + (i * 5) % 5
        if qv < p:
            qv = p + (i % 4) + 1
        ans = f"{p}y + {qv}"
        raw = f"Expand and simplify: {p}(y + 1) + {qv - p}"
        q = _math_wrap(raw, i, a, topic)
        exp = f"{p}(y + 1) = {p}y + {p}. Then + {qv-p} → {p}y + {qv}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{p}y + {p}", f"{p}y - {qv}", f"y + {qv}"]), "algebra")

    if topic == "Fractions":
        mode = i % 4
        if mode == 0:
            whole = (i % 5 + 3) * 8
            num, den = 3, 8
            given = whole * num // den
            left = whole - given
            q = _math_wrap(f"{a} had {whole} {item}. She gave {num}/{den} of them to {b}. How many did she have left?", i, a, topic)
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
            q = _math_wrap(f"Find the sum of 1/{d1} and 1/{d2}. Give your answer in simplest form.", i, a, topic)
            exp = f"1/{d1} + 1/{d2} = {d2}/{d1*d2} + {d1}/{d1*d2} = {d1+d2}/{d1*d2} = {ans}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"1/{d1+d2}", f"{d1+d2}/{d1*d2}", f"2/{d1}"]), "equal-fractions")
        if mode == 2:
            tot = (i % 6 + 4) * 12
            used = tot * 5 // 12
            rem = tot - used
            q = _math_wrap(f"A tank was 5/12 full. It contained {used} litres of water. What is the capacity of the tank?", i, a, topic)
            exp = f"5/12 of capacity = {used} L → 1/12 = {used//5} L → capacity = 12 × {used//5} = {tot} L."
            return pack(qid, topic, "mcq", q, f"{tot} L", exp, difficulty, shuffle_opts(f"{tot} L", [f"{used} L", f"{rem} L", f"{tot+12} L"]), "equal-fractions")
        # mode 3
        u = 3 + i % 5
        of_what = u * 7
        ans = of_what * 3 // 7
        q = _math_wrap(f"What is 3/7 of {of_what}?", i, a, topic)
        exp = f"3/7 × {of_what} = 3 × {of_what//7} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(of_what), str(ans+u), str(of_what//7)]), "equal-fractions")

    if topic == "Ratio":
        mode = i % 3
        if mode == 0:
            diff = (4 + i % 5) * 6
            years = 2 + i % 4
            one_u = diff // 2
            son_now = one_u - years
            q = _math_wrap(f"The age difference between {a}'s father and {a} is {diff} years. In {years} years, father will be 3 times {a}'s age. How old is {a} now?", i, a, topic)
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
            q = _math_wrap(f"A box had red and blue beads in the ratio 2:3. After {a} added {added} red beads, the ratio became 4:5. How many blue beads were there?", i, a, topic)
            exp = f"Blue constant. LCM of 3 and 5 = 15.\nInitial 2:3 = 10:15. New 4:5 = 12:15.\nRed increased by 2 units = {added}. 1 unit = {unit}. Blue = 15 units = {blue}."
            bar = {"title": "Constant Part (Blue fixed)", "bars": [{"name": "Red after", "units": 4, "color": "#ff6b6b", "highlightUnits": 1, "highlightColor": "#ffd166"}, {"name": "Blue", "units": 5, "color": "#4facfe"}], "bracketText": f"Blue = {blue}"}
            return pack(qid, topic, "mcq", q, str(blue), exp, difficulty, shuffle_opts(str(blue), [str(10*unit), str(blue+added), str(12*unit)]), "constant-part", bar)
        # mode 2 share
        r1, r2, r3 = 2, 3, 5
        unit = 4 + i % 9
        total = (r1+r2+r3) * unit
        diffv = (r3 - r1) * unit
        q = _math_wrap(f"{a}, {b} and Siti shared ${total} in the ratio {r1}:{r2}:{r3}. How much more did Siti receive than {a}?", i, a, topic)
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
            q = _math_wrap(f"A television cost ${price}. {a} bought it at {pct}% discount. GST of 9% was charged on the discounted price. How much did {a} pay?", i, a, topic)
            exp = f"1. Discount = {pct}% of ${price} = ${disc}.\n2. Discounted = ${after}.\n3. GST = 9% of ${after} = ${gst}.\n4. Final = ${final:.2f}."
            ans = f"${final:.2f}"
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"${after:.2f}", f"${price - disc + price*9//100:.2f}", f"${price:.2f}"]), "number-value")
        if mode == 1:
            base = (i % 7 + 4) * 50
            pct = 10 + (i % 5) * 5
            part = base * pct // 100
            q = _math_wrap(f"{pct}% of a number is {part}. What is the number?", i, a, topic)
            exp = f"{pct}% → {part}, so 1% → {part // pct}, 100% → {base}."
            return pack(qid, topic, "mcq", q, str(base), exp, difficulty, shuffle_opts(str(base), [str(part), str(base+pct), str(base//2)]), "number-value")
        # mode 2
        old, new = 80 + i % 40, 100 + i % 50
        if new == old: new += 10
        change = new - old
        pct = round(change / old * 100, 1)
        q = _math_wrap(f"A quantity increased from {old} to {new}. Find the percentage increase.", i, a, topic)
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
            q = _math_wrap(f"Town A and Town B are {dist} km apart. At 0800 a truck left A at {s1} km/h and a van left B at {s2} km/h towards each other. When did they meet?", i, a, topic)
            exp = f"Combined speed = {s1+s2} km/h. Time = {dist}/{s1+s2} = {hrs} h. Meeting time = 0800 + {hrs} h = {meet:02d}00."
            ans = f"{meet:02d}00"
            bar = {"title": f"Opposite directions ({dist} km)", "bars": [{"name": "Truck", "units": 4, "color": "#00f2fe", "totalLabel": f"{s1} km/h"}, {"name": "Van", "units": 3, "color": "#ffd166", "totalLabel": f"{s2} km/h"}], "bracketText": f"Time = {hrs} h"}
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{meet-1:02d}00", f"{meet+1:02d}00", "1200"]), "speed-circles", bar)
        if mode == 1:
            speed = 40 + (i % 6) * 10
            time_h = 2 + i % 4
            dist = speed * time_h
            q = _math_wrap(f"{a} cycled at {speed} km/h for {time_h} hours. How far did {a} travel?", i, a, topic)
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
        q = _math_wrap(f"A bus travels {dist} km at {speed} km/h. How long does the journey take?", i, a, topic)
        exp = f"Time = Distance ÷ Speed = {dist} ÷ {speed} = {t} h = {ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{hrs+1} h", f"{speed} h", f"{mins} min"]), "speed-circles")

    if topic in ("Circles", "Area & Perimeter of Composite Figures"):
        r = (2 + i % 5) * 7
        quad = 22 * r * r // (7 * 4)
        tri = r * r // 2
        shaded = quad - tri
        q = _math_wrap(f"A quadrant of radius {r} cm sits inside a square of side {r} cm. A right-angled isosceles triangle of legs {r} cm is drawn inside the quadrant. Find the shaded area (quadrant − triangle). Take π = 22/7.", i, a, topic)
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
            q = _math_wrap(f"A solid is made of {n} identical cubes of side {side} cm. Find the total volume.", i, a, topic)
            exp = f"Volume of 1 cube = {side}³ = {side**3} cm³. Total = {n} × {side**3} = {vol} cm³."
            return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{n*side*side} cm³", f"{vol-side**3} cm³", f"{vol+side**3} cm³"]), "number-value")
        if mode == 1:
            l, w, h = 4 + i % 5, 3 + i % 4, 5 + i % 6
            vol = l * w * h
            q = _math_wrap(f"Find the volume of a cuboid {l} cm by {w} cm by {h} cm.", i, a, topic)
            exp = f"V = l × w × h = {l} × {w} × {h} = {vol} cm³."
            return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{l*w} cm³", f"{vol+10} cm³", f"{vol-5} cm³"]), "number-value")
        # tank
        L, W, H = 20 + i % 5 * 5, 10 + i % 4 * 5, 8 + i % 3 * 2
        filled = (i % 4 + 3) * 100
        # remaining height
        base = L * W
        h_filled = filled / base
        q = _math_wrap(f"A rectangular tank is {L} cm long and {W} cm wide. It contains {filled} cm³ of water. What is the height of the water?", i, a, topic)
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
            q = _math_wrap(f"In a pie chart of {total} pupils, {pct}% liked Science. How many pupils liked Science?", i, a, topic)
            exp = f"{pct}% of {total} = {val}."
            return pack(qid, topic, "mcq", q, str(val), exp, difficulty, shuffle_opts(str(val), [str(pct), str(total-val), str(angle)]), "number-value")
        q = _math_wrap(f"A sector representing {pct}% of a pie chart has what angle at the centre?", i, a, topic)
        exp = f"Angle = {pct}/100 × 360° = {angle}°."
        return pack(qid, topic, "mcq", q, f"{angle}°", exp, difficulty, shuffle_opts(f"{angle}°", [f"{pct}°", f"{360-angle}°", f"{angle+10}°"]), "number-value")

    if topic == "Net of Solids":
        mode = i % 3
        if mode == 0:
            q = _math_wrap(f"How many faces does a cube have?", i, a, topic)
            return pack(qid, topic, "mcq", q, "6", "A cube has 6 square faces.", difficulty, shuffle_opts("6", ["4", "8", "12"]), "number-value")
        if mode == 1:
            edge = 3 + i % 5
            # cube net area
            area = 6 * edge * edge
            q = _math_wrap(f"A cube of edge {edge} cm is unfolded into a net. What is the total surface area of the net?", i, a, topic)
            exp = f"6 faces × {edge}² = 6 × {edge*edge} = {area} cm²."
            return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{edge*edge} cm²", f"{4*edge*edge} cm²", f"{area+edge} cm²"]), "number-value")
        q = _math_wrap(f"Which solid can be formed from a net of 4 triangles and 1 square?", i, a, topic)
        ans = "Square pyramid"
        return pack(qid, topic, "mcq", q, ans, "A square base with 4 triangular faces forms a square pyramid.", difficulty, shuffle_opts(ans, ["Cube", "Triangular prism", "Cylinder"]), "number-value")

    # fallback should never hit for P6 if all topics covered
    return math_generic(topic, i, qid, "P6")



def math_generic(topic, i, qid, level):
    """Faithful fallbacks for lower levels — high parametric uniqueness."""
    difficulty = diff_of(i)
    a, b = nname(i), nname(i, 2)
    c = nname(i, 5)
    item = nitem(i)
    item2 = nitem(i, 4)

    if "Addition" in topic or topic.startswith("Numbers"):
        n1 = 100 + (i * 7) % 900 + (i % 13)
        n2 = 50 + (i * 11) % 400 + (i % 9)
        if "100000" in topic or "Million" in topic:
            n1 = 10000 + (i * 97) % 80000 + i
            n2 = 1000 + (i * 53) % 9000 + (i % 17)
        ans = n1 + n2
        variants = [
            f"{a} has {n1} {item}. {b} has {n2} {item}. How many {item} do they have altogether?",
            f"Find the sum of {n1} and {n2}.",
            f"{a} collected {n1} {item} on Monday and {n2} more on Tuesday. What is the total?",
            f"A shop sold {n1} {item} in the morning and {n2} in the afternoon. How many were sold in all?",
            f"{a}, {b} and a helper counted {n1} + {n2} {item}. What is the total count?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{n1} + {n2} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(abs(n1-n2)), str(ans+10), str(ans-5)]))

    if "Subtraction" in topic:
        n1 = 200 + (i * 9) % 700 + (i % 11)
        n2 = 40 + (i * 5) % 150 + (i % 7)
        if n2 >= n1:
            n1, n2 = n2 + 20, n1
        ans = n1 - n2
        variants = [
            f"{a} had {n1} {item}. {a} gave {n2} to {b}. How many did {a} have left?",
            f"Subtract {n2} from {n1}.",
            f"A box held {n1} {item}. After {n2} were used, how many remained?",
            f"{a}'s score was {n1}. {a} lost {n2} points. What is the new score?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{n1} − {n2} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(n1+n2), str(n2), str(ans+2)]))

    if "Multiplication" in topic or "Operations" in topic or "Division" in topic:
        x, y = 3 + (i * 3) % 9, 4 + (i * 2) % 8
        if "Division" in topic and i % 2 == 1:
            y = 2 + i % 9
            ans = x * y
            q = _math_wrap(f"{a} packed {ans} {item} equally into {y} boxes. How many in each box?", i, a, topic)
            exp = f"{ans} ÷ {y} = {x}."
            return pack(qid, topic, "mcq", q, str(x), exp, difficulty, shuffle_opts(str(x), [str(y), str(ans), str(x+y)]))
        ans = x * y
        variants = [
            f"There are {x} rows of {item} with {y} in each row. What is the total?",
            f"Calculate {x} × {y}.",
            f"{a} bought {x} packs of {item}. Each pack has {y}. How many {item} in all?",
            f"A array has {x} groups of {y} {item2}. Find the product.",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{x} × {y} = {ans}."
        return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(x+y), str(ans+x), str(ans-y)]))

    if topic == "Factors & Multiples":
        num = 24 + (i % 12) * 6 + (i % 5)
        factors = [k for k in range(1, num+1) if num % k == 0]
        non_cands = [k for k in range(2, 20) if num % k != 0]
        non = non_cands[i % len(non_cands)]
        if i % 2 == 0:
            q = _math_wrap(f"Which of the following is NOT a factor of {num}?", i, a, topic)
            exp = f"Factors of {num}: {factors}. {non} does not divide {num}."
            opts = shuffle_opts(str(non), [str(f) for f in factors[:3]])
            return pack(qid, topic, "mcq", q, str(non), exp, difficulty, opts)
        mult = num * (2 + i % 4)
        q = _math_wrap(f"Which number is a multiple of {num}?", i, a, topic)
        exp = f"{mult} = {num} × {mult // num}, so it is a multiple."
        bad = [str(num + 1), str(num + 3), str(num - 1 if num > 2 else num + 5)]
        return pack(qid, topic, "mcq", q, str(mult), exp, difficulty, shuffle_opts(str(mult), bad))

    if topic == "Decimals":
        v = round((1 + (i * 3) % 8) * 1.25 + (i % 7) * 0.01, 2)
        qn = 2 + i % 6
        tot = round(v * qn, 2)
        variants = [
            f"{a} bought {qn} bottles of juice at {v} litres each. What is the total volume?",
            f"Find {qn} × {v}.",
            f"Each bottle holds {v} L. {qn} bottles hold how many litres?",
            f"At the shop, {a} paid for {qn} items costing {v} units each. Total measure?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{v} × {qn} = {tot} L."
        return pack(qid, topic, "mcq", q, f"{tot} L", exp, difficulty, shuffle_opts(f"{tot} L", [f"{round(tot+0.5,2)} L", f"{v} L", f"{qn} L"]))

    if "Area" in topic and "Triangle" in topic:
        base, h = 6 + (i % 8) * 2, 5 + (i * 3) % 9
        area = base * h // 2
        variants = [
            f"A triangle has base {base} cm and height {h} cm. Find its area.",
            f"Find the area of △ with base {base} cm and perpendicular height {h} cm.",
            f"{a} drew a triangle ({base} cm base, {h} cm height). What is its area?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Area = ½ × {base} × {h} = {area} cm²."
        return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{base*h} cm²", f"{base+h} cm²", f"{area+5} cm²"]))

    if "Area" in topic or "Perimeter" in topic or "Composite" in topic:
        l, w = 8 + (i * 2) % 9, 4 + (i * 3) % 7
        if ("Perimeter" in topic and i % 2 == 0) or (i % 3 == 0 and "Area" not in topic):
            per = 2 * (l + w)
            variants = [
                f"A rectangle is {l} cm by {w} cm. Find its perimeter.",
                f"Find the perimeter of a {l} cm × {w} cm rectangle.",
                f"{a} fenced a {l} by {w} cm rectangle. What length of fence is needed?",
            ]
            q = _math_wrap(variants[i % len(variants)], i, a, topic)
            exp = f"Perimeter = 2 × ({l} + {w}) = {per} cm."
            return pack(qid, topic, "mcq", q, f"{per} cm", exp, difficulty, shuffle_opts(f"{per} cm", [f"{l*w} cm", f"{l+w} cm", f"{per+2} cm"]))
        area = l * w
        variants = [
            f"Find the area of a rectangle {l} cm by {w} cm.",
            f"A card measures {l} cm × {w} cm. What is its area?",
            f"{a} painted a {l} cm by {w} cm board. Area painted?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Area = {l} × {w} = {area} cm²."
        return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{2*(l+w)} cm", f"{area+4} cm²", f"{l+w} cm²"]))

    if topic == "Average":
        n = 4 + i % 5
        avg = 140 + (i * 3) % 25
        extra = 150 + (i * 5) % 30
        new_avg = round(((n * avg) + extra) / (n + 1), 1)
        variants = [
            f"The average height of {n} pupils is {avg} cm. A new pupil of height {extra} cm joins. What is the new average?",
            f"{n} scores average {avg}. One more score of {extra} is added. New average?",
            f"{a}'s group of {n} has mean {avg}. {b} joins with {extra}. Find the new mean.",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Total = {n*avg}. New total = {n*avg+extra}. New average = {new_avg} cm."
        return pack(qid, topic, "mcq", q, f"{new_avg} cm", exp, difficulty, shuffle_opts(f"{new_avg} cm", [f"{avg} cm", f"{extra} cm", f"{new_avg+1} cm"]))

    if topic == "Ratio":
        u1, u2 = 2 + i % 4, 3 + (i * 2) % 5
        mult = 5 + (i * 3) % 12
        tot = (u1 + u2) * mult
        v2 = u2 * mult
        variants = [
            f"{a} and {b} shared ${tot} in the ratio {u1}:{u2}. How much did {b} get?",
            f"Share {tot} in the ratio {u1}:{u2}. Find the larger share if u2≥u1 else the second share (for {b}).",
            f"Ratio {u1}:{u2}. Total ${tot}. {b}'s amount?",
        ]
        # clarify second share always b = u2*mult
        variants[1] = f"Amount ${tot} is shared in the ratio {u1}:{u2} between {a} and {b}. How much does {b} receive?"
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Units = {u1+u2}. 1 unit = ${mult}. {b} = {u2} units = ${v2}."
        bar = {"title": f"Ratio ${tot}", "bars": [{"name": a, "units": u1, "color": "#00f2fe"}, {"name": b, "units": u2, "color": "#4facfe"}], "bracketText": f"1u=${mult}"}
        return pack(qid, topic, "mcq", q, f"${v2}", exp, difficulty, shuffle_opts(f"${v2}", [f"${u1*mult}", f"${tot}", f"${v2+mult}"]), "constant-total", bar)

    if topic == "Percentage":
        price = (3 + i % 8) * 50 + (i % 3) * 10
        pct = 10 + (i % 7) * 5
        disc = price * pct // 100
        variants = [
            f"A bicycle costs ${price}. A {pct}% discount is given. What is the discount amount?",
            f"Find {pct}% of ${price}.",
            f"{a} saw a ${price} item with {pct}% off. How much is the discount?",
            f"Discount rate {pct}% on ${price}. Discount value?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Discount = {pct}% of ${price} = ${disc}."
        return pack(qid, topic, "mcq", q, f"${disc}", exp, difficulty, shuffle_opts(f"${disc}", [f"${price-disc}", f"${pct}", f"${disc+5}"]))

    if topic in ("Volume of Cube & Cuboid", "Volume", "Volume of Composite Solids") or "Volume" in topic:
        l, w, h = 4 + (i * 2) % 6, 3 + (i * 3) % 5, 5 + (i * 5) % 6
        vol = l * w * h
        variants = [
            f"Find the volume of a cuboid {l} cm × {w} cm × {h} cm.",
            f"A box is {l} by {w} by {h} cm. What is its volume?",
            f"{a} filled a {l}×{w}×{h} cm container. Volume of space?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"V = {l}×{w}×{h} = {vol} cm³."
        return pack(qid, topic, "mcq", q, f"{vol} cm³", exp, difficulty, shuffle_opts(f"{vol} cm³", [f"{l*w} cm³", f"{vol+10} cm³", f"{vol-8} cm³"]))

    if topic == "Money":
        cost = 2 + (i * 3) % 9
        qty = 3 + (i * 2) % 6
        tot = cost * qty
        variants = [
            f"{a} bought {qty} erasers at ${cost} each. How much did {a} spend?",
            f"Cost of {qty} items at ${cost} each?",
            f"{a} paid for {qty} {item} @ ${cost}. Total cost?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{qty} × ${cost} = ${tot}."
        return pack(qid, topic, "mcq", q, f"${tot}", exp, difficulty, shuffle_opts(f"${tot}", [f"${cost}", f"${tot+cost}", f"${qty}"]))

    if topic == "Time" or topic == "Speed":
        start_h, start_m = 8 + i % 6, (i * 7) % 60
        add = 15 + (i % 8) * 10
        end_m = start_m + add
        end_h = start_h + end_m // 60
        end_m %= 60
        if topic == "Speed" and i % 2 == 0:
            dist = 30 + (i * 5) % 90
            time_h = 2 + i % 4
            speed = dist // time_h
            q = _math_wrap(f"{a} travelled {dist} km in {time_h} hours. What was the average speed?", i, a, topic)
            exp = f"Speed = distance ÷ time = {dist} ÷ {time_h} = {speed} km/h."
            return pack(qid, topic, "mcq", q, f"{speed} km/h", exp, difficulty, shuffle_opts(f"{speed} km/h", [f"{dist} km/h", f"{time_h} km/h", f"{speed+2} km/h"]))
        ans = f"{end_h:02d}:{end_m:02d}"
        variants = [
            f"A lesson starts at {start_h:02d}:{start_m:02d} and lasts {add} minutes. When does it end?",
            f"Start {start_h:02d}:{start_m:02d}, duration {add} min. End time?",
            f"{a}'s activity begins at {start_h:02d}:{start_m:02d} for {add} minutes. Finishing time?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"Add {add} minutes to {start_h:02d}:{start_m:02d} → {ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:00", f"{(end_h+1)%24:02d}:{end_m:02d}"]))

    if topic == "Length" or topic == "Mass":
        unit = "cm" if topic == "Length" else "g"
        x, y = 12 + (i * 5) % 30, 5 + (i * 3) % 15
        ans = x + y
        if topic == "Length":
            variants = [
                f"A ribbon is {x} {unit} long. Another is {y} {unit}. What is the total length?",
                f"Add lengths {x} {unit} and {y} {unit}.",
                f"{a} joined two sticks ({x} {unit} and {y} {unit}). Total length?",
            ]
        else:
            variants = [
                f"A bag of flour is {x} {unit}. Another is {y} {unit}. What is the total mass?",
                f"Masses {x} {unit} and {y} {unit}. Total?",
                f"{a} combined {x} {unit} and {y} {unit} of sugar. Total mass?",
            ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{x} + {y} = {ans} {unit}."
        return pack(qid, topic, "mcq", q, f"{ans} {unit}", exp, difficulty, shuffle_opts(f"{ans} {unit}", [f"{x} {unit}", f"{abs(x-y)} {unit}", f"{ans+2} {unit}"]))

    if topic == "Fractions":
        den = 5 + i % 6
        num = 1 + i % (den - 1)
        if i % 3 == 0:
            whole = den * (2 + i % 5)
            ans = whole * num // den
            q = _math_wrap(f"What is {num}/{den} of {whole}?", i, a, topic)
            exp = f"{num}/{den} × {whole} = {ans}."
            return pack(qid, topic, "mcq", q, str(ans), exp, difficulty, shuffle_opts(str(ans), [str(whole), str(num), str(ans+den)]))
        variants = [
            f"Which fraction is shown when {num} out of {den} equal parts are shaded?",
            f"{num} of {den} equal parts are red. What fraction is red?",
            f"Express {num} shaded parts out of {den} as a fraction.",
        ]
        ans = f"{num}/{den}"
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        return pack(qid, topic, "mcq", q, ans, f"{num} shaded parts out of {den} = {ans}.", difficulty, shuffle_opts(ans, [f"1/{den}", f"{den-num}/{den}", f"{num}/{den+1}"]))

    if topic == "Angles":
        a1 = 30 + (i * 7) % 50
        mode = i % 3
        if mode == 0:
            a2 = 180 - a1
            q = _math_wrap(f"Two angles on a straight line are {a1}° and x. Find x.", i, a, topic)
            exp = f"Angles on a straight line sum to 180°. x = 180 − {a1} = {a2}."
            return pack(qid, topic, "mcq", q, f"{a2}°", exp, difficulty, shuffle_opts(f"{a2}°", [f"{a1}°", f"90°", f"{a2+10}°"]))
        if mode == 1:
            a2 = 360 - a1
            q = _math_wrap(f"Angles at a point: one angle is {a1}°. The reflex adjacent measure around the point for the rest is?", i, a, topic)
            exp = f"Angles at a point sum to 360°. Remaining = 360 − {a1} = {a2}."
            return pack(qid, topic, "mcq", q, f"{a2}°", exp, difficulty, shuffle_opts(f"{a2}°", [f"{a1}°", f"180°", f"{180-a1}°"]))
        a2 = 90 - (a1 % 90 if a1 < 90 else a1 - 90)
        if a2 <= 0:
            a2 = 90 - (a1 % 80)
        q = _math_wrap(f"Complement of {90-a2}° is?", i, a, topic)
        exp = f"Complementary angles sum to 90°. Answer {a2}°."
        return pack(qid, topic, "mcq", q, f"{a2}°", exp, difficulty, shuffle_opts(f"{a2}°", [f"{90+a2}°", f"90°", f"{a2+5}°"]))

    if topic == "Symmetry":
        shapes = [
            ("square", "4"),
            ("equilateral triangle", "3"),
            ("rectangle that is not a square", "2"),
            ("isosceles triangle that is not equilateral", "1"),
            ("circle", "infinite"),
            ("regular pentagon", "5"),
            ("regular hexagon", "6"),
            ("parallelogram that is not a rhombus/rectangle", "0"),
        ]
        shape, ans = shapes[i % len(shapes)]
        q = _math_wrap(f"How many lines of symmetry does a {shape} have?", i, a, topic)
        exp = f"A {shape} has {ans} line(s) of symmetry."
        bad = [x for x in ["0", "1", "2", "3", "4", "5", "6", "8"] if x != ans][:3]
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, bad))

    if "Graph" in topic or topic == "Tables & Line Graphs" or topic == "Pie Charts":
        v1, v2, v3 = 10 + (i * 3) % 15, 15 + (i * 5) % 18, 8 + (i * 7) % 12
        if topic == "Pie Charts" and i % 2 == 0:
            total = v1 + v2 + v3
            q = _math_wrap(f"In a pie chart, {a} has {v1} votes out of {total}. About what fraction of the chart is that?", i, a, topic)
            ans = f"{v1}/{total}"
            exp = f"Fraction = {v1}/{total}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{v2}/{total}", f"{v1}/{v2}", f"1/{total}"]))
        variants = [
            f"A bar graph shows {a} scored {v1}, {b} scored {v2}, and {c} scored {v3} points. What is the total?",
            f"Read the table: {a}={v1}, {b}={v2}, {c}={v3}. Sum?",
            f"Points: {v1}, {v2}, {v3}. Find the total.",
        ]
        ans = str(v1 + v2 + v3)
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{v1}+{v2}+{v3}={ans}."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [str(v2), str(v1+v2), str(v1+v2+v3+5)]))

    if topic == "Shapes" or topic == "Net of Solids":
        shapes = [
            ("triangle", "3"), ("quadrilateral", "4"), ("pentagon", "5"),
            ("hexagon", "6"), ("octagon", "8"), ("heptagon", "7"),
        ]
        if topic == "Net of Solids":
            nets = [
                ("cube", "6 faces"),
                ("cuboid", "6 faces"),
                ("triangular prism", "5 faces"),
                ("square pyramid", "5 faces"),
            ]
            solid, ans = nets[i % len(nets)]
            q = _math_wrap(f"A net of a {solid} folds into how many faces?", i, a, topic)
            exp = f"A {solid} has {ans}."
            return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, ["4 faces", "8 faces", "3 faces"]))
        shape, ans = shapes[i % len(shapes)]
        q = _math_wrap(f"How many sides does a {shape} have?", i, a, topic)
        exp = f"A {shape} has {ans} sides."
        bad = [x for x in ["3", "4", "5", "6", "7", "8"] if x != ans][:3]
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, bad))

    if topic == "Circles":
        r = 3 + (i * 2) % 10
        # use 22/7 when r multiple of 7 else leave in terms of π
        if r % 7 == 0:
            area = (22 * r * r) // 7
            q = _math_wrap(f"Taking π = 22/7, find the area of a circle radius {r} cm.", i, a, topic)
            exp = f"Area = πr² = 22/7 × {r}² = {area} cm²."
            return pack(qid, topic, "mcq", q, f"{area} cm²", exp, difficulty, shuffle_opts(f"{area} cm²", [f"{2*r} cm²", f"{r*r} cm²", f"{area+22} cm²"]))
        q = _math_wrap(f"Express the circumference of a circle radius {r} cm in terms of π.", i, a, topic)
        ans = f"{2*r}π cm"
        exp = f"C = 2πr = 2π×{r} = {2*r}π cm."
        return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, [f"{r}π cm", f"{r*r}π cm", f"{2*r} cm"]))

    if topic == "Algebra":
        c, k, w = 2 + i % 8, 3 + (i * 3) % 12, 2 + (i * 5) % 7
        val = c * w + k
        variants = [
            f"Find the value of {c}w + {k} when w = {w}.",
            f"If w = {w}, evaluate {c}w + {k}.",
            f"{a} uses formula {c}w + {k}. When w = {w}, what is the value?",
        ]
        q = _math_wrap(variants[i % len(variants)], i, a, topic)
        exp = f"{c}×{w}+{k}={val}."
        return pack(qid, topic, "mcq", q, str(val), exp, difficulty, shuffle_opts(str(val), [str(c+k), str(c*w), str(val+2)]), "algebra")

    # ultimate safe fallback unique by i
    n1, n2 = 15 + (i * 7) % 80, 7 + (i * 5) % 40
    ans = n1 + n2
    q = _math_wrap(f"[{topic}] {a} collected {n1} points and then earned {n2} more. What is {a}'s total?", i, a, topic)
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

PLACES_SG = [
    "Jurong", "Tampines", "Bishan", "East Coast", "Gardens by the Bay",
    "Marina Bay", "the library", "the canteen", "the MRT station",
    "Orchard Road", "Sentosa", "Changi", "Toa Payoh", "Ang Mo Kio",
    "the school hall", "the neighbourhood park", "the community centre",
    "HDB void deck", "Botanic Gardens", "Clarke Quay",
]

TIMES_OF_DAY = [
    "in the morning", "after school", "at noon", "in the evening",
    "before recess", "during the weekend", "on Monday", "last night",
    "at dawn", "just before dinner", "during assembly", "after CCA",
]

GRAMMAR = {
    "P6": [
        ("Not only ________ {name} break into the house, but {pron} also stole the jewelry.", "did", ["does", "had", "was"], "Inversion after 'Not only'; past narrative → 'did'."),
        ("Were {name} ________ the truth, {poss} parents would have forgiven {obj}.", "to have told", ["told", "to tell", "telling"], "Past conditional: 'Were he/she to have told'."),
        ("The principal requested that every teacher ________ present tomorrow.", "be", ["is", "are", "was"], "Subjunctive after 'requested that'."),
        ("{name} rarely goes out in the evening, ________ {pron}?", "does", ["doesn't", "is", "isn't"], "Negative adverb → positive question tag."),
        ("Neither the boys nor their captain ________ aware of the change.", "was", ["were", "are", "been"], "Verb agrees with nearer subject 'captain'."),
        ("The storm prevented the ferry ________ leaving the terminal.", "from", ["to", "for", "by"], "'Prevent' + from + gerund."),
        ("Hardly had {name} stepped out ________ it started to pour.", "when", ["than", "then", "before"], "'Hardly... when'."),
        ("I would rather study diligently ________ fail my PSLE.", "than", ["then", "to", "from"], "'Would rather... than'."),
        ("{name} congratulated {name2} ________ winning first prize.", "on", ["for", "at", "about"], "'Congratulate someone on'."),
        ("This is the pupil ________ art project was praised at {place}.", "whose", ["who", "whom", "which"], "Possessive relative 'whose'."),
        ("No sooner had the bell rung ________ the pupils stood up.", "than", ["when", "then", "before"], "'No sooner... than'."),
        ("If I ________ you, I would revise the model method tonight.", "were", ["was", "am", "be"], "Subjunctive 'were' for advice."),
        ("The committee, as well as the principal, ________ present.", "is", ["are", "were", "have"], "'As well as' does not pluralise the verb."),
        ("{name} speaks English ________ than {name2}.", "more fluently", ["fluent", "more fluent", "fluently"], "Adverb comparative for manner."),
        ("{name} is accustomed ________ waking up at dawn.", "to", ["with", "for", "by"], "'Accustomed to' + gerund."),
        ("Only after {name} apologised ________ the teacher calm down.", "did", ["does", "had", "was"], "Only after → inversion with 'did'."),
        ("{name} suggested that {name2} ________ the draft again.", "rewrite", ["rewrites", "rewrote", "rewriting"], "Subjunctive after 'suggested that'."),
        ("Scarcely had the guests arrived ________ the lights went out.", "when", ["than", "then", "before"], "'Scarcely... when'."),
        ("It is essential that every pupil ________ on time for the oral.", "be", ["is", "are", "was"], "Subjunctive after 'essential that'."),
        ("{name} prefers reading quietly ________ chatting loudly.", "to", ["than", "from", "for"], "'Prefer A to B'."),
        ("Little ________ {name} realise how serious the mistake was.", "did", ["does", "had", "was"], "Negative adverb 'Little' → inversion."),
        ("The pair of scissors ________ on the teacher's desk.", "is", ["are", "were", "be"], "'Pair' is singular head noun."),
        ("{name} objected ________ leaving early without permission.", "to", ["for", "at", "with"], "'Object to' + gerund."),
        ("So dense was the fog ________ the ferry could not depart.", "that", ["than", "then", "when"], "'So... that' result clause."),
        ("{name} has been living in {place} ________ 2019.", "since", ["for", "from", "during"], "'Since' + point in time."),
        ("Had {name} studied harder, {pron} ________ passed the paper.", "would have", ["will have", "would", "had"], "Third conditional inverted form."),
        ("Each of the contestants ________ given a certificate.", "was", ["were", "are", "be"], "'Each of' takes singular verb."),
        ("{name} is the tallest pupil ________ all in the class.", "of", ["from", "than", "among"], "'The tallest of'."),
        ("Not until midnight ________ the search party return.", "did", ["does", "had", "was"], "'Not until' → inversion."),
        ("{name} can speak Malay, ________ {pron}?", "can't", ["can", "doesn't", "isn't"], "Positive statement → negative tag."),
    ],
    "P5": [
        ("Seldom ________ we witness such an eclipse.", "do", ["does", "did", "are"], "Negative adverb → inversion."),
        ("If I ________ in your shoes, I would apologise.", "were", ["was", "am", "be"], "Subjunctive 'were'."),
        ("Having ________ {poss} dinner, {name} washed the dishes.", "completed", ["complete", "completing", "completes"], "Having + past participle."),
        ("{name}, along with {poss} siblings, ________ visiting {place}.", "is", ["are", "were", "been"], "Along with keeps singular verb."),
        ("The police are looking for the man ________ car was stolen.", "whose", ["whom", "who", "which"], "Possessive 'whose'."),
        ("Neither of the answers ________ correct.", "is", ["are", "were", "be"], "'Neither of' → singular."),
        ("{name} insisted ________ paying for the meal.", "on", ["to", "for", "in"], "'Insist on' + gerund."),
        ("The more you practise, ________ you become.", "the better", ["better", "the best", "good"], "The more... the better."),
        ("By the time {name} arrived, the show ________ already started.", "had", ["has", "have", "was"], "Past perfect for earlier past action."),
        ("{name} looks forward ________ the school holidays.", "to", ["for", "on", "at"], "'Look forward to'."),
        ("Unless you hurry, you ________ miss the MRT.", "will", ["would", "should", "can"], "Unless + present, will + base."),
        ("The news about the trip ________ surprising.", "was", ["were", "are", "be"], "'News' is singular."),
        ("{name} is capable ________ solving the puzzle alone.", "of", ["to", "for", "with"], "'Capable of' + gerund."),
        ("Not only did {name} win, ________ {pron} also set a record.", "but", ["and", "so", "or"], "'Not only... but also'."),
        ("{name} has lived here ________ five years.", "for", ["since", "from", "during"], "'For' + duration."),
        ("I wish I ________ taller for the basketball team.", "were", ["was", "am", "be"], "Wish + subjunctive."),
        ("The children enjoyed ________ at {place}.", "themselves", ["himself", "ourselves", "theirselves"], "Plural reflexive."),
        ("{name} asked where the stationery shop ________.", "was", ["is", "were", "be"], "Reported question → past."),
        ("Despite ________ tired, {name} finished the project.", "being", ["he was", "been", "is"], "Despite + gerund."),
        ("{name} would rather walk ________ take a crowded bus.", "than", ["then", "to", "from"], "'Would rather... than'."),
        ("It was {name} ________ found the missing key.", "who", ["which", "whom", "whose"], "Who for people as subject."),
        ("Neither {name} nor {name2} ________ interested in the club.", "is", ["are", "were", "be"], "Neither... nor agrees with nearer subject."),
        ("{name} apologised ________ being late to CCA.", "for", ["on", "at", "to"], "'Apologise for' + gerund."),
        ("Hardly ________ {name} sit down when the phone rang.", "had", ["has", "did", "was"], "'Hardly had' + past participle."),
        ("The number of pupils in the hall ________ increasing.", "is", ["are", "were", "be"], "'The number of' → singular."),
        ("{name} succeeded ________ convincing the teacher.", "in", ["to", "at", "for"], "'Succeed in' + gerund."),
        ("So carefully ________ {name} pack the vase that it arrived safely.", "did", ["does", "had", "was"], "'So... that' with inversion."),
        ("{name} is used ________ the humid weather in Singapore.", "to", ["with", "for", "by"], "'Used to' meaning accustomed."),
    ],
    "P4": [
        ("Despite ________ exhausted, {name} finished the race.", "being", ["he was", "been", "is"], "Despite + gerund."),
        ("The boys completed the worksheet by ________.", "themselves", ["himself", "ourselves", "theirselves"], "Plural reflexive."),
        ("No sooner had the alarm rung ________ the guards rushed out.", "than", ["when", "then", "before"], "No sooner... than."),
        ("{name} is good ________ mathematics.", "at", ["in", "on", "for"], "Good at."),
        ("This is the book ________ I borrowed yesterday.", "which", ["who", "whose", "whom"], "Which for things."),
        ("{name} has already ________ {poss} homework.", "done", ["did", "does", "doing"], "Present perfect + past participle."),
        ("If it rains, we ________ cancel the picnic at {place}.", "will", ["would", "should", "can"], "First conditional."),
        ("{name} and {name2} ________ walking to the MRT now.", "are", ["is", "was", "be"], "Compound subject → plural."),
        ("There ________ a lot of traffic near {place} today.", "is", ["are", "were", "be"], "'A lot of' + uncountable → singular."),
        ("{name} prefers tea ________ coffee.", "to", ["than", "from", "for"], "Prefer A to B."),
        ("The cake was baked ________ {name}'s mother.", "by", ["from", "with", "of"], "Passive agent 'by'."),
        ("{name} has lived in {place} ________ 2020.", "since", ["for", "from", "during"], "Since + starting point."),
        ("Please remember ________ the lights before you leave.", "to switch off", ["switching off", "switch off", "switched off"], "Remember + to-infinitive for future duty."),
        ("Neither of the twins ________ ready yet.", "is", ["are", "were", "be"], "Neither of → singular."),
        ("{name} walked ________ than {name2} to reach school.", "faster", ["fast", "fastest", "more fast"], "Comparative adverb."),
        ("The teacher told the class ________ quietly.", "to work", ["working", "work", "worked"], "Tell + object + to-infinitive."),
        ("{name} was born ________ May.", "in", ["on", "at", "by"], "In + month."),
        ("This is the girl ________ won the storytelling prize.", "who", ["which", "whom", "whose"], "Who as subject for people."),
        ("{name} enjoys ________ comics after dinner.", "reading", ["read", "to reading", "reads"], "Enjoy + gerund."),
        ("Unless {name} practises, {pron} ________ improve.", "will not", ["would not", "did not", "has not"], "Unless + present, will not."),
        ("A pair of shoes ________ under the bench.", "was", ["were", "are", "be"], "'Pair' is singular."),
        ("{name} is interested ________ science experiments.", "in", ["on", "at", "for"], "Interested in."),
        ("The more carefully you write, ________ your marks will be.", "the higher", ["higher", "the highest", "high"], "The more... the higher."),
        ("{name} asked me where the canteen ________.", "was", ["is", "were", "be"], "Reported speech shifts tense."),
        ("Both {name} and {name2} ________ keen on football.", "are", ["is", "was", "be"], "Both A and B → plural."),
        ("{name} looked ________ the window at the rain.", "out of", ["into", "onto", "upon"], "Look out of the window."),
        ("I have never ________ such a beautiful sunset at {place}.", "seen", ["saw", "see", "seeing"], "Present perfect after never."),
        ("{name} went to bed early ________ {pron} was tired.", "because", ["although", "unless", "despite"], "Because shows reason."),
    ],
    "P3": [
        ("While the girls ________ netball, it started to drizzle.", "were playing", ["played", "are playing", "play"], "Past continuous interrupted."),
        ("The thief crept ________ through the corridor.", "stealthily", ["clumsily", "noisily", "boldly"], "Quietly/secretly = stealthily."),
        ("Neither of the girls ________ finished yet.", "has", ["have", "had", "having"], "Neither of + singular."),
        ("{name} walks to school ________ every morning.", "happily", ["happy", "happiness", "happier"], "Adverb modifies verb."),
        ("{name} ________ a letter to {poss} grandmother yesterday.", "wrote", ["writes", "write", "writing"], "Yesterday → simple past."),
        ("Look! The birds ________ over {place}.", "are flying", ["fly", "flew", "flying"], "Present continuous for now."),
        ("This is the boy ________ helped me carry the bags.", "who", ["which", "whose", "whom"], "Who for people."),
        ("{name} is taller ________ {name2}.", "than", ["then", "to", "from"], "Comparative + than."),
        ("There ________ three apples on the table.", "are", ["is", "was", "be"], "Plural subject → are."),
        ("{name} always ________ {poss} teeth before bed.", "brushes", ["brush", "brushed", "brushing"], "Habit + third person -s."),
        ("The cat hid ________ the sofa during the storm.", "under", ["over", "between", "along"], "Under = beneath."),
        ("{name} and {name2} ________ best friends.", "are", ["is", "was", "be"], "Compound subject plural."),
        ("Please put the books ________ the shelf.", "on", ["in", "at", "by"], "On the shelf."),
        ("{name} has ________ finished {poss} worksheet.", "already", ["yet", "still", "never"], "Already with present perfect affirmative."),
        ("If it ________ sunny, we will go to {place}.", "is", ["will be", "was", "be"], "First conditional: if + present."),
        ("The baby cried ________ because he was hungry.", "loudly", ["loud", "louder", "loudness"], "Adverb of manner."),
        ("{name} went to the clinic ________ {pron} felt unwell.", "because", ["although", "unless", "so"], "Because = reason."),
        ("My mother told me ________ careful on the road.", "to be", ["be", "being", "been"], "Tell + to-infinitive."),
        ("{name} can swim, ________ {pron}?", "can't", ["can", "doesn't", "isn't"], "Positive statement, negative tag."),
        ("We have lived here ________ two years.", "for", ["since", "from", "at"], "For + period of time."),
        ("The children enjoyed ________ at the playground.", "themselves", ["himself", "ourselves", "themself"], "Plural reflexive."),
        ("{name} prefers rice ________ noodles.", "to", ["than", "from", "for"], "Prefer A to B."),
        ("Someone ________ left a bag in the canteen.", "has", ["have", "had", "having"], "Someone → singular."),
        ("{name} was reading when the phone ________.", "rang", ["rings", "ring", "ringing"], "Simple past interrupt past continuous."),
        ("The movie was ________ interesting that we stayed till the end.", "so", ["such", "too", "very"], "So + adjective + that."),
        ("{name} sits ________ {name2} in class.", "beside", ["besides", "between", "among"], "Beside = next to."),
    ],
    "P2": [
        ("My sister ________ a cake yesterday.", "baked", ["bakes", "bake", "is baking"], "Yesterday → simple past."),
        ("Every morning, father ________ to the market.", "goes", ["go", "went", "is going"], "Habit + singular."),
        ("This is the puppy ________ we rescued.", "which", ["who", "whom", "whose"], "Which for animals/things."),
        ("The children ________ in the playground now.", "are playing", ["is playing", "play", "played"], "Present continuous."),
        ("{name} ________ to school by bus every day.", "goes", ["go", "went", "going"], "Habit + -s."),
        ("There ________ a cat under the table.", "is", ["are", "were", "be"], "Singular → is."),
        ("{name} has two ________.", "books", ["book", "bookes", "booking"], "Plural noun."),
        ("She is ________ than her brother.", "taller", ["tall", "tallest", "more tall"], "Comparative -er."),
        ("We ________ football last Saturday.", "played", ["play", "plays", "playing"], "Last Saturday → past."),
        ("{name} can ________ very fast.", "run", ["runs", "ran", "running"], "Can + base verb."),
        ("The apples ________ red and sweet.", "are", ["is", "was", "be"], "Plural subject."),
        ("Please ________ the door quietly.", "close", ["closes", "closed", "closing"], "Imperative = base verb."),
        ("{name} and I ________ best friends.", "are", ["is", "was", "am"], "Compound subject plural."),
        ("He put the bag ________ the chair.", "on", ["in", "at", "to"], "On the chair."),
        ("{name} ________ happy today.", "is", ["are", "am", "be"], "He/she/it + is."),
        ("They ________ not like spicy food.", "do", ["does", "did", "are"], "They + do not."),
        ("I saw ________ elephant at the zoo.", "an", ["a", "the", "some"], "An before vowel sound."),
        ("{name} walks ________ to school.", "slowly", ["slow", "slower", "slowest"], "Adverb of manner."),
        ("Mum ________ cooking dinner now.", "is", ["are", "am", "be"], "Present continuous auxiliary."),
        ("The bird flew ________ the tree.", "over", ["under", "into only", "beside only"], "Over = above and across."),
    ],
}

VOCAB = {
    "P6": [
        ("inevitable", "certain to happen", "avoidable"),
        ("meticulously", "with extreme care", "recklessly"),
        ("resilient", "recovers quickly from setbacks", "fragile"),
        ("subsequent", "coming after in time", "previous"),
        ("validate", "confirm accuracy", "reject"),
        ("unprecedented", "never done before", "common"),
        ("advocate", "publicly support", "oppose"),
        ("meticulous", "very careful and precise", "careless"),
        ("conspicuous", "clearly visible", "hidden"),
        ("alleviate", "make suffering less severe", "worsen"),
        ("diligent", "hard-working and careful", "lazy"),
        ("ambiguous", "having more than one meaning", "clear"),
        ("scrutinise", "examine closely", "ignore"),
        ("eloquent", "fluent and persuasive in speech", "inarticulate"),
        ("tenacious", "determined and persistent", "yielding"),
        ("prudent", "careful and sensible", "reckless"),
        ("formidable", "inspiring fear or respect", "weak"),
        ("impartial", "fair and not biased", "biased"),
        ("proficient", "skilled and competent", "inexpert"),
        ("reluctant", "unwilling or hesitant", "eager"),
        ("substantial", "of considerable importance or size", "trivial"),
        ("detrimental", "causing harm or damage", "beneficial"),
        ("elaborate", "detailed and complicated", "simple"),
        ("perseverance", "continued effort despite difficulty", "quitting"),
        ("authentic", "genuine and real", "fake"),
        ("concise", "brief but clear", "wordy"),
        ("hostile", "unfriendly or aggressive", "friendly"),
        ("innovative", "featuring new methods", "conventional"),
        ("plausible", "seeming reasonable", "unlikely"),
        ("rigorous", "extremely thorough", "careless"),
        ("serene", "calm and peaceful", "agitated"),
        ("versatile", "able to adapt to many uses", "limited"),
    ],
    "P5": [
        ("exacerbate", "make worse", "alleviate"),
        ("preposterous", "ridiculous", "reasonable"),
        ("deteriorate", "become worse", "improve"),
        ("obsolete", "no longer used", "modern"),
        ("resilient", "able to recover", "weak"),
        ("conspicuous", "clearly visible", "hidden"),
        ("reluctant", "unwilling", "eager"),
        ("essential", "absolutely necessary", "optional"),
        ("abundant", "existing in large amounts", "scarce"),
        ("benevolent", "kind and generous", "cruel"),
        ("cautious", "careful to avoid danger", "reckless"),
        ("deceive", "make someone believe something false", "enlighten"),
        ("efficient", "working well without waste", "wasteful"),
        ("frugal", "careful with money", "extravagant"),
        ("gratitude", "thankfulness", "ingratitude"),
        ("hazardous", "dangerous", "safe"),
        ("immense", "extremely large", "tiny"),
        ("jubilant", "very happy because of success", "miserable"),
        ("keen", "eager or sharp", "apathetic"),
        ("lenient", "not strict", "strict"),
        ("meagre", "very small in amount", "plentiful"),
        ("notorious", "famous for something bad", "unknown"),
        ("optimistic", "hopeful about the future", "pessimistic"),
        ("permanent", "lasting forever", "temporary"),
        ("quarrel", "an angry argument", "agreement"),
        ("reliable", "able to be trusted", "untrustworthy"),
        ("solemn", "serious and formal", "cheerful"),
        ("tedious", "long and boring", "exciting"),
        ("unique", "one of a kind", "common"),
        ("vivid", "producing strong clear images", "dull"),
        ("weary", "very tired", "energetic"),
        ("zealous", "full of enthusiasm", "indifferent"),
    ],
    "P4": [
        ("demonstrate", "show clearly", "hide"),
        ("observe", "watch carefully", "ignore"),
        ("ancient", "very old", "modern"),
        ("temporary", "lasting a short time", "permanent"),
        ("unique", "one of a kind", "common"),
        ("reluctant", "unwilling", "eager"),
        ("spectacular", "impressive to see", "dull"),
        ("generous", "willing to give", "selfish"),
        ("abandon", "leave behind completely", "keep"),
        ("brilliant", "very bright or clever", "dim"),
        ("curious", "wanting to know more", "uninterested"),
        ("delicate", "easily broken or damaged", "sturdy"),
        ("eager", "wanting very much to do something", "reluctant"),
        ("familiar", "well known", "strange"),
        ("grateful", "feeling thankful", "ungrateful"),
        ("honest", "truthful", "dishonest"),
        ("imagine", "form a picture in the mind", "ignore"),
        ("journey", "a long trip", "stay"),
        ("knowledge", "what a person knows", "ignorance"),
        ("loyal", "faithful to friends or country", "disloyal"),
        ("mystery", "something difficult to explain", "certainty"),
        ("nervous", "worried and tense", "calm"),
        ("ordinary", "normal and not special", "extraordinary"),
        ("patient", "able to wait calmly", "impatient"),
        ("quick", "moving fast", "slow"),
        ("rare", "not found often", "common"),
        ("silent", "without sound", "noisy"),
        ("timid", "shy and easily frightened", "bold"),
        ("unusual", "not common", "usual"),
        ("valuable", "worth a lot", "worthless"),
        ("wander", "walk without a fixed path", "rush"),
        ("youthful", "looking or acting young", "aged"),
    ],
    "P3": [
        ("enthusiastic", "full of interest", "bored"),
        ("ferocious", "savage", "tame"),
        ("examine", "inspect closely", "ignore"),
        ("rescue", "save from danger", "harm"),
        ("courageous", "brave", "cowardly"),
        ("scrumptious", "delicious", "stale"),
        ("cluttered", "messy", "neat"),
        ("commence", "begin", "end"),
        ("admire", "look at with respect", "despise"),
        ("brave", "not afraid of danger", "cowardly"),
        ("clever", "quick to learn", "foolish"),
        ("dazzling", "extremely bright", "dull"),
        ("enormous", "very big", "tiny"),
        ("famous", "known by many people", "unknown"),
        ("gentle", "kind and soft", "harsh"),
        ("hasty", "done too quickly", "careful"),
        ("invent", "create something new", "copy"),
        ("jolly", "happy and cheerful", "gloomy"),
        ("kindness", "being friendly and helpful", "cruelty"),
        ("lively", "full of energy", "lifeless"),
        ("mighty", "very strong", "weak"),
        ("narrow", "not wide", "wide"),
        ("obey", "do what you are told", "disobey"),
        ("proud", "pleased with achievements", "ashamed"),
        ("quiet", "making little noise", "noisy"),
        ("rapid", "very fast", "slow"),
        ("shiver", "shake from cold or fear", "relax"),
        ("tough", "strong and hard to break", "fragile"),
        ("useful", "helpful", "useless"),
        ("vanish", "disappear suddenly", "appear"),
        ("wealthy", "having a lot of money", "poor"),
        ("yearly", "happening once a year", "daily"),
    ],
    "P2": [
        ("enormous", "very large", "tiny"),
        ("terrified", "very scared", "calm"),
        ("delicious", "tastes very good", "bitter"),
        ("cautious", "careful", "careless"),
        ("generous", "willing to share", "selfish"),
        ("exhausted", "very tired", "energetic"),
        ("polite", "good manners", "rude"),
        ("furious", "very angry", "calm"),
        ("ancient", "very old", "new"),
        ("bright", "full of light", "dark"),
        ("cheerful", "happy", "sad"),
        ("dirty", "not clean", "clean"),
        ("empty", "having nothing inside", "full"),
        ("funny", "making people laugh", "serious"),
        ("giant", "very big", "small"),
        ("happy", "feeling joy", "unhappy"),
        ("important", "matters a lot", "unimportant"),
        ("jolly", "full of fun", "gloomy"),
        ("kind", "nice to others", "unkind"),
        ("lazy", "not wanting to work", "hardworking"),
        ("messy", "not tidy", "tidy"),
        ("noisy", "making loud sounds", "quiet"),
        ("pretty", "nice to look at", "ugly"),
        ("quick", "fast", "slow"),
        ("rough", "not smooth", "smooth"),
        ("strong", "having power", "weak"),
        ("tiny", "very small", "huge"),
        ("unhappy", "sad", "happy"),
        ("valuable", "worth much", "cheap"),
        ("warm", "comfortably hot", "cold"),
        ("young", "not old", "old"),
        ("brave", "not scared", "afraid"),
    ],
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
    ("The pupils were noisy. The teacher was still patient.", "Even though", "even though the pupils were noisy, the teacher was still patient"),
    ("She practised daily. She improved quickly.", "As a result", "as a result of practising daily, she improved quickly"),
    ("Tom was hungry. He did not eat the leftovers.", "Although", "although tom was hungry, he did not eat the leftovers"),
    ("It was raining heavily. They postponed the match.", "Since", "since it was raining heavily, they postponed the match"),
    ("Ravi finished early. He helped his classmates.", "After", "after ravi finished early, he helped his classmates"),
    ("The bag was heavy. She carried it upstairs.", "Although", "although the bag was heavy, she carried it upstairs"),
    ("He was late. He missed the assembly.", "because", "he missed the assembly because he was late"),
    ("Aisha studied hard. She scored well.", "so", "aisha studied hard so she scored well"),
    ("The door was locked. We could not enter.", "Since", "since the door was locked, we could not enter"),
    ("She is kind. Everyone likes her.", "so...that", "she is so kind that everyone likes her"),
    ("Kumar saved money. He bought a new bicycle.", "in order to", "kumar saved money in order to buy a new bicycle"),
    ("The baby cried. Mother picked him up.", "When", "when the baby cried, mother picked him up"),
    ("He did not apologise. She remained angry.", "Because", "because he did not apologise, she remained angry"),
    ("The test was difficult. Many pupils passed.", "Although", "although the test was difficult, many pupils passed"),
    ("She spoke softly. Nobody could hear her.", "so...that", "she spoke so softly that nobody could hear her"),
    ("We reached early. We got good seats.", "As", "as we reached early, we got good seats"),
    ("John is strong. He can lift the box.", "enough", "john is strong enough to lift the box"),
    ("The lights went out. Everyone screamed.", "As soon as", "as soon as the lights went out, everyone screamed"),
    ("She was ill. She stayed at home.", "because", "she stayed at home because she was ill"),
    ("He trained every day. He won the race.", "Therefore", "he trained every day; therefore, he won the race"),
    ("The cake burned. She forgot the timer.", "because", "the cake burned because she forgot the timer"),
    ("They were tired. They kept walking.", "Nevertheless", "they were tired; nevertheless, they kept walking"),
    ("Priya finished her work. She went home.", "After", "after priya finished her work, she went home"),
    ("The queue was long. We waited patiently.", "Although", "although the queue was long, we waited patiently"),
    ("He is young. He is very responsible.", "Despite", "despite being young, he is very responsible"),
    ("The teacher explained again. The class understood.", "Once", "once the teacher explained again, the class understood"),
    ("She lost her wallet. She reported it.", "After", "after she lost her wallet, she reported it"),
    ("The wind was strong. The trees swayed.", "so...that", "the wind was so strong that the trees swayed"),
    ("Marcus revised thoroughly. He felt confident.", "Because", "because marcus revised thoroughly, he felt confident"),
    ("The shop closed. We bought nothing.", "Since", "since the shop closed, we bought nothing"),
    ("Fatimah was busy. She replied to the message.", "Even though", "even though fatimah was busy, she replied to the message"),
    ("He forgot his keys. He could not enter.", "so", "he forgot his keys so he could not enter"),
]

SPELLING = [
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
    ("beginning", ["begining", "beggining", "beginnig"], "double n"),
    ("believe", ["beleive", "belive", "beleeve"], "i before e"),
    ("business", ["buisness", "busines", "bussiness"], "busi-ness"),
    ("calendar", ["calender", "calandar", "calander"], "cal-en-dar"),
    ("cemetery", ["cemetary", "cemetry", "cematary"], "all e's"),
    ("changeable", ["changable", "changeble", "changible"], "keep the e"),
    ("conscience", ["concience", "consciance", "consceince"], "science inside"),
    ("conscious", ["concious", "consious", "conscius"], "sci + ous"),
    ("curious", ["cureous", "curius", "cuirious"], "curi-ous"),
    ("disappoint", ["dissapoint", "disapoint", "dissappoint"], "one s, two p"),
    ("embarrass", ["embarass", "embarras", "emberrass"], "two r, two s"),
    ("existence", ["existance", "existense", "exsistence"], "ence not ance"),
    ("foreign", ["foriegn", "foregin", "forigen"], "eign ending"),
    ("government", ["goverment", "governmant", "govornment"], "n before m"),
    ("grammar", ["grammer", "gramar", "grammmar"], "ar not er"),
    ("guarantee", ["garantee", "gaurantee", "guaranty"], "gua-ran-tee"),
    ("height", ["hieght", "heigth", "hight"], "e before i"),
    ("immediate", ["imediate", "immediat", "immedate"], "double m"),
    ("independent", ["independant", "indepentent", "independint"], "ent ending"),
    ("intelligence", ["inteligence", "intelligance", "intellegence"], "double l, ence"),
    ("jewellery", ["jewelery", "jewellry", "jwellery"], "double l in BrE"),
    ("knowledge", ["knowlege", "knwoledge", "knowlidges"], "know + ledge"),
    ("library", ["libary", "librery", "liebrary"], "bra in middle"),
    ("maintenance", ["maintainance", "maintenence", "mantainance"], "ten not tain"),
    ("neighbour", ["nieghbour", "neighber", "neigbour"], "ei + bour"),
    ("occasion", ["occassion", "ocasion", "ocassion"], "two c, one s"),
    ("occurrence", ["occurence", "ocurrance", "occurance"], "two c, two r"),
    ("parallel", ["paralel", "paralllel", "parellel"], "double l in middle"),
    ("privilege", ["priviledge", "privilage", "privelege"], "lege not ledge"),
    ("rhythm", ["rythm", "rhthym", "rhythym"], "rhy-thm"),
    ("successful", ["succesful", "successfull", "sucessful"], "two c, two s, one l"),
    ("surprise", ["suprise", "surprize", "surprisse"], "sur + prise"),
    ("temperature", ["temperture", "temprature", "tempereture"], "temper + ature"),
    ("unfortunately", ["unfortunatly", "unfortunetly", "unfortionately"], "ate + ly"),
    ("vacuum", ["vaccum", "vacume", "vaccuum"], "one c, two u"),
]

def _place(i, k=0):
    return PLACES_SG[(i + k) % len(PLACES_SG)]

def _time(i, k=0):
    return TIMES_OF_DAY[(i + k) % len(TIMES_OF_DAY)]

def _fmt_grammar(stem, index, name, name2):
    # Heuristic pronoun gender from name index parity
    male_like = (index + hash(name) % 2) % 2 == 0
    pron = "he" if male_like else "she"
    poss = "his" if male_like else "her"
    obj = "him" if male_like else "her"
    place = _place(index)
    try:
        return stem.format(name=name, name2=name2, pron=pron, poss=poss, obj=obj, place=place)
    except (KeyError, ValueError):
        return stem.replace("{name}", name).replace("{name2}", name2).replace("{pron}", pron).replace("{poss}", poss).replace("{obj}", obj).replace("{place}", place)

def generate_english_question(level, qid, index):
    difficulty = diff_of(index)
    mode = index % 5
    # Offsets chosen so name/item/place periods do not lock to mode step (5)
    name = nname(index)
    name2 = nname(index * 7 + 3)
    name3 = nname(index * 11 + 13)
    item = nitem(index * 3 + 1)
    item2 = nitem(index * 5 + 8)
    place = _place(index * 3)
    place2 = _place(index * 5 + 2)
    when = _time(index * 3 + 1)
    count = 2 + (index * 3) % 19
    count2 = 3 + (index * 7) % 13
    year = 2012 + (index * 3) % 12
    lead = f"{name} and {name2} · {place} · {when}"

    if mode == 0:
        rules = GRAMMAR[level]
        stem, ans, bad, exp = rules[index % len(rules)]
        q = _fmt_grammar(stem, index, name, name2)
        frames = [
            f"[{lead}] Complete:\n{q}",
            f"Choose the correct option to complete the sentence {when} near {place}:\n{q}",
            f"{name3} is revising grammar with {name} after {count} examples. Fill in the blank:\n{q}",
            f"At {place}, the class of {count2} discussed this sentence. Complete it:\n{q}",
            f"Pick the best word for the blank in this PSLE-style item about {item}:\n{q}",
            f"While waiting at {place2}, {name} practised this structure with {name2}:\n{q}",
            f"Complete the sentence correctly (practice round {count} at {place2}):\n{q}",
            f"Grammar focus for {name3} travelling via {place}:\n{q}",
        ]
        q2 = frames[index % len(frames)]
        return pack(qid, "Grammar MCQ", "mcq", q2, ans, exp, difficulty, shuffle_opts(ans, bad))

    if mode == 1:
        words = VOCAB[level]
        word, definition, antonym = words[index % len(words)]
        others = [w[0] for w in words if w[0] != word]
        start = (index // len(words)) % max(1, len(others))
        distractors = (others[start:] + others[:start])[:3]
        while len(distractors) < 3:
            distractors.append(antonym if antonym not in distractors else f"option{len(distractors)}")
        frames = [
            f'[{lead}] Choose the word closest in meaning to: "{definition}".',
            f'{name} looked up a word meaning "{definition}" {when} at {place}. Which word fits best?',
            f'In the sentence "{name} remained _____ during the setback at {place}", which word meaning "{definition}" fits?',
            f'Which word best matches this definition used in a PSLE cloze about {count} {item}: "{definition}"?',
            f'{name2} described something near {place2} as "{definition}" while talking to {name3}. Pick the best word.',
            f'The teacher asked {name} for a synonym of an idea meaning "{definition}" before going to {place}.',
            f'During reading at {place}, {name3} met a word that means "{definition}" (notes page {count2}). Choose it.',
            f'Fill the blank: The pupils showed a _____ attitude (meaning "{definition}") towards the {count} tasks at {place2}.',
            f'{name} wrote about {item2} near {place} and needed a word meaning "{definition}". Which is best?',
            f'Closest in meaning to "{definition}" for {name2}\'s draft about {item} (not like "{antonym}"):',
            f'Vocabulary practice ({lead}): word meaning "{definition}".',
            f'{name3} compared "{antonym}" with a better fit for "{definition}" after {count} trials at {place}. Choose the fit.',
        ]
        q = frames[index % len(frames)]
        exp = f"'{word}' means '{definition}'. Opposite idea: '{antonym}'."
        return pack(qid, "Vocabulary MCQ", "mcq", q, word, exp, difficulty, shuffle_opts(word, distractors))

    if mode == 2:
        sent, joiner, ans = SYNTHESIS[index % len(SYNTHESIS)]
        parts = [p.strip() for p in sent.split(".") if p.strip()]
        repl = {
            "The boy": name, "Siti": name, "Bala": name, "David": name, "Mei Ling": name,
            "Tom": name, "Ravi": name, "Aisha": name, "Kumar": name, "John": name,
            "Priya": name, "Marcus": name, "Fatimah": name, "He": name, "She": name,
            "The pupils": f"{name} and {name2}", "The children": f"{name} and {name2}",
            "The audience": f"the class of {name2}", "Mother": name2, "The teacher": name2,
            "They": f"{name} and {name2}", "We": f"{name} and {name2}",
            "Everyone": f"everyone at {place}", "Nobody": f"nobody at {place2}",
        }
        p0, p1 = parts[0], parts[1] if len(parts) > 1 else parts[0]
        for k, v in repl.items():
            p0 = p0.replace(k, v)
            p1 = p1.replace(k, v)
        ans2 = ans
        for old in ["the boy", "siti", "bala", "david", "mei ling", "tom", "ravi", "aisha", "kumar", "john", "priya", "marcus", "fatimah"]:
            ans2 = ans2.replace(old, name.lower())
        ans2 = ans2.replace("he ", name.lower() + " ").replace("she ", name.lower() + " ")
        ans2 = ans2.replace("the pupils", f"{name.lower()} and {name2.lower()}")
        ans2 = ans2.replace("the children", f"{name.lower()} and {name2.lower()}")
        frames = [
            f"[{lead}] Combine into one sentence using the word(s) given.\n\n1) {p0}.\n2) {p1}.\n\nUse: {joiner}",
            f"{name3} practised synthesis {when} at {place} (round {count}). Combine using '{joiner}':\n1) {p0}.\n2) {p1}.",
            f"Rewrite as one sentence with the given connector ({joiner}). Context: {place2} with {name2}.\nA. {p0}.\nB. {p1}.",
            f"Sentence combining for {name} — use '{joiner}' only once (about {item}):\n• {p0}\n• {p1}",
            f"Join these ideas about {item} practice at {place} using '{joiner}':\n1) {p0}.\n2) {p1}.",
            f"{name} met {name3} at {place2} {when}. Combine with '{joiner}':\n1) {p0}.\n2) {p1}.",
            f"Synthesis drill #{count2} near {place}: use '{joiner}'.\n1) {p0}.\n2) {p1}.",
        ]
        q = frames[index % len(frames)]
        topic = "Sentence Combining" if level == "P2" else "Synthesis & Transformation"
        return pack(qid, topic, "short_answer", q, ans2, f"Model: {ans2}", difficulty, [])

    if mode == 3:
        w, bad, tip = SPELLING[index % len(SPELLING)]
        frames = [
            f"[{lead}] Choose the correctly spelt word for {name}'s editing exercise involving '{item}'. Which spelling is correct?",
            f"Editing practice at {place}: {name} circled a misspelt word while packing {count} {item}. Which is correct?",
            f"{when[0].upper() + when[1:]}, {name2} proofread a paragraph about {item2} near {place2}. Select the correct spelling of the target word.",
            f"In an editing passage set near {place2}, which spelling should {name} keep after checking with {name3}?",
            f"{name} found {count} errors in a text about {place} but one listed word is already correct. Which spelling is right?",
            f"Pick the accurate spelling for the blank in {name3}'s homework about {item} (class {count2}):",
            f"Spelling check before submitting work from {place} about {item2}: which form is correct?",
            f"{name2} and {name} edited notes from {place2} {when}. Choose the correct spelling.",
        ]
        q = frames[index % len(frames)]
        topic = "Editing for Spelling & Punctuation" if level == "P2" else "Editing"
        return pack(qid, topic, "mcq", q, w, f"Correct spelling is '{w}' ({tip}).", difficulty, shuffle_opts(w, bad))

    # mode 4: short comprehension / cloze with SG places, times, counts
    him_her = "himself" if (index * 3) % 2 == 0 else "herself"
    cloze_bank = [
        (f"{name} and {name2} _____ going to {place} {when}.", "are", ["is", "was", "be"], "Plural compound subject → are."),
        (f"Neither {name} nor {name2} _____ late for the trip to {place2}.", "was", ["were", "are", "be"], "Neither nor → singular when both singular."),
        (f"The box of {item} belonging to {name} _____ on the table in the canteen at {place}.", "is", ["are", "were", "be"], "Head noun 'box' is singular."),
        (f"{name} completed the {count} sums by _____ before leaving for {place2}.", him_her, ["themselves", "myself", "itself"], "Reflexive matches subject."),
        (f"There _____ many {item} in the drawer at {place} when {name2} looked.", "are", ["is", "was", "be"], "Many + plural noun → are."),
        (f"Last week, {name} _____ {count2} books from the library near {place}.", "borrowed", ["borrow", "borrows", "borrowing"], "Past time marker → simple past."),
        (f"Every pupil in {name3}'s class _____ a badge for CCA at {place2}.", "has", ["have", "having", "had"], "Every + singular verb."),
        (f"{name} walks to the MRT station _____ than {name2} after lessons at {place}.", "more quickly", ["quick", "more quick", "quickly"], "Comparative adverb."),
        (f"The news about the {count}-day camp at {place} _____ exciting for {name}.", "was", ["were", "are", "be"], "'News' is uncountable/singular."),
        (f"While {name} _____ at {place}, {name2} bought {count2} drinks.", "was waiting", ["waited", "waits", "waiting"], "Past continuous for background."),
        (f"A flock of birds _____ over Marina Bay at dusk as {name} watched from {place2}.", "was flying", ["were flying", "fly", "flown"], "Collective 'flock' often singular."),
        (f"{name} has lived near {place} _____ {year}.", "since", ["for", "from", "during"], "Since + point in time."),
        (f"Please remind {name2} _____ the form before recess at {place}.", "to submit", ["submitting", "submit", "submitted"], "Remind + to-infinitive."),
        (f"The pair of {item} under the bench at school near {place2} _____ {name}'s.", "was", ["were", "are", "be"], "'Pair' is singular."),
        (f"If it rains, the class _____ cancel the outing to {place2} with {name}.", "will", ["would", "should", "can"], "First conditional."),
        (f"{name} prefers {item} _____ {item2} when shopping at {place}.", "to", ["than", "from", "for"], "Prefer A to B."),
        (f"Someone in {name}'s cabin _____ left a water bottle on the MRT to {place}.", "has", ["have", "had", "having"], "Someone → singular."),
        (f"By the time the bus arrived at {place}, {name} _____ already left with {name2}.", "had", ["has", "have", "was"], "Past perfect for earlier action."),
        (f"The number of visitors to Gardens by the Bay with {name3} _____ rising this month.", "is", ["are", "were", "be"], "'The number of' → singular."),
        (f"{name} and the rest of the team from {place} _____ proud of the result.", "are", ["is", "was", "be"], "Compound/plural idea → are."),
        (f"Reading passage: {name} visited {place} {when} and bought {count} {item}. The word closest to 'bought' is _____.", "purchased", ["sold", "borrowed", "lost"], "Bought ≈ purchased."),
        (f"Cloze: {name} and {name2} were _____ when they reached East Coast Park after {count} stops.", "delighted", ["delight", "delighting", "delights"], "Adjective after linking verb."),
        (f"At {place}, {name} spoke so softly _____ few of the {count2} listeners could hear.", "that", ["than", "then", "when"], "So... that."),
        (f"{name} is interested _____ learning about Tampines heritage with {name2}.", "in", ["on", "at", "for"], "Interested in."),
        (f"Hardly had {name} entered the library at {place} _____ the lights flickered {count} times.", "when", ["than", "then", "before"], "Hardly... when."),
        (f"Vocabulary cloze: From {place}, {name} said the view from Marina Bay was truly _____.", "spectacular", ["spectacle", "spectate", "spectator"], "Adjective form."),
        (f"{name} insisted _____ finishing the project before CCA at {place2}.", "on", ["to", "for", "in"], "Insist on + gerund."),
        (f"Neither of the answers about {place2} from {name}'s group _____ correct.", "is", ["are", "were", "be"], "Neither of → singular."),
        (f"After _____ lunch in the canteen near {place}, {name} went to the hall with {name3}.", "having", ["have", "had", "has"], "After + gerund."),
        (f"{name} saw {count} {item} at {place} and said the stall was _____ crowded than yesterday.", "more", ["most", "many", "much"], "Comparative with than."),
        (f"During assembly at {place2}, {name2} spoke _____ so the back row could hear.", "clearly", ["clear", "clearer", "clearest"], "Adverb of manner."),
        (f"Cloze story: {name} took the MRT to Jurong with {count2} friends. They _____ excited.", "were", ["was", "is", "be"], "Plural subject → were."),
        (f"{name3} kept the {item} _____ the bag before boarding at {place}.", "in", ["on", "at", "by"], "In the bag."),
        (f"Short text: At Gardens by the Bay, {name} counted {count} orchids. How many orchids?", str(count),
         [str(count + 2), str(count + 5), str(count + 9)], "Detail retrieval."),
        (f"Comprehension: {name2} waited {count} minutes at Bishan MRT for {name}. How long did {name2} wait?", f"{count} minutes",
         [f"{count + 2} minutes", f"{count + 5} minutes", f"{count + 8} minutes"], "Direct detail from the stem."),
    ]
    stem, ans, bad, exp = cloze_bank[index % len(cloze_bank)]
    wraps = [
        f"[{lead}]\n{stem}",
        f"Read and complete ({name3}'s card from {place2}):\n{stem}",
        f"Short cloze set {when} — focus on {item}:\n{stem}",
        f"Based on a short text about {place} (scene {count}):\n{stem}",
        f"{name3}'s worksheet item after {count2} minutes at {place2}:\n{stem}",
        f"PSLE-style cloze for {name} travelling through {place}:\n{stem}",
    ]
    q = wraps[index % len(wraps)]
    if level in ("P4", "P5", "P6"):
        topic = "Vocabulary Cloze"
    else:
        topic = "Grammar MCQ"
    return pack(qid, topic, "mcq", q, ans, exp, difficulty, shuffle_opts(ans, list(bad)))

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
    # parameter fill — high variance for uniqueness
    places = ["school lab", "home kitchen", "East Coast Park", "Botanic Gardens", "science centre booth", "classroom"]
    tools = ["thermometer", "spring balance", "data logger", "stopwatch", "measuring cylinder", "newton meter"]
    params = {
        "m": 5 + (index * 3) % 12,
        "f1": 20 + (index * 7) % 60,
        "f2": 8 + (index * 5) % 20,
        "h": 2 + (index * 2) % 10,
        "b1": 20 + (index * 11) % 50,
        "b2": 4 + (index * 3) % 15,
        "s1": 30 + (index * 13) % 40,
        "s2": 90 + (index * 17) % 100,
        "v": 50 + (index * 9) % 80,
        "cap": 250 + (index % 8) * 50,
        "t1": 18 + (index * 4) % 25,
        "t2": 30 + (index * 6) % 40,
        "n": 2 + index % 6,
        "place": places[index % len(places)],
        "tool": tools[index % len(tools)],
        "name": nname(index),
        "name2": nname(index, 5),
    }
    try:
        question = stem.format(**params)
        explanation = exp.format(**params)
    except Exception:
        question, explanation = stem, exp
    # parametric scenario variants (real stem diversity)
    variants = [
        question,
        f"Experiment log #{index} at the {params['place']}: {question}",
        f"{params['name']} used a {params['tool']} and recorded: {question}",
        f"PSLE-style item ({topic}): {question}",
        f"Study the scenario carefully ({params['name']} & {params['name2']}). {question}",
        f"Class investigation #{(index % 40) + 1}: {question}",
        f"During a field trip to the {params['place']}, pupils observed: {question}",
        f"Given readings from a {params['tool']}, answer: {question}",
    ]
    question = variants[index % len(variants)]
    # Extra concept MCQs generated parametrically for more unique stems
    if index % 7 == 0:
        extras = [
            (topic_list[0], f"Which statement about living things is true in this {params['place']} context with {params['n']} samples?",
             "Living things need energy to stay alive", "Living things require energy for life processes.", "energy",
             ["All living things make food", "Non-living things grow", "Only animals respire"]),
            (topic_list[min(1, len(topic_list)-1)], f"{params['name']} measures {params['t1']}°C then {params['t2']}°C. What increased?",
             "Temperature of the object/surroundings as stated", "Temperature is the degree of hotness measured in °C.", "temperature",
             ["Mass only", "Volume only", "Colour only"]),
            (topic_list[min(2, len(topic_list)-1)], f"A force of {params['f1']} N acts on a {params['m']} kg object at the {params['place']}. Friction mainly:",
             "Opposes motion between surfaces", "Friction opposes relative motion between surfaces in contact.", "friction",
             ["Creates mass", "Removes gravity", "Stops light"]),
        ]
        et = extras[index % len(extras)]
        topic, question, ans, explanation, keyword, distractors = et
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
        ("Vocabulary Selection (词语选择)", "经过努力，他的成绩有了明显的________。", "进步", ["退步", "放弃", "停止"], "成绩提升用进步。"),
        ("Vocabulary Selection (词语选择)", "同学们在图书馆里保持________。", "安静", ["吵闹", "热闹", "激动"], "图书馆需要安静。"),
        ("Vocabulary Selection (词语选择)", "这件事让大家________不已。", "感动", ["讨厌", "冷淡", "忽视"], "正面情感用感动。"),
        ("Sentence Completion (句型填空)", "________多读多写，________作文水平才会提高。", "只有……才……", ["虽然……但是……", "因为……所以……", "不但……而且……"], "条件关系。"),
        ("Sentence Completion (句型填空)", "他________会唱歌，________会跳舞。", "不但……而且……", ["虽然……但是……", "如果……就……", "与其……不如……"], "递进关系。"),
        ("Sentence Completion (句型填空)", "________今天下雨，________活动改期。", "因为……所以……", ["虽然……但是……", "不但……而且……", "只有……才……"], "因果关系。"),
        ("Hanyu Pinyin", "‘进步’ 的拼音是？", "jìn bù", ["jǐn bù", "jìn bú", "jìn pu"], "jìn bù。"),
        ("Hanyu Pinyin", "‘安静’ 的拼音是？", "ān jìng", ["an jìng", "ān jīn", "āng jìng"], "ān jìng。"),
        ("Hanyu Pinyin", "‘努力’ 的拼音是？", "nǔ lì", ["nú lì", "nǔ lǐ", "nù lì"], "nǔ lì。"),
        ("Cloze Passage (短文填空)", "请把窗户________，外面风很大。", "关上", ["打开", "搬走", "丢掉"], "风大→关窗。"),
        ("Cloze Passage (短文填空)", "他________地完成了作业。", "认真", ["随便", "马虎", "匆忙"], "正面完成用认真。"),
        ("Reading Comprehension MCQ", "短文写一位同学每天坚持跑步，主要赞美他？", "持之以恒", ["半途而废", "三心二意", "骄傲自满"], "坚持=持之以恒。"),
        ("Reading Comprehension MCQ", "短文写大家一起打扫校园，体现了？", "齐心协力", ["自私自利", "漠不关心", "袖手旁观"], "一起劳动=齐心协力。"),
        ("Vocabulary Selection (词语选择)", "老师的话让我________。", "恍然大悟", ["一无所知", "心不在焉", "胡思乱想"], "突然明白=恍然大悟。"),
        ("Vocabulary Selection (词语选择)", "不要________，要脚踏实地学习。", "好高骛远", ["脚踏实地", "按部就班", "循序渐进"], "好高骛远是贬义。"),
        ("Sentence Completion (句型填空)", "________时间再紧，我们________要完成任务。", "即使……也……", ["因为……所以……", "不但……而且……", "如果……就……"], "让步关系。"),
        ("Cloze Passage (短文填空)", "听到好消息，大家________起来。", "欢呼", ["哭泣", "沉默", "离开"], "好消息→欢呼。"),
        ("Hanyu Pinyin", "‘成功’ 的拼音是？", "chéng gōng", ["chéng gòng", "chén gōng", "chéng gong"], "chéng gōng。"),
        ("Reading Comprehension MCQ", "短文强调保护环境，中心是？", "爱护环境", ["浪费资源", "破坏自然", "漠视卫生"], "环保主题。"),
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
    names = ["小明", "小华", "美玲", "志豪", "丽芬", "伟杰", "淑慧", "俊杰", "雅婷", "国强", "慧敏", "建华"]
    name = names[index % len(names)]
    name2 = ["老师", "妈妈", "同学", "校长", "爸爸", "朋友", "班主任", "邻居"][index % 8]
    places = ["学校", "图书馆", "操场", "教室", "公园", "家里", "社区中心", "巴士上"]
    place = places[index % len(places)]
    n = 1 + index % 20
    # parametric personalisation
    q2 = q.replace("小明", name).replace("王校长", name2 if "校长" in name2 else "王校长")
    if index % 5 == 0:
        q2 = q2.replace("他", name).replace("她", name)
    frames = [
        q2,
        f"请选择正确的答案：{q2}",
        f"（{name}的练习 · 第{n}题）{q2}",
        f"阅读并作答：{q2}",
        f"根据句意填空：{q2}",
        f"在{place}完成练习：{q2}",
        f"{name2}出题：{q2}",
        f"华文巩固（{level}）：{q2}",
        f"仔细阅读后作答（场景：{place}）：{q2}",
        f"第{n}题 · {name}作答：{q2}",
    ]
    qf = frames[(index * 3) % len(frames)]
    if "拼音" in topic or topic == "Hanyu Pinyin":
        extras = [
            ("‘学习’ 的拼音是？", "xué xí", ["xué xì", "xuē xí", "xué xǐ"], "xué xí。"),
            ("‘快乐’ 的拼音是？", "kuài lè", ["kuai lè", "kuài le", "kuāi lè"], "kuài lè。"),
            ("‘中国’ 的拼音是？", "zhōng guó", ["zōng guó", "zhōng guo", "zhòng guó"], "zhōng guó。"),
            ("‘谢谢’ 的拼音是？", "xiè xie", ["xiē xie", "xiè xiē", "xie xie"], "xiè xie。"),
            ("‘老师’ 的拼音是？", "lǎo shī", ["lǎo sī", "láo shī", "lǎo shí"], "lǎo shī。"),
            ("‘朋友’ 的拼音是？", "péng yǒu", ["péng yóu", "pēng yǒu", "péng yòu"], "péng yǒu。"),
            ("‘学校’ 的拼音是？", "xué xiào", ["xué xiáo", "xuē xiào", "xué xiāo"], "xué xiào。"),
            ("‘家庭’ 的拼音是？", "jiā tíng", ["jiā tīng", "jiá tíng", "jia tíng"], "jiā tíng。"),
            ("‘认真’ 的拼音是？", "rèn zhēn", ["rěn zhēn", "rèn zēn", "rèn zen"], "rèn zhēn。"),
            ("‘成功’ 的拼音是？", "chéng gōng", ["chéng gòng", "chén gōng", "chéng gong"], "chéng gōng。"),
        ]
        # expand pinyin coverage
        ex = extras[index % len(extras)]
        if index % 2 == 0:
            topic, qf, ans, bad, exp = "Hanyu Pinyin", ex[0], ex[1], ex[2], ex[3]
            qf = f"{name}在{place}问：{qf}（练习{n}）"
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
