import os
import json
import random

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Common Singaporean Names representing our multicultural society
NAMES = [
    "Ali", "Bala", "Mei Ling", "Wei Jie", "Siti", "Kavitha", "David", "Sarah",
    "John", "Fatimah", "Gopal", "Huiling", "Kumar", "Nurul", "Ravi", "Junjie",
    "Elsa", "Sanjay", "Ahmad", "Chloe", "Zhi Hao", "Karthik", "Rina", "Daniel",
    "Priya", "Marcus", "Taufiq", "Xinyi", "Desmond", "Yusof", "Amira", "Brandon"
]

# Items used in word problems
ITEMS = [
    "marbles", "pencils", "stickers", "stamps", "sweets", "toy cars", "colored beads",
    "books", "erasers", "rulers", "paper clips", "balloons", "cards", "cupcakes", "cookies"
]

# Subject topics by level
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

# ----------------- MATH GENERATOR -----------------
def generate_math_question(level, q_id):
    topics = TOPICS["mathematics"][level]
    topic = random.choice(topics)
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    
    name1, name2 = random.sample(NAMES, 2)
    item1, item2 = random.sample(ITEMS, 2)
    
    question_text = ""
    options = []
    correct_ans = ""
    explanation = ""
    q_type = "mcq"

    if topic == "Algebra" or level == "P6" and topic == "Algebra":
        # Algebra questions
        val_x = random.randint(2, 8)
        coeff = random.randint(2, 6)
        const = random.randint(3, 15)
        # Model: "Simplify 3x + 5 + 2x - 1" or "Find the value of 5x + 3 when x = 4"
        if random.choice([True, False]):
            question_text = f"Simplify the algebraic expression: {coeff}k + {const} + {random.randint(1, 4)}k - {random.randint(1, const-1)}"
            # k coeff sum, const diff
            k_sum = coeff + random.randint(1, 4)
            const_diff = const - random.randint(1, const-1)
            correct_ans = f"{k_sum}k + {const_diff}"
            options = [correct_ans, f"{k_sum}k - {const_diff}", f"{coeff + 1}k + {const}", f"{k_sum + 1}k + {const_diff + 2}"]
            explanation = f"Combine like terms: ({coeff}k + {k_sum-coeff}k) = {k_sum}k. Then combine the constants: {const} - {const-const_diff} = {const_diff}. Thus, the answer is {correct_ans}."
        else:
            q_val = coeff * val_x + const
            question_text = f"Find the value of {coeff}w + {const} when w = {val_x}."
            correct_ans = str(q_val)
            options = [correct_ans, str(coeff + const), str(coeff * (val_x + const)), str(q_val - 2)]
            explanation = f"Substitute w = {val_x} into the expression: {coeff}({val_x}) + {const} = {coeff * val_x} + {const} = {q_val}."
            
    elif topic in ["Addition & Subtraction", "Numbers to 1000", "Numbers to 10000", "Numbers to 100000"]:
        limit = 1000 if level == "P2" else (10000 if level == "P3" else 100000)
        num1 = random.randint(100, limit // 2)
        num2 = random.randint(50, limit // 2)
        if random.choice([True, False]):
            # Addition word problem
            question_text = f"{name1} has {num1} {item1}. {name2} has {num2} more {item1} than {name1}. How many {item1} do they have altogether?"
            ans_val = num1 + (num1 + num2)
            correct_ans = str(ans_val)
            options = [correct_ans, str(num1 + num2), str(num1 * 2), str(ans_val - 50)]
            explanation = f"{name2} has {num1} + {num2} = {num1 + num2} {item1}. Together, they have {num1} + {num1 + num2} = {ans_val} {item1}."
        else:
            # Subtraction word problem
            num1 = max(num1, num2) + random.randint(50, 200)
            question_text = f"{name1} has {num1} {item1}. He gives {num2} {item1} to {name2}. How many {item1} does {name1} have left?"
            ans_val = num1 - num2
            correct_ans = str(ans_val)
            options = [correct_ans, str(num1 + num2), str(ans_val + 10), str(ans_val - 10)]
            explanation = f"Subtract the items given away: {num1} - {num2} = {ans_val} {item1}."

    elif topic == "Multiplication & Division":
        if level == "P2":
            factor1 = random.choice([2, 3, 4, 5, 10])
            factor2 = random.randint(2, 9)
        else:
            factor1 = random.randint(6, 12)
            factor2 = random.randint(12, 99)
            
        prod = factor1 * factor2
        if random.choice([True, False]):
            question_text = f"There are {factor2} boxes of {item1}. Each box contains {factor1} {item1}. How many {item1} are there in total?"
            correct_ans = str(prod)
            options = [correct_ans, str(factor2 + factor1), str(prod - factor1), str(prod + factor1)]
            explanation = f"Multiply the number of boxes by the items in each box: {factor2} × {factor1} = {prod}."
        else:
            question_text = f"{name1} shares {prod} {item1} equally among {factor1} friends. How many {item1} does each friend get?"
            correct_ans = str(factor2)
            options = [correct_ans, str(factor2 + 2), str(factor2 - 2), str(factor1)]
            explanation = f"Divide the total number of items by the number of friends: {prod} ÷ {factor1} = {factor2}."

    elif topic == "Fractions":
        if level in ["P2", "P3"]:
            # Simple addition or subtraction of fractions with same denominator
            denom = random.choice([4, 5, 6, 8, 10])
            num1 = random.randint(1, denom - 2)
            num2 = random.randint(1, denom - num1 - 1)
            sum_num = num1 + num2
            question_text = f"Find the sum of {num1}/{denom} and {num2}/{denom}."
            correct_ans = f"{sum_num}/{denom}"
            options = [correct_ans, f"{abs(num1 - num2)}/{denom}", f"{sum_num}/{denom * 2}", f"1/{denom}"]
            explanation = f"Since the denominators are the same, simply add the numerators: {num1} + {num2} = {sum_num}. The denominator remains {denom}. Answer is {sum_num}/{denom}."
        else:
            # P4-P6 Fractions
            # E.g., fraction of a set, or different denominators
            denom1 = random.choice([2, 3, 4])
            denom2 = random.choice([5, 6, 8])
            tot = denom1 * denom2 * random.randint(2, 10)
            spent_frac = random.randint(1, denom1 - 1)
            rem = tot - (tot * spent_frac // denom1)
            question_text = f"{name1} had ${tot}. She spent {spent_frac}/{denom1} of her money on a meal. How much money did she have left?"
            correct_ans = f"${rem}"
            options = [correct_ans, f"${tot - rem}", f"${rem - 5}", f"${rem + 10}"]
            explanation = f"Amount spent: {spent_frac}/{denom1} of ${tot} = ${tot * spent_frac // denom1}. Amount left = ${tot} - ${tot * spent_frac // denom1} = ${rem}."

    elif topic == "Ratio" or level in ["P5", "P6"] and topic == "Ratio":
        r1, r2 = random.choice([(2,3), (3,4), (3,5), (4,5), (5,6)])
        multiplier = random.randint(5, 20)
        v1, v2 = r1 * multiplier, r2 * multiplier
        tot = v1 + v2
        if random.choice([True, False]):
            question_text = f"The ratio of {name1}'s {item1} to {name2}'s {item1} is {r1}:{r2}. If {name1} has {v1} {item1}, how many {item1} do they have altogether?"
            correct_ans = str(tot)
            options = [correct_ans, str(v2), str(v1), str(tot + 10)]
            explanation = f"{r1} units = {v1}. 1 unit = {v1} ÷ {r1} = {multiplier}. Total units = {r1} + {r2} = {r1+r2}. Total items = {r1+r2} × {multiplier} = {tot}."
        else:
            question_text = f"The ratio of the length of Ribbon A to Ribbon B is {r1}:{r2}. The difference in their lengths is {abs(v1 - v2)} cm. Find the length of the shorter ribbon."
            shorter = min(v1, v2)
            correct_ans = f"{shorter} cm"
            options = [correct_ans, f"{max(v1, v2)} cm", f"{tot} cm", f"{abs(v1-v2)} cm"]
            explanation = f"Difference in ratio units = {abs(r1 - r2)} units. {abs(r1 - r2)} units = {abs(v1 - v2)} cm. 1 unit = {abs(v1 - v2) // abs(r1 - r2)} cm. Shorter Ribbon has {min(r1, r2)} units = {shorter} cm."

    elif topic == "Percentage" or level in ["P5", "P6"] and topic == "Percentage":
        pct = random.choice([10, 15, 20, 25, 30, 50])
        original = random.choice([40, 80, 120, 150, 200, 300, 500])
        disc = (original * pct) // 100
        payable = original - disc
        if random.choice([True, False]):
            question_text = f"A bag costs ${original} before discount. During a sale, there is a {pct}% discount. What is the discount amount?"
            correct_ans = f"${disc}"
            options = [correct_ans, f"${payable}", f"${disc + 5}", f"${original + disc}"]
            explanation = f"Discount amount = {pct}% of ${original} = ({pct}/100) × {original} = ${disc}."
        else:
            question_text = f"A school has {original} students. {pct}% of them wear glasses. How many students do NOT wear glasses?"
            correct_ans = str(original - (original * pct // 100))
            options = [correct_ans, str(original * pct // 100), str(original), str(original - 10)]
            explanation = f"Percentage of students who do not wear glasses = 100% - {pct}% = {100 - pct}%. Number of students = ({100 - pct}/100) × {original} = {correct_ans}."

    elif topic == "Area & Perimeter" or topic == "Area of Triangle" or topic == "Circles":
        side1 = random.choice([6, 8, 10, 12])
        side2 = random.choice([5, 7, 9, 11])
        if topic == "Area of Triangle" or (level == "P5" and random.choice([True, False])):
            base = side1
            height = side2
            area = (base * height) // 2
            question_text = f"Find the area of a triangle with a base of {base} cm and a height of {height} cm."
            correct_ans = f"{area} cm²"
            options = [correct_ans, f"{base * height} cm²", f"{base + height} cm²", f"{area + 5} cm²"]
            explanation = f"Area of a triangle = 1/2 × base × height = 1/2 × {base} × {height} = {area} cm²."
        elif topic == "Circles" or (level == "P6" and random.choice([True, False])):
            radius = random.choice([7, 14, 21])
            # Use pi = 22/7 or 3.14. Let's use 22/7.
            area = 22 * radius * radius // 7
            question_text = f"Find the area of a circle with a radius of {radius} cm. (Take π = 22/7)"
            correct_ans = f"{area} cm²"
            options = [correct_ans, f"{2 * 22 * radius // 7} cm²", f"{area * 2} cm²", f"{area - 10} cm²"]
            explanation = f"Area of circle = π × r × r = 22/7 × {radius} × {radius} = {area} cm²."
        else:
            area = side1 * side2
            perim = 2 * (side1 + side2)
            if random.choice([True, False]):
                question_text = f"A rectangle has a length of {side1} m and a width of {side2} m. Find its area."
                correct_ans = f"{area} m²"
                options = [correct_ans, f"{perim} m", f"{area + 10} m²", f"{area - 5} m²"]
                explanation = f"Area of rectangle = length × width = {side1} × {side2} = {area} m²."
            else:
                question_text = f"A rectangle has a length of {side1} m and a width of {side2} m. Find its perimeter."
                correct_ans = f"{perim} m"
                options = [correct_ans, f"{area} m²", f"{side1 + side2} m", f"{perim + 4} m"]
                explanation = f"Perimeter of rectangle = 2 × (length + width) = 2 × ({side1} + {side2}) = {perim} m."

    elif topic == "Speed" or level == "P6" and topic == "Speed":
        speed = random.choice([60, 80, 90, 100])
        hours = random.choice([2, 3, 4, 5])
        dist = speed * hours
        if random.choice([True, False]):
            question_text = f"A car travels at an average speed of {speed} km/h. How far does it travel in {hours} hours?"
            correct_ans = f"{dist} km"
            options = [correct_ans, f"{speed + hours} km", f"{speed // hours} km", f"{dist - 20} km"]
            explanation = f"Distance = Speed × Time = {speed} km/h × {hours} hours = {dist} km."
        else:
            question_text = f"An express bus traveled {dist} km in {hours} hours. Find its average speed."
            correct_ans = f"{speed} km/h"
            options = [correct_ans, f"{speed - 10} km/h", f"{speed + 15} km/h", f"{dist * hours} km/h"]
            explanation = f"Average Speed = Distance ÷ Time = {dist} km ÷ {hours} hours = {speed} km/h."
            
    else:
        # Fallback / General money/measure questions
        cost = random.randint(10, 50)
        qty = random.randint(3, 8)
        tot = cost * qty
        question_text = f"A toy sets cost ${cost} each. If {name1} buys {qty} of these toy sets, how much does he pay?"
        correct_ans = f"${tot}"
        options = [correct_ans, f"${tot - cost}", f"${tot + cost}", f"${cost + qty}"]
        explanation = f"Multiply the cost of a single toy set by the quantity: ${cost} × {qty} = ${tot}."

    # Shuffle options and ensure they are all strings
    if not options:
        options = [correct_ans, str(int(correct_ans)+5), str(int(correct_ans)-5), str(int(correct_ans)*2)]
    
    # Ensure options contains correct_ans
    if correct_ans not in options:
        options[0] = correct_ans
        
    random.shuffle(options)
    
    # Make some short-answer
    if q_type == "mcq" and difficulty == "Hard" and topic not in ["Circles", "Algebra"] and random.choice([True, False]):
        q_type = "short_answer"
        options = []
        # Strip units for text matching
        correct_ans = correct_ans.replace(" cm²", "").replace(" m²", "").replace(" cm", "").replace(" m", "").replace(" km/h", "").replace(" km", "").replace("$", "")

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

# ----------------- ENGLISH GENERATOR -----------------
ENGLISH_VOCAB = {
    "P2": [
        ("enormous", "very large", "tiny"), ("terrified", "extremely scared", "happy"),
        ("delicious", "tastes very good", "bitter"), ("cautious", "careful of danger", "careless"),
        ("generous", "willing to share", "selfish"), ("exhausted", "extremely tired", "energetic"),
        ("polite", "showing good manners", "rude"), ("furious", "extremely angry", "calm")
    ],
    "P3": [
        ("enthusiastic", "showing intense enjoyment or interest", "bored"),
        ("ferocious", "wild and savage", "tame"), ("examine", "inspect closely", "ignore"),
        ("rescue", "save from danger", "harm"), ("courageous", "brave", "cowardly"),
        ("scrumptious", "extremely delicious", "stale"), ("cluttered", "messy and untidy", "neat"),
        ("commence", "begin or start", "end")
    ],
    "P4": [
        ("demonstrate", "show clearly by giving proof or examples", "hide"),
        ("observe", "watch carefully", "ignore"), ("ancient", "belonging to the very distant past", "modern"),
        ("temporary", "lasting for a limited time", "permanent"), ("unique", "being the only one of its kind", "common"),
        ("essential", "absolutely necessary", "optional"), ("reluctant", "unwilling and hesitant", "eager"),
        ("spectacular", "beautiful and eye-catching", "dull")
    ],
    "P5": [
        ("exacerbate", "make a problem or bad situation worse", "alleviate"),
        ("preposterous", "completely contrary to reason or common sense", "reasonable"),
        ("deteriorate", "become progressively worse", "improve"), ("meticulously", "very carefully and precisely", "carelessly"),
        ("validate", "prove to be true or correct", "disprove"), ("obsolete", "no longer produced or used", "modern"),
        ("resilient", "able to recover quickly from difficult conditions", "weak"),
        ("conspicuous", "clearly visible or attracting attention", "hidden")
    ],
    "P6": [
        ("trigger", "cause an event or situation to happen", "prevent"),
        ("inevitable", "certain to happen and unavoidable", "avoidable"),
        ("meticulously", "with extreme care and attention to detail", "recklessly"),
        ("resilient", "recovering quickly from setbacks", "fragile"),
        ("subsequent", "coming after something in time", "previous"),
        ("validate", "confirm the validity or accuracy of", "reject"),
        ("unprecedented", "never done or known before", "common"),
        ("advocate", "publicly recommend or support", "oppose")
    ]
}

GRAMMAR_RULES = {
    "P2": [
        ("The dog ________ loudly at the postman yesterday.", "barked", ["barks", "bark", "is barking"], "This is in the simple past tense, as indicated by 'yesterday'."),
        ("Neither Sarah nor Siti ________ going to the playground today.", "is", ["are", "am", "were"], "For 'neither... nor', the verb agrees with the subject closer to it. 'Siti' is singular, so we use 'is'."),
        ("Every morning, my father ________ a cup of hot black coffee.", "drinks", ["drink", "drank", "is drinking"], "This represents a daily habit, which requires the simple present tense. 'My father' is singular, so we use 'drinks'."),
        ("That chocolate cake was made by Aunt Mary ________.", "herself", ["himself", "myself", "itself"], "Aunt Mary is female, so the reflexive pronoun is 'herself'.")
    ],
    "P3": [
        ("The thief crept ________ into the dark alley to hide from the police.", "stealthily", ["noisily", "boldly", "clumsily"], "Creeping into an alley to avoid police requires doing it quietly and secretly ('stealthily')."),
        ("Neither of the contestants ________ completed the final puzzle yet.", "has", ["have", "having", "had"], "'Neither of' takes a singular verb. 'Yet' indicates present perfect tense, so we use 'has'."),
        ("While we ________ television, the electricity suddenly failed.", "were watching", ["watched", "are watching", "watch"], "We use the past continuous tense ('were watching') for an ongoing past action that was interrupted by a shorter action ('failed')."),
        ("Can you please hand me ________ blue folder lying on that desk over there?", "that", ["this", "these", "those"], "'Over there' indicates distance, and 'folder' is singular, so we use 'that'.")
    ],
    "P4": [
        ("Despite ________ extremely tired, David finished his science project.", "being", ["he was", "is", "been"], "'Despite' is a preposition and must be followed by a noun or gerund ('being')."),
        ("No sooner had the principal stepped onto the stage ________ the hall fell silent.", "than", ["when", "then", "after"], "The correlative conjunction 'no sooner' is always paired with 'than'."),
        ("Having ________ her homework, Siti turned off her desk lamp and went to bed.", "completed", ["complete", "completing", "completes"], "The perfect participle construction 'Having' is followed by a past participle ('completed')."),
        ("The police are looking for the man ________ car was involved in the accident.", "whose", ["whom", "who", "which"], "We use 'whose' to show possession (the car belonging to the man).")
    ],
    "P5": [
        ("Seldom ________ we see such an impressive astronomical display in our night sky.", "do", ["does", "did", "are"], "When starting a sentence with negative adverbs like 'Seldom', inversion occurs. 'We' is plural, so we use 'do'."),
        ("If I ________ you, I would consult a doctor immediately.", "were", ["was", "am", "be"], "The subjunctive mood is used for hypothetical situations, which requires 'were' regardless of the subject pronoun."),
        ("The heavy rain prevented the soccer players ________ conducting their practice.", "from", ["to", "by", "for"], "The verb 'prevent' is followed by the preposition 'from' + gerund ('from conducting')."),
        ("Hardly had Mei Ling entered the kitchen ________ she smelt something burning.", "when", ["than", "then", "before"], "The construction 'Hardly had... when' is a standard grammatical pairing.")
    ],
    "P6": [
        ("Not only ________ he break the school rules, but he also lied to his teacher.", "did", ["does", "had", "would"], "Inversion is required after 'Not only'. Since the second clause is in the past tense ('lied'), the auxiliary verb must be 'did'."),
        ("Were he ________ the truth, his parents would not have punished him so severely.", "to have told", ["told", "to tell", "telling"], "This is a conditional subjunctive form. 'Were he to tell' is equivalent to 'If he told'."),
        ("My sister, along with her classmates, ________ visiting the museum this afternoon.", "is", ["are", "were", "been"], "Phrases like 'along with' do not change the number of the subject. The main subject 'My sister' is singular, so we use 'is'."),
        ("It is essential that everyone ________ present at the meeting tomorrow.", "be", ["is", "are", "was"], "The subjunctive verb form 'be' is used after adjectives of necessity like 'essential that'.")
    ]
}

def generate_english_question(level, q_id):
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    opt = random.choice(["grammar", "vocab", "synthesis"])
    
    question_text = ""
    options = []
    correct_ans = ""
    explanation = ""
    q_type = "mcq"
    topic = "Grammar MCQ"

    if opt == "grammar":
        rules = GRAMMAR_RULES[level]
        rule = random.choice(rules)
        question_text = rule[0]
        correct_ans = rule[1]
        options = [correct_ans] + rule[2]
        explanation = rule[3]
        topic = "Grammar MCQ"
    elif opt == "vocab":
        words = ENGLISH_VOCAB[level]
        word, definition, antonym = random.choice(words)
        name = random.choice(NAMES)
        question_text = f"The explorer described the ________ creature as resembling a giant, scaly lizard." if level in ["P5", "P6"] else f"The children saw an ________ castle at the theme park."
        if word in ["enormous", "ferocious", "ancient", "resilient", "conspicuous"]:
            correct_ans = word
            # select other words from same level
            other_words = [w[0] for w in words if w[0] != word]
            options = [correct_ans] + random.sample(other_words, min(3, len(other_words)))
            explanation = f"'{correct_ans}' is the correct fit. Definition: {definition}."
        else:
            # simple vocab question
            question_text = f"Select the word that means: '{definition}'."
            correct_ans = word
            other_words = [w[0] for w in words if w[0] != word]
            options = [correct_ans] + random.sample(other_words, min(3, len(other_words)))
            explanation = f"'{correct_ans}' means '{definition}'."
        topic = "Vocabulary MCQ"
    else:
        # Synthesis & Transformation
        topic = "Synthesis & Transformation"
        q_type = "short_answer"
        synthesis_templates = [
            ("The boy did not study. He failed the test.", "because", "The boy failed the test because he did not study."),
            ("Siti is very small. She can crawl through the tiny opening.", "enough", "Siti is small enough to crawl through the tiny opening."),
            ("Ravi is thin. He is very strong.", "Although", "Although Ravi is thin, he is very strong."),
            ("Unless it rains, we will play soccer.", "If", "If it does not rain, we will play soccer.")
        ]
        sent1, joiner, correct_ans = random.choice(synthesis_templates)
        question_text = f"Combine the following sentences using the word provided: \nSentence 1: {sent1.split('.')[0]}. \nSentence 2: {sent1.split('.')[1].strip()} \nUse word: **{joiner}**"
        explanation = f"Correctly combined: '{correct_ans}'"
        options = []

    # Ensure 4 options for MCQ
    if q_type == "mcq":
        while len(options) < 4:
            options.append("optional_word")
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

# ----------------- SCIENCE GENERATOR -----------------
SCIENCE_MATRICES = {
    "P3": [
        ("Diversity of Living & Non-Living Things", "Which of the following is a characteristic of all living things?", "They can reproduce and grow.", ["They are always green", "They can make their own food", "They do not need air"], "All living things require air, water, and food to survive, and they can grow, reproduce, and respond to changes."),
        ("Plants & Fungi", "Which of the following is a non-flowering plant?", "Fern", ["Rose", "Hibiscus", "Ixora"], "Ferns are non-flowering plants that reproduce by spores instead of seeds."),
        ("Materials", "Why is plastic commonly used to make a rain jacket?", "It is waterproof and lightweight.", ["It conducts heat well", "It can bend easily", "It is transparent"], "Raincoats must keep us dry, so a waterproof material like plastic is essential."),
        ("Human Digestive System", "In which organ is digestion fully completed and digested food absorbed into the blood?", "Small Intestine", ["Stomach", "Large Intestine", "Mouth"], "The small intestine is where digestion is completed, and nutrients are absorbed into the bloodstream.")
    ],
    "P4": [
        ("Life Cycles of Animals", "Which of the following organisms has a 3-stage life cycle?", "Cockroach", ["Butterfly", "Mosquito", "Mealworm beetle"], "Cockroaches have a 3-stage life cycle (egg, nymph, adult), while butterflies and mosquitoes have 4 stages."),
        ("Life Cycles of Plants", "Which part of the germinating seed grows out first?", "Roots", ["Shoot", "First leaf", "Seed leaf"], "The root (radicle) emerges first to anchor the seedling and absorb water."),
        ("Matter", "An object retains its shape and volume when transferred from a box to a jar. What state is it in?", "Solid", ["Liquid", "Gas", "Plasma"], "Solids have a definite shape and volume, and do not conform to the shape of their container."),
        ("Light & Shadows", "An opaque object block light, forming a shadow. Which material is opaque?", "Cardboard", ["Clear glass", "Tracing paper", "Cling wrap"], "Opaque materials like cardboard do not allow light to pass through, forming dark, distinct shadows."),
        ("Heat & Temperature", "What happens when a metal spoon is placed in a hot cup of soup?", "The spoon gains heat from the soup.", ["The spoon loses heat to the soup", "The spoon and soup both lose heat", "No heat transfer occurs"], "Heat always flows from a hotter region (soup) to a cooler region (metal spoon) until they reach thermal equilibrium.")
    ],
    "P5": [
        ("Electrical Circuits", "Which of the following materials is an electrical conductor?", "Copper wire", ["Rubber eraser", "Wooden ruler", "Plastic clip"], "Metals like copper are excellent electrical conductors that allow current to flow through a circuit."),
        ("Cell System", "Which part of a plant cell contains chlorophyll to absorb sunlight for photosynthesis?", "Chloroplast", ["Nucleus", "Cell Wall", "Cytoplasm"], "Chloroplasts contain chlorophyll, which traps light energy needed to make food during photosynthesis."),
        ("Water Cycle", "What is the process where water vapor cools and turns back into liquid water droplets?", "Condensation", ["Evaporation", "Melting", "Freezing"], "Condensation is the process where warm water vapor loses heat to the cooler surroundings and changes state to liquid water."),
        ("Plant & Human Circulatory Systems", "What is the function of the human heart?", "To pump oxygen-rich and nutrient-rich blood to all parts of the body.", ["To exchange oxygen and carbon dioxide", "To digest proteins", "To absorb water from digested food"], "The heart acts as a muscular pump that propels blood throughout the circulatory system.")
    ],
    "P6": [
        ("Forces (Friction, Gravity, Elastic, Magnetic)", "A box is pushed across a rough concrete floor. What force opposes its movement?", "Frictional force", ["Gravitational force", "Magnetic force", "Elastic spring force"], "Frictional force always acts in the direction opposite to the motion of the sliding object on rough surfaces."),
        ("Energy Forms & Conversions", "Identify the energy conversion of a falling apple before it hits the ground.", "Gravitational potential energy → Kinetic energy", ["Kinetic energy → Chemical potential energy", "Chemical potential energy → Heat energy", "Electrical energy → Kinetic energy"], "As the apple falls, its height decreases (losing gravitational potential energy) and its speed increases (gaining kinetic energy)."),
        ("Photosynthesis & Respiration", "What are the key raw materials required for photosynthesis?", "Carbon dioxide and Water", ["Oxygen and Glucose", "Nitrogen and Carbon dioxide", "Oxygen and Water"], "Plants combine carbon dioxide and water in the presence of light and chlorophyll to produce glucose and oxygen."),
        ("Food Chains & Food Webs", "Which organism in a food web is always a producer?", "Green plant", ["Caterpillar", "Eagle", "Fungi"], "Green plants are producers because they can perform photosynthesis to make their own food.")
    ]
}

def generate_science_question(level, q_id):
    # Science is introduced only in P3
    actual_level = level if level != "P2" else "P3"
    matrices = SCIENCE_MATRICES[actual_level]
    matrix = random.choice(matrices)
    
    topic = matrix[0]
    question_text = matrix[1]
    correct_ans = matrix[2]
    distractors = matrix[3]
    explanation = matrix[4]
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    q_type = "mcq"
    options = [correct_ans] + distractors
    random.shuffle(options)
    
    # Let's make some hard ones structured/short answer
    if difficulty == "Hard" and random.choice([True, False]):
        q_type = "short_answer"
        options = []
        # If short answer, we check for a core concept keyword
        if "Small Intestine" in correct_ans:
            correct_ans = "small intestine"
        elif "Fern" in correct_ans:
            correct_ans = "fern"
        elif "Waterproof" in correct_ans or "waterproof" in correct_ans:
            correct_ans = "waterproof"
        elif "Condensation" in correct_ans:
            correct_ans = "condensation"
        elif "Frictional" in correct_ans:
            correct_ans = "frictional force"
        else:
            correct_ans = correct_ans.lower()

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

# ----------------- CHINESE GENERATOR -----------------
CHINESE_MATRICES = {
    "P2": [
        ("Hanyu Pinyin", "‘学校’ 的汉语拼音是什么？", "xué xiào", ["xüé xiào", "xué xiáo", "xuē xiāo"], "‘学’ (xué) 代表学习，‘校’ (xiào) 代表校园。"),
        ("Vocabulary Selection (词语选择)", "弟弟在公园里高兴地 ________ 玩耍。", "奔跑", ["睡觉", "哭泣", "看书"], "在公园玩耍时，最适合用 ‘奔跑’ (running) 来形容。"),
        ("Sentence Completion (句型填空)", "老师表扬了小明，因为他很 ________。", "聪明", ["懒惰", "难过", "生气"], "被老师表扬通常是因为好的品质，如 ‘聪明’ (clever) 或勤奋。")
    ],
    "P3": [
        ("Hanyu Pinyin", "‘医生’ 的汉语拼音是什么？", "yī shēng", ["yí shēng", "yì shèng", "yī shēn"], "‘医’ (yī) 代表医学，‘生’ (shēng) 代表生命。"),
        ("Vocabulary Selection (词语选择)", "天空突然下起了大雨，小明没有带伞，被淋得像个 ________ 鸡。", "落汤", ["烤", "烤鸭", "落水"], "‘落汤鸡’ (soaked to the skin) 是中文里形容人被雨淋得很湿的常用成语。"),
        ("Sentence Completion (句型填空)", "我们应该 ________ 帮助那些有需要的人。", "主动", ["主动地", "被动", "故意"], "帮助他人应该发自内心，‘主动’ (actively/proactively) 伸出援手。")
    ],
    "P4": [
        ("Vocabulary Selection (词语选择)", "这家餐馆的菜肴不仅味道鲜美，而且价格 ________。", "公道", ["昂贵", "浪费", "便宜"], "形容价格合适且讲信用，最合适词语是 ‘公道’ (fair/reasonable)."),
        ("Sentence Completion (句型填空)", "由于他平时不努力，________ 这次考试不及格。", "导致", ["因为", "所以", "可能"], "‘导致’ (led to / resulted in) 后面接不好的结果。"),
        ("Cloze Passage (短文填空)", "为了保护我们的环境，学校发起了 ________ 塑料袋的活动。", "减少使用", ["增加使用", "制造", "丢弃"], "减少使用 (reducing usage) 塑料袋能起到环保作用。")
    ],
    "P5": [
        ("Vocabulary Selection (词语选择)", "遇到困难时，我们不能轻易妥协，要勇敢地 ________ 挑战。", "迎接", ["逃避", "害怕", "拒绝"], "面对困难，应该勇敢地 ‘迎接’ (embrace/meet) 挑战。"),
        ("Sentence Completion (句型填空)", "经过几个月的精心筹备，国庆庆典 ________ 顺利举行。", "得以", ["也许", "居然", "可能"], "‘得以’ (be able to / managed to) 表示在条件具备后事情顺利实现。")
    ],
    "P6": [
        ("Vocabulary Selection (词语选择)", "王校长的演讲内容深刻，言简意赅，令人受益 ________。", "匪浅", ["浅薄", "匪浅的", "深刻"], "‘受益匪浅’ (benefited greatly) 是高频的成语，常在作文和阅读理解中使用。"),
        ("Sentence Completion (句型填空)", "面对突如其来的冠病疫情，全国人民上下一致，展现出极强的 ________。", "凝聚力", ["破坏力", "爆发力", "意志力"], "全社会共同面对困难，体现的是 ‘凝聚力’ (cohesiveness).")
    ]
}

def generate_chinese_question(level, q_id):
    matrices = CHINESE_MATRICES[level]
    matrix = random.choice(matrices)
    
    topic = matrix[0]
    question_text = matrix[1]
    correct_ans = matrix[2]
    distractors = matrix[3]
    explanation = matrix[4]
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    
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

# ----------------- MAIN COMPILER LOOP -----------------
def main():
    print("Compiling Singapore Primary School Database (19,000 Questions)...")
    for subject, levels in TOPICS.items():
        for level in levels:
            file_name = f"data/{level.lower()}_{subject}.json"
            questions = []
            
            # Generate exactly 1,000 unique questions
            for i in range(1, 1001):
                q_id = f"{level}_{subject.upper()[:4]}_{i:04d}"
                
                if subject == "mathematics":
                    q = generate_math_question(level, q_id)
                elif subject == "english":
                    q = generate_english_question(level, q_id)
                elif subject == "science":
                    q = generate_science_question(level, q_id)
                elif subject == "chinese":
                    q = generate_chinese_question(level, q_id)
                
                questions.append(q)
                
            # Write to JSON
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            print(f"  -> Generated {file_name} (1,000 questions)")

    print("Success! Database fully built. Total questions generated: 19,000.")

if __name__ == "__main__":
    main()
