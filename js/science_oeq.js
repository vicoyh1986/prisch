/* Science Claim-Evidence-Reasoning (C-E-R) Diagnostic Evaluator for PSLE Section B */
import { sound } from "./sound.js";

export const SCIENCE_OEQ_QUESTIONS = [
  {
    id: "oeq-heat-1",
    theme: "Energy (Heat)",
    level: "P4-P6",
    title: "Heat Conduction in Dual-Material Cups",
    scenario: "Ali poured 200 ml of boiling water at 100°C into Cup A (made of stainless steel) and Cup B (made of styrofoam). After 15 minutes, the temperature of water in Cup A was 52°C while in Cup B it was 84°C.",
    question: "Based on the experiment, explain why the water in Cup B remained hotter than Cup A.",
    maxMarks: 2,
    rubric: {
      conceptKeywords: ["poor conductor of heat", "poorer conductor", "insulator of heat", "conductor of heat"],
      evidenceKeywords: ["cup b", "84°c", "52°c", "higher temperature", "water in cup b"],
      reasoningKeywords: ["conducts heat slower", "lost heat slower", "at a slower rate", "slower rate of heat loss", "retards heat loss"]
    },
    modelAnswer: "Styrofoam is a poorer conductor of heat than stainless steel. Therefore, the water in Cup B lost heat to the cooler surrounding air at a slower rate than in Cup A.",
    markingTips: "MOE Rule: Must compare both materials (poorer conductor / slower rate). Stating only 'Styrofoam is an insulator' gets 0m without comparison!"
  },
  {
    id: "oeq-plants-1",
    theme: "Systems (Photosynthesis)",
    level: "P5-P6",
    title: "Light Intensity on Aquatic Plants",
    scenario: "An aquatic plant in a beaker of water was placed under a lamp. When the lamp was 10 cm away, 48 oxygen bubbles per minute were produced. When the lamp was moved to 60 cm away, only 8 bubbles were produced per minute.",
    question: "Explain why moving the lamp further away caused the number of bubbles to decrease.",
    maxMarks: 2,
    rubric: {
      conceptKeywords: ["photosynthesis", "rate of photosynthesis", "light intensity", "traps light", "chlorophyll"],
      evidenceKeywords: ["lamp further away", "distance increased", "bubbles decreased", "8 bubbles"],
      reasoningKeywords: ["less light", "lower light intensity", "slower rate of photosynthesis", "decreased rate of photosynthesis", "less oxygen"]
    },
    modelAnswer: "Increasing the distance of the lamp reduced the light intensity reaching the plant. This decreased the rate of photosynthesis, producing fewer oxygen bubbles per minute.",
    markingTips: "MOE Rule: Must link distance to 'light intensity' and then to 'rate of photosynthesis'!"
  },
  {
    id: "oeq-forces-1",
    theme: "Interactions (Forces)",
    level: "P6",
    title: "Friction & Surface Textures",
    scenario: "A 5 kg wooden block was pulled across two surfaces: Surface X (sandpaper) and Surface Y (polished marble). The spring balance showed 45 N on Surface X and 12 N on Surface Y.",
    question: "Explain why more force was needed to pull the block across Surface X.",
    maxMarks: 2,
    rubric: {
      conceptKeywords: ["frictional force", "friction", "roughness", "rougher"],
      evidenceKeywords: ["surface x", "sandpaper", "45 n", "12 n", "marble"],
      reasoningKeywords: ["rougher surface", "greater frictional force", "opposes motion", "more friction between"]
    },
    modelAnswer: "Surface X is rougher than Surface Y, creating a greater frictional force between the block and the surface that opposes motion. Hence, more pulling force was needed to overcome the friction.",
    markingTips: "MOE Rule: Always identify the specific force ('frictional force') and direction ('opposes motion')!"
  },
  {
    id: "oeq-evap-1",
    theme: "Cycles (Water Cycle)",
    level: "P5-P6",
    title: "Exposed Surface Area & Evaporation",
    scenario: "Container P (diameter 10 cm) and Container Q (diameter 25 cm) were filled with 100 ml of water each and placed in the same room. After 4 hours, Container Q had 30 ml left while Container P had 75 ml left.",
    question: "Explain why more water evaporated from Container Q than Container P.",
    maxMarks: 2,
    rubric: {
      conceptKeywords: ["exposed surface area", "rate of evaporation", "evaporated", "water molecules"],
      evidenceKeywords: ["container q", "larger diameter", "30 ml left", "container p"],
      reasoningKeywords: ["larger exposed surface area", "evaporated faster", "at a faster rate", "gain heat and evaporate faster"]
    },
    modelAnswer: "Container Q has a larger exposed surface area in contact with the surrounding air than Container P. This increases the rate of evaporation, causing water to evaporate faster.",
    markingTips: "MOE Rule: Must use the exact phrase 'exposed surface area' rather than just 'surface area' or 'size'!"
  }
];

