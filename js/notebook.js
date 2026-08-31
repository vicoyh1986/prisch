/* Smart Mistake Notebook (错题本) & Spaced Repetition Mastery Engine */
import { sound } from "./sound.js";

export class MistakeNotebook {
  constructor(app) {
    this.app = app;
    this.storageKey = "moe_prep_mistakes_v2";
    this.mistakes = this.loadMistakes();
    this.bookmarkedIds = new Set(JSON.parse(localStorage.getItem("moe_prep_bookmarks") || "[]"));
    this.activeSubjectFilter = "all";
  }

  loadMistakes() {
    try {
      return JSON.parse(localStorage.getItem(this.storageKey) || "[]");
    } catch (e) {
      return [];
    }
  }

  saveMistakes() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.mistakes));
  }

  saveBookmarks() {
    localStorage.setItem("moe_prep_bookmarks", JSON.stringify(Array.from(this.bookmarkedIds)));
  }

  addMistake(question, studentAnswer, subject, level) {
    if (!question || !question.id) return;

    // Check if already in notebook
    const existingIdx = this.mistakes.findIndex(m => m.id === question.id);
    const entry = {
      id: question.id,
      question: question.question,
      topic: question.topic,
      options: question.options || [],
      answer: question.answer,
      explanation: question.explanation,
      type: question.type,
      studentAnswer: studentAnswer || "",
      subject: subject || "mathematics",
      level: level || "P6",
      timestamp: Date.now(),
      attempts: existingIdx >= 0 ? this.mistakes[existingIdx].attempts + 1 : 1,
      mastered: false
    };

    if (existingIdx >= 0) {
      this.mistakes[existingIdx] = entry;
    } else {
      this.mistakes.unshift(entry);
    }

    this.saveMistakes();
  }

  markAsMastered(id) {
    const item = this.mistakes.find(m => m.id === id);
    if (item) {
      item.mastered = true;
      this.saveMistakes();
      const masteredCount = this.mistakes.filter(m => m.mastered).length;
      if (masteredCount >= 10 && this.app.analytics) {
        this.app.analytics.unlockBadge("mistake-master");
      }
    }
  }

  toggleBookmark(id) {
    if (this.bookmarkedIds.has(id)) {
      this.bookmarkedIds.delete(id);
    } else {
      this.bookmarkedIds.add(id);
    }
    this.saveBookmarks();
  }

  render(container) {
    const filtered = this.mistakes.filter(m => {
      if (this.activeSubjectFilter === "all") return true;
      return m.subject === this.activeSubjectFilter;
    });

    const activeMistakes = filtered.filter(m => !m.mastered);
    const masteredMistakes = filtered.filter(m => m.mastered);

    container.innerHTML = `
      <div class="notebook-wrapper">
        <div class="panel" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(255, 107, 107, 0.08), rgba(255, 184, 0, 0.08)); border-color: rgba(255, 107, 107, 0.25);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
              <h2 style="font-size: 20px; color: var(--text-primary); margin-bottom: 4px;">📖 Smart Mistake Notebook (错题本)</h2>
              <p style="color: var(--text-secondary); font-size: 13px; margin: 0;">Target your weak areas with spaced repetition. Retest and master mistakes until achieving 100% AL1 accuracy.</p>
            </div>
            
            <div style="display: flex; gap: 10px;">
              <button class="btn btn-primary" id="nb-replay-all-btn" ${activeMistakes.length === 0 ? 'disabled' : ''}>
                🔁 Replay Active Mistakes (${activeMistakes.length})
              </button>
            </div>
          </div>
        </div>

        <!-- Subject Filter Pills -->
        <div style="display: flex; gap: 8px; margin-bottom: 16px; overflow-x: auto; padding-bottom: 4px;">
          ${["all", "mathematics", "english", "science", "chinese"].map(sub => `
            <button class="btn-pill ${this.activeSubjectFilter === sub ? 'active' : ''} nb-filter-btn" data-sub="${sub}">
              ${sub === 'all' ? 'All Subjects' : sub.charAt(0).toUpperCase() + sub.slice(1)}
            </button>
          `).join("")}
        </div>

        <!-- Mistake Questions List -->
        <div style="display: flex; flex-direction: column; gap: 14px;" id="nb-items-container">
          ${filtered.length === 0 ? `
            <div class="panel" style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
              <div style="font-size: 32px; margin-bottom: 10px;">🎉</div>
              <h3>No Recorded Mistakes!</h3>
              <p style="font-size: 13px; margin-top: 4px;">Great job! You have no unmastered mistakes in this subject.</p>
            </div>
          ` : filtered.map((m, idx) => `
            <div class="panel nb-card" style="border-left: 4px solid ${m.mastered ? 'var(--success)' : 'var(--error)'}; position: relative;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span class="tag ${m.mastered ? 'tag-easy' : 'tag-hard'}">${m.level} ${m.subject.toUpperCase()}</span>
                  <span style="font-size: 13px; font-weight: 700; color: var(--text-primary);">${m.topic}</span>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span class="tag" style="background: rgba(255,255,255,0.05); color: var(--text-muted); font-size: 10px;">
                    ${m.mastered ? '✓ Mastered' : `Attempts: ${m.attempts}`}
                  </span>
                  <button class="btn-icon nb-star-btn" data-id="${m.id}" title="Bookmark question">
                    ${this.bookmarkedIds.has(m.id) ? '⭐' : '☆'}
                  </button>
                </div>
              </div>

              <div style="font-size: 14px; color: var(--text-primary); line-height: 1.6; margin-bottom: 12px; white-space: pre-line;">
                ${m.question}
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.25); border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; font-size: 13px;">
                <div>
                  <span style="color: var(--error);">Your Previous Answer: <strong>${m.studentAnswer || 'Unanswered'}</strong></span>
                </div>
                <div>
                  <span style="color: var(--success);">Correct Answer: <strong>${m.answer}</strong></span>
                </div>
              </div>

              <div style="background: rgba(0, 242, 254, 0.04); border: 1px solid rgba(0, 242, 254, 0.15); border-radius: 6px; padding: 10px; font-size: 12px; color: var(--text-secondary); line-height: 1.6; white-space: pre-line;">
                <strong>💡 Step-by-Step Model Explanation:</strong>\n${m.explanation}
              </div>

              <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px;">
                ${!m.mastered ? `
                  <button class="btn btn-outline nb-mark-mastered-btn" data-id="${m.id}" style="font-size: 11px; padding: 4px 12px;">
                    ✓ Mark as Mastered
                  </button>
                ` : ''}
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;

    this.attachEvents(container);
  }

  attachEvents(container) {
    container.querySelectorAll(".nb-filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playClick();
        this.activeSubjectFilter = btn.dataset.sub;
        this.render(container);
      });
    });

    container.querySelectorAll(".nb-star-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playClick();
        const id = btn.dataset.id;
        this.toggleBookmark(id);
        this.render(container);
      });
    });

    container.querySelectorAll(".nb-mark-mastered-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        sound.playCorrect();
        const id = btn.dataset.id;
        this.markAsMastered(id);
        this.render(container);
      });
    });

    const replayBtn = container.querySelector("#nb-replay-all-btn");
    if (replayBtn) {
      replayBtn.addEventListener("click", () => {
        const activeMistakes = this.mistakes.filter(m => !m.mastered);
        if (activeMistakes.length > 0) {
          sound.playClick();
          this.app.quiz.startWithCustomQuestions(activeMistakes.map(m => ({
            id: m.id,
            topic: m.topic,
            question: m.question,
            options: m.options,
            answer: m.answer,
            explanation: m.explanation,
            type: m.type,
            difficulty: "Hard"
          })));
          this.app.switchSection("quiz");
        }
      });
    }
  }
}
