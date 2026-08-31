/* Student Profile, Real Streaks, Topic Mastery & Gamification */
export const BADGES = [
  { id: "first-step", title: "First Step", desc: "Complete your first practice set", icon: "👣" },
  { id: "streak-master", title: "Streak Master", desc: "Reach a 3-day practice streak", icon: "🔥" },
  { id: "streak-7", title: "Week Warrior", desc: "Maintain a 7-day streak without cramming", icon: "🗓️" },
  { id: "writing-star", title: "Writing Prodigy", desc: "Submit an essay in the PSLE Writing Lab", icon: "✍" },
  { id: "perfect-score", title: "AL1 Perfectionist", desc: "Achieve a 100% score in any practice session", icon: "💯" },
  { id: "syllabus-conqueror", title: "Syllabus Explorer", desc: "Practice all four subjects", icon: "🌍" },
  { id: "anti-cram", title: "Anti-Cram Champion", desc: "Complete 5 Smart Coach sessions", icon: "🧠" },
  { id: "mistake-master", title: "Mistake Master", desc: "Master 10 items in the Mistake Notebook", icon: "📕" }
];

export class AnalyticsManager {
  constructor(app) {
    this.app = app;
    this.xp = 0;
    this.streak = 0;
    this.questionsDone = 0;
    this.questionsCorrect = 0;
    this.essaysWritten = 0;
    this.smartSessions = 0;
    this.lastPracticeDate = null;
    this.subjectsPracticed = [];
    this.activityLog = [];
    this.mastery = {
      english: 0,
      mathematics: 0,
      science: 0,
      chinese: 0
    };
    this.unlockedBadges = [];
    this.loadState();
    this.refreshStreak();
  }

  loadState() {
    const saved = localStorage.getItem("moe_prep_profile_state");
    if (!saved) {
      this.saveState();
      return;
    }
    try {
      const state = JSON.parse(saved);
      // Migrate away from old fake seed defaults if never truly practised
      const looksFake = (state.questionsDone === 42 && state.questionsCorrect === 37 && (state.xp === 450 || state.xp === 0));
      if (looksFake && !(state.activityLog && state.activityLog.length)) {
        this.xp = 0;
        this.streak = 0;
        this.questionsDone = 0;
        this.questionsCorrect = 0;
        this.essaysWritten = 0;
        this.mastery = { english: 0, mathematics: 0, science: 0, chinese: 0 };
        this.unlockedBadges = [];
        this.activityLog = [];
        this.lastPracticeDate = null;
        this.subjectsPracticed = [];
        this.smartSessions = 0;
        this.saveState();
        return;
      }
      this.xp = state.xp ?? 0;
      this.streak = state.streak ?? 0;
      this.questionsDone = state.questionsDone ?? 0;
      this.questionsCorrect = state.questionsCorrect ?? 0;
      this.essaysWritten = state.essaysWritten ?? 0;
      this.mastery = state.mastery ?? this.mastery;
      this.unlockedBadges = state.unlockedBadges ?? [];
      this.activityLog = state.activityLog ?? [];
      this.lastPracticeDate = state.lastPracticeDate ?? null;
      this.subjectsPracticed = state.subjectsPracticed ?? [];
      this.smartSessions = state.smartSessions ?? 0;
    } catch (e) {
      console.error("Could not parse profile state, using defaults", e);
    }
  }

  saveState() {
    const state = {
      xp: this.xp,
      streak: this.streak,
      questionsDone: this.questionsDone,
      questionsCorrect: this.questionsCorrect,
      essaysWritten: this.essaysWritten,
      mastery: this.mastery,
      unlockedBadges: this.unlockedBadges,
      activityLog: this.activityLog.slice(0, 40),
      lastPracticeDate: this.lastPracticeDate,
      subjectsPracticed: this.subjectsPracticed,
      smartSessions: this.smartSessions
    };
    localStorage.setItem("moe_prep_profile_state", JSON.stringify(state));
  }

  todayKey() {
    return new Date().toISOString().slice(0, 10);
  }

  refreshStreak() {
    if (!this.lastPracticeDate) {
      this.streak = 0;
      return;
    }
    const today = this.todayKey();
    const last = this.lastPracticeDate;
    const diff = Math.floor((new Date(today) - new Date(last)) / (24 * 60 * 60 * 1000));
    if (diff > 1) {
      this.streak = 0;
      this.saveState();
    }
  }