export class ScienceOEQStudio {
  constructor(app) {
    this.app = app;
    this.currentIdx = 0;
  }

  renderStudio(container) {
    const q = SCIENCE_OEQ_QUESTIONS[this.currentIdx];

    container.innerHTML = `
      <div class="science-oeq-wrapper" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <!-- Left: Question & Experiment Card -->
        <div class="panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span class="tag tag-easy">${q.theme}</span>
            <span style="font-size: 12px; color: var(--primary); font-weight: 700;">[ ${q.maxMarks} Marks ]</span>
          </div>
          <h3 style="color: var(--text-primary); margin-bottom: 10px;">${q.title}</h3>
          
          <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 14px; margin-bottom: 14px; line-height: 1.6; font-size: 13.5px; color: var(--text-secondary);">
            <strong>🔬 Experimental Setup:</strong><br>
            ${q.scenario}
          </div>

          <div style="font-weight: 700; color: var(--text-primary); margin-bottom: 14px; font-size: 14px;">
            Question: ${q.question}
          </div>

          <div style="background: rgba(255, 184, 0, 0.06); border: 1px solid rgba(255, 184, 0, 0.2); border-radius: 8px; padding: 10px 14px; font-size: 12px; color: var(--warning); line-height: 1.5;">
            <strong>⚠️ Official MOE PSLE Marker Tip:</strong><br>
            ${q.markingTips}
          </div>

          <!-- Navigation buttons -->
          <div style="display: flex; gap: 10px; margin-top: 16px;">
            <button class="btn btn-outline" id="oeq-prev-btn" style="flex: 1;">← Previous</button>
            <button class="btn btn-outline" id="oeq-next-btn" style="flex: 1;">Next Case →</button>
          </div>
        </div>

        <!-- Right: Student Answering & Live C-E-R Analyzer -->
        <div class="panel" style="display: flex; flex-direction: column;">
          <h4 style="margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
            <span>✍️ Your Scientific Explanation (C-E-R)</span>
            <span id="oeq-word-count" style="font-size: 11px; color: var(--text-muted);">0 words</span>
          </h4>
          
          <textarea id="oeq-answer-input" class="input-text" style="height: 130px; resize: vertical; font-family: inherit; font-size: 13px; line-height: 1.6; padding: 12px; margin-bottom: 12px;" placeholder="Write your full C-E-R explanation here... (e.g., [Concept] + [Evidence] + [Reasoning])"></textarea>

          <!-- Live C-E-R Checklist Cards -->
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 14px;">
            <div id="cer-badge-concept" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; padding: 8px; text-align: center;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">1. Concept</div>
              <div class="cer-status" style="font-size: 12px; font-weight: 700; color: var(--error);">❌ Missing</div>
            </div>
            <div id="cer-badge-evidence" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; padding: 8px; text-align: center;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">2. Evidence</div>
              <div class="cer-status" style="font-size: 12px; font-weight: 700; color: var(--error);">❌ Missing</div>
            </div>
            <div id="cer-badge-reasoning" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; padding: 8px; text-align: center;">
              <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">3. Reasoning</div>
              <div class="cer-status" style="font-size: 12px; font-weight: 700; color: var(--error);">❌ Missing</div>
            </div>
          </div>

          <button class="btn btn-primary" id="oeq-evaluate-btn" style="width: 100%; margin-bottom: 12px;">
            🎯 Grade My C-E-R Answer
          </button>

          <!-- Diagnostic Feedback Output -->
          <div id="oeq-feedback-pane" style="display: none; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.6; flex: 1;">
          </div>
        </div>
      </div>
    `;

    this.attachEvents(container, q);
  }

