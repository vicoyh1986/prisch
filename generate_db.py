import os
import json
import random

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Common Singaporean Names representing our multicultural society
NAMES = [
    "Ali", "Bala", "Mei Ling", "Wei Jie", "Siti", "Kavitha", "David", "Sarah",
    "Fatimah", "Gopal", "Huiling", "Kumar", "Nurul", "Ravi", "Junjie",
    "Sanjay", "Ahmad", "Chloe", "Zhi Hao", "Xinyi", "Desmond", "Yusof", "Amira", "Brandon"
]

ITEMS = [
    "marbles", "pencils", "stickers", "stamps", "sweets", "toy cars", "colored beads",
    "books", "erasers", "rulers", "paper clips", "balloons", "cards", "cupcakes", "cookies"
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

def generate_math_question(level, q_id, index):
    difficulty = "Easy" if index % 3 == 0 else ("Medium" if index % 3 == 1 else "Hard")
    topics = TOPICS["mathematics"][level]
    topic = topics[index % len(topics)]
    
    name1, name2 = NAMES[index % len(NAMES)], NAMES[(index + 1) % len(NAMES)]
    item1 = ITEMS[index % len(ITEMS)]
    
    question_text = ""
    options = []
    correct_ans = ""
    explanation = ""
    q_type = "mcq"
    heuristic_id = "constant-part"
    bar_model = None

    if level == "P6":
        if topic == "Algebra":
            heuristic_id = "algebra"
            coeff = (index % 5) + 2
            const = (index % 12) + 3
            val = (index % 4) + 2
            expr_type = index % 3

            if expr_type == 0:
                added_coeff = (index % 3) + 1
                question_text = f"Simplify the algebraic expression: {coeff}x + {const} + {added_coeff}x - {(index % const) + 1}"
                ans_coeff = coeff + added_coeff
                ans_const = const - ((index % const) + 1)
                correct_ans = f"{ans_coeff}x + {ans_const}"
                options = [correct_ans, f"{ans_coeff}x - {ans_const}", f"{coeff}x + {const}", f"{ans_coeff + 1}x + {ans_const + 1}"]
                explanation = f"1. Group the 'x' terms together: {coeff}x + {added_coeff}x = {ans_coeff}x.\n2. Group the constants together: {const} - {(index % const) + 1} = {ans_const}.\n3. Combining them yields: {correct_ans}."
            elif expr_type == 1:
                q_val = coeff * val + const
                question_text = f"Find the value of {coeff}w + {const} when w = {val}."
                correct_ans = str(q_val)
                options = [correct_ans, str(coeff + const), str(coeff * (val + const)), str(q_val - 3)]
                explanation = f"Substitute w = {val} into the algebraic expression:\n{coeff} × {val} + {const} = {coeff * val} + {const} = {q_val}."
            else:
                question_text = f"{name1} had {coeff}m stickers. {name2} had twice as many stickers as {name1}. If they shared them and gave {const} stickers away, express the remaining stickers in terms of m."
                correct_ans = f"{coeff * 3}m - {const}"
                options = [correct_ans, f"{coeff * 2}m - {const}", f"{coeff * 3}m + {const}", f"{coeff * 2}m + {const}"]
                explanation = f"1. {name1}'s stickers = {coeff}m.\n2. {name2}'s stickers = 2 × {coeff}m = {coeff * 2}m.\n3. Total stickers at first = {coeff}m + {coeff * 2}m = {coeff * 3}m.\n4. Subtract the stickers given away: {correct_ans}."

        elif topic == "Ratio":
            scenario_type = index % 3
            if scenario_type == 0:
                heuristic_id = "constant-difference"
                diff = ((index % 5) + 4) * 6
                son_age_future_units = 1
                father_age_future_units = 3
                unit_diff = father_age_future_units - son_age_future_units
                one_unit_val = diff // unit_diff
                years_in_future = (index % 4) + 2
                son_age_now = one_unit_val - years_in_future

                question_text = f"The difference in age between {name1}'s father and {name1} is {diff} years. In {years_in_future} years, the father's age will be 3 times {name1}'s age. How old is {name1} now?"
                correct_ans = f"{son_age_now} years old"
                options = [correct_ans, f"{son_age_now + years_in_future} years old", f"{son_age_now + diff} years old", f"{son_age_now - 2} years old"]
                explanation = f"1. Age difference is constant: Father is always {diff} years older.\n2. In {years_in_future} years, the ratio Father : {name1} is 3:1. The ratio difference is 2 units.\n3. 2 units = {diff} years. Therefore, 1 unit = {diff} ÷ 2 = {one_unit_val} years (this is {name1}'s age in {years_in_future} years).\n4. {name1}'s age now = {one_unit_val} - {years_in_future} = {son_age_now} years old."
                bar_model = {
                    "title": f"Constant Difference: {diff} Years",
                    "bars": [
                        {"name": "Father", "units": 3, "color": "#4facfe"},
                        {"name": name1, "units": 1, "color": "#00f2fe"}
                    ],
                    "bracketText": f"2 units difference = {diff} years. 1 unit = {one_unit_val} years."
                }
            elif scenario_type == 1:
                heuristic_id = "constant-part"
                u1, u2 = 2, 3
                u3, u4 = 4, 5
                multiplier = (index % 5) + 3
                red_at_first = u1 * multiplier
                blue_at_first = u2 * multiplier
                added_red = (u3 * blue_at_first // u4) - red_at_first

                question_text = f"A container had red and blue beads in the ratio {u1}:{u2}. After adding {added_red} red beads, the ratio of red beads to blue beads became {u3}:{u4}. How many blue beads were there?"
                correct_ans = str(blue_at_first)
                options = [correct_ans, str(red_at_first), str(blue_at_first + added_red), str(blue_at_first - 5)]
                explanation = f"1. Blue beads do not change. Make Blue units equal in both ratios: LCM of {u2} and {u4} is 12.\n2. Initial ratio Red : Blue = {u1}:{u2} = 8:12.\n3. New ratio Red : Blue = {u3}:{u4} = 15:12.\n4. Change in Red units = 15 - 8 = 7 units.\n5. 7 units = {added_red} beads. 1 unit = {added_red // 7} beads.\n6. Blue beads = 12 units = 12 × {added_red // 7} = {blue_at_first} beads."
                bar_model = {
                    "title": "Constant Part (Blue Beads Constant)",
                    "bars": [
                        {"name": "Red (After)", "units": 5, "color": "#ff6b6b", "highlightUnits": 2, "highlightColor": "#ffd166"},
                        {"name": "Blue (Fixed)", "units": 4, "color": "#4facfe"}
                    ],
                    "bracketText": f"Blue units are unchanged. Added Red = {added_red} beads."
                }
            else:
                heuristic_id = "constant-total"
                r1, r2, r3 = 2, 3, 5
                unit_val = (index % 8) + 4
                v1, v2, v3 = r1 * unit_val, r2 * unit_val, r3 * unit_val
                question_text = f"{name1}, {name2}, and Siti shared ${r1*unit_val + r2*unit_val + r3*unit_val} in the ratio {r1}:{r2}:{r3}. How much more money did Siti receive than {name1}?"
                diff_val = v3 - v1
                correct_ans = f"${diff_val}"
                options = [correct_ans, f"${v3}", f"${v1}", f"${v2}"]
                explanation = f"1. Total units = {r1} + {r2} + {r3} = {r1+r2+r3} units.\n2. Total money = ${v1+v2+v3}. Therefore, 1 unit = ${v1+v2+v3} ÷ {r1+r2+r3} = ${unit_val}.\n3. Difference between Siti (5 units) and {name1} (2 units) = 3 units.\n4. Difference in money = 3 × ${unit_val} = ${diff_val}."
                bar_model = {
                    "title": "Ratio Model (Sharing)",
                    "bars": [
                        {"name": name1, "units": r1, "color": "#00f2fe"},
                        {"name": name2, "units": r2, "color": "#4facfe"},
                        {"name": "Siti", "units": r3, "color": "#a855f7"}
                    ],
                    "bracketText": f"Total = ${v1+v2+v3}. 1 unit = ${unit_val}."
                }

        elif topic == "Percentage":
            heuristic_id = "number-value"
            price = ((index % 8) + 5) * 100
            pct_disc = 20 if index % 2 == 0 else 15
            disc_amount = price * pct_disc // 100
            disc_price = price - disc_amount
            gst_pct = 9
            gst_amount = round(disc_price * gst_pct / 100, 2)
            final_price = round(disc_price + gst_amount, 2)

            question_text = f"The usual price of a television set was ${price}. During a store promotion, {name1} bought it at a {pct_disc}% discount. A GST of {gst_pct}% was then applied on the discounted price. Find the final price {name1} paid."
            correct_ans = f"${final_price:.2f}"
            options = [correct_ans, f"${disc_price:.2f}", f"${price + (price*gst_pct//100):.2f}", f"${price - disc_amount:.2f}"]
            explanation = f"1. Discount amount = {pct_disc}% of ${price} = ${disc_amount}.\n2. Discounted price = ${price} - ${disc_amount} = ${disc_price}.\n3. GST on discounted price = {gst_pct}% of ${disc_price} = ${gst_amount}.\n4. Final price = ${disc_price} + ${gst_amount} = ${final_price:.2f}."

        elif topic == "Speed":
            heuristic_id = "speed-circles"
            s1 = (index % 4) * 10 + 60
            s2 = (index % 3) * 10 + 50
            hours = (index % 3) + 2
            dist = (s1 + s2) * hours
            
            question_text = f"Town A and Town B are {dist} km apart. At 0800, a truck left Town A for Town B at an average speed of {s1} km/h. At the same time, a van left Town B for Town A at an average speed of {s2} km/h. At what time did they pass each other?"
            meeting_time = 8 + hours
            correct_ans = f"{meeting_time:02d}00"
            options = [correct_ans, f"{(meeting_time-1):02d}00", f"{(meeting_time+1):02d}00", "1200"]
            explanation = f"1. Combined speed of both vehicles = {s1} + {s2} = {s1+s2} km/h.\n2. Time taken to meet = Total Distance ÷ Combined Speed = {dist} ÷ {s1+s2} = {hours} hours.\n3. Meeting time = 0800 + {hours} hours = {correct_ans}."
            bar_model = {
                "title": f"Speed: Opposite Directions ({dist} km)",
                "bars": [
                    {"name": "Truck", "units": 4, "color": "#00f2fe", "totalLabel": f"{s1} km/h"},
                    {"name": "Van", "units": 3, "color": "#ffd166", "totalLabel": f"{s2} km/h"}
                ],
                "bracketText": f"Combined Speed = {s1+s2} km/h. Time = {hours} hrs."
            }

        elif topic == "Circles" or topic == "Area & Perimeter of Composite Figures":
            heuristic_id = "speed-circles"
            side = ((index % 5) + 2) * 7
            quad_area = 22 * side * side // (7 * 4)
            tri_area = side * side // 2
            shaded = quad_area - tri_area

            question_text = f"The figure shows a quadrant of radius {side} cm inside a square. A right-angled triangle with a height of {side} cm is drawn inside it. Find the area of the shaded region. (Take π = 22/7)"
            correct_ans = f"{shaded} cm²"
            options = [correct_ans, f"{quad_area} cm²", f"{tri_area} cm²", f"{shaded + 14} cm²"]
            explanation = f"1. Area of quadrant = 1/4 × π × r² = 1/4 × 22/7 × {side} × {side} = {quad_area} cm².\n2. Area of unshaded triangle = 1/2 × base × height = 1/2 × {side} × {side} = {tri_area} cm².\n3. Shaded Area = Quadrant Area - Triangle Area = {quad_area} - {tri_area} = {shaded} cm²."
        
        else:
            val_a = (index % 5) + 4
            question_text = f"A solid is made of {val_a} identical cubes of side 3 cm. Find the total volume of the composite solid."
            vol = val_a * (3 * 3 * 3)
            correct_ans = f"{vol} cm³"
            options = [correct_ans, f"{val_a * 9} cm³", f"{vol - 27} cm³", f"{vol + 27} cm³"]
            explanation = f"1. Volume of 1 cube = 3 × 3 × 3 = 27 cm³.\n2. Volume of {val_a} cubes = {val_a} × 27 = {vol} cm³."

    elif level == "P5":
        if topic == "Ratio":
            heuristic_id = "constant-total"
            u1, u2 = (index % 3) + 2, (index % 3) + 5
            mult = (index % 10) + 5
            tot = (u1 + u2) * mult
            v1 = u1 * mult
            v2 = u2 * mult
            question_text = f"{name1} and {name2} shared ${tot} in the ratio {u1}:{u2}. How much money did {name2} receive?"
            correct_ans = f"${v2}"
            options = [correct_ans, f"${v1}", f"${tot}", f"${v2 - 5}"]
            explanation = f"1. Total units = {u1} + {u2} = {u1+u2} units.\n2. {u1+u2} units = ${tot}. Therefore, 1 unit = ${tot} ÷ {u1+u2} = ${mult}.\n3. {name2} has {u2} units = {u2} × ${mult} = ${v2}."
            bar_model = {
                "title": f"Ratio Model (${tot})",
                "bars": [
                    {"name": name1, "units": u1, "color": "#00f2fe"},
                    {"name": name2, "units": u2, "color": "#4facfe"}
                ],
                "bracketText": f"{u1+u2} units = ${tot}. 1 unit = ${mult}."
            }
        elif topic == "Average":
            heuristic_id = "number-value"
            count = (index % 3) + 4
            avg = (index % 15) + 140
            extra_height = (index % 12) + 160
            new_tot = (count * avg) + extra_height
            new_avg = round(new_tot / (count + 1), 1)

            question_text = f"The average height of {count} students is {avg} cm. When a new student of height {extra_height} cm joins them, what is the new average height of the group?"
            correct_ans = f"{new_avg} cm"
            options = [correct_ans, f"{avg + 2} cm", f"{new_avg - 1} cm", f"{avg} cm"]
            explanation = f"1. Total height of {count} students = {count} × {avg} = {count * avg} cm.\n2. Total height with new student = {count * avg} + {extra_height} = {new_tot} cm.\n3. Total number of students = {count} + 1 = {count + 1}.\n4. New average height = {new_tot} ÷ {count + 1} = {new_avg} cm."
        elif topic == "Area of Triangle":
            base = ((index % 5) + 4) * 2
            height = (index % 6) + 5
            area = (base * height) // 2
            question_text = f"A triangle has a base of {base} cm and a height of {height} cm. Find its area."
            correct_ans = f"{area} cm²"
            options = [correct_ans, f"{base * height} cm²", f"{base + height} cm²", f"{area + 10} cm²"]
            explanation = f"Area of triangle = 1/2 × base × height = 1/2 × {base} × {height} = {area} cm²."
        elif topic == "Percentage":
            pct = 10 + (index % 6) * 5
            price = ((index % 6) + 3) * 50
            disc = price * pct // 100
            payable = price - disc
            question_text = f"A bicycle is priced at ${price}. During a sale, a {pct}% discount is offered. What is the discount amount?"
            correct_ans = f"${disc}"
            options = [correct_ans, f"${payable}", f"${disc + 5}", f"${disc - 5}"]
            explanation = f"Discount = {pct}% of ${price} = ({pct}/100) × {price} = ${disc}."
        else:
            l, w, h = (index % 3) + 4, (index % 3) + 3, (index % 3) + 5
            vol = l * w * h
            question_text = f"Find the volume of a rectangular metal box with length {l} cm, width {w} cm, and height {h} cm."
            correct_ans = f"{vol} cm³"
            options = [correct_ans, f"{l*w} cm³", f"{vol + 20} cm³", f"{vol - 10} cm³"]
            explanation = f"Volume = Length × Width × Height = {l} × {w} × {h} = {vol} cm³."

    elif level == "P4":
        if topic == "Factors & Multiples":
            num = (index % 3) * 12 + 24
            question_text = f"Which of the following is NOT a factor of {num}?"
            non_factors = [5, 7, 9, 10, 11]
            correct_ans = str(non_factors[index % len(non_factors)])
            all_factors = [i for i in range(1, num+1) if num % i == 0]
            options = [correct_ans] + [str(f) for f in random.sample(all_factors, 3)]
            explanation = f"The factors of {num} are {all_factors}. {correct_ans} does not divide {num} exactly, so it is NOT a factor."
        elif topic == "Decimals":
            v_dec = round(((index % 8) + 1) * 1.5, 2)
            qty = (index % 4) + 3
            tot = round(v_dec * qty, 2)
            question_text = f"{name1} bought {qty} bottles of juice. Each bottle contained {v_dec} liters of juice. How many liters of juice did {name1} buy in total?"
            correct_ans = f"{tot} L"
            options = [correct_ans, f"{round(tot - 0.5, 2)} L", f"{round(tot + 1.2, 2)} L", f"{round(v_dec + qty, 2)} L"]
            explanation = f"Multiply the volume of one bottle by the quantity: {v_dec} × {qty} = {tot} liters."
        elif topic == "Area & Perimeter":
            side = (index % 6) + 6
            area = side * side
            question_text = f"A square field has an area of {area} m². Find its perimeter."
            perim = side * 4
            correct_ans = f"{perim} m"
            options = [correct_ans, f"{side} m", f"{area} m", f"{perim + 4} m"]
            explanation = f"1. Since it is a square, side × side = Area = {area} m². Therefore, side = {side} m.\n2. Perimeter of square = 4 × side = 4 × {side} = {perim} m."
        else:
            tot = ((index % 5) + 3) * 8
            spent = tot * 3 // 8
            question_text = f"{name1} had {tot} stamps. She gave 3/8 of them to {name2}. How many stamps did she have left?"
            rem = tot - spent
            correct_ans = str(rem)
            options = [correct_ans, str(spent), str(tot), str(rem - 2)]
            explanation = f"1. Stamps given away = 3/8 × {tot} = {spent}.\n2. Remaining stamps = {tot} - {spent} = {rem}."

    elif level == "P3":
        if topic == "Addition & Subtraction":
            n1 = (index % 500) + 1200
            n2 = (index % 300) + 400
            question_text = f"A library has {n1} English books and {n2} Chinese books. How many books are there in total?"
            correct_ans = str(n1 + n2)
            options = [correct_ans, str(n1 - n2), str(n1 + n2 + 100), str(n1 + n2 - 50)]
            explanation = f"Add the two groups of books: {n1} + {n2} = {correct_ans}."
        elif topic == "Multiplication & Division":
            mult = (index % 12) + 6
            qty = (index % 8) + 12
            prod = mult * qty
            question_text = f"There are {qty} rows of chairs in a hall. Each row has {mult} chairs. Find the total number of chairs."
            correct_ans = str(prod)
            options = [correct_ans, str(prod + mult), str(prod - mult), str(qty + mult)]
            explanation = f"Multiply the number of rows by chairs per row: {qty} × {mult} = {prod}."
        elif topic == "Area & Perimeter":
            l, w = (index % 4) + 8, (index % 4) + 4
            area = l * w
            question_text = f"Find the area of a rectangle with length {l} cm and width {w} cm."
            correct_ans = f"{area} cm²"
            options = [correct_ans, f"{2 * (l+w)} cm", f"{area + 10} cm²", f"{area - 5} cm²"]
            explanation = f"Area = Length × Width = {l} × {w} = {area} cm²."
        else:
            mass = (index % 5) * 50 + 200
            question_text = f"A packet of flour has a mass of {mass} g. What is the mass of 3 such packets?"
            correct_ans = f"{mass * 3} g"
            options = [correct_ans, f"{mass * 2} g", f"{mass * 3 - 100} g", f"{mass + 3} g"]
            explanation = f"Multiply the mass of one packet by 3: {mass} g × 3 = {mass * 3} g."

    else: # P2
        if topic == "Addition & Subtraction":
            n1 = (index % 100) + 120
            n2 = (index % 50) + 40
            question_text = f"{name1} has {n1} stickers. {name2} has {n2} fewer stickers than {name1}. How many stickers does {name2} have?"
            correct_ans = str(n1 - n2)
            options = [correct_ans, str(n1 + n2), str(n1 - n2 + 10), str(n1 - n2 - 5)]
            explanation = f"Subtract {n2} from {n1} to find {name2}'s stickers: {n1} - {n2} = {correct_ans}."
        elif topic == "Multiplication & Division":
            groups = (index % 4) + 3
            each = (index % 4) * 2 + 2
            prod = groups * each
            question_text = f"{name1} places {prod} cookies equally into {groups} bags. How many cookies are in each bag?"
            correct_ans = str(each)
            options = [correct_ans, str(each + 1), str(each - 1), str(groups)]
            explanation = f"Divide total cookies by number of bags: {prod} ÷ {groups} = {each}."
        elif topic == "Fractions":
            denom = (index % 4) + 5
            num = (index % (denom - 1)) + 1
            question_text = f"What fraction of the figure must be shaded to show {num}/{denom}?"
            correct_ans = f"{num}/{denom}"
            options = [correct_ans, f"1/{denom}", f"{denom - num}/{denom}", f"{num + 1}/{denom}"]
            explanation = f"The fraction {num}/{denom} represents {num} parts out of a total of {denom} equal parts."
        else:
            cost = (index % 4) * 5 + 10
            question_text = f"Siti spent ${cost} on a toy and had $5 left. How much money did she have at first?"
            correct_ans = f"${cost + 5}"
            options = [correct_ans, f"${cost}", f"${cost - 5}", f"${cost + 10}"]
            explanation = f"Add the cost of the toy and remaining money: ${cost} + $5 = ${cost + 5}."

    if not options or len(options) < 4:
        clean_ans = correct_ans.replace(" cm²", "").replace(" m²", "").replace(" cm³", "").replace(" g", "").replace(" m", "").replace(" L", "").replace("$", "").replace(" years old", "")
        try:
            val_ans = int(float(clean_ans))
            options = [correct_ans, f"${val_ans + 5}" if "$" in correct_ans else str(val_ans + 5), f"${val_ans - 2}" if "$" in correct_ans else str(val_ans - 2), f"${val_ans * 2}" if "$" in correct_ans else str(val_ans * 2)]
        except ValueError:
            options = [correct_ans, "None of the above", "Cannot be determined", "Both options are correct"]

    random.shuffle(options)
    
    if difficulty == "Hard" and index % 2 == 0:
        q_type = "short_answer"
        options = []
        correct_ans = correct_ans.replace(" cm²", "").replace(" m²", "").replace(" cm³", "").replace(" g", "").replace(" m", "").replace(" L", "").replace("$", "").replace(" years old", "").lower()

    return {
        "id": q_id,
        "topic": topic,
        "type": q_type,
        "question": question_text,
        "options": options,
        "answer": correct_ans,
        "explanation": explanation,
        "difficulty": difficulty,
        "heuristicId": heuristic_id,
        "barModel": bar_model
    }

GRAMMAR_TEMPLATES = {
    "P6": [
        ("Not only ________ the suspect break into the house, but he also stole the jewelry.", "did", ["does", "had", "was"], "Inversion is required after 'Not only'. Since the second clause is past tense ('stole'), we use 'did'."),
        ("Were he ________ the truth, his parents would have forgiven him.", "to have told", ["told", "to tell", "telling"], "This is the past conditional subjunctive: 'Were he to have told' is equivalent to 'If he had told'."),
        ("The principal requested that every teacher ________ present at the school hall tomorrow.", "be", ["is", "are", "was"], "The subjunctive verb 'be' is used after verbs/adjectives of demand or request like 'requested that'."),
        ("My grandmother rarely goes out in the evening, ________ she?", "does", ["doesn't", "is", "isn't"], "The adverb 'rarely' is negative, so the question tag must be positive: 'does she?'."),
        ("Neither the boys nor their captain ________ aware of the change in schedule.", "was", ["were", "are", "been"], "For 'neither... nor', the verb agrees with the closer subject. 'Their captain' is singular, so we use 'was'."),
        ("The heavy storm prevented the ferry ________ leaving the terminal.", "from", ["to", "for", "by"], "The verb 'prevent' collocates with 'from' + gerund: 'prevented... from leaving'."),
        ("Hardly had David stepped out of the house ________ it started to pour cats and dogs.", "when", ["than", "then", "before"], "The correlative structure is 'Hardly had... when'."),
        ("I would rather study diligently ________ fail my upcoming PSLE examinations.", "than", ["then", "to", "from"], "The expression 'would rather' is followed by 'than'."),
        ("She congratulated her classmate ________ winning the first prize in the national essay competition.", "on", ["for", "at", "about"], "The verb 'congratulate' takes the preposition 'on': 'congratulate someone on something'."),
        ("This is the pupil ________ art project was highly praised by the guest of honor.", "whose", ["who", "whom", "which"], "We use 'whose' to express possessive relation (the art project belonging to the pupil).")
    ],
    "P5": [
        ("Seldom ________ we witness such a magnificent solar eclipse in Singapore.", "do", ["does", "did", "are"], "Seldom is a negative adverb that triggers inversion. Since 'we' is plural and present, we use 'do'."),
        ("If I ________ in your shoes, I would apologize to the teacher immediately.", "were", ["was", "am", "be"], "We use 'were' in the subjunctive mood for hypothetical or imaginary situations."),
        ("Having ________ her dinner, Siti cleared the dining table and washed the dishes.", "completed", ["complete", "completing", "completes"], "The perfect participle construction 'Having' is followed by a past participle."),
        ("Siti, along with her siblings, ________ visiting the Botanic Gardens this Sunday.", "is", ["are", "were", "been"], "The phrase 'along with' does not change the singular subject 'Siti'. So we use 'is'."),
        ("The police are looking for the man ________ car was stolen yesterday.", "whose", ["whom", "who", "which"], "'Whose' is used to show possession of the car.")
    ],
    "P4": [
        ("Despite ________ extremely exhausted, Bala pushed on to finish the marathon.", "being", ["he was", "been", "is"], "'Despite' is a preposition and must be followed by a noun or a gerund like 'being'."),
        ("The boys were instructed to complete the science worksheet by ________.", "themselves", ["himself", "ourselves", "theirselves"], "The plural subject 'The boys' matches with the reflexive pronoun 'themselves'."),
        ("No sooner had the alarm rung ________ the security guards rushed to the main gate.", "than", ["when", "then", "before"], "The pairing structure is 'No sooner had... than'." )
    ],
    "P3": [
        ("While the girls ________ netball in the school field, it started to drizzle.", "were playing", ["played", "are playing", "play"], "Past continuous 'were playing' is used for an ongoing past action interrupted by a shorter action ('started')."),
        ("The thief crept ________ through the quiet corridor to avoid being seen.", "stealthily", ["clumsily", "noisily", "boldly"], "'Stealthily' means quietly and secretly, which fits avoiding detection."),
        ("Neither of the girls ________ completed the homework yet.", "has", ["have", "had", "having"], "'Neither of' takes a singular verb. 'Yet' indicates present perfect, so 'has' fits.")
    ],
    "P2": [
        ("My sister ________ a delicious chocolate cake for my birthday yesterday.", "baked", ["bakes", "bake", "is baking"], "Yesterday indicates simple past tense, so we use 'baked'."),
        ("Every morning, my father ________ to the market to buy fresh vegetables.", "goes", ["go", "went", "is going"], "Daily habits take the simple present tense. 'My father' is singular, so we use 'goes'."),
        ("This is the puppy ________ we rescued from the rain yesterday.", "which", ["who", "whom", "whose"], "We use 'which' or 'that' for animals and objects.")
    ]
}

ENGLISH_VOCAB_WORDS = {
    "P6": [
        ("inevitable", "certain to happen and unavoidable", "avoidable"),
        ("meticulously", "with extreme care and attention to detail", "recklessly"),
        ("resilient", "recovering quickly from setbacks", "fragile"),
        ("subsequent", "coming after something in time", "previous"),
        ("validate", "confirm the validity or accuracy of", "reject"),
        ("unprecedented", "never done or known before", "common"),
        ("advocate", "publicly recommend or support", "oppose")
    ],
    "P5": [
        ("exacerbate", "make a problem or bad situation worse", "alleviate"),
        ("preposterous", "completely contrary to reason or common sense", "reasonable"),
        ("deteriorate", "become progressively worse", "improve"),
        ("meticulously", "very carefully and precisely", "carelessly"),
        ("validate", "prove to be true or correct", "disprove"),
        ("obsolete", "no longer produced or used", "modern"),
        ("resilient", "able to recover quickly from difficult conditions", "weak"),
        ("conspicuous", "clearly visible or attracting attention", "hidden")
    ],
    "P4": [
        ("demonstrate", "show clearly by giving proof or examples", "hide"),
        ("observe", "watch carefully", "ignore"),
        ("ancient", "belonging to the very distant past", "modern"),
        ("temporary", "lasting for a limited time", "permanent"),
        ("unique", "being the only one of its kind", "common"),
        ("essential", "absolutely necessary", "optional"),
        ("reluctant", "unwilling and hesitant", "eager"),
        ("spectacular", "beautiful and eye-catching", "dull")
    ],
    "P3": [
        ("enthusiastic", "showing intense enjoyment or interest", "bored"),
        ("ferocious", "wild and savage", "tame"),
        ("examine", "inspect closely", "ignore"),
        ("rescue", "save from danger", "harm"),
        ("courageous", "brave", "cowardly"),
        ("scrumptious", "extremely delicious", "stale"),
        ("cluttered", "messy and untidy", "neat"),
        ("commence", "begin or start", "end")
    ],
    "P2": [
        ("enormous", "very large", "tiny"),
        ("terrified", "extremely scared", "happy"),
        ("delicious", "tastes very good", "bitter"),
        ("cautious", "careful of danger", "careless"),
        ("generous", "willing to share", "selfish"),
        ("exhausted", "extremely tired", "energetic"),
        ("polite", "showing good manners", "rude"),
        ("furious", "extremely angry", "calm")
    ]
}

SYNTHESIS_TEMPLATES = [
    ("The boy did not study. He failed the examination.", "because", "the boy failed the examination because he did not study"),
    ("Siti is very agile. She can scale the high wall easily.", "enough", "siti is agile enough to scale the high wall easily"),
    ("Bala worked hard. He was still unable to complete the task.", "Although", "although bala worked hard, he was still unable to complete the task"),
    ("You must start now. Otherwise, you will miss the last train.", "Unless", "unless you start now, you will miss the last train"),
    ("He finished his speech. The audience broke into rapturous applause.", "No sooner had", "no sooner had he finished his speech than the audience broke into rapturous applause"),
    ("She entered the room. She immediately heard an odd scratching noise.", "Hardly had", "hardly had she entered the room when she immediately heard an odd scratching noise"),
    ("David was poor. He contributed generously to the charity fund.", "Despite", "despite being poor, david contributed generously to the charity fund")
]

def generate_english_question(level, q_id, index):
    difficulty = "Easy" if index % 3 == 0 else ("Medium" if index % 3 == 1 else "Hard")
    opt = index % 3

    question_text = ""
    options = []
    correct_ans = ""
    explanation = ""
    q_type = "mcq"
    topic = "Grammar MCQ"

    if opt == 0:
        rules = GRAMMAR_TEMPLATES[level]
        rule = rules[index % len(rules)]
        question_text = rule[0]
        correct_ans = rule[1]
        options = [correct_ans] + rule[2]
        explanation = rule[3]
        topic = "Grammar MCQ"

    elif opt == 1:
        words = ENGLISH_VOCAB_WORDS[level]
        word, definition, antonym = words[index % len(words)]
        
        question_text = f"Select the word that best defines or matches the context: '{definition}'."
        correct_ans = word
        other_words = [w[0] for w in words if w[0] != word]
        options = [correct_ans] + random.sample(other_words, min(3, len(other_words)))
        explanation = f"'{correct_ans}' means '{definition}'. Antonym: '{antonym}'."
        topic = "Vocabulary MCQ"

    else:
        topic = "Synthesis & Transformation"
        q_type = "short_answer"
        
        sent, joiner, correct_ans = SYNTHESIS_TEMPLATES[index % len(SYNTHESIS_TEMPLATES)]
        question_text = f"Combine the sentences into one without changing its meaning, using the word(s) provided:\n\nSentence 1: {sent.split('.')[0]}.\nSentence 2: {sent.split('.')[1].strip()}\n\nUse: **{joiner}**"
        explanation = f"Correct synthesis: '{correct_ans}'"
        options = []
        correct_ans = correct_ans.lower().strip()

    if q_type == "mcq" and len(options) < 4:
        options = [correct_ans, "alternative_a", "alternative_b", "alternative_c"]
    
    if q_type == "mcq":
        random.shuffle(options)

    return {
        "id": q_id,
        "topic": topic,
        "type": q_type,
        "question": question_text,
        "options": options,
        "answer": correct_ans,
        "explanation": explanation,
        "difficulty": difficulty
    }

SCIENCE_TEMPLATES = {
    "P6": [
        (
            "Forces (Friction, Gravity, Elastic, Magnetic)",
            "A heavy wooden crate of mass 50 kg was dragged across a rough concrete floor and a smooth glass surface using a spring balance. It required 80 N of force on concrete, but only 20 N on glass.\n\nExplain why more force was needed on the concrete floor.",
            "the concrete floor is rougher, creating greater frictional force which opposes the motion of the crate",
            "Concept: Friction opposes motion and depends on the roughness of contact surfaces.\nEvidence: Crate on concrete required 80 N compared to 20 N on glass.\nReasoning: Concrete is rougher than glass, so it creates a larger frictional force. More pulling force is needed to overcome this friction.",
            "concrete floor is rougher"
        ),
        (
            "Energy Forms & Conversions",
            "A steel ball was released from the top of a smooth ramp. As it rolled down, its speed increased continuously.\n\nState the energy conversion that occurred as the ball rolled down.",
            "gravitational potential energy -> kinetic energy",
            "Concept: Energy conservation states that potential energy is converted to kinetic energy as height decreases.\nEvidence: Height decreases and speed increases.\nReasoning: Gravitational potential energy decreases as height decreases, converting into kinetic energy, causing speed to rise.",
            "gravitational potential energy"
        ),
        (
            "Photosynthesis & Respiration",
            "An aquatic plant was exposed to light at varying distances. The number of oxygen bubbles produced per minute was measured: 10 cm away = 45 bubbles; 50 cm away = 12 bubbles.\n\nExplain how the distance of the light source affected the rate of photosynthesis.",
            "increasing the distance decreases light intensity, slowing down the rate of photosynthesis",
            "Concept: Rate of photosynthesis depends on light intensity.\nEvidence: Rate fell from 45 to 12 bubbles as distance increased.\nReasoning: Moving light further away reduces light intensity on chloroplasts, reducing the rate of photosynthesis and releasing less oxygen bubbles.",
            "decreases light intensity"
        )
    ],
    "P5": [
        (
            "Electrical Circuits",
            "A series circuit had 2 bulbs and 1 battery. When a third bulb was added in series, the brightness of all bulbs decreased.\n\nExplain why adding a bulb in series reduced the brightness.",
            "adding a bulb in series increases electrical resistance, reducing current flowing through each bulb",
            "Concept: Total resistance increases in a series circuit as more bulbs are added.\nEvidence: Bulb brightness decreased.\nReasoning: More bulbs in series increase circuit resistance, which decreases electric current flowing through, reducing brightness.",
            "increases electrical resistance"
        ),
        (
            "Water Cycle",
            "Siti poured equal volumes of water into Beaker A (exposed surface area = 50 cm²) and Beaker B (exposed surface area = 150 cm²). After 3 hours, Beaker B lost more water.\n\nExplain why Beaker B evaporated water faster.",
            "beaker b has a larger exposed surface area, which increases the rate of evaporation",
            "Concept: Rate of evaporation is directly proportional to exposed surface area.\nEvidence: Beaker B lost more water than Beaker A.\nReasoning: Beaker B has a larger surface area in contact with air, allowing more water molecules to absorb heat and escape as water vapor faster.",
            "larger exposed surface area"
        ),
        (
            "Cell System",
            "An onion skin cell was observed under a microscope. It had a cell wall, cell membrane, and nucleus, but lacked chloroplasts.\n\nExplain why onion skin cells do not have chloroplasts.",
            "onion skin cells grow underground where there is no light, so they do not need chloroplasts to perform photosynthesis",
            "Concept: Chloroplasts trap light to perform photosynthesis.\nEvidence: Onion skin cells grow underground in the dark.\nReasoning: Onion skins grow underground where light cannot reach. Since they cannot perform photosynthesis, they do not require chloroplasts.",
            "do not perform photosynthesis"
        )
    ],
    "P4": [
        (
            "Matter",
            "100 cm³ of air was pumped into a sealed metal container of capacity 500 cm³. The final volume of air inside the container remained 500 cm³.\n\nExplain why the volume of air did not change to 600 cm³.",
            "air has no definite volume and can be compressed to fit the shape of its container",
            "Concept: Gases have no definite volume and can be compressed.\nEvidence: Volume of container remained 500 cm³.\nReasoning: Air is a gas and can be compressed, allowing it to occupy the fixed 500 cm³ volume of the metal container.",
            "no definite volume"
        ),
        (
            "Light & Shadows",
            "A plastic sheet, a piece of tracing paper, and a cardboard sheet were placed between a lamp and a screen. Only the cardboard formed a dark, sharp shadow.\n\nExplain why only the cardboard formed a dark shadow.",
            "cardboard is opaque and blocks all light from passing through, creating a shadow",
            "Concept: Shadows are formed when light is blocked by opaque materials.\nEvidence: Only cardboard formed a dark shadow.\nReasoning: Cardboard is opaque and does not allow light to pass through. Plastic is transparent and tracing paper is translucent, allowing light through.",
            "cardboard is opaque"
        ),
        (
            "Heat & Temperature",
            "A glass jar was tightly fitted with a metal lid. When hot water was poured over the metal lid, the lid loosened and was easily unscrewed.\n\nExplain why pouring hot water loosened the lid.",
            "the metal lid gained heat from the hot water and expanded faster than the glass jar",
            "Concept: Metals expand when they gain heat.\nEvidence: Pouring hot water loosened the lid.\nReasoning: Metal gains heat and expands. Since metal expands more and faster than glass, the lid loosened from the jar.",
            "gained heat and expanded"
        )
    ],
    "P3": [
        (
            "Diversity of Living & Non-Living Things",
            "A mushroom and a fern were observed. Neither produced seeds, but both reproduced successfully.\n\nState how the mushroom and fern reproduce.",
            "both reproduce by spores",
            "Concept: Non-flowering plants (ferns) and fungi (mushrooms) reproduce by spores.\nEvidence: Neither produces seeds but both multiply.\nReasoning: Both organisms use spores as their reproductive units to distribute and grow in favorable conditions.",
            "by spores"
        ),
        (
            "Materials",
            "A plastic bottle and a ceramic bottle were dropped from a height of 1 meter. The ceramic bottle shattered, while the plastic bottle remained intact.\n\nIdentify the property of plastic that kept the bottle intact.",
            "plastic is strong, flexible, and not brittle compared to ceramic",
            "Concept: Materials have varying strengths and brittleness.\nEvidence: Ceramic shattered but plastic survived.\nReasoning: Plastic has high strength and impact resistance, whereas ceramic is brittle and shatters easily under force.",
            "not brittle"
        ),
        (
            "Human Digestive System",
            "Food was chewed in the mouth for 1 minute before swallowing.\n\nExplain how chewing food helps the digestive process.",
            "chewing breaks food into smaller pieces, increasing its surface area for digestive enzymes to act on faster",
            "Concept: Digestion is accelerated by physical breakdown.\nEvidence: Food is broken into smaller pieces.\nReasoning: Chewing breaks food into smaller bits, increasing the exposed surface area, which allows saliva and digestive juices to break down food faster.",
            "surface area"
        )
    ]
}

def generate_science_question(level, q_id, index):
    actual_level = level if level != "P2" else "P3"
    difficulty = "Easy" if index % 3 == 0 else ("Medium" if index % 3 == 1 else "Hard")
    
    templates = SCIENCE_TEMPLATES[actual_level]
    template = templates[index % len(templates)]
    
    topic = template[0]
    question_text = template[1]
    correct_ans = template[2]
    explanation = template[3]
    keyword_match = template[4]
    
    q_type = "mcq"
    options = []

    if difficulty == "Easy":
        distractors = [
            "no heat transfer or expansion occurs during the process",
            "the container contracts and traps the elements inside",
            "both materials dissolve due to chemical potential alterations"
        ]
        options = [correct_ans] + distractors
        random.shuffle(options)
    else:
        q_type = "short_answer"
        correct_ans = keyword_match.lower()
        question_text += f"\n\n*(Tip: Include key scientific terms like '{keyword_match}' in your answer)*"

    return {
        "id": q_id,
        "topic": topic,
        "type": q_type,
        "question": question_text,
        "options": options,
        "answer": correct_ans,
        "explanation": explanation,
        "difficulty": difficulty
    }

CHINESE_TEMPLATES = {
    "P6": [
        ("Vocabulary Selection (词语选择)", "王校长的演讲内容深刻，言简意赅，令我们受益 ________。", "匪浅", ["浅薄", "深刻", "困难"], "‘受益匪浅’ (benefited greatly) 是新加坡高频的成语，常在作文和阅读理解中使用。"),
        ("Sentence Completion (句型填空)", "面对突如其来的疫情，全国上下表现出极强的 ________，共同克服了重重难关。", "凝聚力", ["破坏力", "爆发力", "想象力"], "全社会共同团结面对灾难，体现的是 ‘凝聚力’ (cohesiveness)."),
        ("Hanyu Pinyin", "‘勉励’ 的汉语拼音是什么？", "miǎn lì", ["mián lǐ", "miǎn lí", "miàn lǐ"], "‘勉’ (miǎn) 代表鼓励，‘励’ (lì) 代表励志。")
    ],
    "P5": [
        ("Vocabulary Selection (词语选择)", "在遇到学习上的困难时，我们千万不能轻易妥协，要勇敢地 ________ 挑战。", "迎接", ["逃避", "害怕", "拒绝"], "面对困难，应该勇敢地 ‘迎接’ (embrace/meet) 挑战。"),
        ("Sentence Completion (句型填空)", "经过大家几个月的精心筹备，国庆庆典活动终于 ________ 顺利举行。", "得以", ["也许", "居然", "很难"], "‘得以’ (be able to / managed to) 表示在条件具备后事情顺利实现。"),
        ("Hanyu Pinyin", "‘诚恳’ 的汉语拼音是什么？", "chéng kěn", ["chén kēn", "chén kěn", "chéng kē"], "‘诚’ (chéng) 诚实，‘恳’ (kěn) 诚恳。")
    ],
    "P4": [
        ("Vocabulary Selection (词语选择)", "这家百年老字号的菜肴不仅味道鲜美，而且价格十分 ________。", "公道", ["昂贵", "浪费", "便宜"], "形容价格合适且讲信用，最合适词语是 ‘公道’ (fair/reasonable)."),
        ("Sentence Completion (句型填空)", "由于他平时上课不专心，________ 这次考试成绩一落千丈。", "导致", ["因为", "所以", "可能"], "‘导致’ (led to / resulted in) 后面接不好的结果。"),
        ("Hanyu Pinyin", "‘偶尔’ 的汉语拼音是什么？", "ǒu ěr", ["ǒu ér", "óu ěr", "ōu ēr"], "‘偶尔’ (ǒu ěr) 表示间或、有时候。")
    ],
    "P3": [
        ("Vocabulary Selection (词语选择)", "天空突然下起了倾盆大雨，小明没有带伞，被淋得像个 ________ 鸡。", "落汤", ["烤", "烤鸭", "落水"], "‘落汤鸡’ (soaked to the skin) 是中文里形容人被雨淋得很湿的常用成语。"),
        ("Sentence Completion (句型填空)", "我们应该 ________ 帮助那些在生活中有困难的邻居。", "主动", ["主动地", "被动", "故意"], "帮助他人应该发自内心，‘主动’ (actively/proactively) 伸出援手。"),
        ("Hanyu Pinyin", "‘医生’ 的汉语拼音是什么？", "yī shēng", ["yí shēng", "yì shèng", "yī shēn"], "‘医’ (yī) 代表医学，‘生’ (shēng) 代表生命。")
    ],
    "P2": [
        ("Hanyu Pinyin", "‘学校’ 的汉语拼音是什么？", "xué xiào", ["xüé xiào", "xué xiáo", "xuē xiāo"], "‘学’ (xué) 代表学习，‘校’ (xiào) 代表校园。"),
        ("Vocabulary Selection (词语选择)", "弟弟在宽阔的草地上高兴地 ________ 玩耍。", "奔跑", ["睡觉", "哭泣", "看书"], "在草地上玩耍，最适合用 ‘奔跑’ (running) 来形容。"),
        ("Sentence Completion (句型填空)", "老师今天在全班面前表扬了小明，因为他很 ________。", "聪明", ["懒惰", "难过", "生气"], "被老师表扬通常是因为好的品质，如 ‘聪明’ (clever) 或勤奋。")
    ]
}

def generate_chinese_question(level, q_id, index):
    difficulty = "Easy" if index % 3 == 0 else ("Medium" if index % 3 == 1 else "Hard")
    templates = CHINESE_TEMPLATES[level]
    template = templates[index % len(templates)]

    topic = template[0]
    question_text = template[1]
    correct_ans = template[2]
    distractors = template[3]
    explanation = template[4]

    options = [correct_ans] + distractors
    random.shuffle(options)

    return {
        "id": q_id,
        "topic": topic,
        "type": "mcq",
        "question": question_text,
        "options": options,
        "answer": correct_ans,
        "explanation": explanation,
        "difficulty": difficulty
    }

def main():
    print("Compiling Singapore Primary School Database with Visual Bar Models (19,000 Questions)...")
    for subject, levels in TOPICS.items():
        for level in levels:
            file_name = f"data/{level.lower()}_{subject}.json"
            questions = []
            
            for i in range(1, 1001):
                q_id = f"{level}_{subject.upper()[:4]}_{i:04d}"
                
                if subject == "mathematics":
                    q = generate_math_question(level, q_id, i)
                elif subject == "english":
                    q = generate_english_question(level, q_id, i)
                elif subject == "science":
                    q = generate_science_question(level, q_id, i)
                elif subject == "chinese":
                    q = generate_chinese_question(level, q_id, i)
                
                questions.append(q)
                
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            print(f"  -> Generated {file_name} (1,000 questions)")

    print("Success! Database fully compiled with Bar Models. Total: 19,000 questions.")

if __name__ == "__main__":
    main()
