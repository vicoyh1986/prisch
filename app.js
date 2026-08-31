/* Central Application State Manager & Router - Singapore AL1 Anti-Cram Suite */
import { DatabaseManager } from "./js/db.js";
import { QuizPlayer } from "./js/quiz.js";
import { WritingLab } from "./js/writing.js";
import { AnalyticsManager } from "./js/analytics.js";
import { sound } from "./js/sound.js";
import { confetti } from "./js/confetti.js";
import { heuristicsEngine } from "./js/heuristics.js";
import { ScienceOEQStudio } from "./js/science_oeq.js";
import { EnglishEliteSuite } from "./js/english_elite.js";
import { ChineseAL1Hub } from "./js/chinese_al1.js";
import { MockExamSimulator } from "./js/exam_mode.js";
import { MistakeNotebook } from "./js/notebook.js";
import { WorksheetExporter } from "./js/export.js";
import { MasteryCoach } from "./js/coach.js";

class PortalApp {
  constructor() {
    this.currentLevel = "P6";
    this.selectedLevel = "P6";
    this.selectedSubject = "mathematics";
    this.studentName = "Alex Tan";
    this.targetGrade = "AL1";

    // Instantiate Sub-Systems
    this.db = new DatabaseManager();
    this.analytics = new AnalyticsManager(this);
    this.quiz = new QuizPlayer(this);
    this.writing = new WritingLab(this);
    
    // Legendary PSLE Studios
    this.scienceOEQ = new ScienceOEQStudio(this);
    this.englishElite = new EnglishEliteSuite(this);
    this.chineseAL1 = new ChineseAL1Hub(this);
    this.mockExam = new MockExamSimulator(this);
    this.notebook = new MistakeNotebook(this);
    this.exporter = new WorksheetExporter(this);
    this.coach = new MasteryCoach(this);
    heuristicsEngine.app = this;

    // Cache Global Elements
    this.navLinks = document.querySelectorAll(".nav-link");
    this.sections = document.querySelectorAll(".view-section");
    this.sectionTitle = document.getElementById("current-section-title");
    this.themeToggleBtn = document.getElementById("theme-toggle-btn");
    this.soundToggleBtn = document.getElementById("sound-toggle-btn");
    this.printWorksheetBtn = document.getElementById("global-print-worksheet-btn");
    
    this.levelSelectTabs = document.getElementById("level-select-tabs");
    this.subjectsArenaGrid = document.getElementById("subjects-arena-grid");
    
    this.settingsForm = document.getElementById("settings-form");
    this.studentNameInput = document.getElementById("student-name-input");
    this.studentLevelSelect = document.getElementById("student-level-select");
    this.targetGradeSelect = document.getElementById("target-grade-select");
    this.geminiApiKeyInput = document.getElementById("gemini-api-key");

    this.initCoreEvents();
    this.loadSettings();
    this.bootstrapApp();
  }

