/* Anti-Cram Mastery Coach — adaptive daily plans, spaced repetition, topic mastery */
import { sound } from "./sound.js";

const STORAGE_KEY = "moe_prep_coach_v1";
const MS_DAY = 24 * 60 * 60 * 1000;

/** SM-2 lite intervals in days after each successful recall */
const SR_INTERVALS = [1, 3, 7, 14, 30, 60];

export class MasteryCoach {
  constructor(app) {
    this.app = app;
    this.pinnedHeuristic = null;
    this.state = this.load();
  }

  load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (_) { /* ignore */ }
    return {
      topicMastery: {},       // "mathematics::Ratio" -> 0-100
      seenIds: [],            // recently practised question ids
      reviewQueue: [],        // spaced repetition cards
      dailyHistory: {},       // YYYY-MM-DD -> { minutes, questions, subjects[] }
      lastPlanDate: null,
      lastPlan: null,
      philosophyAccepted: false
    };
  }

  save() {
    // Cap seenIds to avoid unbounded growth
    if (this.state.seenIds.length > 800) {
      this.state.seenIds = this.state.seenIds.slice(-500);
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
  }

  todayKey() {
    return new Date().toISOString().slice(0, 10);
  }

  pinHeuristic(id) {
    this.pinnedHeuristic = id;
    sound.playCorrect();
  }

  getTopicKey(subject, topic) {
    return `${subject}::${topic}`;
  }

  getTopicMastery(subject, topic) {
    return this.state.topicMastery[this.getTopicKey(subject, topic)] ?? 40;
  }

  /**
   * Record one answered item for mastery + spaced repetition
   */
  recordAnswer({ subject, topic, questionId, correct, difficulty }) {
    if (!subject || !topic) return;

    const key = this.getTopicKey(subject, topic);
    const prev = this.state.topicMastery[key] ?? 40;
    const delta = correct
      ? (difficulty === "Hard" ? 6 : difficulty === "Medium" ? 4 : 3)
      : (difficulty === "Hard" ? -5 : difficulty === "Medium" ? -7 : -8);
    this.state.topicMastery[key] = Math.max(0, Math.min(100, Math.round(prev + delta * 0.85 + (correct ? 1 : -1))));

    if (questionId) {
      if (!this.state.seenIds.includes(questionId)) this.state.seenIds.push(questionId);
    }

    // Spaced repetition queue
    if (questionId) {
      let card = this.state.reviewQueue.find(c => c.id === questionId);
      const now = Date.now();
      if (!card) {
        card = {
          id: questionId,
          subject,
          topic,
          ease: 0,
          due: now + MS_DAY,
          lastResult: correct ? "correct" : "wrong"
        };
        this.state.reviewQueue.push(card);
      }
      if (correct) {
        card.ease = Math.min(SR_INTERVALS.length - 1, (card.ease || 0) + 1);
        card.due = now + SR_INTERVALS[card.ease] * MS_DAY;
        card.lastResult = "correct";
      } else {
        card.ease = 0;
        card.due = now + MS_DAY; // restudy tomorrow, not tonight cram
        card.lastResult = "wrong";
      }
    }

    // Daily history
    const day = this.todayKey();
    if (!this.state.dailyHistory[day]) {
      this.state.dailyHistory[day] = { questions: 0, correct: 0, subjects: [], minutes: 0 };
    }
    this.state.dailyHistory[day].questions += 1;
    if (correct) this.state.dailyHistory[day].correct += 1;
    if (!this.state.dailyHistory[day].subjects.includes(subject)) {
      this.state.dailyHistory[day].subjects.push(subject);
    }

    this.save();
  }

  recordSessionMinutes(mins) {
    const day = this.todayKey();
    if (!this.state.dailyHistory[day]) {
      this.state.dailyHistory[day] = { questions: 0, correct: 0, subjects: [], minutes: 0 };
    }
    this.state.dailyHistory[day].minutes += mins;
    this.save();
  }

  getDueReviews(limit = 8) {
    const now = Date.now();
    return this.state.reviewQueue
      .filter(c => c.due <= now)
      .sort((a, b) => a.due - b.due)
      .slice(0, limit);
  }

  getWeakTopics(limit = 6) {
    const entries = Object.entries(this.state.topicMastery)
      .map(([key, score]) => {
        const [subject, topic] = key.split("::");
        return { key, subject, topic, score };
      })
      .sort((a, b) => a.score - b.score);
    return entries.slice(0, limit);
  }

  getStrongTopics(limit = 4) {
    return Object.entries(this.state.topicMastery)
      .map(([key, score]) => {
        const [subject, topic] = key.split("::");
        return { key, subject, topic, score };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  /**
   * Build a science-based daily plan (no marathon cramming)
   * Target: ~25 focused minutes
   */
  buildDailyPlan() {
    const level = this.app.currentLevel || "P6";
    const due = this.getDueReviews(5);
    const weak = this.getWeakTopics(4);
    const day = this.todayKey();

    const blocks = [];

    // 1. Spaced review first (highest ROI vs cramming)
    if (due.length > 0) {
      blocks.push({
        id: "sr-review",
        type: "spaced_review",
        title: "Spaced Mistake Review",
        minutes: 8,
        count: Math.min(6, due.length),
        why: "Science shows revisiting mistakes after a gap beats same-day re-drilling. This locks learning into long-term memory.",
        icon: "🔁"
      });
    }

    // 2. Weak topic deep work
    const focusSubject = weak[0]?.subject || "mathematics";
    const focusTopic = weak[0]?.topic || null;
    blocks.push({
      id: "weak-focus",
      type: "weak_topic",
      title: focusTopic ? `Focus: ${focusTopic}` : "Adaptive Weak-Spot Drill",
      subject: focusSubject,
      topic: focusTopic,
      minutes: 10,
      count: 8,
      why: focusTopic
        ? `Your mastery in ${focusTopic} is only ${weak[0]?.score ?? 40}%. Short, focused practice beats long mixed cramming.`
        : "We'll detect weak spots as you practise and retarget automatically.",
      icon: "🎯"
    });

    // 3. Interleaved mini-set (prevents illusion of mastery)
    blocks.push({
      id: "interleave",
      type: "interleave",
      title: "Interleaved Mixed Set",
      minutes: 7,
      count: 6,
      subjects: level === "P2" ? ["mathematics", "english", "chinese"] : ["mathematics", "english", "science", "chinese"],
      why: "Mixing subjects forces your brain to choose the right method each time — the opposite of mindless worksheet cramming.",
      icon: "🔀"
    });

    const plan = {
      date: day,
      level,
      totalMinutes: blocks.reduce((s, b) => s + b.minutes, 0),
      blocks,
      mantra: "Short daily mastery > weekend cram marathons. Understanding first, then deliberate practice."
    };

    this.state.lastPlanDate = day;
    this.state.lastPlan = plan;
    this.save();
    return plan;
  }

  getOrBuildPlan() {
    const day = this.todayKey();
    if (this.state.lastPlan && this.state.lastPlanDate === day) return this.state.lastPlan;
    return this.buildDailyPlan();
  }

  async startHeuristicDrill(heuristicId) {
    const level = this.app.currentLevel || "P6";
    const set = await this.app.db.getPracticeSet(level, "mathematics", 10, {
      heuristicId,
      excludeIds: this.state.seenIds.slice(-200)
    });
    if (!set.length) {
      const fallback = await this.app.db.getPracticeSet(level, "mathematics", 10);
      this.app.quiz.startQuiz(fallback, "mathematics", level);
      return;
    }
    this.app.quiz.startQuiz(set, "mathematics", level);
  }

  async startBlock(block) {
    sound.playClick();
    const level = this.app.currentLevel || "P6";
    const mastery = this.state.topicMastery;

    if (block.type === "spaced_review") {
      const due = this.getDueReviews(block.count || 6);
      if (!due.length) {
        alert("No reviews due right now — great job staying on schedule! Try a weak-topic block instead.");
        return;
      }
      // Rebuild full question objects from notebook + db
      const notebook = this.app.notebook?.mistakes || [];
      const fromNotebook = due.map(d => notebook.find(m => m.id === d.id)).filter(Boolean);
      if (fromNotebook.length) {
        this.app.quiz.startWithCustomQuestions(fromNotebook.map(m => ({
          id: m.id,
          topic: m.topic,
          question: m.question,
          options: m.options,
          answer: m.answer,
          explanation: m.explanation,
          type: m.type || "mcq",
          difficulty: "Hard",
          subject: m.subject,
          level: m.level
        })));
        return;
      }
      // Fallback adaptive
      const set = await this.app.db.getAdaptiveSet(level, due[0].subject || "mathematics", block.count || 6, mastery);
      this.app.quiz.startQuiz(set, due[0].subject || "mathematics", level);
      return;
    }

    if (block.type === "weak_topic") {
      const subject = block.subject || "mathematics";
      const options = { topic: block.topic || undefined, excludeIds: this.state.seenIds.slice(-150) };
      let set = await this.app.db.getPracticeSet(level, subject, block.count || 8, options);
      if (set.length < 4) {
        set = await this.app.db.getAdaptiveSet(level, subject, block.count || 8, mastery, this.state.seenIds.slice(-150));
      }
      this.app.quiz.startQuiz(set, subject, level);
      return;
    }

    if (block.type === "interleave") {
      const subjects = block.subjects || ["mathematics", "english", "science", "chinese"];
      const set = await this.app.db.getInterleavedSet(level, subjects, block.count || 6, mastery);
      // Tag subject on each for notebook logging
      set.forEach((q, i) => {
        if (!q.subject) q.subject = subjects[i % subjects.length];
      });
      this.app.quiz.startWithCustomQuestions(set);
      return;
    }

    if (block.type === "topic") {
      const set = await this.app.db.getPracticeSet(level, block.subject, block.count || 10, {
        topic: block.topic,
        excludeIds: this.state.seenIds.slice(-150)
      });
      this.app.quiz.startQuiz(set, block.subject, level);
    }
  }

  async startSmartSession() {
    const plan = this.getOrBuildPlan();
    if (this.app.analytics?.recordSmartSession) {
      this.app.analytics.recordSmartSession();
    }
    // Start first block: prefer spaced review
    const block = plan.blocks[0];
    await this.startBlock(block);
  }

  render(container) {
    if (!container) return;
    const plan = this.getOrBuildPlan();
    const weak = this.getWeakTopics(5);
    const strong = this.getStrongTopics(3);
    const due = this.getDueReviews(20);
    const day = this.state.dailyHistory[this.todayKey()] || { questions: 0, correct: 0, minutes: 0 };
    const accuracy = day.questions ? Math.round((day.correct / day.questions) * 100) : null;

    container.innerHTML = `
      <div class="coach-wrapper">
        <div class="panel coach-hero" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(0,242,161,0.1), rgba(0,242,254,0.12)); border-color: rgba(0,242,161,0.3);">
          <div style="display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; align-items: flex-start;">
            <div style="flex: 1; min-width: 260px;">
              <div class="tag tag-easy" style="margin-bottom: 8px;">Anti-Cram Mastery Coach</div>
              <h2 style="font-size: 24px; margin-bottom: 8px;">Learn once. Remember forever.</h2>
              <p style="color: var(--text-secondary); font-size: 13.5px; line-height: 1.65; max-width: 640px; margin: 0;">
                This coach replaces tuition marathons with <strong>spaced repetition</strong>, <strong>weak-spot targeting</strong>, and
                <strong>interleaved practice</strong> — the same cognitive science top scorers use without cramming the night before.
              </p>
              <p style="margin-top: 10px; font-size: 12px; color: var(--primary); font-weight: 600;">${plan.mantra}</p>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; min-width: 220px;">
              <div class="coach-stat"><div class="coach-stat-val">${plan.totalMinutes}m</div><div class="coach-stat-lbl">Today's Plan</div></div>
              <div class="coach-stat"><div class="coach-stat-val">${due.length}</div><div class="coach-stat-lbl">Reviews Due</div></div>
              <div class="coach-stat"><div class="coach-stat-val">${day.questions}</div><div class="coach-stat-lbl">Done Today</div></div>
              <div class="coach-stat"><div class="coach-stat-val">${accuracy === null ? "—" : accuracy + "%"}</div><div class="coach-stat-lbl">Today Accuracy</div></div>
            </div>
          </div>
          <div style="margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap;">
            <button class="btn btn-primary" id="coach-start-smart">🚀 Start Smart Session (~${plan.blocks[0]?.minutes || 10} min)</button>
            <button class="btn btn-outline" id="coach-rebuild-plan">♻️ Rebuild Today's Plan</button>
            <button class="btn btn-outline" id="coach-parent-report">👨‍👩‍👧 Parent Progress Snapshot</button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px;">
          <div>
            <h3 style="margin-bottom: 12px; font-size: 15px;">Today's Mastery Blocks</h3>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${plan.blocks.map((b, idx) => `
                <div class="panel coach-block" style="border-left: 4px solid var(--primary);">
                  <div style="display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; flex-wrap: wrap;">
                    <div>
                      <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 20px;">${b.icon}</span>
                        <strong style="font-size: 15px;">${idx + 1}. ${b.title}</strong>
                        <span class="tag" style="font-size: 10px;">${b.minutes} min · ${b.count} Qs</span>
                      </div>
                      <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.55; margin: 0; max-width: 520px;">${b.why}</p>
                    </div>
                    <button class="btn btn-primary coach-run-block" data-idx="${idx}" style="font-size: 12px; padding: 8px 14px; white-space: nowrap;">Start Block →</button>
                  </div>
                </div>
              `).join("")}
            </div>

            <div class="panel" style="margin-top: 16px;">
              <h3 style="margin-bottom: 10px; font-size: 14px;">Why this beats tuition cramming</h3>
              <ul style="margin: 0 0 0 18px; color: var(--text-secondary); font-size: 12.5px; line-height: 1.7;">
                <li><strong>Spaced repetition</strong> schedules mistakes for tomorrow/next week — not 50 repeats tonight.</li>
                <li><strong>Interleaving</strong> stops the false confidence you get from doing 20 similar sums in a row.</li>
                <li><strong>Topic mastery meters</strong> show exactly what to fix, so you never waste hours on already-strong topics.</li>
                <li><strong>25-minute daily ceiling</strong> protects sleep and attention — both beat extra worksheets for PSLE scores.</li>
              </ul>
            </div>
          </div>

          <div>
            <div class="panel" style="margin-bottom: 14px;">
              <h3 style="margin-bottom: 12px; font-size: 14px;">Weak Spots (fix first)</h3>
              ${weak.length === 0 ? `<p style="font-size: 12px; color: var(--text-muted);">Practise a few questions and your weak topics will appear here automatically.</p>` : `
                <div style="display: flex; flex-direction: column; gap: 10px;">
                  ${weak.map(w => `
                    <div>
                      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                        <span><strong>${w.topic}</strong> <span style="color: var(--text-muted);">· ${w.subject}</span></span>
                        <span style="color: ${w.score < 50 ? 'var(--error)' : 'var(--warning)'};">${w.score}%</span>
                      </div>
                      <div class="progress-bar-bg" style="height: 6px;"><div class="progress-bar-fill" style="width: ${w.score}%; background: ${w.score < 50 ? 'var(--error)' : 'var(--warning)'};"></div></div>
                    </div>
                  `).join("")}
                </div>
              `}
            </div>

            <div class="panel" style="margin-bottom: 14px;">
              <h3 style="margin-bottom: 12px; font-size: 14px;">Strengths (maintain lightly)</h3>
              ${strong.length === 0 ? `<p style="font-size: 12px; color: var(--text-muted);">Strengths unlock after consistent practice.</p>` : strong.map(s => `
                <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 6px 0; border-bottom: 1px solid var(--border-color);">
                  <span>${s.topic}</span>
                  <span style="color: var(--success); font-weight: 700;">${s.score}%</span>
                </div>
              `).join("")}
            </div>

            <div class="panel" id="coach-parent-panel" style="display: none;">
              <h3 style="margin-bottom: 8px; font-size: 14px;">Parent Snapshot</h3>
              <p style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.6;" id="coach-parent-body"></p>
            </div>
          </div>
        </div>
      </div>
    `;

    container.querySelector("#coach-start-smart")?.addEventListener("click", () => this.startSmartSession());
    container.querySelector("#coach-rebuild-plan")?.addEventListener("click", () => {
      sound.playClick();
      this.buildDailyPlan();
      this.render(container);
    });
    container.querySelectorAll(".coach-run-block").forEach(btn => {
      btn.addEventListener("click", () => {
        const idx = parseInt(btn.dataset.idx, 10);
        this.startBlock(plan.blocks[idx]);
      });
    });
    container.querySelector("#coach-parent-report")?.addEventListener("click", () => {
      sound.playClick();
      const panel = container.querySelector("#coach-parent-panel");
      const body = container.querySelector("#coach-parent-body");
      const days = Object.entries(this.state.dailyHistory).sort((a, b) => b[0].localeCompare(a[0])).slice(0, 7);
      const totalQ = days.reduce((s, [, d]) => s + (d.questions || 0), 0);
      const totalC = days.reduce((s, [, d]) => s + (d.correct || 0), 0);
      const weakTxt = weak.slice(0, 3).map(w => `${w.topic} (${w.score}%)`).join(", ") || "Not enough data yet";
      body.innerHTML = `
        Over the last ${days.length || 1} active day(s), ${this.app.studentName || "your child"} completed
        <strong>${totalQ}</strong> deliberate practice questions
        (${totalQ ? Math.round((totalC / totalQ) * 100) : 0}% accuracy) without marathon cramming.<br><br>
        <strong>Priority topics this week:</strong> ${weakTxt}.<br><br>
        Recommended home routine: one Smart Session (~${plan.totalMinutes} min) after school, then free play.
        Sleep and consistency beat extra tuition worksheets.
      `;
      panel.style.display = "block";
    });
  }
}