  attachEvents(container, q) {
    const input = container.querySelector("#oeq-answer-input");
    const countDisplay = container.querySelector("#oeq-word-count");
    const evalBtn = container.querySelector("#oeq-evaluate-btn");
    const feedbackPane = container.querySelector("#oeq-feedback-pane");

    const badgeConcept = container.querySelector("#cer-badge-concept");
    const badgeEvidence = container.querySelector("#cer-badge-evidence");
    const badgeReasoning = container.querySelector("#cer-badge-reasoning");

    const updateLiveChecklist = () => {
      const text = input.value.toLowerCase().trim();
      const words = text ? text.split(/\s+/).length : 0;
      countDisplay.innerText = `${words} words`;

      const hasConcept = q.rubric.conceptKeywords.some(k => text.includes(k.toLowerCase()));
      const hasEvidence = q.rubric.evidenceKeywords.some(k => text.includes(k.toLowerCase()));
      const hasReasoning = q.rubric.reasoningKeywords.some(k => text.includes(k.toLowerCase()));

      const setBadge = (el, passed) => {
        const status = el.querySelector(".cer-status");
        if (passed) {
          el.style.borderColor = "var(--success)";
          el.style.background = "rgba(0, 242, 161, 0.08)";
          status.innerText = "✓ Detected";
          status.style.color = "var(--success)";
        } else {
          el.style.borderColor = "var(--border-color)";
          el.style.background = "rgba(255,255,255,0.03)";
          status.innerText = "❌ Missing";
          status.style.color = "var(--error)";
        }
      };

      setBadge(badgeConcept, hasConcept);
      setBadge(badgeEvidence, hasEvidence);
      setBadge(badgeReasoning, hasReasoning);

      return { hasConcept, hasEvidence, hasReasoning };
    };

    input.addEventListener("input", updateLiveChecklist);

    evalBtn.addEventListener("click", () => {
      const text = input.value.trim();
      if (!text) {
        alert("Please write your answer before submitting for evaluation!");
        return;
      }

      const { hasConcept, hasEvidence, hasReasoning } = updateLiveChecklist();
      let awardedMarks = 0;
      if (hasConcept) awardedMarks += 1;
      if (hasEvidence && hasReasoning) awardedMarks += 1;
      else if (hasReasoning) awardedMarks += 0.5;

      sound.playClick();
      if (awardedMarks === q.maxMarks) {
        sound.playCorrect();
      } else {
        sound.playIncorrect();
      }

      feedbackPane.style.display = "block";
      feedbackPane.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <strong style="font-size: 15px; color: ${awardedMarks === q.maxMarks ? 'var(--success)' : 'var(--warning)'};">
            Score: ${awardedMarks} / ${q.maxMarks} Marks ${awardedMarks === q.maxMarks ? '🏆 (AL1 Standard!)' : '⚠️'}
          </strong>
        </div>

        <div style="margin-bottom: 10px; color: var(--text-secondary);">
          ${awardedMarks === q.maxMarks 
            ? "🌟 <strong>Outstanding!</strong> You included all required scientific concepts, comparative evidence, and directional reasoning required for full marks." 
            : "🔍 <strong>Examiner Feedback:</strong> To reach full 2/2 marks, make sure you compare both setups and use comparative keywords (e.g. 'slower rate of heat loss', 'greater friction')."}
        </div>

        <div style="background: rgba(0, 242, 161, 0.06); border: 1px solid rgba(0, 242, 161, 0.2); border-radius: 6px; padding: 10px; margin-top: 8px;">
          <strong style="color: var(--success); font-size: 12px;">📋 PSLE Standard Model Answer:</strong>
          <p style="margin: 4px 0 0; color: var(--text-primary); font-size: 13px;">${q.modelAnswer}</p>
        </div>
      `;

      if (awardedMarks === q.maxMarks) {
        this.app.addXP(25);
      }
    });

    container.querySelector("#oeq-prev-btn").addEventListener("click", () => {
      this.currentIdx = (this.currentIdx - 1 + SCIENCE_OEQ_QUESTIONS.length) % SCIENCE_OEQ_QUESTIONS.length;
      this.renderStudio(container);
    });

    container.querySelector("#oeq-next-btn").addEventListener("click", () => {
      this.currentIdx = (this.currentIdx + 1) % SCIENCE_OEQ_QUESTIONS.length;
      this.renderStudio(container);
    });
  }
}