  initCoreEvents() {
    this.navLinks.forEach(link => {
      link.addEventListener("click", () => {
        sound.playClick();
        const id = link.id.replace("nav-", "");
        this.showSection(id);
      });
    });

    if (this.themeToggleBtn) {
      this.themeToggleBtn.addEventListener("click", () => {
        sound.playClick();
        this.toggleTheme();
      });
    }

    if (this.soundToggleBtn) {
      this.updateSoundButtonUI();
      this.soundToggleBtn.addEventListener("click", () => {
        const isMuted = sound.toggleMute();
        this.updateSoundButtonUI();
        if (!isMuted) sound.playCorrect();
      });
    }

    if (this.printWorksheetBtn) {
      this.printWorksheetBtn.addEventListener("click", () => {
        sound.playClick();
        this.exporter.generatePrintableWorksheet(this.currentLevel, this.selectedSubject || "mathematics", 10);
      });
    }

    if (this.levelSelectTabs) {
      this.levelSelectTabs.querySelectorAll(".btn-pill").forEach(btn => {
        btn.addEventListener("click", () => {
          sound.playClick();
          this.levelSelectTabs.querySelector(".btn-pill.active")?.classList.remove("active");
          btn.classList.add("active");
          this.currentLevel = btn.dataset.level;
          this.selectedLevel = btn.dataset.level;
          this.renderPracticeSubjects();
        });
      });
    }

    if (this.settingsForm) {
      this.settingsForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.saveSettings();
      });
    }

    // Dashboard smart session CTA
    document.getElementById("dash-start-smart-btn")?.addEventListener("click", () => {
      sound.playClick();
      this.showSection("coach");
      this.coach.startSmartSession();
    });
  }

  updateSoundButtonUI() {
    if (this.soundToggleBtn) {
      this.soundToggleBtn.innerText = sound.isMuted ? "🔇" : "🔊";
      this.soundToggleBtn.title = sound.isMuted ? "Audio Muted (Click to un-mute)" : "Audio Enabled (Click to mute)";
    }
  }

  bootstrapApp() {
    setTimeout(() => {
      const splash = document.getElementById("splash-screen");
      if (splash) {
        splash.style.opacity = "0";
        setTimeout(() => splash.remove(), 500);
      }
    }, 800);

    this.renderProfileWidgets();
    this.renderPracticeSubjects();
    this.showSection("dashboard");
  }

  switchSection(sectionId) {
    sound.playClick();
    this.showSection(sectionId);
  }

  showSection(sectionId) {
    this.sections.forEach(sec => sec.classList.remove("active"));
    this.navLinks.forEach(link => link.classList.remove("active"));

    const activeSec = document.getElementById(`section-${sectionId}`);
    const activeLink = document.getElementById(`nav-${sectionId}`);

    if (activeSec) activeSec.classList.add("active");
    if (activeLink) activeLink.classList.add("active");

    const titles = {
      dashboard: "PSLE Mastery Command Center",
      coach: "Anti-Cram Mastery Coach",
      practice: "MOE Practice Arena",
      heuristics: "Singapore Math Bar Model & Heuristics Lab",
      "science-oeq": "Science Section B C-E-R Studio",
      "english-elite": "English Synthesis & Oral SBC Suite",
      "chinese-al1": "华文成语与关联词 AL1 冲刺站",
      "exam-mode": "Top School Mock Exam Simulator",
      notebook: "错题本 Smart Mistake Notebook",
      quiz: "Deliberate Practice Session",
      writing: "PSLE Writing Lab",
      achievements: "Achievements Trophy Room",
      settings: "Configurations"
    };
    if (this.sectionTitle) {
      this.sectionTitle.innerText = titles[sectionId] || "MOE Prep";
    }

    if (sectionId === "dashboard") {
      this.analytics.renderDashboardWidgets();
    } else if (sectionId === "coach") {
      const c = document.getElementById("coach-container");
      if (c) this.coach.render(c);
    } else if (sectionId === "heuristics") {
      const c = document.getElementById("heuristics-container");
      if (c) heuristicsEngine.renderTaxonomyStudio(c);
    } else if (sectionId === "science-oeq") {
      const c = document.getElementById("science-oeq-container");
      if (c) this.scienceOEQ.render(c);
    } else if (sectionId === "english-elite") {
      const c = document.getElementById("english-elite-container");
      if (c) this.englishElite.render(c);
    } else if (sectionId === "chinese-al1") {
      const c = document.getElementById("chinese-al1-container");
      if (c) this.chineseAL1.render(c);
    } else if (sectionId === "exam-mode") {
      const c = document.getElementById("exam-mode-container");
      if (c) this.mockExam.renderLobby(c);
    } else if (sectionId === "notebook") {
      const c = document.getElementById("notebook-container");
      if (c) this.notebook.render(c);
    } else if (sectionId === "achievements") {
      this.analytics.renderAchievementsView();
    } else if (sectionId === "writing") {
      this.writing.startWritingSession();
    } else if (sectionId === "practice") {
      this.renderPracticeSubjects();
    }
  }

  toggleTheme() {
    document.body.classList.toggle("light-theme");
    const isLight = document.body.classList.contains("light-theme");
    this.themeToggleBtn.innerText = isLight ? "🌙" : "💡";
    localStorage.setItem("moe_prep_light_theme", isLight ? "true" : "false");
  }

  loadSettings() {
    const theme = localStorage.getItem("moe_prep_light_theme");
    if (theme === "true") {
      document.body.classList.add("light-theme");
      if (this.themeToggleBtn) this.themeToggleBtn.innerText = "🌙";
    }

    const savedName = localStorage.getItem("moe_prep_student_name");
    const savedLevel = localStorage.getItem("moe_prep_student_level");
    const savedGrade = localStorage.getItem("moe_prep_target_grade");
    const savedKey = localStorage.getItem("moe_prep_api_key");

    if (savedName) this.studentName = savedName;
    if (savedLevel) {
      this.currentLevel = savedLevel;
      this.selectedLevel = savedLevel;
    }
    if (savedGrade) this.targetGrade = savedGrade;
    if (savedKey && this.geminiApiKeyInput) this.geminiApiKeyInput.value = savedKey;

    if (this.studentNameInput) this.studentNameInput.value = this.studentName;
    if (this.studentLevelSelect) this.studentLevelSelect.value = this.currentLevel;
    if (this.targetGradeSelect) this.targetGradeSelect.value = this.targetGrade;

    if (this.levelSelectTabs) {
      const activeTab = this.levelSelectTabs.querySelector(".btn-pill.active");
      if (activeTab) activeTab.classList.remove("active");
      const targetTab = this.levelSelectTabs.querySelector(`[data-level="${this.currentLevel}"]`);
      if (targetTab) targetTab.classList.add("active");
    }
  }

  saveSettings() {
    sound.playCorrect();
    this.studentName = this.studentNameInput.value.trim() || "Alex Tan";
    this.currentLevel = this.studentLevelSelect.value;
    this.selectedLevel = this.currentLevel;
    this.targetGrade = this.targetGradeSelect.value;
    
    const key = this.geminiApiKeyInput.value.trim();
    if (key) localStorage.setItem("moe_prep_api_key", key);
    else localStorage.removeItem("moe_prep_api_key");

    localStorage.setItem("moe_prep_student_name", this.studentName);
    localStorage.setItem("moe_prep_student_level", this.currentLevel);
    localStorage.setItem("moe_prep_target_grade", this.targetGrade);

    this.renderProfileWidgets();
    this.renderPracticeSubjects();
    
    alert("Configurations saved successfully!");
    this.showSection("dashboard");
  }

  renderProfileWidgets() {
    const nameDisp = document.getElementById("student-name-display");
    const nameWelc = document.getElementById("student-name-welcome");
    const targetGrade = document.getElementById("target-grade-display");
    const targetGradePill = document.getElementById("current-target-grade-pill");
    const profLevel = document.getElementById("profile-level");
    const recLevel = document.getElementById("recommended-level-text");
    const profXP = document.getElementById("profile-xp");
    const streakDisp = document.getElementById("streak-days-display");

    if (nameDisp) nameDisp.innerText = this.studentName;
    if (nameWelc) nameWelc.innerText = this.studentName;
    if (targetGrade) targetGrade.innerText = `Target: ${this.targetGrade} · No-Cram Path`;
    if (targetGradePill) targetGradePill.innerText = this.targetGrade;
    if (profLevel) profLevel.innerText = this.currentLevel;
    if (recLevel) recLevel.innerText = this.currentLevel;
    if (profXP) profXP.innerText = `${this.analytics.xp} XP`;
    if (streakDisp) streakDisp.innerText = this.analytics.streak;
  }

  async renderPracticeSubjects() {
    if (!this.subjectsArenaGrid) return;
    this.subjectsArenaGrid.innerHTML = "";

    const subjects = [
      { key: "mathematics", title: "Mathematics", icon: "📐", count: "Heuristics, models & word problems" },
      { key: "science", title: "Science Core", icon: "🔬", count: "C-E-R experiments & concept MCQs" },
      { key: "english", title: "English Language", icon: "📚", count: "Grammar, S&T, cloze & vocab" },
      { key: "chinese", title: "Mother Tongue (CL)", icon: "🏮", count: "成语, 关联词 & 阅读理解" }
    ];

    for (const sub of subjects) {
      const card = document.createElement("div");
      card.className = `subject-card card-${sub.key}`;
      
      const isScienceDisabled = (this.currentLevel === "P2" && sub.key === "science");
      let topicsHtml = "";
      if (!isScienceDisabled) {
        try {
          const topics = await this.db.getTopics(this.currentLevel, sub.key);
          const top = topics.slice(0, 4).map(t => t.topic).join(" · ");
          topicsHtml = `<div style="font-size: 11px; color: var(--text-muted); margin-top: 8px; line-height: 1.4;">${top}</div>`;
        } catch (_) { /* ignore */ }
      }

      card.innerHTML = `
        <div class="subject-icon">${sub.icon}</div>
        <h4 class="subject-title">${sub.title}</h4>
        <span class="subject-count">${isScienceDisabled ? "Starts in Primary 3" : sub.count}</span>
        ${topicsHtml}
        ${!isScienceDisabled ? `
          <div style="display: flex; gap: 6px; margin-top: 12px; flex-wrap: wrap;">
            <button class="btn-pill practice-mode-btn" data-mode="adaptive" data-sub="${sub.key}" style="font-size: 10px; padding: 4px 8px;">🧠 Adaptive</button>
            <button class="btn-pill practice-mode-btn" data-mode="random" data-sub="${sub.key}" style="font-size: 10px; padding: 4px 8px;">🎲 Mixed</button>
            <button class="btn-pill practice-mode-btn" data-mode="topics" data-sub="${sub.key}" style="font-size: 10px; padding: 4px 8px;">📂 By Topic</button>
          </div>
        ` : ""}
      `;

      if (isScienceDisabled) {
        card.style.opacity = "0.5";
        card.style.cursor = "not-allowed";
        card.title = "Science is only introduced in Primary 3 under Singapore's MOE curriculum.";
      } else {
        card.querySelectorAll(".practice-mode-btn").forEach(btn => {
          btn.addEventListener("click", (e) => {
            e.stopPropagation();
            this.selectedSubject = sub.key;
            this.startPracticeMode(sub.key, btn.dataset.mode);
          });
        });
        card.addEventListener("click", (e) => {
          if (e.target.classList.contains("practice-mode-btn")) return;
          this.selectedSubject = sub.key;
          this.startPracticeMode(sub.key, "adaptive");
        });
      }

      this.subjectsArenaGrid.appendChild(card);
    }
  }

  async startPracticeMode(subject, mode) {
    sound.playClick();
    this.selectedSubject = subject;

    if (mode === "topics") {
      const topics = await this.db.getTopics(this.currentLevel, subject);
      const pick = prompt(`Type a topic exactly to drill:\n\n${topics.map(t => t.topic).join("\n")}`, topics[0]?.topic || "");
      if (!pick) return;
      this.showSection("quiz");
      const set = await this.db.getPracticeSet(this.currentLevel, subject, 10, {
        topic: pick,
        excludeIds: this.coach?.state?.seenIds?.slice(-100) || []
      });
      if (!set.length) {
        alert("No questions found for that topic.");
        return;
      }
      this.quiz.startQuiz(set, subject, this.currentLevel);
      return;
    }

    this.showSection("quiz");
    const loadText = document.getElementById("quiz-question-text");
    if (loadText) loadText.innerText = `Building a ${mode} set for ${subject} (${this.currentLevel})...`;

    let set = [];
    if (mode === "adaptive") {
      set = await this.db.getAdaptiveSet(
        this.currentLevel,
        subject,
        10,
        this.coach?.state?.topicMastery || {},
        this.coach?.state?.seenIds?.slice(-150) || []
      );
    } else {
      set = await this.db.getPracticeSet(this.currentLevel, subject, 10, {
        excludeIds: this.coach?.state?.seenIds?.slice(-100) || []
      });
    }

    if (!set.length) {
      if (loadText) loadText.innerText = `Failed to load practice questions for ${this.currentLevel} ${subject}.`;
      return;
    }
    this.quiz.startQuiz(set, subject, this.currentLevel);
  }

  async loadQuiz(subject) {
    return this.startPracticeMode(subject, "adaptive");
  }

  addXP(amount) {
    this.analytics.addXP(amount);
  }

  recordQuizCompletion(score, total, subject) {
    this.analytics.recordQuiz(score, total, subject);
    this.renderProfileWidgets();
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.app = new PortalApp();
});
