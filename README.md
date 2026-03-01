# 🤖 AI Job Application Agent

An intelligent browser automation agent that automatically fills and submits job application forms using your personal profile. Built with [`browser-use`](https://github.com/browser-use/browser-use) and powered by Claude AI.

---

## ✨ Features

- 🧠 **AI-powered form filling** — understands field context and maps your profile intelligently
- 📄 **Auto resume upload** — injects PDF/DOCX directly via JavaScript, no OS file dialog needed
- 📝 **Cover letter auto-fill** — loads from your `.docx` file and pastes into cover letter fields
- 🔽 **Smart dropdown handling** — selects closest matching option automatically
- 🙋 **Human fallback** — asks you in the terminal whenever it's stuck or unsure
- ✅ **Checkbox fix** — simulates full pointer events to handle React-based custom checkboxes (e.g. LinkedIn consent)
- 🔍 **Final review step** — scrolls the full page and fixes validation errors before submitting

---

## 📁 Project Structure

```
.
├── job_agent.py                        # Main agent script
├── Arul_Murugan_Fullstack_Resume.pdf   # Your resume (place here)
├── Arul_Murugan_Cover_Letter.docx      # Your cover letter (place here)
└── README.md
```

---

## ⚙️ Requirements

### System
- Python 3.10+
- Google Chrome (running with remote debugging enabled)

### Python packages
```bash
pip install browser-use
```

### Start Chrome with remote debugging
```bash
# Windows
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"

# Linux
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
```

> **Why remote debugging?** The agent connects to your real browser session so LinkedIn recognizes you as already logged in. This avoids login automation and CAPTCHA issues.

---

## 🚀 Usage

### 1. Clone the repo
```bash
git clone https://github.com/arulmurugan01/ai-job-agent.git
cd ai-job-agent
```

### 2. Place your files
Put your resume and cover letter in the same folder:
```
Arul_Murugan_Fullstack_Resume.pdf
Arul_Murugan_Cover_Letter.docx
```

### 3. Set the job link
Open `job_agent.py` and update the `JOB_LINK` variable:
```python
JOB_LINK = "https://www.linkedin.com/jobs/view/YOUR_JOB_ID"
```

### 4. Run the agent
```bash
python job_agent.py
```

The agent will open the job page, fill the form, upload your resume, answer screening questions, and submit — asking you in the terminal only when it needs your help.

---

## 🛠 Configuration

At the top of `job_agent.py`:

```python
RESUME_PATH       = "./Arul_Murugan_Fullstack_Resume.pdf"
COVER_LETTER_PATH = "./Arul_Murugan_Cover_Letter.docx"
JOB_LINK          = "https://www.linkedin.com/jobs/view/..."
```

---

## 🙋 Human Fallback

When the agent can't fill a field automatically, it pauses and asks you in the terminal:

```
============================================================
🤖 Agent needs your input:
   Please manually select the location from the suggestions for field: Current Location
============================================================
Your answer: 
```

Type your answer and press Enter to continue.

---

## ⚠️ Known Issues & Fixes

### LinkedIn "I consent" checkbox won't check
**Why it happens:** LinkedIn uses React-based custom checkbox components that ignore simple `.click()` or `dispatchEvent` calls. The form validates against React's internal state, not the raw DOM.

**Fix applied:** The agent dispatches a full `mousedown → mouseup → click` pointer event sequence on the checkbox's parent container (`role="checkbox"` or associated label), which triggers React's synthetic event system properly. If that also fails, it falls back to simulating a `Space` keypress on the focused element. As a last resort it calls `ask_human` asking you to check it manually.

### Autocomplete fields don't resolve
**Why it happens:** Some portals (LinkedIn, Naukri) use async autocomplete that requires a real typing delay before suggestions appear.

**Fix applied:** The agent waits after typing and clicks the best suggestion. If no suggestion appears it calls `ask_human` immediately instead of guessing.

### Resume upload button opens OS dialog
**Why it happens:** Default file inputs trigger the OS file picker which automation tools can't control.

**Fix applied:** The `upload_resume` tool injects the file directly into the `<input type="file">` element via JavaScript `DataTransfer`, bypassing the OS dialog entirely.

---

## 📌 Supported Job Portals

| Portal | Status |
|---|---|
| LinkedIn Easy Apply | ✅ Tested |
| Naukri | 🔄 Compatible |
| Indeed | 🔄 Compatible |
| Internshala | 🔄 Compatible |
| Company career pages | 🔄 Most work |

---

## 📄 License

MIT License — free to use and modify.

---

## 🙏 Credits

Built using [browser-use](https://github.com/browser-use/browser-use) — open source browser automation for AI agents.