  touchStreak() {
    const today = this.todayKey();
    if (this.lastPracticeDate === today) return;
    const last = this.lastPracticeDate;
    if (!last) {
      this.streak = 1;
    } else {
      const diff = Math.floor((new Date(today) - new Date(last)) / (24 * 60 * 60 * 1000));
      if (diff === 1) this.streak += 1;
      else if (diff > 1) this.streak = 1;
      else return;
    }
    this.lastPracticeDate = today;
    if (this.streak >= 3) this.unlockBadge("streak-master");
    if (this.streak >= 7) this.unlockBadge("streak-7");
  }

  addXP(amount) {
    this.xp += amount;
    this.saveState();
    this.app.renderProfileWidgets();
  }

  pushActivity(icon, title) {
    this.activityLog.unshift({
      icon,
      title,
      at: Date.now()
    });
    if (this.activityLog.length > 40) this.activityLog.length = 40;
  }

  formatAgo(ts) {
    const mins = Math.floor((Date.now() - ts) / 60000);
    if (mins < 1) return "Just now";
    if (mins < 60) return `${mins} min ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs} hour${hrs > 1 ? "s" : ""} ago`;
    const days = Math.floor(hrs / 24);
    return `${days} day${days > 1 ? "s" : ""} ago`;
  }

  recordQuiz(score, total, subject) {
    this.questionsDone += total;
    this.questionsCorrect += score;
    const accuracy = total > 0 ? Math.round((score / total) * 100) : 0;

    const currentMastery = this.mastery[subject] || 0;
    const weight = this.questionsDone < 30 ? 0.45 : 0.25;
    this.mastery[subject] = Math.max(0, Math.min(100, Math.round(currentMastery * (1 - weight) + accuracy * weight)));

    this.touchStreak();
    if (subject && !this.subjectsPracticed.includes(subject)) {
      this.subjectsPracticed.push(subject);
    }
    if (this.subjectsPracticed.length >= 4) this.unlockBadge("syllabus-conqueror");
    if (score === total && total > 0) this.unlockBadge("perfect-score");
    if (this.questionsDone >= 1) this.unlockBadge("first-step");

    this.pushActivity("📝", `Scored ${score}/${total} in ${this.app.currentLevel || "P6"} ${subject || "practice"}`);
    this.saveState();
    this.app.renderProfileWidgets();
  }

  recordSmartSession() {
    this.smartSessions += 1;
    if (this.smartSessions >= 5) this.unlockBadge("anti-cram");
    this.pushActivity("🧠", "Completed an Anti-Cram Smart Session");
    this.saveState();
  }

  recordEssay() {
    this.essaysWritten++;
    this.unlockBadge("writing-star");
    this.touchStreak();
    this.pushActivity("✍", "Submitted an essay in Writing Lab");
    this.saveState();
    this.app.renderProfileWidgets();
  }

  unlockBadge(badgeId) {
    if (!this.unlockedBadges.includes(badgeId)) {
      this.unlockedBadges.push(badgeId);
      this.saveState();
      const badge = BADGES.find(b => b.id === badgeId);
      if (badge) this.showBadgeNotification(badge);
    }
  }

  showBadgeNotification(badge) {
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.bottom = "24px";
    container.style.right = "24px";
    container.style.background = "linear-gradient(135deg, var(--bg-sidebar), rgba(0,242,161,0.15))";
    container.style.border = "1px solid var(--success)";
    container.style.borderRadius = "12px";
    container.style.padding = "16px 20px";
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.gap = "14px";
    container.style.boxShadow = "var(--glow-success)";
    container.style.zIndex = "2000";
    container.style.animation = "slideInUp 0.4s ease";

    container.innerHTML = `
      <div style="font-size: 32px;">${badge.icon}</div>
      <div>
        <div style="font-weight: 700; color: var(--success); font-size: 14px;">Achievement Unlocked!</div>
        <div style="font-weight: 600; font-size: 13px; color: var(--text-primary);">${badge.title}</div>
        <div style="font-size: 11px; color: var(--text-muted);">${badge.desc}</div>
      </div>
    `;

    document.body.appendChild(container);
    setTimeout(() => {
      container.style.animation = "slideOutDown 0.4s ease";
      setTimeout(() => container.remove(), 400);
    }, 5000);
  }

