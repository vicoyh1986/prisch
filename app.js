/* Central Application State Manager & Router */
import { DatabaseManager } from "./js/db.js";
import { QuizPlayer } from "./js/quiz.js";
import { WritingLab } from "./js/writing.js";
import { AnalyticsManager } from "./js/analytics.js";

class PortalApp {
  constructor() {
    this.currentLevel = "P6";
    this.studentName = "Alex Tan";
    this.targetGrade = "AL1";

    // Instantiate Sub-Systems
    this.db = new DatabaseManager();
    this.quiz = new QuizPlayer(this);
    this.writing = new WritingLab(this);
    this.analytics = new AnalyticsManager(this);

    // Cache Global Elements
    this.navLinks = document.querySelectorAll(".nav-link");
    this.sections = document.querySelectorAll(".view-section");
    this.sectionTitle = document.getElementById("current-section-title");
    this.themeToggleBtn = document.getElementById("theme-toggle-btn");
    
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
        const id = link.id.replace("nav-", "");
        this.showSection(id);
      });
    });

    // Theme Toggle
    this.themeToggleBtn.addEventListener("click", () => this.toggleTheme());

    // Practice Arena level filter tabs
    if (this.levelSelectTabs) {
      this.levelSelectTabs.querySelectorAll(".btn-pill").forEach(btn => {
        btn.addEventListener("click", () => {
          this.levelSelectTabs.querySelector(".btn-pill.active").classList.remove("active");
          btn.classList.add("active");
          this.currentLevel = btn.dataset.level;
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

  bootstrapApp() {
    // Fade splash screen
    setTimeout(() => {
      const splash = document.getElementById("splash-screen");
      if (splash) {
        splash.style.opacity = "0";
        setTimeout(() => splash.remove(), 500);
      }
    }, 1000);

    // Initial renders
    this.renderProfileWidgets();
    this.renderPracticeSubjects();
    this.showSection("dashboard");
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
      dashboard: "Dashboard",
      practice: "Practice Arena",
      quiz: "Practice Quiz Session",
      writing: "PSLE Writing Lab",
      achievements: "Achievements Trophy Room",
      settings: "Configurations"
    };
    this.sectionTitle.innerText = titles[sectionId] || "MOE Prep";

    // View-specific initialization triggers
    if (sectionId === "dashboard") {
      this.analytics.renderDashboardWidgets();
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
    // Set theme
    const theme = localStorage.getItem("moe_prep_light_theme");
    if (theme === "true") {
      document.body.classList.add("light-theme");
      this.themeToggleBtn.innerText = "🌙";
    }

    // Set credentials / names
    const savedName = localStorage.getItem("moe_prep_student_name");
    const savedLevel = localStorage.getItem("moe_prep_student_level");
    const savedGrade = localStorage.getItem("moe_prep_target_grade");
    const savedKey = localStorage.getItem("moe_prep_api_key");

    if (savedName) this.studentName = savedName;
    if (savedLevel) this.currentLevel = savedLevel;
    if (savedGrade) this.targetGrade = savedGrade;
    if (savedKey) this.geminiApiKeyInput.value = savedKey;

    // Apply to inputs
    this.studentNameInput.value = this.studentName;
    this.studentLevelSelect.value = this.currentLevel;
    this.targetGradeSelect.value = this.targetGrade;

    // Align tabs in Practice section
    if (this.levelSelectTabs) {
      const activeTab = this.levelSelectTabs.querySelector(".btn-pill.active");
      if (activeTab) activeTab.classList.remove("active");
      const targetTab = this.levelSelectTabs.querySelector(`[data-level="${this.currentLevel}"]`);
      if (targetTab) targetTab.classList.add("active");
    }
  }

  saveSettings() {
    this.studentName = this.studentNameInput.value.trim() || "Alex Tan";
    this.currentLevel = this.studentLevelSelect.value;
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
    document.getElementById("student-name-display").innerText = this.studentName;
    document.getElementById("student-name-welcome").innerText = this.studentName;
    document.getElementById("target-grade-display").innerText = `Target: ${this.targetGrade}`;
    document.getElementById("current-target-grade-pill").innerText = this.targetGrade;
    
    document.getElementById("profile-level").innerText = this.currentLevel;
    document.getElementById("recommended-level-text").innerText = this.currentLevel;
    
    document.getElementById("profile-xp").innerText = `${this.analytics.xp} XP`;
    document.getElementById("streak-days-display").innerText = this.analytics.streak;
  }

  renderPracticeSubjects() {
    if (!this.subjectsArenaGrid) return;
    this.subjectsArenaGrid.innerHTML = "";

    const subjects = [
      { key: "english", title: "English Language", icon: "📚", count: "Grammar, Vocab & Cloze" },
      { key: "mathematics", title: "Mathematics", icon: "📐", count: "Arithmetic & Model Sums" },
      { key: "science", title: "Science Core", icon: "🍀", count: "Systems, Energy & Cycles" },
      { key: "chinese", title: "Mother Tongue (CL)", icon: "🏮", count: "Pinyin & Cloze Sentences" }
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
        card.addEventListener("click", () => this.loadQuiz(sub.key));
      }

      this.subjectsArenaGrid.appendChild(card);
    });
  }

  async loadQuiz(subject) {
    this.showSection("quiz");
    const loadText = document.getElementById("quiz-question-text");
    loadText.innerText = `Loading 10 random ${subject.toUpperCase()} questions from the Level ${this.currentLevel} database...`;

    // Fetch questions
    const set = await this.db.getPracticeSet(this.currentLevel, subject, 10);
    if (set.length === 0) {
      loadText.innerText = `Failed to load practice questions for ${this.currentLevel} ${subject}. Please verify your data compile status.`;
      return;
    }

    this.quiz.startQuiz(set, subject, this.currentLevel);
  }

  // Bridging methods to delegate triggers
  addXP(amount) {
    this.analytics.addXP(amount);
  }

  recordQuizCompletion(score, total, subject) {
    this.analytics.recordQuiz(score, total, subject);
  }

  recordEssayWritten() {
    this.analytics.recordEssay();
  }
}

// Instantiate global app scope
window.app = new PortalApp();
export { PortalApp as default };
