/* Central Application State Manager & Router - Singapore AL4 Suite */
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
    
    // Instantiate Legendary PSLE Studios
    this.scienceOEQ = new ScienceOEQStudio(this);
    this.englishElite = new EnglishEliteSuite(this);
    this.chineseAL1 = new ChineseAL1Hub(this);
    this.mockExam = new MockExamSimulator(this);
    this.notebook = new MistakeNotebook(this);
    this.exporter = new WorksheetExporter(this);

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
    // Navigation Tabs Router
    this.navLinks.forEach(link => {
      link.addEventListener("click", () => {
        sound.playClick();
        const id = link.id.replace("nav-", "");
        this.showSection(id);
      });
    });

    // Theme Toggle
    if (this.themeToggleBtn) {
      this.themeToggleBtn.addEventListener("click", () => {
        sound.playClick();
        this.toggleTheme();
      });
    }

    // Sound Toggle
    if (this.soundToggleBtn) {
      this.updateSoundButtonUI();
      this.soundToggleBtn.addEventListener("click", () => {
        const isMuted = sound.toggleMute();
        this.updateSoundButtonUI();
        if (!isMuted) sound.playCorrect();
      });
    }

    // Print Worksheet Button
    if (this.printWorksheetBtn) {
      this.printWorksheetBtn.addEventListener("click", () => {
        sound.playClick();
        this.exporter.generatePrintableWorksheet(this.currentLevel, this.selectedSubject || "mathematics", 10);
      });
    }

    // Practice Arena level filter tabs
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

    // Settings Submit
    if (this.settingsForm) {
      this.settingsForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.saveSettings();
      });
    }
  }

  updateSoundButtonUI() {
    if (this.soundToggleBtn) {
      this.soundToggleBtn.innerText = sound.isMuted ? "🔇" : "🔊";
      this.soundToggleBtn.title = sound.isMuted ? "Audio Muted (Click to un-mute)" : "Audio Enabled (Click to mute)";
    }
  }

  bootstrapApp() {
    // Fade splash screen
    setTimeout(() => {
      const splash = document.getElementById("splash-screen");
      if (splash) {
        splash.style.opacity = "0";
        setTimeout(() => splash.remove(), 500);
      }
    }, 800);

    // Initial renders
    this.renderProfileWidgets();
    this.renderPracticeSubjects();
    this.showSection("dashboard");
  }

  switchSection(sectionId) {
    sound.playClick();
    this.showSection(sectionId);
  }

  showSection(sectionId) {
    // Hide all sections & deactivate all links
    this.sections.forEach(sec => sec.classList.remove("active"));
    this.navLinks.forEach(link => link.classList.remove("active"));

    // Activate selected
    const activeSec = document.getElementById(`section-${sectionId}`);
    const activeLink = document.getElementById(`nav-${sectionId}`);

    if (activeSec) activeSec.classList.add("active");
    if (activeLink) activeLink.classList.add("active");

    // Title mapping
    const titles = {
      dashboard: "PSLE AL4 Command Center",
      practice: "MOE Practice Arena (19,000 Questions)",
      heuristics: "Singapore Math Bar Model & Heuristics Lab",
      "science-oeq": "Science Section B C-E-R Studio",
      "english-elite": "English Synthesis & Oral SBC Suite",
      "chinese-al1": "华文成语与关联词 AL1 冲刺站",
      "exam-mode": "Top School Mock Exam Simulator",
      notebook: "错题本 Smart Mistake Notebook",
      quiz: "Practice Quiz Session",
      writing: "PSLE Writing Lab",
      achievements: "Achievements Trophy Room",
      settings: "Configurations"
    };
    if (this.sectionTitle) {
      this.sectionTitle.innerText = titles[sectionId] || "MOE Prep";
    }

    // Studio Initializers
    if (sectionId === "dashboard") {
      this.analytics.renderDashboardWidgets();
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
    if (key) {
      localStorage.setItem("moe_prep_api_key", key);
    } else {
      localStorage.removeItem("moe_prep_api_key");
    }

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
    if (targetGrade) targetGrade.innerText = `Target: ${this.targetGrade} (AL4 Total)`;
    if (targetGradePill) targetGradePill.innerText = this.targetGrade;
    if (profLevel) profLevel.innerText = this.currentLevel;
    if (recLevel) recLevel.innerText = this.currentLevel;
    if (profXP) profXP.innerText = `${this.analytics.xp} XP`;
    if (streakDisp) streakDisp.innerText = this.analytics.streak;
  }

  renderPracticeSubjects() {
    if (!this.subjectsArenaGrid) return;
    this.subjectsArenaGrid.innerHTML = "";

    const subjects = [
      { key: "mathematics", title: "Mathematics", icon: "📐", count: "1,000 Heuristics & Model Sums" },
      { key: "science", title: "Science Core", icon: "🔬", count: "1,000 C-E-R Experiments & MCQs" },
      { key: "english", title: "English Language", icon: "📚", count: "1,000 Grammar, S&T & Cloze" },
      { key: "chinese", title: "Mother Tongue (CL)", icon: "🏮", count: "1,000 成语, 关联词 & 阅读理解" }
    ];

    subjects.forEach(sub => {
      const card = document.createElement("div");
      card.className = `subject-card card-${sub.key}`;
      
      const isScienceDisabled = (this.currentLevel === "P2" && sub.key === "science");

      card.innerHTML = `
        <div class="subject-icon">${sub.icon}</div>
        <h4 class="subject-title">${sub.title}</h4>
        <span class="subject-count">${isScienceDisabled ? 'Starts in Primary 3' : sub.count}</span>
      `;

      if (isScienceDisabled) {
        card.style.opacity = "0.5";
        card.style.cursor = "not-allowed";
        card.title = "Science is only introduced in Primary 3 under Singapore's MOE curriculum.";
      } else {
        card.addEventListener("click", () => {
          this.selectedSubject = sub.key;
          this.loadQuiz(sub.key);
        });
      }

      this.subjectsArenaGrid.appendChild(card);
    });
  }

  async loadQuiz(subject) {
    sound.playClick();
    this.selectedSubject = subject;
    this.showSection("quiz");
    const loadText = document.getElementById("quiz-question-text");
    loadText.innerText = `Loading 10 random ${subject.toUpperCase()} questions from the Level ${this.currentLevel} database...`;

    const set = await this.db.getPracticeSet(this.currentLevel, subject, 10);
    if (set.length === 0) {
      loadText.innerText = `Failed to load practice questions for ${this.currentLevel} ${subject}. Please verify your data compile status.`;
      return;
    }

    this.quiz.startQuiz(set, subject, this.currentLevel);
  }

  addXP(amount) {
    this.analytics.addXP(amount);
  }

  recordQuizCompletion(score, total, subject) {
    this.analytics.recordQuiz(score, total, subject);
    this.renderProfileWidgets();
  }
}

// Global bootstrap instance
window.addEventListener("DOMContentLoaded", () => {
  window.app = new PortalApp();
});
