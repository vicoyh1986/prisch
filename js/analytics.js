/* Student Profile, Streaks, Gamification & Mastery Indicators */
export const BADGES = [
  { id: "first-step", title: "First Step", desc: "Complete your first practice set", icon: "👣" },
  { id: "streak-master", title: "Streak Master", desc: "Reach a 3-day practice streak", icon: "🔥" },
  { id: "writing-star", title: "Writing Prodigy", desc: "Submit an essay in the PSLE Writing Lab", icon: "✍" },
  { id: "perfect-score", title: "AL1 Perfectionist", desc: "Achieve a 100% score in any practice session", icon: "💯" },
  { id: "syllabus-conqueror", title: "Syllabus Explorer", desc: "Practice all four subjects", icon: "🌍" }
];

export class AnalyticsManager {
  constructor(app) {
    this.app = app;
    this.xp = 0;
    this.streak = 3; // Seed standard streak
    this.questionsDone = 42;
    this.accuracySum = 3696; // 88% avg
    this.essaysWritten = 2;
    
    // Subject mastery caches
    this.mastery = {
      english: 72,
      mathematics: 85,
      science: 64,
      chinese: 68
    };

    this.unlockedBadges = ["first-step", "streak-master"];

    this.loadState();
  }

  loadState() {
    const saved = localStorage.getItem("moe_prep_profile_state");
    if (saved) {
      try {
        const state = JSON.parse(saved);
        this.xp = state.xp ?? 450;
        this.streak = state.streak ?? 3;
        this.questionsDone = state.questionsDone ?? 42;
        this.accuracySum = state.accuracySum ?? 3696;
        this.essaysWritten = state.essaysWritten ?? 2;
        this.mastery = state.mastery ?? this.mastery;
        this.unlockedBadges = state.unlockedBadges ?? this.unlockedBadges;
      } catch (e) {
        console.error("Could not parse profile state, using defaults", e);
      }
    } else {
      this.saveState();
    }
  }

  saveState() {
    const state = {
      xp: this.xp,
      streak: this.streak,
      questionsDone: this.questionsDone,
      accuracySum: this.accuracySum,
      essaysWritten: this.essaysWritten,
      mastery: this.mastery,
      unlockedBadges: this.unlockedBadges
    };
    localStorage.setItem("moe_prep_profile_state", JSON.stringify(state));
  }

  addXP(amount) {
    this.xp += amount;
    this.saveState();
    this.app.renderProfileWidgets();
  }

  recordQuiz(score, total, subject) {
    this.questionsDone += total;
    const accuracy = Math.round((score / total) * 100);
    this.accuracySum += accuracy;
    
    // Update mastery metric
    const currentMastery = this.mastery[subject] || 50;
    this.mastery[subject] = Math.min(100, Math.round(currentMastery * 0.8 + accuracy * 0.2));

    // Check perfect score
    if (score === total) {
      this.unlockBadge("perfect-score");
    }

    // Check conqueror badge (if practicing all 4 subjects)
    // Add logic as needed

    this.saveState();
    this.app.renderProfileWidgets();
  }

  recordEssay() {
    this.essaysWritten++;
    this.unlockBadge("writing-star");
    this.saveState();
    this.app.renderProfileWidgets();
  }

  unlockBadge(badgeId) {
    if (!this.unlockedBadges.includes(badgeId)) {
      this.unlockedBadges.push(badgeId);
      this.saveState();
      
      const badge = BADGES.find(b => b.id === badgeId);
      if (badge) {
        this.showBadgeNotification(badge);
      }
    }
  }

  showBadgeNotification(badge) {
    // Elegant floating non-blocking notification toast
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
    
    // Auto remove
    setTimeout(() => {
      container.style.animation = "slideOutDown 0.4s ease";
      setTimeout(() => container.remove(), 400);
    }, 5000);
  }

  renderDashboardWidgets() {
    // Mastery bars inside Dashboard panel
    const container = document.getElementById("mastery-bars-container");
    if (!container) return;

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

    // Populate summary stats in Dashboard
    document.getElementById("stats-questions-done").innerText = this.questionsDone;
    
    const avgAccuracy = this.questionsDone > 0 ? Math.round(this.accuracySum / (this.questionsDone / 10)) : 88;
    document.getElementById("stats-avg-accuracy").innerText = `${avgAccuracy}%`;
    document.getElementById("stats-essays-written").innerText = this.essaysWritten;

    // Daily progress goal
    const todayGoalDone = this.questionsDone % 10; // Simple cyclical mock goal
    document.getElementById("daily-goal-fraction").innerText = `${todayGoalDone} / 10 Practiced`;
    document.getElementById("daily-goal-fill").style.width = `${(todayGoalDone / 10) * 100}%`;
  }

  renderAchievementsView() {
    const container = document.getElementById("badges-container");
    if (!container) return;

    container.innerHTML = "";
    BADGES.forEach(badge => {
      const isUnlocked = this.unlockedBadges.includes(badge.id);
      const item = document.createElement("div");
      item.className = `badge-item ${isUnlocked ? 'unlocked' : ''}`;
      item.innerHTML = `
        <div class="badge-icon">${badge.icon}</div>
        <div class="badge-title" style="color: ${isUnlocked ? 'var(--text-primary)' : 'var(--text-muted)'}">${badge.title}</div>
        <div class="badge-desc" style="margin-top: 4px;">${badge.desc}</div>
        <div style="font-size: 10px; color: ${isUnlocked ? 'var(--success)' : 'var(--text-muted)'}; margin-top: 6px; font-weight: 700;">
          ${isUnlocked ? 'UNLOCKED' : 'LOCKED'}
        </div>
      `;
      container.appendChild(item);
    });
  }
}
export { BADGES as default };
