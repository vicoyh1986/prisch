/* Chinese Mother Tongue AL1 Mastery Hub: Idioms, Linking Particles, & Model Essays */
import { sound } from "./sound.js";

export const CHINESE_IDIOMS = [
  {
    idiom: "专心致志",
    pinyin: "zhuān xīn zhì zhì",
    meaning: "Wholly absorbed / focused with single-minded dedication",
    example: "他在书房里专心致志地做功课，连外面的雷声都没有听到。",
    category: "学习与品格"
  },
  {
    idiom: "坚持不懈",
    pinyin: "jiān chí bù xiè",
    meaning: "Persevere relentlessly without giving up",
    example: "经过五年的坚持不懈，他终于在全国游泳比赛中夺得冠军。",
    category: "毅力与奋斗"
  },
  {
    idiom: "见义勇为",
    pinyin: "jiàn yì yǒng wéi",
    meaning: "Act bravely for a just cause / step up courageously",
    example: "看到老奶奶被抢劫，李叔叔见义勇为，立刻冲上前抓住了小偷。",
    category: "品德与助人"
  },
  {
    idiom: "齐心协力",
    pinyin: "qí xīn xié lì",
    meaning: "Work together with one heart and united effort",
    example: "只要全班同学齐心协力，我们就一定能赢得拔河比赛的胜利。",
    category: "团队合作"
  },
  {
    idiom: "迫不及待",
    pinyin: "pò bù jí dài",
    meaning: "Too impatient to wait / eager to do something",
    example: "一放学，小明就迫不及待地跑回家拆开妈妈送的生日礼物。",
    category: "情绪与行为"
  },
  {
    idiom: "受益匪浅",
    pinyin: "shòu yì fěi qiǎn",
    meaning: "Benefit immensely from an experience or advice",
    example: "听了陈博士生动有趣的科学讲座，同学们都感到受益匪浅。",
    category: "收获与启迪"
  },
  {
    idiom: "大公无私",
    pinyin: "dà gōng wú sī",
    meaning: "Selfless and completely impartial",
    example: "班长处理同学之间的纠纷时一向大公无私，深受大家敬佩。",
    category: "品德与公正"
  },
  {
    idiom: "滔滔不绝",
    pinyin: "tāo tāo bù jué",
    meaning: "Talking fluently in an endless stream",
    example: "一谈起他最喜爱的恐龙知识，伟杰就滔滔不绝地说个不停。",
    category: "言语与表达"
  }
];

export const CHINESE_CONNECTORS = [
  {
    pair: "不但……而且……",
    meaning: "Not only... but also...",
    example: "小丽不但学习成绩优异，而且乐于助人。",
    quiz: "这本百科全书 ________ 内容丰富，________ 插图精美。",
    options: ["不但……而且……", "虽然……但是……", "因为……所以……", "只要……就……"],
    ans: "不但……而且……"
  },
  {
    pair: "虽然……但是……",
    meaning: "Although... yet...",
    example: "虽然天上下着倾盆大雨，但是运动员们依然坚持完成比赛。",
    quiz: "________ 爷爷年纪大了，________ 他的身体依然非常硬朗。",
    options: ["虽然……但是……", "不但……而且……", "宁可……也不……", "由于……因此……"],
    ans: "虽然……但是……"
  },
  {
    pair: "只要……就……",
    meaning: "As long as... then...",
    example: "只要我们坚持努力，就一定能取得好成绩。",
    quiz: "________ 你肯虚心向他人请教，________ 能克服学习上的困难。",
    options: ["只要……就……", "只有……才……", "宁可……也不……", "与其……不如……"],
    ans: "只要……就……"
  },
  {
    pair: "宁可……也不……",
    meaning: "Would rather... than...",
    example: "他宁可自己吃苦，也不愿意给父母增添负担。",
    quiz: "我们 ________ 诚实承认错误，________ 能撒谎隐瞒事实。",
    options: ["宁可……也不……", "虽然……但是……", "不但……而且……", "因为……所以……"],
    ans: "宁可……也不……"
  }
];

export class ChineseAL1Hub {
  constructor(app) {
    this.app = app;
    this.activeTab = "idioms"; // 'idioms' | 'connectors'
    this.idiomIdx = 0;
  }

  render(container) {
    container.innerHTML = `
      <div class="chinese-hub-wrapper">
        <div style="display: flex; gap: 10px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
          <button class="btn ${this.activeTab === 'idioms' ? 'btn-primary' : 'btn-outline'}" id="cn-tab-idioms">
            📖 成语特训 (PSLE 必考成语闪卡)
          </button>
          <button class="btn ${this.activeTab === 'connectors' ? 'btn-primary' : 'btn-outline'}" id="cn-tab-connectors">
            🔗 关联词辨析与实战训练
          </button>
        </div>

        <div id="cn-tab-content"></div>
      </div>
    `;

    const content = container.querySelector("#cn-tab-content");
    container.querySelector("#cn-tab-idioms").addEventListener("click", () => {
      this.activeTab = "idioms";
      this.render(container);
    });

    container.querySelector("#cn-tab-connectors").addEventListener("click", () => {
      this.activeTab = "connectors";
      this.render(container);
    });

    if (this.activeTab === "idioms") {
      this.renderIdioms(content);
    } else {
      this.renderConnectors(content);
    }
  }

