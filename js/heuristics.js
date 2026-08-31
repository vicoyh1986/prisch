/* Singapore Math 12 Core Heuristics & Visual Bar Model Engine */
import { sound } from "./sound.js";

export const HEURISTIC_CATEGORIES = [
  {
    id: "constant-part",
    name: "Constant Part (One Quantity Unchanged)",
    icon: "🔒",
    desc: "One quantity stays the same while another increases or decreases. Equalize the unchanged unit.",
    example: "Red & Blue beads in ratio 2:3. Add 12 Red beads. Ratio becomes 4:5. Blue beads remain unchanged."
  },
  {
    id: "constant-difference",
    name: "Constant Difference (Age Problems)",
    icon: "👥",
    desc: "The difference between two quantities never changes (e.g. age difference, or equal amount added/subtracted).",
    example: "Father is 28 years older than son. In 4 years, Father is 3 times son's age. The age difference is always 28."
  },
  {
    id: "constant-total",
    name: "Constant Total (Internal Transfer)",
    icon: "🔄",
    desc: "Quantities are transferred between parties. The sum of units remains the same before and after.",
    example: "Ali gives $30 to Bala. The total amount of money they have together remains unchanged."
  },
  {
    id: "supposition",
    name: "Supposition (Assumption / Guess & Check)",
    icon: "🕵️",
    desc: "Assume all items are of one type, find the total difference, and divide by the individual difference.",
    example: "A farm has 30 chickens and cows with 88 legs. Assume all are chickens (60 legs). Shortage = 28. Cow = +2 legs."
  },
  {
    id: "repeated-identity",
    name: "Repeated Identity",
    icon: "🔗",
    desc: "One common item appears in multiple comparison ratios. Find the lowest common multiple (LCM) to link them.",
    example: "A:B is 2:3. B:C is 4:5. Make B's units equal to 12. Ratio A:B:C = 8:12:15."
  },
  {
    id: "equal-fractions",
    name: "Equal Fractions (Numerator Equalization)",
    icon: "⚖️",
    desc: "When fractions of two different wholes are equal (e.g. 2/3 of A = 4/5 of B), make the numerators identical.",
    example: "2/3 of A = 4/5 of B. Change 2/3 to 4/6. Then A has 6 units and B has 5 units."
  },
  {
    id: "working-backwards",
    name: "Working Backwards",
    icon: "⏪",
    desc: "Start with the final result and reverse every mathematical operation in reverse order.",
    example: "A number is doubled, added to 14, and divided by 2 to get 20. Reverse: 20 × 2 = 40; 40 - 14 = 26; 26 ÷ 2 = 13."
  },
  {
    id: "excess-shortage",
    name: "Excess & Shortage (Gap & Difference)",
    icon: "📦",
    desc: "Comparing two scenarios: giving x items leaves excess, giving y items results in shortage.",
    example: "Give 4 sweets each: 6 sweets left. Give 6 sweets each: short of 8 sweets. Gap = 6 + 8 = 14. Diff = 2. Pupils = 7."
  },
  {
    id: "number-value",
    name: "Number × Value (Item × Quantity)",
    icon: "💰",
    desc: "Distinguish between the NUMBER of items and the monetary or point VALUE of each item.",
    example: "50-cent and 20-cent coins with total value $14.40. Ratio of 50c to 20c coins is 3:2."
  },
  {
    id: "speed-circles",
    name: "Speed & Composite Geometry",
    icon: "⚡",
    desc: "Speed ratio relationships, opposite direction catch-ups, and composite circular quadrant geometry.",
    example: "Two cars start from opposite ends. Time taken to meet = Total Distance ÷ Total Speed."
  }
];

export class HeuristicsEngine {
  constructor(app) {
    this.app = app;
    this.currentHeuristic = "constant-part";
    this.hintTier = 0;
  }

