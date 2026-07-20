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
  async getPracticeSet(level, subject, count = 10) {
    const questions = await this.fetchQuestions(level, subject);
    if (!questions || questions.length === 0) return [];

    // Shuffle and slice
    const shuffled = [...questions].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
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
