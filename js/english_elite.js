/* English Elite Suite: Synthesis & Transformation (S&T) Studio & PSLE Oral Simulator */
import { sound } from "./sound.js";

export const SYNTHESIS_DRILLS = [
  {
    id: "st-1",
    type: "Correlative Inversion",
    promptSentence1: "David entered the house.",
    promptSentence2: "The telephone immediately rang.",
    connector: "No sooner had",
    acceptableAnswers: [
      "no sooner had david entered the house than the telephone rang",
      "no sooner had david entered the house than the telephone rang."
    ],
    rule: "Rule: 'No sooner had' + [Subject] + [Past Participle] + 'than' + [Second clause in simple past]. Never use 'when' or 'then' with 'No sooner'!",
    explanation: "Correct: No sooner had David entered the house than the telephone rang."
  },
  {
    id: "st-2",
    type: "Prepositional Gerund",
    promptSentence1: "Bala was terribly exhausted.",
    promptSentence2: "He continued to complete the final lap of the marathon.",
    connector: "Despite",
    acceptableAnswers: [
      "despite being terribly exhausted, bala continued to complete the final lap of the marathon",
      "despite being terribly exhausted bala continued to complete the final lap of the marathon",
      "despite his terrible exhaustion, bala continued to complete the final lap of the marathon"
    ],
    rule: "Rule: 'Despite' must be followed by a noun or gerund (e.g. 'being exhausted' or 'his exhaustion'). Never write 'Despite of'!",
    explanation: "Correct: Despite being terribly exhausted, Bala continued to complete the final lap of the marathon."
  },
  {
    id: "st-3",
    type: "Conditional Clause",
    promptSentence1: "You do not submit your application today.",
    promptSentence2: "You will not be eligible for the school camp.",
    connector: "Unless",
    acceptableAnswers: [
      "unless you submit your application today, you will not be eligible for the school camp",
      "unless you submit your application today you will not be eligible for the school camp"
    ],
    rule: "Rule: 'Unless' means 'If... not'. The verb following 'unless' becomes positive ('submit'), while the main clause retains the negative condition ('will not be eligible').",
    explanation: "Correct: Unless you submit your application today, you will not be eligible for the school camp."
  },
  {
    id: "st-4",
    type: "Adverbial Inversion",
    promptSentence1: "Mr Tan arrived at the airport.",
    promptSentence2: "He realized he had forgotten his passport.",
    connector: "Only upon",
    acceptableAnswers: [
      "only upon arriving at the airport did mr tan realize that he had forgotten his passport",
      "only upon arriving at the airport did mr tan realize he had forgotten his passport",
      "only upon his arrival at the airport did mr tan realize he had forgotten his passport"
    ],
    rule: "Rule: 'Only upon' + [Gerund / Noun phrase] triggers inversion in the main clause ('did Mr Tan realize').",
    explanation: "Correct: Only upon arriving at the airport did Mr Tan realize he had forgotten his passport."
  },
  {
    id: "st-5",
    type: "Subject-Verb Concord",
    promptSentence1: "The captain was not aware of the change in schedule.",
    promptSentence2: "The players were not aware of the change in schedule.",
    connector: "Neither",
    acceptableAnswers: [
      "neither the captain nor the players were aware of the change in schedule",
      "neither the captain nor the players were aware of the change in schedule."
    ],
    rule: "Rule: With 'Neither... nor', the verb agrees with the closer subject. Since 'the players' is plural, the verb must be 'were'.",
    explanation: "Correct: Neither the captain nor the players were aware of the change in schedule."
  }
];

export const ORAL_SBC_PROMPTS = [
  {
    id: "oral-1",
    title: "Community Recycling & Green Living",
    readingText: "Singapore has made tremendous strides toward sustainability through the Singapore Green Plan 2030. Every citizen, young and old, plays an indispensable role in minimizing waste and conserving precious resources. By recycling diligently and adopting reusable bags, we protect our vibrant city for future generations.",
    stimulusPrompt: "Look at the picture of a neighbourhood recycling drive. Would you take part in this activity? Why or why not?",
    starterFramework: "T-R-E-E-S Framework:\n• Thought: State your stand clearly.\n• Reason: Why recycling in the neighbourhood matters.\n• Example: Personal experience with recycling at home or school.\n• Emotion: How it feels to contribute to the environment.\n• Summary: Concluding recommendation.",
    modelResponse: "Yes, I would definitely participate in this neighbourhood recycling drive. Firstly, improper waste disposal contributes to overflowing landfills like Pulau Semakau. In my school, our eco-club organizes weekly paper collections, which taught me that small actions produce a colossal impact. Participating with neighbours also fosters stronger community bonding while keeping our estate clean."
  },
  {
    id: "oral-2",
    title: "Healthy Lifestyle & Outdoor Fitness",
    readingText: "Maintaining an active lifestyle is paramount for physical endurance and mental well-being. Engaging in regular brisk walking, cycling, or swimming boosts cardiovascular stamina and alleviates academic stress. Healthy habits cultivated during our youth will serve as a resilient foundation throughout our lives.",
    stimulusPrompt: "Look at the poster promoting an inter-class sports carnival. Which event would you be most eager to join?",
    starterFramework: "T-R-E-E-S Framework:\n• Thought: Choose an event (e.g., 4x100m relay or captain's ball).\n• Reason: Importance of teamwork and physical endurance.\n• Example: Prior participation in sports day.\n• Emotion: Thrill of cheering for classmates.\n• Summary: Value of sportsmanship over winning.",
    modelResponse: "I would be most eager to join the 4x100-meter relay. Relays are not merely about individual speed; they require meticulous baton passing and seamless coordination. Last year, my class took part in sports day and although we did not win gold, the camaraderie and encouragement we shared were priceless."
  }
];

