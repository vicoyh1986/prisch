/* Interactive Quiz Player with Synthesized Audio, Bar Models, and Mistake Sync */
import { sound } from "./sound.js";
import { confetti } from "./confetti.js";
import { heuristicsEngine } from "./heuristics.js";

export class QuizPlayer {
  constructor(app) {
    this.app = app;
    this.questions = [];
    this.currentIndex = 0;
    this.score = 0;
    this.startTime = 0;
    this.timerInterval = null;
    this.selectedOption = null;
    this.isAnswerSubmitted = false;
    this.currentStreak = 0;
    this.hintTier = 0;

    // Cache DOM Elements
    this.section = document.getElementById("section-quiz");
    this.questionText = document.getElementById("quiz-question-text");
    this.answerArea = document.getElementById("quiz-answer-area");
    this.barModelArea = document.getElementById("quiz-bar-model-area");
    this.hintArea = document.getElementById("quiz-progressive-hint-area");
    this.hintBtn = document.getElementById("quiz-hint-btn");
    this.explanationCard = document.getElementById("quiz-explanation-card");
    this.explanationText = document.getElementById("quiz-explanation-text");
    this.submitBtn = document.getElementById("quiz-submit-btn");
    this.explainBtn = document.getElementById("quiz-explain-btn");
    this.progressFill = document.getElementById("quiz-progress-fill");
    this.questionIndexDisplay = document.getElementById("quiz-question-index");
    this.timerDisplay = document.getElementById("quiz-timer");
    this.topicTag = document.getElementById("quiz-topic-tag");
    this.difficultyTag = document.getElementById("quiz-difficulty-tag");
    this.quitBtn = document.getElementById("quiz-quit-btn");

    this.initEvents();
  }

  initEvents() {
    this.submitBtn.addEventListener("click", () => {
      sound.playClick();
      this.handleSubmit();
    });
    
    this.explainBtn.addEventListener("click", () => {
      sound.playClick();
      this.toggleExplanation();
    });

    if (this.hintBtn) {
      this.hintBtn.addEventListener("click", () => {
        sound.playClick();
        this.revealNextHint();
      });
    }

    this.quitBtn.addEventListener("click", () => {
      sound.playClick();
      if (confirm("Are you sure you want to quit this practice session? Your progress will not be saved.")) {
        this.quitQuiz();
      }
    });
  }

  startQuiz(questions, subject, level) {
    this.questions = questions;
    this.subject = subject;
    this.level = level;
    this.currentIndex = 0;
    this.score = 0;
    this.currentStreak = 0;
    this.isAnswerSubmitted = false;
    this.selectedOption = null;
    this.hintTier = 0;

    this.app.showSection("quiz");
    this.resetQuestionCard();

    this.startTime = Date.now();
    this.startTimer();
    this.renderQuestion();
  }

  startWithCustomQuestions(questions) {
    this.questions = questions;
    this.subject = questions[0]?.subject || "mixed";
    this.level = questions[0]?.level || "P6";
    this.currentIndex = 0;
    this.score = 0;
    this.currentStreak = 0;
    this.isAnswerSubmitted = false;
    this.selectedOption = null;
    this.hintTier = 0;

    this.app.showSection("quiz");
    this.resetQuestionCard();

    this.startTime = Date.now();
    this.startTimer();
    this.renderQuestion();
  }

  resetQuestionCard() {
    this.topicTag.style.display = "";
    this.difficultyTag.style.display = "";
    this.explanationCard.style.display = "none";
    this.explainBtn.style.display = "none";
    if (this.hintBtn) this.hintBtn.style.display = "none";
    if (this.hintArea) this.hintArea.style.display = "none";
    if (this.barModelArea) this.barModelArea.style.display = "none";
    this.submitBtn.innerText = "Submit Answer";
    this.submitBtn.disabled = false;
    this.submitBtn.style.background = "";
    this.submitBtn.onclick = null;
  }

  startTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.timerDisplay.innerText = "00:00";
    this.timerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
      const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
      const secs = String(elapsed % 60).padStart(2, '0');
      this.timerDisplay.innerText = `${mins}:${secs}`;
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  }

  renderQuestion() {
    this.isAnswerSubmitted = false;
    this.selectedOption = null;
    this.hintTier = 0;
    this.resetQuestionCard();

    const q = this.questions[this.currentIndex];

    // Update progress
    const pct = ((this.currentIndex) / this.questions.length) * 100;
    this.progressFill.style.width = `${pct}%`;
    this.questionIndexDisplay.innerText = `Q ${this.currentIndex + 1} / ${this.questions.length}`;

    // Meta details
    this.topicTag.innerText = q.topic;
    this.difficultyTag.innerText = q.difficulty;
    this.difficultyTag.className = `tag tag-${q.difficulty.toLowerCase()}`;

    // Question content
    this.questionText.innerText = q.question;

    // Check for Bar Model rendering
    if (this.barModelArea) {
      if (q.barModel) {
        this.barModelArea.innerHTML = heuristicsEngine.renderBarModel(q.barModel);
        this.barModelArea.style.display = "block";
      } else {
        this.barModelArea.style.display = "none";
      }
    }

    // Check for Heuristic Hints
    if (this.hintBtn && (q.heuristicId || q.explanation)) {
      this.hintBtn.style.display = "inline-block";
      this.hintBtn.innerText = "💡 Reveal Strategy Hint (Tier 1)";
    }

    // Build choices or text input depending on answer type
    this.answerArea.innerHTML = "";
    if (q.type === "mcq") {
      const list = document.createElement("div");
      list.className = "options-list";
      q.options.forEach((opt) => {
        const btn = document.createElement("button");
        btn.className = "option-btn";
        btn.innerText = opt;
        btn.addEventListener("click", () => {
          sound.playClick();
          this.selectOption(btn, opt);
        });
        list.appendChild(btn);
      });
      this.answerArea.appendChild(list);
    } else {
      const div = document.createElement("div");
      div.className = "short-answer-container";
      const input = document.createElement("input");
      input.type = "text";
      input.className = "input-text";
      input.id = "quiz-short-answer-input";
      input.placeholder = "Type your answer here...";
      input.autocomplete = "off";
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") this.handleSubmit();
      });
      div.appendChild(input);
      this.answerArea.appendChild(div);
      input.focus();
    }
  }

  revealNextHint() {
    const q = this.questions[this.currentIndex];
    this.hintTier++;
    if (this.hintArea) {
      this.hintArea.innerHTML = heuristicsEngine.renderProgressiveHints(q, this.hintTier);
      this.hintArea.style.display = "block";
    }

    if (this.hintTier === 1) {
      this.hintBtn.innerText = "🔍 Reveal Model Framework (Tier 2)";
    } else if (this.hintTier === 2) {
      this.hintBtn.innerText = "📝 Reveal Step-by-Step Algebra (Tier 3)";
    } else {
      this.hintBtn.innerText = "✓ All 3 Hint Tiers Revealed";
      this.hintBtn.disabled = true;
    }
  }

  selectOption(element, value) {
    if (this.isAnswerSubmitted) return;
    
    const active = this.answerArea.querySelector(".option-btn.selected");
    if (active) active.classList.remove("selected");

    element.classList.add("selected");
    this.selectedOption = value;
  }

  handleSubmit() {
    if (this.isAnswerSubmitted) {
      this.nextQuestion();
      return;
    }

    const q = this.questions[this.currentIndex];
    let userAns = "";
    let isCorrect = false;

    if (q.type === "mcq") {
      if (this.selectedOption === null) {
        alert("Please select an option before submitting!");
        return;
      }
      userAns = this.selectedOption;
      isCorrect = (userAns === q.answer);

      const btns = this.answerArea.querySelectorAll(".option-btn");
      btns.forEach(btn => {
        if (btn.innerText === q.answer) {
          btn.classList.add("correct");
        } else if (btn.innerText === userAns) {
          btn.classList.add("incorrect");
        }
      });
    } else {
      const input = document.getElementById("quiz-short-answer-input");
      if (!input) return;
      userAns = input.value.trim().toLowerCase();
      if (!userAns) {
        alert("Please input an answer before submitting!");
        return;
      }
      
      const cleanAnswer = q.answer.trim().toLowerCase();
      isCorrect = (userAns === cleanAnswer || cleanAnswer.includes(userAns) || userAns.includes(cleanAnswer));

      input.disabled = true;
      if (isCorrect) {
        input.style.borderColor = "var(--success)";
        input.style.backgroundColor = "rgba(0, 242, 161, 0.05)";
        input.style.color = "var(--success)";
      } else {
        input.style.borderColor = "var(--error)";
        input.style.backgroundColor = "rgba(255, 75, 114, 0.05)";
        input.style.color = "var(--error)";
        
        const tip = document.createElement("div");
        tip.style.fontSize = "13px";
        tip.style.color = "var(--success)";
        tip.style.marginTop = "8px";
        tip.innerHTML = `Target Answer: <strong>${q.answer}</strong>`;
        this.answerArea.appendChild(tip);
      }
    }

    this.isAnswerSubmitted = true;
    this.explainBtn.style.display = "inline-block";
    this.showExplanation(q.explanation);

    if (isCorrect) {
      this.score++;
      this.currentStreak++;
      if (this.currentStreak >= 3) {
        sound.playStreak(this.currentStreak);
      } else {
        sound.playCorrect();
      }

      this.app.addXP(10);
      this.submitBtn.innerText = "Correct! Next →";
      this.submitBtn.style.background = "linear-gradient(135deg, var(--success), #059669)";
    } else {
      this.currentStreak = 0;
      sound.playIncorrect();

      // Log to Mistake Notebook
      if (this.app.notebook) {
        this.app.notebook.addMistake(q, userAns, this.subject, this.level);
      }

      this.submitBtn.innerText = "Incorrect. Next →";
      this.submitBtn.style.background = "linear-gradient(135deg, var(--error), #dc2626)";
    }
  }

  showExplanation(text) {
    this.explanationText.innerText = text || "No explanation provided for this question.";
    this.explanationCard.style.display = "block";
  }

  toggleExplanation() {
    const isVisible = (this.explanationCard.style.display === "block");
    this.explanationCard.style.display = isVisible ? "none" : "block";
  }

  nextQuestion() {
    this.submitBtn.style.background = "";
    this.currentIndex++;
    if (this.currentIndex < this.questions.length) {
      this.renderQuestion();
    } else {
      this.finishQuiz();
    }
  }

  finishQuiz() {
    this.stopTimer();
    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
    const mins = Math.floor(elapsed / 60);
    const secs = elapsed % 60;
    
    this.progressFill.style.width = "100%";
    this.app.recordQuizCompletion(this.score, this.questions.length, this.subject);

    const accuracy = Math.round((this.score / this.questions.length) * 100);
    const xpGained = this.score * 10 + (this.score === this.questions.length ? 50 : 0);

    // Audio & Confetti Celebrations
    if (accuracy >= 90) {
      sound.playLevelUp();
      confetti.fire(3500);
    } else if (accuracy >= 70) {
      sound.playCorrect();
    }

    this.topicTag.style.display = "none";
    this.difficultyTag.style.display = "none";
    if (this.hintBtn) this.hintBtn.style.display = "none";
    if (this.hintArea) this.hintArea.style.display = "none";
    if (this.barModelArea) this.barModelArea.style.display = "none";
    this.questionIndexDisplay.innerText = "Practice Complete!";
    
    this.questionText.innerHTML = `
      <div style="text-align: center; display: flex; flex-direction: column; gap: 20px;">
        <div style="font-size: 64px;">${accuracy >= 90 ? '🌟' : '🏆'}</div>
        <h2>${accuracy >= 90 ? 'Outstanding AL1 Performance!' : 'Practice Session Complete!'}</h2>
        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto; font-size: 15px;">
          ${accuracy >= 90 ? 'You demonstrated flawless mastery matching Singapore MOE top-school distinction standard!' : 'Great effort! Review any mistakes in your Mistake Notebook to achieve 100% precision.'}
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 12px 0;">
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 14px; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: 800; color: var(--primary);">${this.score} / ${this.questions.length}</div>
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Correct Answers</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 14px; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: 800; color: ${accuracy >= 90 ? 'var(--success)' : 'var(--warning)'};">${accuracy}%</div>
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Accuracy</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 14px; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: 800; color: var(--success);">+${xpGained} XP</div>
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">XP Gained</div>
          </div>
        </div>

        <p style="font-size: 13px; color: var(--text-muted);">Time Taken: ${mins}m ${secs}s</p>
      </div>
    `;

    this.answerArea.innerHTML = "";
    this.explanationCard.style.display = "none";
    this.explainBtn.style.display = "none";

    this.submitBtn.innerText = "Back to Dashboard";
    this.submitBtn.style.background = "";
    this.isAnswerSubmitted = true;

    this.submitBtn.onclick = () => {
      this.resetQuestionCard();
      this.app.showSection("dashboard");
    };
  }

  quitQuiz() {
    this.stopTimer();
    this.resetQuestionCard();
    this.app.showSection("dashboard");
  }
}