  /**
   * Full taxonomy studio used by the Math Heuristics sidebar section
   */
  renderTaxonomyStudio(container) {
    if (!container) return;
    const active = HEURISTIC_CATEGORIES.find(h => h.id === this.currentHeuristic) || HEURISTIC_CATEGORIES[0];

    container.innerHTML = `
      <div class="heuristics-studio">
        <div class="panel" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(0,242,254,0.08), rgba(79,172,254,0.12)); border-color: rgba(0,242,254,0.25);">
          <h2 style="font-size: 22px; margin-bottom: 6px;">📐 Singapore Math Heuristics Lab</h2>
          <p style="color: var(--text-secondary); font-size: 13px; max-width: 760px; line-height: 1.6; margin: 0;">
            Master the 10 core problem-solving heuristics used in top-school PSLE papers. Understand <strong>why</strong> a method works before drilling — this is how you replace tuition cramming with lasting conceptual mastery.
          </p>
        </div>

        <div style="display: grid; grid-template-columns: 280px 1fr; gap: 16px;">
          <div class="panel" style="padding: 12px;">
            <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">Heuristic Taxonomy</h4>
            <div style="display: flex; flex-direction: column; gap: 6px;">
              ${HEURISTIC_CATEGORIES.map(h => `
                <button class="btn-pill heuristic-pick ${h.id === active.id ? 'active' : ''}" data-hid="${h.id}" style="justify-content: flex-start; text-align: left; width: 100%; padding: 10px 12px; font-size: 12px;">
                  <span style="margin-right: 6px;">${h.icon}</span> ${h.name}
                </button>
              `).join("")}
            </div>
          </div>

          <div class="panel" id="heuristic-detail-pane">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
              <span style="font-size: 28px;">${active.icon}</span>
              <div>
                <h3 style="margin: 0; font-size: 18px;">${active.name}</h3>
                <span class="tag tag-easy" style="margin-top: 4px; display: inline-block;">Core MOE Heuristic</span>
              </div>
            </div>
            <p style="font-size: 14px; line-height: 1.7; color: var(--text-secondary); margin-bottom: 14px;">${active.desc}</p>
            <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; margin-bottom: 16px;">
              <div style="font-size: 11px; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 6px;">Worked Example</div>
              <p style="font-size: 13px; line-height: 1.65; color: var(--text-primary); margin: 0;">${active.example}</p>
            </div>
            ${this.renderBarModel({
              title: active.name,
              bars: [
                { name: "Before", units: 3, color: "#00f2fe" },
                { name: "After", units: 5, color: "#4facfe", highlightUnits: 2, highlightColor: "#ffd166" }
              ],
              bracketText: "Visualise the unchanged quantity, then convert the change into equal units.",
              note: "Bar models turn abstract word problems into concrete unit diagrams."
            })}
            <div style="display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap;">
              <button class="btn btn-primary" id="heuristic-drill-btn">🎯 Drill this heuristic</button>
              <button class="btn btn-outline" id="heuristic-coach-btn">🧠 Add to today's mastery plan</button>
            </div>
          </div>
        </div>
      </div>
    `;

    container.querySelectorAll(".heuristic-pick").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playClick();
        this.currentHeuristic = btn.dataset.hid;
        this.renderTaxonomyStudio(container);
      });
    });

    const drillBtn = container.querySelector("#heuristic-drill-btn");
    if (drillBtn && this.app) {
      drillBtn.addEventListener("click", async () => {
        sound.playClick();
        if (this.app.coach) {
          await this.app.coach.startHeuristicDrill(this.currentHeuristic);
        } else if (this.app.loadQuiz) {
          this.app.loadQuiz("mathematics");
        }
      });
    }

    const coachBtn = container.querySelector("#heuristic-coach-btn");
    if (coachBtn && this.app) {
      coachBtn.addEventListener("click", () => {
        sound.playClick();
        if (this.app.coach) this.app.coach.pinHeuristic(this.currentHeuristic);
        this.app.switchSection("coach");
      });
    }
  }

  /**
   * Progressive 3-tier hints used by QuizPlayer
   */
  renderProgressiveHints(question, tier = 1) {
    const q = question || {};
    const heuristicId = q.heuristicId || "constant-part";
    const heuristicInfo = HEURISTIC_CATEGORIES.find(h => h.id === heuristicId) || HEURISTIC_CATEGORIES[0];
    const safeTier = Math.max(1, Math.min(3, tier || 1));

    if (safeTier === 1) {
      return `
        <div style="background: rgba(255,184,0,0.08); border: 1px solid rgba(255,184,0,0.25); border-radius: 10px; padding: 12px;">
          <div style="font-weight: 700; color: var(--warning); margin-bottom: 4px;">💡 Tier 1 — Strategy</div>
          <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
            Topic: <strong>${q.topic || "Word Problem"}</strong>. Try the <strong>${heuristicInfo.name}</strong> approach.
            ${heuristicInfo.desc}
          </div>
        </div>
      `;
    }

    if (safeTier === 2) {
      const model = q.barModel || {
        title: q.topic || "Bar Model",
        bars: [
          { name: "Before", units: 3, color: "#00f2fe" },
          { name: "After", units: 5, color: "#4facfe", highlightUnits: 2, highlightColor: "#ffd166" }
        ],
        bracketText: "Convert the change into equal units before solving."
      };
      return `
        <div style="background: rgba(0,242,254,0.06); border: 1px solid rgba(0,242,254,0.25); border-radius: 10px; padding: 12px;">
          <div style="font-weight: 700; color: var(--primary); margin-bottom: 6px;">🔍 Tier 2 — Model Framework</div>
          ${this.renderBarModel(model)}
        </div>
      `;
    }

    return `
      <div style="background: rgba(0,242,161,0.06); border: 1px solid rgba(0,242,161,0.25); border-radius: 10px; padding: 12px;">
        <div style="font-weight: 700; color: var(--success); margin-bottom: 4px;">📝 Tier 3 — Step-by-Step Working</div>
        <div style="font-size: 13px; color: var(--text-secondary); white-space: pre-line; line-height: 1.7;">${q.explanation || "Break the problem into equal units, solve for 1 unit, then answer the question asked."}</div>
      </div>
    `;
  }

  /**
   * Generates interactive visual SVG/HTML Bar Model
   */
  renderBarModel(modelData) {
    if (!modelData) return "";

    const { title, bars, bracketText, note } = modelData;

    let barsHtml = "";
    bars.forEach(b => {
      let segmentsHtml = "";
      for (let i = 0; i < b.units; i++) {
        const isHighlighted = b.highlightUnits && i >= b.units - b.highlightUnits;
        const color = isHighlighted ? (b.highlightColor || "var(--warning)") : (b.color || "var(--primary)");
        segmentsHtml += `
          <div class="bar-unit" style="flex: 1; height: 26px; border: 1px solid rgba(255,255,255,0.25); background: ${color}; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #0f172a;">
            ${b.unitLabel || "1u"}
          </div>
        `;
      }

      barsHtml += `
        <div class="bar-row" style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
          <div class="bar-label" style="width: 100px; font-size: 12px; font-weight: 700; color: var(--text-primary); text-align: right;">
            ${b.name}:
          </div>
          <div class="bar-segments" style="display: flex; gap: 2px; flex: 1; max-width: 360px;">
            ${segmentsHtml}
          </div>
          ${b.totalLabel ? `<span style="font-size: 12px; font-weight: 600; color: var(--text-secondary);">${b.totalLabel}</span>` : ""}
        </div>
      `;
    });

    return `
      <div class="visual-bar-model-card" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 10px; padding: 14px; margin: 12px 0;">
        <div style="font-size: 12px; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
          <span>📊 Singapore Bar Model</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: normal;">${title || ""}</span>
        </div>
        <div class="bars-container">
          ${barsHtml}
        </div>
        ${bracketText ? `<div style="font-size: 12px; color: var(--success); font-weight: 600; margin-top: 6px; padding-top: 6px; border-top: 1px dashed rgba(255,255,255,0.1);">💡 ${bracketText}</div>` : ""}
        ${note ? `<div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${note}</div>` : ""}
      </div>
    `;
  }

  /**
   * 3-Tier Progressive Hint Component for Math Quiz
   */
  renderHintBox(question) {
    const q = question;
    const heuristicId = q.heuristicId || "constant-part";
    const heuristicInfo = HEURISTIC_CATEGORIES.find(h => h.id === heuristicId) || HEURISTIC_CATEGORIES[0];

    return `
      <div class="heuristic-hint-container" style="margin-top: 14px;">
        <div style="display: flex; gap: 8px; margin-bottom: 10px;">
          <button class="btn btn-outline hint-btn" id="hint-tier-1-btn" style="flex: 1; font-size: 12px; padding: 6px 10px;">
            💡 Hint 1: Strategy
          </button>
          <button class="btn btn-outline hint-btn" id="hint-tier-2-btn" style="flex: 1; font-size: 12px; padding: 6px 10px;">
            🔍 Hint 2: Bar Model
          </button>
          <button class="btn btn-outline hint-btn" id="hint-tier-3-btn" style="flex: 1; font-size: 12px; padding: 6px 10px;">
            🎯 Hint 3: Full Steps
          </button>
        </div>
        <div id="hint-content-pane" style="display: none; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; font-size: 13px; line-height: 1.6;">
        </div>
      </div>
    `;
  }

  attachHintEvents(question, container) {
    const pane = container.querySelector("#hint-content-pane");
    const b1 = container.querySelector("#hint-tier-1-btn");
    const b2 = container.querySelector("#hint-tier-2-btn");
    const b3 = container.querySelector("#hint-tier-3-btn");

    if (!pane || !b1) return;

    const showTier = (tier) => {
      sound.playClick();
      pane.style.display = "block";
      [b1, b2, b3].forEach((btn, idx) => {
        if (idx + 1 === tier) {
          btn.classList.add("active");
          btn.style.borderColor = "var(--primary)";
          btn.style.color = "var(--primary)";
        } else {
          btn.classList.remove("active");
          btn.style.borderColor = "";
          btn.style.color = "";
        }
      });

      if (tier === 1) {
        pane.innerHTML = `
          <div style="color: var(--warning); font-weight: 700; margin-bottom: 4px;">💡 Strategy & Concept Identification:</div>
          <div style="color: var(--text-secondary);">
            This question tests the <strong>${question.topic}</strong> heuristic. 
            Identify what remains constant and express the before-and-after states in equal units!
          </div>
        `;
      } else if (tier === 2) {
        const sampleModel = question.barModel || {
          title: question.topic,
          bars: [
            { name: "Before State", units: 3, color: "#00f2fe" },
            { name: "After State", units: 5, color: "#4facfe", highlightUnits: 2, highlightColor: "#ffd166" }
          ],
          bracketText: "2 units added = Difference in quantity. 1 unit = Difference ÷ 2."
        };
        pane.innerHTML = `
          <div style="color: var(--primary); font-weight: 700; margin-bottom: 4px;">🔍 Visual Model Representation:</div>
          ${this.renderBarModel(sampleModel)}
        `;
      } else if (tier === 3) {
        pane.innerHTML = `
          <div style="color: var(--success); font-weight: 700; margin-bottom: 4px;">🎯 Complete Step-by-Step Model Algebra:</div>
          <div style="color: var(--text-secondary); white-space: pre-line; line-height: 1.8;">
            ${question.explanation}
          </div>
        `;
      }
    };

    b1.addEventListener("click", () => showTier(1));
    b2.addEventListener("click", () => showTier(2));
    b3.addEventListener("click", () => showTier(3));
  }
}

export const heuristicsEngine = new HeuristicsEngine(null);
