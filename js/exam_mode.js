/* Full Singapore Top-School Mock Exam Simulator with OMR Bubble Sheet & AL Scoring */
import { sound } from "./sound.js";
import { confetti } from "./confetti.js";

export const TOP_SCHOOLS = [
  { id: "nyps", name: "Nanyang Primary School (NYPS)", badge: "🦁 Nanyang Prelim", difficulty: "High Rigor (AL1 Standard)" },
  { id: "rgps", name: "Raffles Girls' Primary School (RGPS)", badge: "👑 RGPS Prelim", difficulty: "Elite Problem Solving" },
  { id: "tns", name: "Tao Nan School (TNS)", badge: "🌊 Tao Nan Prelim", difficulty: "Advanced Heuristics" },
  { id: "chs", name: "Catholic High School (CHS)", badge: "⚔️ Catholic High", difficulty: "Conceptual Mastery" },
  { id: "acs", name: "Anglo-Chinese School (ACS)", badge: "🛡️ ACS Junior/Pri", difficulty: "Challenging Applications" }
];

export class MockExamSimulator {
  constructor(app) {
    this.app = app;
    this.currentExam = null;
    this.timerInterval = null;
    this.timeRemaining = 0; // in seconds
    this.currentQIndex = 0;
    this.answers = {};
    this.flagged = {};
  }

