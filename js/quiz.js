/* Interactive Quiz Player and self-marking system */
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

    // Cache DOM Elements
    this.section = document.getElementById("section-quiz");
    this.questionText = document.getElementById("quiz-question-text");
    this.answerArea = document.getElementById("quiz-answer-area");
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
    this.submitBtn.addEventListener("click", () => this.handleSubmit());
    this.explainBtn.addEventListener("click", () => this.toggleExplanation());
    this.quitBtn.addEventListener("click", () => {
      if (confirm("Are you sure you want to quit this practice session? Your progress will not be saved.")) {
        this.quitQuiz();
      }
    });
  }

  /**
   * Initializes and starts a new practice quiz session
   */
  startQuiz(questions, subject, level) {
    this.questions = questions;
    this.subject = subject;
    this.level = level;
    this.currentIndex = 0;
    this.score = 0;
    this.isAnswerSubmitted = false;
    this.selectedOption = null;

    this.app.showSection("quiz");
    this.explanationCard.style.display = "none";
    this.explainBtn.style.display = "none";
    this.submitBtn.innerText = "Submit Answer";
    this.submitBtn.disabled = false;

    // Start Timer
    this.startTime = Date.now();
    this.startTimer();

    this.renderQuestion();
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
    this.explanationCard.style.display = "none";
    this.explainBtn.style.display = "none";
    this.submitBtn.innerText = "Submit Answer";
    this.submitBtn.disabled = false;

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

    // Build choices or text input depending on answer type
    this.answerArea.innerHTML = "";
    if (q.type === "mcq") {
      const list = document.createElement("div");
      list.className = "options-list";
      q.options.forEach((opt, idx) => {
        const btn = document.createElement("button");
        btn.className = "option-btn";
        btn.innerText = opt;
        btn.addEventListener("click", () => this.selectOption(btn, opt));
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

  selectOption(element, value) {
    if (this.isAnswerSubmitted) return;
    
    // De-select current
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

      // Render styles
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
      isCorrect = (userAns === cleanAnswer);

      // Render styles
      input.disabled = true;
      if (isCorrect) {
        input.style.borderColor = "var(--success)";
        input.style.backgroundColor = "rgba(0, 242, 161, 0.05)";
        input.style.color = "var(--success)";
      } else {
        input.style.borderColor = "var(--error)";
        input.style.backgroundColor = "rgba(255, 75, 114, 0.05)";
        input.style.color = "var(--error)";
        // Show correct answer below
        const tip = document.createElement("div");
        tip.style.fontSize = "13px";
        tip.style.color = "var(--success)";
        tip.style.marginTop = "8px";
        tip.innerHTML = `Correct Answer: <strong>${q.answer}</strong>`;
        this.answerArea.appendChild(tip);
      }
    }

    this.isAnswerSubmitted = true;
    this.explainBtn.style.display = "block";
    this.showExplanation(q.explanation);

    if (isCorrect) {
      this.score++;
      this.app.addXP(10); // Reward XP
      this.submitBtn.innerText = "Correct! Next →";
      this.submitBtn.style.background = "linear-gradient(135deg, var(--success), #059669)";
    } else {
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
    // Reset submit button styling
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
    
    // Save quiz results
    this.app.recordQuizCompletion(this.score, this.questions.length, this.subject);

    // Calculate accuracy
    const accuracy = Math.round((this.score / this.questions.length) * 100);
    const xpGained = this.score * 10 + (this.score === this.questions.length ? 50 : 0); // Perfect score bonus

    // Render summary UI
    this.topicTag.style.display = "none";
    this.difficultyTag.style.display = "none";
    this.questionIndexDisplay.innerText = "Practice Complete!";
    
    this.questionText.innerHTML = `
      <div style="text-align: center; display: flex; flex-direction: column; gap: 20px;">
        <div style="font-size: 64px;">🏆</div>
        <h2>Practice Completed!</h2>
        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto; font-size: 15px;">Excellent effort! You have completed your level ${this.level} ${this.subject} practice set.</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 12px 0;">
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 14px; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: 800; color: var(--primary);">${this.score} / ${this.questions.length}</div>
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Correct Answers</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 14px; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: 800; color: var(--warning);">${accuracy}%</div>
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
    this.isAnswerSubmitted = true; // Set to true so next click hits the return path

    // Override submit action
    this.submitBtn.onclick = () => {
      // Restore state
      this.topicTag.style.display = "";
      this.difficultyTag.style.display = "";
      this.submitBtn.onclick = null; // remove override
      this.app.showSection("dashboard");
    };
  }

  quitQuiz() {
    this.stopTimer();
    this.app.showSection("dashboard");
  }
}