  renderDashboardWidgets() {
    const container = document.getElementById("mastery-bars-container");
    if (container) {
      container.innerHTML = "";
      const subjects = [
        { key: "english", label: "English Language", color: "#818cf8" },
        { key: "mathematics", label: "Mathematics", color: "#2dd4bf" },
        { key: "science", label: "Science Concepts", color: "#34d399" },
        { key: "chinese", label: "Chinese Language", color: "#f87171" }
      ];

      subjects.forEach(sub => {
        const val = this.mastery[sub.key] || 0;
        const bar = document.createElement("div");
        bar.innerHTML = `
          <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px; font-weight: 600;">
            <span style="color: var(--text-secondary);">${sub.label}</span>
            <span style="color: ${sub.color};">${val}% Mastery</span>
          </div>
          <div class="progress-bar-bg" style="height: 6px;">
            <div class="progress-bar-fill" style="width: ${val}%; background: ${sub.color};"></div>
          </div>
        `;
        container.appendChild(bar);
      });
    }

    const doneEl = document.getElementById("stats-questions-done");
    const accEl = document.getElementById("stats-avg-accuracy");
    const essayEl = document.getElementById("stats-essays-written");
    if (doneEl) doneEl.innerText = this.questionsDone;
    const avgAccuracy = this.questionsDone > 0 ? Math.round((this.questionsCorrect / this.questionsDone) * 100) : 0;
    if (accEl) accEl.innerText = `${avgAccuracy}%`;
    if (essayEl) essayEl.innerText = this.essaysWritten;

    const goalDone = Math.min(10, this.activityLog.filter(a => {
      const day = new Date(a.at).toISOString().slice(0, 10);
      return day === this.todayKey();
    }).length);
    const frac = document.getElementById("daily-goal-fraction");
    const fill = document.getElementById("daily-goal-fill");
    if (frac) frac.innerText = `${goalDone} / 10 Focus Blocks`;
    if (fill) fill.style.width = `${(goalDone / 10) * 100}%`;

    const log = document.getElementById("activity-log-container");
    if (log) {
      if (!this.activityLog.length) {
        log.innerHTML = `
          <div style="color: var(--text-muted); font-size: 13px; line-height: 1.5;">
            No activity yet. Start a <strong>Smart Session</strong> in the Mastery Coach — 25 focused minutes beats hours of tuition worksheets.
          </div>`;
      } else {
        log.innerHTML = this.activityLog.slice(0, 6).map((a, i) => `
          <div style="display: flex; gap: 10px; padding-bottom: 10px; ${i < 5 ? "border-bottom: 1px solid var(--border-color);" : ""}">
            <span style="font-size: 16px;">${a.icon}</span>
            <div>
              <div style="font-weight: 600;">${a.title}</div>
              <div style="color: var(--text-muted); font-size: 11px;">${this.formatAgo(a.at)}</div>
            </div>
          </div>
        `).join("");
      }
    }

    const weakBox = document.getElementById("dashboard-coach-teaser");
    if (weakBox && this.app.coach) {
      const weak = this.app.coach.getWeakTopics(3);
      weakBox.innerHTML = weak.length
        ? `<strong style="color: var(--warning);">Focus next:</strong> ${weak.map(w => w.topic).join(" · ")}`
        : `<strong style="color: var(--primary);">Ready:</strong> Complete one Smart Session to map your weak spots.`;
    }
  }

  renderAchievementsView() {
    const container = document.getElementById("badges-container");
    if (!container) return;

    container.innerHTML = "";
    BADGES.forEach(badge => {
      const isUnlocked = this.unlockedBadges.includes(badge.id);
      const item = document.createElement("div");
      item.className = `badge-item ${isUnlocked ? "unlocked" : ""}`;
      item.innerHTML = `
        <div class="badge-icon">${badge.icon}</div>
        <div class="badge-title" style="color: ${isUnlocked ? "var(--text-primary)" : "var(--text-muted)"}">${badge.title}</div>
        <div class="badge-desc" style="margin-top: 4px;">${badge.desc}</div>
        <div style="font-size: 10px; color: ${isUnlocked ? "var(--success)" : "var(--text-muted)"}; margin-top: 6px; font-weight: 700;">
          ${isUnlocked ? "UNLOCKED" : "LOCKED"}
        </div>
      `;
      container.appendChild(item);
    });
  }
}
export { BADGES as default };
