# 📚 AI StudyMate

> Turn your study material into exam-ready knowledge with AI.

AI StudyMate is an AI-powered academic study assistant that transforms lecture notes, textbooks, and PDF study material into structured, exam-focused resources.

Built with **Python, Streamlit, IBM watsonx.ai, and Llama 4 Maverick**.

---

## ✨ Features

- 📄 **PDF Upload** — Upload lecture notes, textbooks, study guides, and other PDF material.
- 📝 **Manual Text Input** — Paste study material directly into the application.
- 🤖 **AI-Powered Study Pack** — Generate structured academic resources using IBM watsonx.ai.
- 📋 **Summary** — Quickly understand the main ideas from the provided material.
- 🧠 **Key Concepts** — Identify important concepts and explanations.
- 🔥 **Exam Focus** — Highlight important topics for examination preparation.
- ❓ **Viva Questions** — Generate viva-style questions and answers.
- 📝 **MCQs** — Generate multiple-choice questions for practice.
- 💡 **Simplify** — Make difficult concepts easier to understand.
- ⚡ **Last-Minute Revision** — Get a concise revision list before an exam.
- 🎨 **Premium UI** — Dark editorial interface with an obsidian, ivory, and champagne-gold design.
- 🔐 **Secure Credentials** — IBM credentials are stored using environment variables.

---

## 🧠 How It Works

```text
                    ┌─────────────────────┐
                    │        USER         │
                    │                     │
                    │   PDF / Text Input  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PDF PROCESSING     │
                    │        pypdf         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   STUDY MATERIAL    │
                    │        TEXT         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   IBM watsonx.ai    │
                    │                     │
                    │  Llama 4 Maverick   │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │          AI STUDY PACK         │
              │                                │
              │  📋 Summary                    │
              │  🧠 Key Concepts               │
              │  🔥 Exam Focus                 │
              │  ❓ Viva Questions             │
              │  📝 MCQs                       │
              │  💡 Simplify                   │
              │  ⚡ Last-Minute Revision       │
              └────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| IBM watsonx.ai | AI platform |
| Llama 4 Maverick | Generative AI model |
| pypdf | PDF text extraction |
| python-dotenv | Environment variable management |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📁 Project Structure

```text
AI-StudyMate/
│
├── app.py
├── pdf_processor.py
├── requirements.txt
├── test_connection.py
├── README.md
├── .gitignore
│
└── .env
```

> `.env` is intentionally excluded from GitHub because it contains private credentials.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/midhilch23/AI-StudyMate.git
```

### 2. Enter the project directory

```bash
cd AI-StudyMate
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
WATSONX_APIKEY=your_ibm_watsonx_api_key
WATSONX_PROJECT_ID=your_ibm_watsonx_project_id
```

Replace the placeholder values with your own IBM watsonx credentials.

### Security

Never commit your `.env` file to GitHub.

The project uses:

```text
.env
venv/
__pycache__/
```

in `.gitignore` to prevent sensitive credentials and local environment files from being committed.

---

## 🚀 Running the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing the IBM watsonx Connection

The project includes a connection test:

```text
test_connection.py
```

Run:

```bash
python test_connection.py
```

This can be used to verify that the IBM watsonx credentials and project configuration are correctly loaded.

---

## 📚 Study Pack

AI StudyMate generates seven different study resources.

### 📋 Summary

Provides a concise overview of the important information contained in the supplied study material.

### 🧠 Key Concepts

Identifies important concepts and provides explanations based on the provided material.

### 🔥 Exam Focus

Highlights important topics for exam preparation.

### ❓ Viva Questions

Generates questions, answers, and key points useful for viva preparation.

### 📝 MCQs

Generates multiple-choice questions with answers and explanations.

### 💡 Simplify

Explains selected concepts in a simpler way while preserving the source material.

### ⚡ Last-Minute Revision

Provides important facts for quick revision before an examination.

---

## 🎯 Source-Grounded Generation

AI StudyMate is designed to keep generated study resources grounded in the user's provided material.

The AI prompt instructs the model to avoid introducing unsupported outside information and to indicate when information is not covered in the provided material.

This makes the generated resources more relevant to the student's actual notes.

---

## 🎓 Example Workflow

A student has a lecture PDF before an examination.

Instead of manually creating revision material:

```text
Upload PDF
    ↓
Extract PDF text
    ↓
Send study material to IBM watsonx.ai
    ↓
Generate AI Study Pack
    ↓
Review Summary
    ↓
Study Key Concepts
    ↓
Review Exam Focus
    ↓
Practice Viva Questions
    ↓
Practice MCQs
    ↓
Simplify Difficult Concepts
    ↓
Use Last-Minute Revision
```

---

## 🔒 Security

Sensitive credentials are stored through environment variables rather than directly inside the source code.

The IBM watsonx API key should never be:

- Hardcoded into `app.py`
- Uploaded to GitHub
- Shared publicly
- Included in screenshots
- Committed to version control

---

## 📌 Current Project Status

| Feature | Status |
|---|---|
| Python Application | ✅ |
| Streamlit UI | ✅ |
| Premium UI | ✅ |
| PDF Upload | ✅ |
| PDF Text Extraction | ✅ |
| Manual Text Input | ✅ |
| IBM watsonx Integration | ✅ |
| Llama 4 Maverick | ✅ |
| AI Summary | ✅ |
| Key Concepts | ✅ |
| Exam Focus | ✅ |
| Viva Questions | ✅ |
| MCQs | ✅ |
| Concept Simplification | ✅ |
| Last-Minute Revision | ✅ |
| Environment Variables | ✅ |
| Git Repository | ✅ |
| GitHub Repository | ✅ |

---

## 🚀 Future Improvements

Planned future features include:

- 🧠 Interactive quiz mode
- 💬 Chat with uploaded study material
- 🔎 Retrieval-Augmented Generation (RAG)
- 📚 Multiple PDF/document support
- 📊 Study progress tracking
- 📥 Downloadable study packs
- 🎯 Personalized revision plans
- 🗂️ Study material management
- 📱 Improved mobile experience
- ☁️ Public deployment
- 📈 Learning analytics
- 🔖 Bookmarking important concepts

---

## 🎯 Project Goals

AI StudyMate aims to make academic preparation faster and more structured by transforming existing study material into useful, exam-focused resources.

The project combines:

**Generative AI + Document Processing + Cloud AI + Web Development**

into a practical student-focused application.

---

## 👨‍💻 Author

**Midhil**

B.Tech Computer Science — Artificial Intelligence & Machine Learning

---

## 📜 License

This project is currently intended as a personal portfolio and academic project.