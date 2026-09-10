/* Database Fetch and Query Manager */
export class DatabaseManager {
  constructor() {
    this.cache = {};
  }

  /**
   * Fetches the 1,000-question database for a specific level and subject
   * @param {string} level - P2, P3, P4, P5, P6
   * @param {string} subject - english, mathematics, science, chinese
   */
  async fetchQuestions(level, subject) {
    const key = `${level.toLowerCase()}_${subject.toLowerCase()}`;
    if (this.cache[key]) {
      return this.cache[key];
    }

    try {
      const response = await fetch(`data/${key}.json`);
      if (!response.ok) {
        throw new Error(`Failed to fetch data/${key}.json - Status: ${response.status}`);
      }
      const data = await response.json();
      this.cache[key] = data;
      return data;
    } catch (error) {
      console.error("Database fetch error:", error);
      return [];
    }
  }

  /**
   * Generates a random quiz subset of questions
   */
  async getPracticeSet(level, subject, count = 10, options = {}) {
    const questions = await this.fetchQuestions(level, subject);
    if (!questions || questions.length === 0) return [];

    let pool = [...questions];
    const { topic, difficulty, heuristicId, excludeIds = [] } = options;
    const excluded = new Set(excludeIds);

    if (topic) pool = pool.filter(q => q.topic === topic);
    if (difficulty) pool = pool.filter(q => q.difficulty === difficulty);
    if (heuristicId) pool = pool.filter(q => q.heuristicId === heuristicId);
    if (excluded.size) pool = pool.filter(q => !excluded.has(q.id));
    if (pool.length === 0) pool = questions.filter(q => !excluded.has(q.id));

    // Fisher-Yates shuffle for better randomness
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }
    return pool.slice(0, Math.min(count, pool.length));
  }

  /** Alias used by Mock Exam Simulator */
  async getRandomQuestions(level, subject, count = 15, options = {}) {
    return this.getPracticeSet(level, subject, count, options);
  }

  /**
   * Topic inventory for adaptive practice UI
   */
  async getTopics(level, subject) {
    const questions = await this.fetchQuestions(level, subject);
    const map = new Map();
    (questions || []).forEach(q => {
      const t = q.topic || "General";
      map.set(t, (map.get(t) || 0) + 1);
    });
    return Array.from(map.entries()).map(([topic, count]) => ({ topic, count })).sort((a, b) => a.topic.localeCompare(b.topic));
  }

  /**
   * Adaptive weak-topic set: prefer topics with lower mastery, mix difficulties
   */
  async getAdaptiveSet(level, subject, count = 10, topicMastery = {}, excludeIds = []) {
    const questions = await this.fetchQuestions(level, subject);
    if (!questions || questions.length === 0) return [];

    const excluded = new Set(excludeIds);
    const scored = questions
      .filter(q => !excluded.has(q.id))
      .map(q => {
        const mastery = topicMastery[`${subject}::${q.topic}`] ?? topicMastery[q.topic] ?? 50;
        const diffBoost = q.difficulty === "Hard" ? 8 : q.difficulty === "Medium" ? 4 : 0;
        const weakness = Math.max(0, 100 - mastery);
        const weight = weakness + diffBoost + Math.random() * 12;
        return { q, weight };
      })
      .sort((a, b) => b.weight - a.weight);

    // Soft diversity: take from top half with mild shuffle
    const top = scored.slice(0, Math.max(count * 4, count));
    for (let i = top.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [top[i], top[j]] = [top[j], top[i]];
    }
    return top.slice(0, count).map(x => x.q);
  }

  /**
   * Mixed interleaved set across multiple subjects
   */
  async getInterleavedSet(level, subjects, count = 12, topicMastery = {}) {
    const per = Math.max(2, Math.ceil(count / subjects.length));
    const chunks = await Promise.all(
      subjects.map(sub => this.getAdaptiveSet(level, sub, per, topicMastery))
    );
    const mixed = chunks.flat();
    for (let i = mixed.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [mixed[i], mixed[j]] = [mixed[j], mixed[i]];
    }
    return mixed.slice(0, count).map((q, idx) => ({
      ...q,
      subject: q.subject || subjects[Math.floor(idx / per)] || subjects[0]
    }));
  }

  /**
   * Searches questions by topic or keyword
   */
  async searchQuestions(level, subject, keyword) {
    const questions = await this.fetchQuestions(level, subject);
    if (!questions) return [];
    
    const term = keyword.toLowerCase();
    return questions.filter(q => 
      q.question.toLowerCase().includes(term) || 
      q.topic.toLowerCase().includes(term)
    );
  }
}