  renderLobby(container) {
    this.lobbySubject = this.lobbySubject || this.app.selectedSubject || "mathematics";
    const level = this.app.selectedLevel || this.app.currentLevel || "P6";
    const subjects = level === "P2"
      ? ["mathematics", "english", "chinese"]
      : ["mathematics", "english", "science", "chinese"];

    container.innerHTML = `
      <div class="exam-lobby-wrapper">
        <div class="panel" style="margin-bottom: 20px; background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.05)); border-color: rgba(0, 242, 254, 0.3);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
              <h2 style="font-size: 22px; color: var(--text-primary); margin-bottom: 4px;">🏆 Singapore Top-School Mock Exam Arena</h2>
              <p style="color: var(--text-secondary); font-size: 13px; margin: 0;">Timed OMR prelims with instant AL diagnostics. Use after Smart Coach sessions — mocks measure mastery, they are not a cram tool.</p>
            </div>
            <span class="tag tag-easy" style="font-size: 13px; padding: 6px 14px;">${level} · Official Format</span>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px;">
            ${subjects.map(s => `
              <button class="btn-pill exam-sub-pick ${this.lobbySubject === s ? 'active' : ''}" data-sub="${s}">${s.charAt(0).toUpperCase() + s.slice(1)}</button>
            `).join("")}
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px;" id="school-paper-grid">
          ${TOP_SCHOOLS.map(s => `
            <div class="panel school-paper-card" style="display: flex; flex-direction: column; justify-content: space-between; transition: all 0.2s; border-color: var(--border-color); cursor: pointer;" data-school="${s.id}">
              <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                  <span style="font-weight: 700; color: var(--primary); font-size: 13px;">${s.badge}</span>
                  <span class="tag tag-hard" style="font-size: 10px;">${s.difficulty}</span>
                </div>
                <h3 style="font-size: 16px; margin-bottom: 8px; color: var(--text-primary);">${s.name}</h3>
                <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">15-question timed paper · ${this.lobbySubject} · Booklet A MCQ + Booklet B short answer.</p>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; pt: 10px; border-top: 1px solid var(--border-color); padding-top: 10px;">
                <span style="font-size: 12px; color: var(--text-muted);">⏱️ 20 Minutes</span>
                <button class="btn btn-primary start-exam-btn" data-school="${s.id}" style="font-size: 12px; padding: 6px 14px;">
                  Start Prelim Paper →
                </button>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;

    container.querySelectorAll(".exam-sub-pick").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playClick();
        this.lobbySubject = btn.dataset.sub;
        this.app.selectedSubject = this.lobbySubject;
        this.renderLobby(container);
      });
    });

    container.querySelectorAll(".start-exam-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const schoolId = btn.dataset.school;
        this.startExam(schoolId, container);
      });
    });
  }

  async startExam(schoolId, container) {
    sound.playClick();
    const school = TOP_SCHOOLS.find(s => s.id === schoolId) || TOP_SCHOOLS[0];
    const level = this.app.selectedLevel || this.app.currentLevel || "P6";
    const subject = this.lobbySubject || this.app.selectedSubject || "mathematics";

    const questions = await this.app.db.getRandomQuestions(level, subject, 15);
    if (!questions || questions.length === 0) {
      alert("Unable to load exam questions for this level/subject combination.");
      return;
    }

    this.currentExam = {
      school,
      level,
      subject,
      questions,
      timeLimitMinutes: 20
    };

    this.answers = {};
    this.flagged = {};
    this.currentQIndex = 0;
    this.timeRemaining = 20 * 60; // 20 minutes

    this.renderExamInterface(container);
    this.startTimer(container);
  }

  startTimer(container) {
    if (this.timerInterval) clearInterval(this.timerInterval);

    const timerDisplay = container.querySelector("#exam-timer-display");

    this.timerInterval = setInterval(() => {
      this.timeRemaining--;
      if (this.timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        alert("⏱️ Time is up! Submitting your exam paper for automated AL grading.");
        this.submitExam(container);
        return;
      }

      const mins = Math.floor(this.timeRemaining / 60);
      const secs = this.timeRemaining % 60;
      if (timerDisplay) {
        timerDisplay.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        if (this.timeRemaining <= 300) {
          timerDisplay.style.color = "var(--error)";
          timerDisplay.style.fontWeight = "800";
        }
      }
    }, 1000);
  }

  renderExamInterface(container) {
    const exam = this.currentExam;
    const q = exam.questions[this.currentQIndex];
    const isBookletA = q.type === "mcq";

    container.innerHTML = `
      <div class="exam-active-wrapper" style="display: flex; flex-direction: column; gap: 16px;">
        <!-- Top Exam Status Bar -->
        <div class="panel" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: rgba(15, 23, 42, 0.9);">
          <div>
            <span class="tag tag-easy" style="margin-right: 8px;">${exam.school.name}</span>
            <strong style="color: var(--text-primary); font-size: 14px;">${exam.level} ${exam.subject.toUpperCase()} Prelim</strong>
          </div>
          
          <div style="display: flex; align-items: center; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 6px; background: rgba(0,0,0,0.4); border: 1px solid var(--border-color); padding: 6px 14px; border-radius: 50px;">
              <span>⏱️</span>
              <span id="exam-timer-display" style="font-family: monospace; font-size: 15px; font-weight: 700; color: var(--primary);">20:00</span>
            </div>
            <button class="btn btn-outline" id="exam-flag-btn" style="font-size: 12px; padding: 6px 12px;">
              ${this.flagged[this.currentQIndex] ? "🚩 Flagged" : "🏳️ Flag for Review"}
            </button>
            <button class="btn btn-primary" id="exam-submit-btn" style="font-size: 12px; padding: 6px 16px; background: var(--success); border-color: var(--success);">
              Submit Paper ✓
            </button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 300px; gap: 16px;">
          <!-- Left: Question Sheet -->
          <div class="panel" style="min-height: 400px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span class="tag ${isBookletA ? 'tag-easy' : 'tag-hard'}">
                  ${isBookletA ? 'Booklet A (MCQ)' : 'Booklet B (Structured Short Answer)'}
                </span>
                <span style="font-size: 13px; font-weight: 700; color: var(--text-secondary);">
                  Question ${this.currentQIndex + 1} of ${exam.questions.length}
                </span>
              </div>

              <div style="font-size: 15px; font-weight: 600; color: var(--text-primary); line-height: 1.7; margin-bottom: 20px; white-space: pre-line;">
                ${q.question}
              </div>

              <!-- Question Options or Input -->
              <div class="exam-answers-area">
                ${isBookletA ? `
                  <div style="display: flex; flex-direction: column; gap: 10px;">
                    ${q.options.map((opt, i) => {
                      const isSelected = this.answers[this.currentQIndex] === opt;
                      const optLabel = ["(1)", "(2)", "(3)", "(4)"][i] || `(${i+1})`;
                      return `
                        <div class="exam-option-row ${isSelected ? 'selected' : ''}" data-opt="${opt}" style="display: flex; align-items: center; gap: 12px; background: ${isSelected ? 'rgba(0, 242, 254, 0.15)' : 'rgba(255,255,255,0.03)'}; border: 1px solid ${isSelected ? 'var(--primary)' : 'var(--border-color)'}; border-radius: 8px; padding: 12px 16px; cursor: pointer; transition: all 0.2s;">
                          <div style="width: 28px; height: 28px; border-radius: 50%; border: 1px solid ${isSelected ? 'var(--primary)' : 'rgba(255,255,255,0.3)'}; background: ${isSelected ? 'var(--primary)' : 'transparent'}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 12px; color: ${isSelected ? '#0f172a' : 'var(--text-secondary)'};">
                            ${optLabel}
                          </div>
                          <span style="font-size: 14px; color: var(--text-primary);">${opt}</span>
                        </div>
                      `;
                    }).join("")}
                  </div>
                ` : `
                  <div>
                    <label style="font-size: 12px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px;">Your Final Answer / Working:</label>
                    <input type="text" id="exam-short-input" class="input-text" style="width: 100%; font-size: 14px; padding: 12px;" placeholder="Type your answer here..." value="${this.answers[this.currentQIndex] || ''}">
                  </div>
                `}
              </div>
            </div>

            <!-- Bottom Question Navigation Controls -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-color);">
              <button class="btn btn-outline" id="exam-nav-prev" ${this.currentQIndex === 0 ? 'disabled' : ''}>
                ← Previous Question
              </button>
              <button class="btn btn-primary" id="exam-nav-next">
                ${this.currentQIndex === exam.questions.length - 1 ? 'Review Summary →' : 'Next Question →'}
              </button>
            </div>
          </div>

          <!-- Right: Interactive OMR Bubble Sheet & Question Grid -->
          <div class="panel" style="display: flex; flex-direction: column;">
            <h4 style="margin-bottom: 12px; font-size: 14px; color: var(--text-primary); display: flex; align-items: center; justify-content: space-between;">
              <span>📝 OMR Question Navigator</span>
              <span style="font-size: 11px; color: var(--text-muted);">${Object.keys(this.answers).length} / ${exam.questions.length} Done</span>
            </h4>

            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin-bottom: 16px;">
              ${exam.questions.map((_, i) => {
                const isDone = this.answers[i] !== undefined && this.answers[i] !== "";
                const isFlagged = this.flagged[i];
                const isCurrent = this.currentQIndex === i;

                let bg = "rgba(255,255,255,0.03)";
                let border = "var(--border-color)";
                let color = "var(--text-secondary)";

                if (isCurrent) {
                  border = "var(--primary)";
                  bg = "rgba(0, 242, 254, 0.2)";
                  color = "var(--primary)";
                } else if (isDone) {
                  bg = "rgba(0, 242, 161, 0.15)";
                  border = "rgba(0, 242, 161, 0.4)";
                  color = "var(--success)";
                }

                return `
                  <button class="omr-q-btn" data-index="${i}" style="height: 36px; border-radius: 6px; background: ${bg}; border: 1px solid ${border}; color: ${color}; font-weight: 700; font-size: 12px; cursor: pointer; position: relative; transition: all 0.2s;">
                    ${i + 1}
                    ${isFlagged ? '<span style="position: absolute; top: 1px; right: 2px; font-size: 9px;">🚩</span>' : ''}
                  </button>
                `;
              }).join("")}
            </div>

            <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; font-size: 11px; color: var(--text-muted); line-height: 1.6;">
              <span style="color: var(--success); font-weight: 700;">● Green:</span> Answered<br>
              <span style="color: var(--primary); font-weight: 700;">● Cyan:</span> Current Question<br>
              <span>🚩 Flag: Marked for review</span>
            </div>
          </div>
        </div>
      </div>
    `;

    this.attachExamEvents(container);
  }

  attachExamEvents(container) {
    const isBookletA = this.currentExam.questions[this.currentQIndex].type === "mcq";

    if (isBookletA) {
      container.querySelectorAll(".exam-option-row").forEach(row => {
        row.addEventListener("click", () => {
          sound.playClick();
          const opt = row.dataset.opt;
          this.answers[this.currentQIndex] = opt;
          this.renderExamInterface(container);
        });
      });
    } else {
      const input = container.querySelector("#exam-short-input");
      if (input) {
        input.addEventListener("input", (e) => {
          this.answers[this.currentQIndex] = e.target.value.trim();
        });
      }
    }

    container.querySelectorAll(".omr-q-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playClick();
        this.currentQIndex = parseInt(btn.dataset.index);
        this.renderExamInterface(container);
      });
    });

    const flagBtn = container.querySelector("#exam-flag-btn");
    flagBtn.addEventListener("click", () => {
      sound.playClick();
      this.flagged[this.currentQIndex] = !this.flagged[this.currentQIndex];
      this.renderExamInterface(container);
    });

    const prevBtn = container.querySelector("#exam-nav-prev");
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        if (this.currentQIndex > 0) {
          sound.playClick();
          this.currentQIndex--;
          this.renderExamInterface(container);
        }
      });
    }

    const nextBtn = container.querySelector("#exam-nav-next");
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        sound.playClick();
        if (this.currentQIndex < this.currentExam.questions.length - 1) {
          this.currentQIndex++;
          this.renderExamInterface(container);
        } else {
          // Confirm submit
          if (confirm("Are you sure you want to submit your completed exam paper?")) {
            this.submitExam(container);
          }
        }
      });
    }

    const submitBtn = container.querySelector("#exam-submit-btn");
    submitBtn.addEventListener("click", () => {
      sound.playClick();
      if (confirm("Submit your examination paper for automated AL grading?")) {
        this.submitExam(container);
      }
    });
  }

  submitExam(container) {
    if (this.timerInterval) clearInterval(this.timerInterval);

    const exam = this.currentExam;
    let score = 0;
    const reviewData = [];

    exam.questions.forEach((q, idx) => {
      const userAns = (this.answers[idx] || "").toLowerCase().trim();
      const correctAns = (q.answer || "").toLowerCase().trim();

      let isCorrect = false;
      if (q.type === "mcq") {
        isCorrect = userAns === correctAns;
      } else {
        isCorrect = userAns.includes(correctAns) || correctAns.includes(userAns);
      }

      if (isCorrect) score++;

      // Log incorrect questions to the Mistake Notebook!
      if (!isCorrect && this.app.notebook) {
        this.app.notebook.addMistake(q, userAns, exam.subject, exam.level);
      }

      reviewData.push({
        question: q,
        userAns: this.answers[idx] || "Unattempted",
        correctAns: q.answer,
        isCorrect,
        explanation: q.explanation
      });
    });

    const percentage = Math.round((score / exam.questions.length) * 100);
    
    // Convert to official Singapore MOE PSLE AL Band
    let alBand = "AL8";
    let alColor = "var(--error)";
    if (percentage >= 90) { alBand = "AL1 (Outstanding Mastery)"; alColor = "var(--success)"; }
    else if (percentage >= 85) { alBand = "AL2 (Excellent)"; alColor = "#00f2fe"; }
    else if (percentage >= 80) { alBand = "AL3 (Very Good)"; alColor = "#4facfe"; }
    else if (percentage >= 75) { alBand = "AL4 (Good Progress)"; alColor = "var(--warning)"; }
    else if (percentage >= 65) { alBand = "AL5 (Credit)"; alColor = "#f59e0b"; }
    else if (percentage >= 45) { alBand = "AL6 (Pass)"; alColor = "#f97316"; }
    else if (percentage >= 20) { alBand = "AL7"; alColor = "var(--error)"; }

    if (percentage >= 90) {
      sound.playLevelUp();
      confetti.fire(4000);
    } else if (percentage >= 75) {
      sound.playCorrect();
    } else {
      sound.playIncorrect();
    }

    this.app.recordQuizCompletion(score, exam.questions.length, exam.subject);

    container.innerHTML = `
      <div class="exam-report-card-wrapper" style="display: flex; flex-direction: column; gap: 20px;">
        <div class="panel" style="text-align: center; background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(79, 172, 254, 0.15)); border-color: rgba(0, 242, 254, 0.4); padding: 30px 20px;">
          <span class="tag tag-easy" style="margin-bottom: 12px; font-size: 13px;">${exam.school.name} Diagnostic Report</span>
          <h2 style="font-size: 28px; margin-bottom: 8px;">Examination Results</h2>
          
          <div style="display: flex; justify-content: center; gap: 24px; margin: 20px 0; flex-wrap: wrap;">
            <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px 28px;">
              <div style="font-size: 12px; color: var(--text-muted); text-transform: uppercase;">Raw Score</div>
              <div style="font-size: 32px; font-weight: 800; color: var(--primary);">${score} / ${exam.questions.length}</div>
              <div style="font-size: 13px; color: var(--text-secondary);">${percentage}%</div>
            </div>

            <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px 28px;">
              <div style="font-size: 12px; color: var(--text-muted); text-transform: uppercase;">PSLE Achievement Level</div>
              <div style="font-size: 28px; font-weight: 800; color: ${alColor};">${alBand}</div>
              <div style="font-size: 12px; color: var(--text-muted);">Target: AL4 in total</div>
            </div>
          </div>

          <div style="display: flex; justify-content: center; gap: 12px;">
            <button class="btn btn-primary" id="exam-return-lobby-btn">← Back to Exam Arena</button>
            <button class="btn btn-outline" id="exam-view-notebook-btn">📖 Open Mistake Notebook</button>
          </div>
        </div>

        <!-- Detailed Question Review Breakdown -->
        <div class="panel">
          <h3 style="margin-bottom: 16px;">🔍 Detailed Question Breakdown & Heuristic Explanations:</h3>
          <div style="display: flex; flex-direction: column; gap: 14px;">
            ${reviewData.map((item, idx) => `
              <div style="background: ${item.isCorrect ? 'rgba(0, 242, 161, 0.05)' : 'rgba(255, 107, 107, 0.05)'}; border: 1px solid ${item.isCorrect ? 'rgba(0, 242, 161, 0.25)' : 'rgba(255, 107, 107, 0.25)'}; border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-weight: 700; font-size: 13px; color: var(--text-primary);">Q${idx + 1}. [${item.question.topic}]</span>
                  <span class="tag ${item.isCorrect ? 'tag-easy' : 'tag-hard'}">${item.isCorrect ? '✓ Correct (Full Marks)' : '❌ Incorrect'}</span>
                </div>

                <p style="margin: 0 0 10px 0; color: var(--text-primary); font-size: 13.5px; line-height: 1.6;">${item.question.question}</p>

                <div style="font-size: 12.5px; margin-bottom: 6px;">
                  <strong>Your Answer:</strong> <span style="color: ${item.isCorrect ? 'var(--success)' : 'var(--error)'}; font-weight: 600;">${item.userAns}</span>
                  ${!item.isCorrect ? ` | <strong>Correct Answer:</strong> <span style="color: var(--success); font-weight: 600;">${item.correctAns}</span>` : ''}
                </div>

                <div style="background: rgba(0,0,0,0.2); border-radius: 6px; padding: 10px; font-size: 12px; color: var(--text-secondary); line-height: 1.6; white-space: pre-line;">
                  <strong>💡 Model Working & Strategy:</strong>\n${item.explanation}
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    `;

    container.querySelector("#exam-return-lobby-btn").addEventListener("click", () => {
      this.renderLobby(container);
    });

    container.querySelector("#exam-view-notebook-btn").addEventListener("click", () => {
      this.app.switchSection("notebook");
    });
  }
}