export class EnglishEliteSuite {
  constructor(app) {
    this.app = app;
    this.stIdx = 0;
    this.oralIdx = 0;
    this.activeTab = "synthesis"; // 'synthesis' | 'oral'
  }

  render(container) {
    container.innerHTML = `
      <div class="english-suite-wrapper">
        <!-- Tab selector -->
        <div style="display: flex; gap: 10px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
          <button class="btn ${this.activeTab === 'synthesis' ? 'btn-primary' : 'btn-outline'}" id="eng-tab-st">
            🔀 Synthesis & Transformation (S&T) Studio
          </button>
          <button class="btn ${this.activeTab === 'oral' ? 'btn-primary' : 'btn-outline'}" id="eng-tab-oral">
            🎙️ PSLE Oral & Stimulus-Based Conversation (SBC)
          </button>
        </div>

        <div id="eng-tab-content"></div>
      </div>
    `;

    const content = container.querySelector("#eng-tab-content");
    const tabSt = container.querySelector("#eng-tab-st");
    const tabOral = container.querySelector("#eng-tab-oral");

    tabSt.addEventListener("click", () => {
      this.activeTab = "synthesis";
      this.render(container);
    });

    tabOral.addEventListener("click", () => {
      this.activeTab = "oral";
      this.render(container);
    });

    if (this.activeTab === "synthesis") {
      this.renderSynthesis(content);
    } else {
      this.renderOral(content);
    }
  }

