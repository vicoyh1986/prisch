/* Printable Singapore Exam Worksheet Generator with Working Grids & Answer Keys */
import { sound } from "./sound.js";

export class WorksheetExporter {
  constructor(app) {
    this.app = app;
  }

  async generatePrintableWorksheet(level, subject, questionCount = 10) {
    sound.playClick();
    const questions = await this.app.db.getRandomQuestions(level, subject, questionCount);
    if (!questions || questions.length === 0) {
      alert("Unable to generate worksheet for selected level/subject.");
      return;
    }

    const printWin = window.open("", "_blank");
    if (!printWin) {
      alert("Please allow popups to generate printable worksheets.");
      return;
    }

    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>MOE Prep - ${level} ${subject.toUpperCase()} Practice Worksheet</title>
        <style>
          @page {
            size: A4;
            margin: 15mm;
          }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #000;
            background: #fff;
            line-height: 1.6;
            font-size: 13pt;
            padding: 10px;
          }
          .header-box {
            border: 2px solid #000;
            padding: 12px;
            margin-bottom: 24px;
          }
          .header-title {
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
          }
          .meta-row {
            display: flex;
            justify-content: space-between;
            font-size: 11pt;
            margin-bottom: 6px;
          }
          .question-item {
            margin-bottom: 24px;
            page-break-inside: avoid;
          }
          .q-text {
            font-weight: 600;
            margin-bottom: 8px;
          }
          .mcq-opts {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-left: 20px;
          }
          .opt-item {
            font-size: 11pt;
          }
          .working-space {
            height: 90px;
            border: 1px dashed #bbb;
            border-radius: 4px;
            margin: 8px 0;
            position: relative;
          }
          .working-space::after {
            content: "Show your working here:";
            position: absolute;
            top: 4px;
            left: 6px;
            font-size: 9pt;
            color: #888;
          }
          .ans-line {
            text-align: right;
            font-weight: bold;
            margin-top: 6px;
          }
          .page-break {
            page-break-before: always;
          }
          .ans-key-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 14px;
          }
          .ans-key-table th, .ans-key-table td {
            border: 1px solid #000;
            padding: 8px;
            font-size: 10pt;
            text-align: left;
          }
          .ans-key-table th {
            background: #eee;
          }
        </style>
      </head>
      <body>
        <div class="header-box">
          <div class="header-title">SINGAPORE PRIMARY SCHOOL MASTERY PORTAL</div>
          <div class="meta-row">
            <span><strong>Level:</strong> ${level}</span>
            <span><strong>Subject:</strong> ${subject.toUpperCase()}</span>
            <span><strong>Marks:</strong> _____ / ${questions.length * 2}</span>
          </div>
          <div class="meta-row">
            <span><strong>Student Name:</strong> ______________________</span>
            <span><strong>Date:</strong> ________________</span>
          </div>
        </div>

        <div class="questions-list">
          ${questions.map((q, idx) => `
            <div class="question-item">
              <div class="q-text">
                Question ${idx + 1}. [${q.topic}]
              </div>
              <div style="margin-bottom: 8px; font-size: 11.5pt;">
                ${q.question}
              </div>

              ${q.type === 'mcq' ? `
                <div class="mcq-opts">
                  ${q.options.map((opt, i) => `
                    <div class="opt-item">(${i + 1}) ${opt}</div>
                  `).join("")}
                </div>
                <div class="ans-line">Answer: ( &nbsp;&nbsp;&nbsp;&nbsp; )</div>
              ` : `
                <div class="working-space"></div>
                <div class="ans-line">Ans: _________________________</div>
              `}
            </div>
          `).join("")}
        </div>

        <!-- Answer Key on Separate Page -->
        <div class="page-break"></div>
        <div style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 14px;">
          EXAMINER'S ANSWER KEY & HEURISTIC SOLUTIONS
        </div>
        
        <table class="ans-key-table">
          <thead>
            <tr>
              <th style="width: 40px;">Qn</th>
              <th style="width: 140px;">Topic</th>
              <th style="width: 120px;">Correct Answer</th>
              <th>Heuristic / Model Working Method</th>
            </tr>
          </thead>
          <tbody>
            ${questions.map((q, idx) => `
              <tr>
                <td style="text-align: center; font-weight: bold;">${idx + 1}</td>
                <td>${q.topic}</td>
                <td style="font-weight: bold; color: #008000;">${q.answer}</td>
                <td style="font-size: 9.5pt; white-space: pre-line;">${q.explanation}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>

        <script>
          window.onload = function() {
            window.print();
          };
        </script>
      </body>
      </html>
    `;

    printWin.document.write(htmlContent);
    printWin.document.close();
  }
}