  renderIdioms(container) {
    const idiom = CHINESE_IDIOMS[this.idiomIdx];

    container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <!-- Left: Interactive Flashcard -->
        <div class="panel" style="text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 320px; background: linear-gradient(135deg, rgba(236, 72, 153, 0.05), rgba(168, 85, 247, 0.1)); border-color: rgba(236, 72, 153, 0.3);">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 16px;">
            <span class="tag tag-easy">${idiom.category}</span>
            <span style="font-size: 12px; color: var(--text-muted); font-weight: 700;">${this.idiomIdx + 1} / ${CHINESE_IDIOMS.length}</span>
          </div>

          <div style="font-size: 38px; font-weight: 800; color: #f43f5e; letter-spacing: 4px; margin-bottom: 6px;">
            ${idiom.idiom}
          </div>
          
          <div style="font-size: 16px; color: var(--primary); font-weight: 600; margin-bottom: 16px; letter-spacing: 1px;">
            ${idiom.pinyin}
          </div>

          <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 18px; width: 90%; margin-bottom: 16px;">
            <div style="font-size: 13px; color: var(--text-primary); font-weight: 600; margin-bottom: 6px;">
              💡 英文解释: ${idiom.meaning}
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6; text-align: left;">
              📝 <strong>造句示例:</strong> ${idiom.example}
            </div>
          </div>

          <div style="display: flex; gap: 10px; width: 90%;">
            <button class="btn btn-outline" id="idiom-prev-btn" style="flex: 1;">← 上一个成语</button>
            <button class="btn btn-primary" id="idiom-next-btn" style="flex: 1;">下一个成语 →</button>
          </div>
        </div>

        <!-- Right: Idiom List & Fast Jump -->
        <div class="panel">
          <h4 style="margin-bottom: 12px;">🌟 PSLE 高频成语总览 (点击快速跳转):</h4>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; max-height: 280px; overflow-y: auto;">
            ${CHINESE_IDIOMS.map((item, idx) => `
              <div class="idiom-jump-card ${idx === this.idiomIdx ? 'active' : ''}" data-idx="${idx}" style="background: ${idx === this.idiomIdx ? 'rgba(244, 63, 94, 0.15)' : 'rgba(255,255,255,0.03)'}; border: 1px solid ${idx === this.idiomIdx ? '#f43f5e' : 'var(--border-color)'}; border-radius: 6px; padding: 10px; cursor: pointer; transition: all 0.2s;">
                <div style="font-weight: 700; font-size: 14px; color: ${idx === this.idiomIdx ? '#f43f5e' : 'var(--text-primary)'};">${item.idiom}</div>
                <div style="font-size: 11px; color: var(--text-muted);">${item.pinyin}</div>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    `;

    container.querySelector("#idiom-prev-btn").addEventListener("click", () => {
      sound.playClick();
      this.idiomIdx = (this.idiomIdx - 1 + CHINESE_IDIOMS.length) % CHINESE_IDIOMS.length;
      this.renderIdioms(container);
    });

    container.querySelector("#idiom-next-btn").addEventListener("click", () => {
      sound.playClick();
      this.idiomIdx = (this.idiomIdx + 1) % CHINESE_IDIOMS.length;
      this.renderIdioms(container);
    });

    container.querySelectorAll(".idiom-jump-card").forEach(card => {
      card.addEventListener("click", () => {
        sound.playClick();
        this.idiomIdx = parseInt(card.dataset.idx);
        this.renderIdioms(container);
      });
    });
  }

  renderConnectors(container) {
    container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="panel">
          <h3 style="margin-bottom: 12px;">🔗 核心关联词速记表:</h3>
          <div style="display: flex; flex-direction: column; gap: 10px;">
            ${CHINESE_CONNECTORS.map(c => `
              <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <strong style="color: var(--primary); font-size: 14px;">${c.pair}</strong>
                  <span style="font-size: 11px; color: var(--text-muted);">${c.meaning}</span>
                </div>
                <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
                  例句：${c.example}
                </div>
              </div>
            `).join("")}
          </div>
        </div>

        <div class="panel" id="connector-quiz-panel">
          <h4 style="margin-bottom: 12px;">✍️ 关联词真题填空演练:</h4>
          <div id="connector-quiz-box"></div>
        </div>
      </div>
    `;

    const quizBox = container.querySelector("#connector-quiz-box");
    let currentQuizIdx = 0;

    const renderQuizItem = () => {
      const q = CHINESE_CONNECTORS[currentQuizIdx];
      quizBox.innerHTML = `
        <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 16px; margin-bottom: 14px; font-size: 14px; font-weight: 600; line-height: 1.8;">
          题目 ${currentQuizIdx + 1}：<br>
          ${q.quiz}
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px;">
          ${q.options.map(opt => `
            <button class="btn btn-outline connector-opt-btn" data-val="${opt}" style="font-size: 13px; padding: 10px;">
              ${opt}
            </button>
          `).join("")}
        </div>

        <div id="connector-quiz-feedback" style="display: none; padding: 12px; border-radius: 6px; font-size: 13px;"></div>
      `;

      quizBox.querySelectorAll(".connector-opt-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const val = btn.dataset.val;
          const fb = quizBox.querySelector("#connector-quiz-feedback");
          fb.style.display = "block";

          sound.playClick();
          if (val === q.ans) {
            sound.playCorrect();
            this.app.addXP(15);
            fb.style.background = "rgba(0, 242, 161, 0.1)";
            fb.style.border = "1px solid var(--success)";
            fb.style.color = "var(--success)";
            fb.innerHTML = `🎉 <strong>回答正确！</strong> ${q.example}`;
          } else {
            sound.playIncorrect();
            fb.style.background = "rgba(255, 107, 107, 0.1)";
            fb.style.border = "1px solid var(--error)";
            fb.style.color = "var(--error)";
            fb.innerHTML = `❌ <strong>答案错误。</strong> 正确关联词是：<strong>${q.ans}</strong>。<br>${q.example}`;
          }

          setTimeout(() => {
            currentQuizIdx = (currentQuizIdx + 1) % CHINESE_CONNECTORS.length;
            renderQuizItem();
          }, 2400);
        });
      });
    };

    renderQuizItem();
  }
}