  renderSynthesis(container) {
    const drill = SYNTHESIS_DRILLS[this.stIdx];

    container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span class="tag tag-medium">${drill.type}</span>
            <span style="font-size: 12px; color: var(--primary); font-weight: 700;">Question ${this.stIdx + 1} of ${SYNTHESIS_DRILLS.length}</span>
          </div>

          <h3 style="margin-bottom: 12px;">Combine the sentences:</h3>
          
          <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 14px; margin-bottom: 14px;">
            <p style="margin: 0 0 6px 0; color: var(--text-primary); font-size: 14px;"><strong>Sentence 1:</strong> ${drill.promptSentence1}</p>
            <p style="margin: 0; color: var(--text-primary); font-size: 14px;"><strong>Sentence 2:</strong> ${drill.promptSentence2}</p>
          </div>

          <div style="font-size: 14px; font-weight: 700; color: var(--warning); margin-bottom: 14px;">
            Connecting word / phrase: <u>${drill.connector}</u>
          </div>

          <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 10px 14px; font-size: 12px; color: var(--primary);">
            💡 <strong>Key Grammar Rule:</strong><br>${drill.rule}
          </div>

          <div style="display: flex; gap: 10px; margin-top: 16px;">
            <button class="btn btn-outline" id="st-prev-btn" style="flex: 1;">← Previous</button>
            <button class="btn btn-outline" id="st-next-btn" style="flex: 1;">Next Drill →</button>
          </div>
        </div>

        <div class="panel" style="display: flex; flex-direction: column;">
          <h4 style="margin-bottom: 10px;">✍️ Your Transformed Sentence:</h4>
          
          <textarea id="st-input" class="input-text" style="height: 100px; resize: vertical; font-family: inherit; font-size: 14px; line-height: 1.6; padding: 12px; margin-bottom: 12px;" placeholder="Type your full combined sentence here..."></textarea>

          <button class="btn btn-primary" id="st-check-btn" style="width: 100%; margin-bottom: 12px;">
            ✓ Verify Sentence Transformation
          </button>

          <div id="st-feedback-pane" style="display: none; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.6; flex: 1;">
          </div>
        </div>
      </div>
    `;

    const input = container.querySelector("#st-input");
    const checkBtn = container.querySelector("#st-check-btn");
    const feedback = container.querySelector("#st-feedback-pane");

    checkBtn.addEventListener("click", () => {
      const val = input.value.trim().toLowerCase().replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
      const isCorrect = drill.acceptableAnswers.some(ans => {
        const cleanAns = ans.toLowerCase().replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
        return val === cleanAns;
      });

      sound.playClick();
      feedback.style.display = "block";

      if (isCorrect) {
        sound.playCorrect();
        this.app.addXP(20);
        feedback.innerHTML = `
          <div style="color: var(--success); font-weight: 700; font-size: 15px; margin-bottom: 8px;">
            🎉 Correct! Flawless Transformation (AL1 Precision)
          </div>
          <div style="color: var(--text-secondary); margin-bottom: 8px;">${drill.explanation}</div>
        `;
      } else {
        sound.playIncorrect();
        feedback.innerHTML = `
          <div style="color: var(--warning); font-weight: 700; font-size: 15px; margin-bottom: 8px;">
            ⚠️ Almost! Check your word order, tense, or connector pairing:
          </div>
          <div style="background: rgba(255,184,0,0.06); border: 1px solid rgba(255,184,0,0.2); padding: 8px 12px; border-radius: 6px; color: var(--text-primary); font-size: 13px; margin-bottom: 8px;">
            <strong>Target Answer:</strong> ${drill.explanation}
          </div>
          <div style="font-size: 12px; color: var(--text-muted);">${drill.rule}</div>
        `;
      }
    });

    container.querySelector("#st-prev-btn").addEventListener("click", () => {
      this.stIdx = (this.stIdx - 1 + SYNTHESIS_DRILLS.length) % SYNTHESIS_DRILLS.length;
      this.renderSynthesis(container);
    });

    container.querySelector("#st-next-btn").addEventListener("click", () => {
      this.stIdx = (this.stIdx + 1) % SYNTHESIS_DRILLS.length;
      this.renderSynthesis(container);
    });
  }

  renderOral(container) {
    const oral = ORAL_SBC_PROMPTS[this.oralIdx];

    container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <!-- Left: Reading Aloud Passage -->
        <div class="panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span class="tag tag-easy">Part 1: Reading Aloud</span>
            <span style="font-size: 12px; color: var(--primary); font-weight: 700;">Passage ${this.oralIdx + 1}</span>
          </div>
          <h3 style="margin-bottom: 12px;">${oral.title}</h3>
          
          <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 16px; margin-bottom: 14px; font-size: 14.5px; line-height: 1.8; color: var(--text-primary);">
            ${oral.readingText}
          </div>

          <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; font-size: 12px; color: var(--text-secondary);">
            🎙️ <strong>Oral Pacing & Intonation Tips:</strong><br>
            • Pause for 1 second at full stops and half a second at commas.<br>
            • Pronounce end consonants clearly (e.g. <em>strides</em>, <em>waste</em>, <em>vibrant</em>).<br>
            • Vary your pitch and stress important keywords naturally!
          </div>

          <div style="display: flex; gap: 10px; margin-top: 16px;">
            <button class="btn btn-outline" id="oral-prev-btn" style="flex: 1;">← Previous Passage</button>
            <button class="btn btn-outline" id="oral-next-btn" style="flex: 1;">Next Passage →</button>
          </div>
        </div>

        <!-- Right: Stimulus-Based Conversation (SBC) -->
        <div class="panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span class="tag tag-hard">Part 2: Stimulus Conversation</span>
            <span style="font-size: 12px; color: var(--warning); font-weight: 700;">T-R-E-E-S Rubric</span>
          </div>

          <div style="background: rgba(255,184,0,0.08); border: 1px solid rgba(255,184,0,0.25); border-radius: 8px; padding: 14px; margin-bottom: 14px;">
            <strong style="color: var(--warning); font-size: 14px;">🖼️ Examiner Prompt:</strong>
            <p style="margin: 6px 0 0; color: var(--text-primary); font-size: 13.5px; font-weight: 600;">"${oral.stimulusPrompt}"</p>
          </div>

          <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-bottom: 14px;">
            <strong style="color: var(--primary); font-size: 12px;">🌟 AL1 Conversation Framework (T-R-E-E-S):</strong>
            <pre style="margin: 6px 0 0; font-family: inherit; font-size: 12px; color: var(--text-secondary); white-space: pre-line; line-height: 1.6;">${oral.starterFramework}</pre>
          </div>

          <div style="background: rgba(0, 242, 161, 0.06); border: 1px solid rgba(0, 242, 161, 0.2); border-radius: 8px; padding: 12px;">
            <strong style="color: var(--success); font-size: 12px;">🗣️ Model AL1 Spoken Response:</strong>
            <p style="margin: 6px 0 0; color: var(--text-primary); font-size: 13px; line-height: 1.7;">"${oral.modelResponse}"</p>
          </div>
        </div>
      </div>
    `;

    container.querySelector("#oral-prev-btn").addEventListener("click", () => {
      this.oralIdx = (this.oralIdx - 1 + ORAL_SBC_PROMPTS.length) % ORAL_SBC_PROMPTS.length;
      this.renderOral(container);
    });

    container.querySelector("#oral-next-btn").addEventListener("click", () => {
      this.oralIdx = (this.oralIdx + 1) % ORAL_SBC_PROMPTS.length;
      this.renderOral(container);
    });
  }
}
