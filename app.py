import html
import os
import re

import streamlit as st
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from pdf_processor import extract_text_from_pdf


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")


# ============================================================
# IBM WATSONX CREDENTIALS
# ============================================================

credentials = Credentials(
    url="https://eu-gb.ml.cloud.ibm.com",
    api_key=api_key
)


# ============================================================
# IBM WATSONX MODEL
# ============================================================

model = Model(
    model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    credentials=credentials,
    project_id=project_id
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# AI PROMPT (unchanged)
# ============================================================

def build_prompt(study_material):
    return f"""
You are AI StudyMate, an academic AI assistant for university students.

STRICT SOURCE RULE:

You must use ONLY the information contained in the STUDY MATERIAL below.

You must NOT add, invent, assume, expand, infer, or explain any information
that is not explicitly stated in the STUDY MATERIAL.

Do NOT use your general knowledge.

If something cannot be answered using the STUDY MATERIAL, write exactly:

"Not covered in the provided material."

Create concise, exam-focused study resources using this exact format:

## 📋 SUMMARY

5-8 bullet points.

Every bullet must contain information explicitly stated in the
STUDY MATERIAL.

## 🧠 KEY CONCEPTS

Exactly 8 important concepts.

For each concept provide:
- Concept:
- Explanation:

The explanation must contain ONLY information explicitly stated
in the STUDY MATERIAL.

## 🔥 EXAM FOCUS

Exactly 5 important topics.

For each provide:
- Topic:
- Why it is important:

Use ONLY information from the STUDY MATERIAL.

## ❓ VIVA QUESTIONS

Exactly 8 questions.

For each provide:
- Q:
- Answer:
- Key points:

Every answer must be directly supported by the STUDY MATERIAL.

## 📝 MCQs

Exactly 5 MCQs.

Each MCQ must contain:

Question:
A)
B)
C)
D)
Correct Answer:
Explanation:

All questions, options, answers, and explanations must use ONLY
information from the STUDY MATERIAL.

Do not create options using outside knowledge.

## 💡 SIMPLIFY

Exactly 3 concepts.

Explain them simply while preserving the meaning of the
STUDY MATERIAL.

Do not add outside examples or information.

## ⚡ LAST-MINUTE REVISION

Give 8-12 of the most important facts from the STUDY MATERIAL.

FINAL SOURCE CHECK:

Before producing the answer, check every statement against the
STUDY MATERIAL.

If a statement is not explicitly supported by the STUDY MATERIAL,
remove it.

Do not add:
- outside facts
- outside examples
- additional terminology
- additional definitions
- additional metrics
- applications not mentioned
- assumptions
- general knowledge

STUDY MATERIAL:

{study_material}
"""


# ============================================================
# STYLING
# ============================================================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0A0A0B; --bg2: #11110F; --card: #151513; --elev: #1A1916; --border: #292720;
    --border-hi: #4A4331; --text: #F2EFE7; --text2: #B8B3A8; --muted: #77736A;
    --gold: #C6A15B; --gold-hi: #D4B56E; --gold-dk: #8F7545; --ok: #8FAF8F; --err: #B87970;
    --serif: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
    --sans: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif;
}
html, body { overflow-x: hidden; }
html, body, .stApp, .stMarkdown, button, textarea, input { font-family: var(--sans); }
.stApp {
    color: var(--text); overflow-x: hidden; background-attachment: fixed;
    background:
        radial-gradient(ellipse 70% 45% at 50% -5%, rgba(198,161,91,.13), transparent 70%),
        radial-gradient(ellipse 60% 40% at 92% 100%, rgba(84,58,32,.20), transparent 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, transparent 55%, rgba(0,0,0,.45) 100%),
        var(--bg);
}
.stApp::before {
    content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: .04;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='.6'/></svg>");
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { position: relative; z-index: 1; max-width: 1040px; padding: 1.75rem 1.25rem 3rem; }
.stMarkdown p, .stMarkdown li { color: var(--text); }
code { background: var(--elev); color: var(--gold-hi); padding: 1px 6px; border-radius: 5px; font-size: .88em; }

/* Header */
.sm-header { display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding-bottom: 1.1rem; border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.sm-brand-wrap { display: flex; align-items: center; gap: 12px; }
.sm-logo { width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(180deg, #1F1D18, #151513); border: 1px solid var(--border);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05), 0 4px 12px rgba(0,0,0,.4); }
.sm-brand { font-size: 1rem; font-weight: 600; letter-spacing: .01em; color: var(--text); line-height: 1.2; }
.sm-brand-sub { font-size: .74rem; color: var(--muted); letter-spacing: .04em; }
.sm-status { font-size: .68rem; font-weight: 500; letter-spacing: .16em; color: var(--text2);
    display: flex; align-items: center; gap: 8px; }
.sm-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--ok); box-shadow: 0 0 8px rgba(143,175,143,.55); }
.sm-dot.off { background: var(--gold-dk); box-shadow: none; }

/* Hero */
.sm-hero { text-align: center; padding: 2.6rem 0 1.9rem; }
.sm-eyebrow-gold { font-size: .68rem; font-weight: 500; letter-spacing: .28em; color: var(--gold); margin-bottom: 1rem; }
.sm-hero h1 { font-family: var(--serif); font-weight: 500; font-size: clamp(2.1rem, 5vw, 3.4rem); line-height: 1.08;
    letter-spacing: -.01em; color: var(--text); margin: 0 0 1rem; padding: 0; }
.sm-hero h1 em { color: var(--gold); font-style: italic; }
.sm-hero p { color: var(--text2); font-size: 1rem; line-height: 1.65; max-width: 520px; margin: 0 auto; }

/* Workspace card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, #1A1916 0%, #151513 100%);
    border: 1px solid var(--border) !important; border-radius: 14px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05), 0 2px 4px rgba(0,0,0,.3), 0 24px 48px -12px rgba(0,0,0,.6);
}
.sm-ws-title { font-size: .72rem; font-weight: 500; letter-spacing: .2em; color: var(--text); }
.sm-ws-sub { font-size: .88rem; color: var(--muted); margin: .3rem 0 .6rem; }

/* Tabs: underline style (results) */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--border); overflow-x: auto;
    scrollbar-width: none; flex-wrap: nowrap; }
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
.stTabs [data-baseweb="tab"] { height: auto; padding: 12px 14px; background: transparent; white-space: nowrap;
    transition: color .2s ease; }
.stTabs [data-baseweb="tab"] p { font-size: .72rem; font-weight: 500; letter-spacing: .14em; color: var(--muted); transition: color .2s ease; }
.stTabs [data-baseweb="tab"]:hover p { color: var(--text2); }
.stTabs [aria-selected="true"] p { color: var(--text) !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--gold) !important; height: 2px; }
.stTabs [data-baseweb="tab-border"] { background-color: transparent !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem; }

/* Tabs: segmented style (input modes) */
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [data-baseweb="tab-list"] {
    width: fit-content; max-width: 100%; background: #0F0F0D; border: 1px solid var(--border);
    border-radius: 10px; padding: 4px; gap: 4px; }
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [data-baseweb="tab"] { padding: 7px 16px; border-radius: 7px;
    transition: background .2s ease, color .2s ease; }
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [aria-selected="true"] { background: var(--gold) !important; }
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [aria-selected="true"] p { color: #0A0A0B !important; font-weight: 600; }
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [data-baseweb="tab-highlight"] { display: none; }
[data-testid="stVerticalBlockBorderWrapper"] .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }

/* Inputs */
[data-testid="stFileUploaderDropzone"], [data-testid="stFileUploader"] section {
    background: #0F0F0D; border: 1px dashed #3B372B; border-radius: 12px; padding: 2rem 1.25rem;
    transition: border-color .25s ease, background .25s ease; }
[data-testid="stFileUploaderDropzone"]:hover, [data-testid="stFileUploader"] section:hover {
    border-color: var(--gold-dk); background: #12120F; }
[data-testid="stFileUploaderDropzoneInstructions"] span, [data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploader"] small { color: var(--text2); }
[data-testid="stFileUploader"] button { background: transparent; color: var(--gold-hi); border: 1px solid var(--gold-dk);
    border-radius: 8px; transition: background .2s ease; }
[data-testid="stFileUploader"] button:hover { background: rgba(198,161,91,.08); border-color: var(--gold); color: var(--gold-hi); }
[data-testid="stFileUploaderFile"] { color: var(--text); }
.stTextArea textarea { background: #0F0F0D; color: var(--text); border: 1px solid var(--border); border-radius: 10px;
    font-size: .96rem; line-height: 1.65; transition: border-color .2s ease; }
.stTextArea textarea::placeholder { color: var(--muted); }
.stTextArea textarea:focus { border-color: var(--gold-dk); box-shadow: 0 0 0 1px var(--gold-dk); }

/* Primary button */
.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {
    background: var(--gold); border: none; border-radius: 10px; height: 2.9rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.28), 0 6px 18px rgba(198,161,91,.12);
    transition: transform .2s ease, box-shadow .2s ease, background .2s ease; }
.stButton > button[kind="primary"] p, [data-testid="stBaseButton-primary"] p {
    color: #0A0A0B; font-weight: 600; font-size: .82rem; letter-spacing: .12em; }
.stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background: var(--gold-hi); transform: translateY(-2px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.3), 0 12px 28px rgba(198,161,91,.2); }
.stButton > button[kind="primary"]:active { transform: translateY(0); }

/* Notices */
.sm-notice { display: flex; gap: 12px; align-items: flex-start; padding: .85rem 1rem; margin: .75rem 0 0;
    background: var(--elev); border: 1px solid var(--border); border-radius: 10px; color: var(--text2); font-size: .9rem; }
.sm-notice .sm-n-label { font-size: .66rem; font-weight: 600; letter-spacing: .18em; margin-bottom: 2px; }
.sm-notice .sm-n-file { color: var(--text); font-size: .94rem; word-break: break-all; }
.sm-notice.ok { border-left: 2px solid var(--ok); } .sm-notice.ok .sm-n-label, .sm-notice.ok .sm-n-ico { color: var(--ok); }
.sm-notice.err { border-left: 2px solid var(--err); } .sm-notice.err .sm-n-label, .sm-notice.err .sm-n-ico { color: var(--err); }
.sm-notice.warn { border-left: 2px solid var(--gold-dk); } .sm-notice.warn .sm-n-label, .sm-notice.warn .sm-n-ico { color: var(--gold); }

/* Results heading */
.sm-results { margin: 2.8rem 0 1.4rem; }
.sm-results h2 { font-family: var(--serif); font-weight: 500; font-size: 2rem; color: var(--text); margin: 0 0 .3rem; padding: 0; }
.sm-results p { color: var(--muted); font-size: .92rem; margin: 0 0 1.2rem; }
.sm-rule { height: 1px; background: linear-gradient(90deg, var(--gold-dk), var(--border) 40%, transparent); }
.sm-fade { animation: smFade .5s ease both; }
@keyframes smFade { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

/* Cards */
.sm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 14px; perspective: 1000px; }
.sm-card { position: relative; background: linear-gradient(180deg, #171715, #151513); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.2rem 1.3rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 1px 2px rgba(0,0,0,.4), 0 10px 24px -8px rgba(0,0,0,.5);
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease; }
.sm-card:hover { transform: translateY(-3px); border-color: var(--border-hi);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 2px 4px rgba(0,0,0,.4), 0 18px 36px -8px rgba(0,0,0,.65); }
.sm-eyebrow { font-size: .64rem; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: .55rem; }
.sm-eyebrow.muted { color: var(--muted); margin: .7rem 0 .25rem; }
.sm-title { font-size: 1.03rem; font-weight: 600; color: var(--text); line-height: 1.4; margin-bottom: .45rem; }
.sm-body { color: var(--text2); font-size: .93rem; line-height: 1.7; }
.sm-body strong, .sm-read strong { color: var(--text); font-weight: 600; }
.sm-prio { display: flex; gap: 16px; align-items: flex-start; }
.sm-num { font-family: var(--serif); font-size: 1.9rem; line-height: 1; color: var(--gold); min-width: 38px; }

/* Summary reading card */
.sm-read { background: linear-gradient(180deg, #1A1916, #151513); border: 1px solid var(--border); border-radius: 14px;
    padding: 1.6rem 1.8rem; box-shadow: inset 0 1px 0 rgba(255,255,255,.05), 0 20px 40px -12px rgba(0,0,0,.55); }
.sm-read ul { list-style: none; margin: 0; padding: 0; }
.sm-read li { position: relative; padding: .7rem 0 .7rem 1.4rem; font-size: 1.02rem; line-height: 1.8; color: #E4E0D6;
    border-bottom: 1px solid #23211B; }
.sm-read li:last-child { border-bottom: none; }
.sm-read li::before { content: ""; position: absolute; left: 0; top: 1.35rem; width: 5px; height: 5px; border-radius: 50%; background: var(--gold); }

/* Viva + generic expanders */
[data-testid="stExpander"] { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    overflow: hidden; margin-bottom: .6rem; transition: border-color .25s ease; }
[data-testid="stExpander"]:hover { border-color: var(--border-hi); }
[data-testid="stExpander"] details { border: none !important; background: transparent !important; }
[data-testid="stExpander"] summary { padding: .9rem 1.1rem; }
[data-testid="stExpander"] summary p { color: var(--text); font-size: .98rem; font-weight: 500; }
[data-testid="stExpander"] summary:hover p { color: var(--gold-hi); }
.sm-lbl { font-size: .64rem; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: .35rem; }
.sm-lbl.gap { margin-top: 1rem; }
.sm-bullets { margin: 0; padding-left: 1.1rem; color: var(--text2); line-height: 1.75; font-size: .93rem; }
.sm-bullets li::marker { color: var(--gold-dk); }

/* MCQ */
.sm-opt { display: flex; gap: 12px; align-items: flex-start; padding: .6rem .8rem; margin-top: .5rem; background: #11110F;
    border: 1px solid var(--border); border-radius: 9px; color: var(--text2); font-size: .94rem; line-height: 1.55;
    transition: border-color .2s ease; }
.sm-opt:hover { border-color: var(--border-hi); }
.sm-opt-l { flex: 0 0 24px; height: 24px; border-radius: 6px; border: 1px solid var(--gold-dk); color: var(--gold);
    font-size: .74rem; font-weight: 600; display: flex; align-items: center; justify-content: center; }
.sm-correct { color: var(--ok); font-weight: 500; line-height: 1.55; }
.sm-mcq-gap { height: .9rem; }

/* Revision */
.sm-rev { position: relative; background: radial-gradient(ellipse 70% 120% at 50% -20%, rgba(198,161,91,.09), transparent 60%),
    linear-gradient(180deg, #1A1916, #151513); border: 1px solid var(--border); border-radius: 14px; padding: 1.8rem 1.8rem 1.2rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05), 0 24px 48px -12px rgba(0,0,0,.6); overflow: hidden; }
.sm-rev::before { content: ""; position: absolute; top: 0; left: 12%; right: 12%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.sm-rev h3 { font-family: var(--serif); font-weight: 500; font-size: 1.55rem; letter-spacing: .02em; color: var(--text); margin: 0 0 .25rem; padding: 0; }
.sm-rev-sub { color: var(--muted); font-size: .9rem; margin-bottom: 1.1rem; }
.sm-rev-row { display: flex; gap: 18px; align-items: baseline; padding: .85rem .5rem; border-top: 1px solid #23211B;
    border-radius: 8px; transition: background .2s ease; }
.sm-rev-row:hover { background: rgba(198,161,91,.04); }
.sm-rev-n { font-family: var(--serif); font-size: 1.45rem; color: var(--gold); min-width: 38px; line-height: 1; }
.sm-rev-t { color: var(--text); font-size: 1.02rem; line-height: 1.65; }

/* Footer */
.sm-footer { text-align: center; margin-top: 3.5rem; padding-top: 1.3rem; border-top: 1px solid var(--border);
    color: var(--muted); font-size: .76rem; letter-spacing: .06em; line-height: 1.8; }
.sm-footer b { color: var(--text2); font-weight: 500; letter-spacing: .14em; text-transform: uppercase; font-size: .7rem; }

@media (max-width: 640px) {
    .block-container { padding: 1rem .8rem 2rem; }
    .sm-hero { padding: 1.6rem 0 1.2rem; }
    .sm-read { padding: 1.1rem 1.1rem; } .sm-rev { padding: 1.3rem 1rem .8rem; }
    .sm-results h2 { font-size: 1.6rem; }
}
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
    .sm-card:hover, .stButton > button[kind="primary"]:hover { transform: none; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# PARSING HELPERS (presentation only - AI text is never altered)
# ============================================================

SECTION_PREFIXES = [
    ("SUMMARY", "📋 SUMMARY"),
    ("KEY_CONCEPTS", "🧠 KEY CONCEPTS"),
    ("EXAM_FOCUS", "🔥 EXAM FOCUS"),
    ("VIVA", "❓ VIVA QUESTIONS"),
    ("MCQS", "📝 MCQs"),
    ("SIMPLIFY", "💡 SIMPLIFY"),
    ("REVISION", "⚡ LAST-MINUTE REVISION"),
]

TAB_LABELS = [
    "SUMMARY", "CONCEPTS", "EXAM FOCUS", "VIVA", "MCQs", "SIMPLIFY", "REVISION",
]

KEY_PATTERNS = {
    "CONCEPT": r"Concept(?:\s*\d+)?",
    "EXPLANATION": r"Explanation",
    "TOPIC": r"Topic(?:\s*\d+)?",
    "WHY": r"Why(?:\s+it\s+is\s+important)?",
    "QUESTION": r"Question(?:\s*\d+)?|Q\s*\d*",
    "ANSWER": r"Answer",
    "KEY_POINTS": r"Key\s+points?",
    "A": r"A", "B": r"B", "C": r"C", "D": r"D",
    "CORRECT": r"Correct\s+Answer",
}

SEPARATOR_RE = re.compile(r"^\s*[-_=*]{3,}\s*$")
MARKER_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)]|#{1,6})\s+")


def split_response(response):
    """Route AI output into sections using the same '## ' split and prefixes."""
    found = {}
    for section in response.split("## "):
        for key, prefix in SECTION_PREFIXES:
            if section.startswith(prefix):
                body = section.split("\n", 1)[1] if "\n" in section else ""
                found[key] = body.strip()
    return found


def parse_records(text, keys, start_key):
    """Parse 'Key: value' blocks (tolerant of bullets and bold) into dicts."""
    matchers = [
        (
            key,
            re.compile(
                r"^\s*(?:[-*•]\s*)?(?:\d+[.)]\s*)?(?:\*\*)?(?:" + KEY_PATTERNS[key]
                + r")(?:\*\*)?\s*[:)]\s*(?:\*\*)?\s*(.*)$",
                re.IGNORECASE,
            ),
        )
        for key in keys
    ]
    records, current, last_key = [], None, None
    for line in text.splitlines():
        if SEPARATOR_RE.match(line):
            continue
        hit = None
        for key, pattern in matchers:
            match = pattern.match(line)
            if match:
                hit = (key, match.group(1).strip().strip("*").strip())
                break
        if hit:
            key, value = hit
            if current is None or key == start_key:
                if current:
                    records.append(current)
                current = {}
            current[key] = value
            last_key = key
        elif line.strip() and current is not None and last_key:
            current[last_key] += "\n" + line.strip()
    if current:
        records.append(current)
    return [r for r in records if start_key in r]


def group_items(text):
    """Split free text into items (bullets/numbers/headings, else paragraphs)."""
    lines = [l for l in text.splitlines() if not SEPARATOR_RE.match(l)]
    items = []
    if any(MARKER_RE.match(l) for l in lines):
        for line in lines:
            if not line.strip():
                continue
            if MARKER_RE.match(line) or not items:
                items.append(MARKER_RE.sub("", line).strip())
            else:
                items[-1] += " " + line.strip()
    else:
        paragraph = []
        for line in lines + [""]:
            if line.strip():
                paragraph.append(line.strip())
            elif paragraph:
                items.append(" ".join(paragraph))
                paragraph = []
    return [i for i in items if i]


def split_title(item):
    """Split 'Title: body' / '**Title** body' into (title, body)."""
    match = re.match(r"^\*\*(.+?)\*\*\s*[:\-–—]*\s*(.*)$", item)
    if match:
        return match.group(1).strip(" :"), match.group(2).strip()
    match = re.match(r"^([^:]{2,70}):\s+(.+)$", item)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, item



# ============================================================
# HTML HELPERS
# ============================================================

def fmt(text):
    """Escape text for HTML, keep line breaks, render **bold** and `code`."""
    safe = html.escape(text or "")
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"`(.+?)`", r"<code>\1</code>", safe)
    return safe.replace("\n", "<br>")


def html_block(markup):
    # Collapse whitespace so Markdown never treats indented HTML as code.
    st.markdown(re.sub(r"\n\s*", "", markup), unsafe_allow_html=True)


def bullets_html(text):
    items = group_items(text)
    if not items:
        return ""
    return "<ul class='sm-bullets'>" + "".join(f"<li>{fmt(i)}</li>" for i in items) + "</ul>"


def render_raw(text):
    """Fallback: show the AI's own markdown untouched."""
    st.markdown(text if text.strip() else "No content generated for this section.")


def render_notice(kind, message, label=None):
    """Styled status message. kind: ok | err | warn."""
    icon = {"ok": "✓", "err": "!", "warn": "!"}[kind]
    label_html = f"<div class='sm-n-label'>{html.escape(label)}</div>" if label else ""
    body_class = "sm-n-file" if kind == "ok" else ""
    html_block(
        f"""<div class='sm-notice {kind}'><span class='sm-n-ico'>{icon}</span>
        <div>{label_html}<div class='{body_class}'>{html.escape(message)}</div></div></div>"""
    )


def render_card_grid(cards):
    html_block(f"<div class='sm-grid sm-fade'>{''.join(cards)}</div>")


# ============================================================
# UI COMPONENTS
# ============================================================

def render_header():
    ready = bool(api_key) and bool(project_id)
    status = (
        "<span class='sm-dot'></span>SYSTEM READY" if ready
        else "<span class='sm-dot off'></span>SETUP REQUIRED"
    )
    logo = (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#C6A15B" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5C4.7 19 4 18.3 4 17.5z"/>'
        '<path d="M20 5.5C20 4.7 19.3 4 18.5 4H13v15h5.5c.8 0 1.5-.7 1.5-1.5z"/></svg>'
    )
    html_block(
        f"""<div class='sm-header'>
        <div class='sm-brand-wrap'><div class='sm-logo'>{logo}</div>
        <div><div class='sm-brand'>AI StudyMate</div><div class='sm-brand-sub'>AI-powered academic workspace</div></div></div>
        <div class='sm-status'>{status}</div></div>"""
    )


def render_hero():
    html_block(
        """<div class='sm-hero'><div class='sm-eyebrow-gold'>AI STUDY WORKSPACE</div>
        <h1>Turn your notes<br><em>into exam-ready knowledge.</em></h1>
        <p>Transform lecture notes, textbooks and PDFs into focused study resources using AI.</p></div>"""
    )


def render_input_workspace():
    """Input card with PDF / pasted text. Returns the study material text."""
    with st.container(border=True):
        html_block(
            "<div class='sm-ws-title'>YOUR STUDY MATERIAL</div>"
            "<div class='sm-ws-sub'>Upload a PDF or paste your notes. If both are provided, the PDF is used.</div>"
        )
        pdf_tab, text_tab = st.tabs(["Upload PDF", "Paste Text"])
        with pdf_tab:
            uploaded_pdf = st.file_uploader(
                "Upload PDF",
                type=["pdf"],
                label_visibility="collapsed"
            )
        with text_tab:
            study_material = st.text_area(
                "📖 Study Material",
                height=280,
                placeholder="Paste lecture notes, textbook content, or study material...",
                label_visibility="collapsed"
            )

        # ====================================================
        # PDF TEXT EXTRACTION
        # ====================================================

        if uploaded_pdf:

            try:
                study_material = extract_text_from_pdf(uploaded_pdf)
            except Exception as e:
                study_material = ""
                with pdf_tab:
                    render_notice("err", f"Could not read this PDF: {e}")
            else:
                with pdf_tab:
                    if study_material.strip():
                        render_notice("ok", uploaded_pdf.name, label="DOCUMENT READY")
                    else:
                        render_notice("err", "Could not extract text from this PDF.")

    return study_material


def render_summary(text):
    items = bullets_html(text)
    if not items:
        render_raw(text)
        return
    html_block(f"<div class='sm-read sm-fade'>{items.replace('sm-bullets', 'sm-read-list')}</div>")


def render_concepts(text):
    records = parse_records(text, ["CONCEPT", "EXPLANATION"], "CONCEPT")
    if not records:
        render_raw(text)
        return
    render_card_grid([
        f"""<div class='sm-card'><div class='sm-eyebrow'>Concept {i:02d}</div>
        <div class='sm-title'>{fmt(r.get('CONCEPT'))}</div>
        <div class='sm-body'>{fmt(r.get('EXPLANATION'))}</div></div>"""
        for i, r in enumerate(records, start=1)
    ])


def render_exam_focus(text):
    records = parse_records(text, ["TOPIC", "WHY"], "TOPIC")
    if not records:
        render_raw(text)
        return
    render_card_grid([
        f"""<div class='sm-card sm-prio'><div class='sm-num'>{i:02d}</div>
        <div><div class='sm-title'>{fmt(r.get('TOPIC'))}</div>
        <div class='sm-eyebrow muted'>Why it matters</div>
        <div class='sm-body'>{fmt(r.get('WHY'))}</div></div></div>"""
        for i, r in enumerate(records, start=1)
    ])


def render_viva(text):
    records = parse_records(text, ["QUESTION", "ANSWER", "KEY_POINTS"], "QUESTION")
    if not records:
        render_raw(text)
        return
    for index, record in enumerate(records, start=1):
        question = record.get("QUESTION", "").replace("*", "")
        with st.expander(f"{index:02d}   {question}"):
            html_block(f"<div class='sm-lbl'>Answer</div><div class='sm-body'>{fmt(record.get('ANSWER'))}</div>")
            points = bullets_html(record.get("KEY_POINTS", ""))
            if points:
                html_block(f"<div class='sm-lbl gap'>Key points</div>{points}")


def render_mcqs(text):
    records = parse_records(
        text, ["QUESTION", "A", "B", "C", "D", "CORRECT", "EXPLANATION"], "QUESTION"
    )
    if not records:
        render_raw(text)
        return
    for index, record in enumerate(records, start=1):
        options = "".join(
            f"<div class='sm-opt'><span class='sm-opt-l'>{letter}</span><span>{fmt(record.get(letter))}</span></div>"
            for letter in "ABCD" if record.get(letter)
        )
        html_block(
            f"""<div class='sm-card' style='margin-bottom:.5rem'><div class='sm-eyebrow'>Question {index:02d}</div>
            <div class='sm-title'>{fmt(record.get('QUESTION'))}</div>{options}</div>"""
        )
        with st.expander("Reveal answer and explanation"):
            html_block(
                f"""<div class='sm-lbl'>Correct answer</div>
                <div class='sm-correct'>{fmt(record.get('CORRECT'))}</div>
                <div class='sm-lbl gap'>Explanation</div>
                <div class='sm-body'>{fmt(record.get('EXPLANATION'))}</div>"""
            )
        html_block("<div class='sm-mcq-gap'></div>")


def render_simplify(text):
    records = parse_records(text, ["CONCEPT", "EXPLANATION"], "CONCEPT")
    if records:
        pairs = [(r.get("CONCEPT"), r.get("EXPLANATION", "")) for r in records]
    else:
        pairs = [split_title(i) for i in group_items(text)]
    if not pairs:
        render_raw(text)
        return
    render_card_grid([
        f"""<div class='sm-card'><div class='sm-eyebrow'>In plain words · {i:02d}</div>
        {f"<div class='sm-title'>{fmt(title)}</div>" if title else ""}
        <div class='sm-body'>{fmt(body)}</div></div>"""
        for i, (title, body) in enumerate(pairs, start=1)
    ])


def render_revision(text):
    items = group_items(text)
    if not items:
        render_raw(text)
        return
    rows = "".join(
        f"<div class='sm-rev-row'><div class='sm-rev-n'>{i:02d}</div><div class='sm-rev-t'>{fmt(item)}</div></div>"
        for i, item in enumerate(items, start=1)
    )
    html_block(
        f"""<div class='sm-rev sm-fade'><h3>LAST-MINUTE REVISION</h3>
        <div class='sm-rev-sub'>The essentials to remember before the exam.</div>{rows}</div>"""
    )


def render_results(response):
    html_block(
        "<div class='sm-results'><h2>Your Study Pack</h2>"
        "<p>Prepared from your source material.</p><div class='sm-rule'></div></div>"
    )
    sections = split_response(response)
    tabs = st.tabs(TAB_LABELS)

    with tabs[0]:
        render_summary(sections.get("SUMMARY", ""))
    with tabs[1]:
        render_concepts(sections.get("KEY_CONCEPTS", ""))
    with tabs[2]:
        render_exam_focus(sections.get("EXAM_FOCUS", ""))
    with tabs[3]:
        render_viva(sections.get("VIVA", ""))
    with tabs[4]:
        render_mcqs(sections.get("MCQS", ""))
    with tabs[5]:
        render_simplify(sections.get("SIMPLIFY", ""))
    with tabs[6]:
        render_revision(sections.get("REVISION", ""))


def render_footer():
    html_block(
        "<div class='sm-footer'><b>AI StudyMate</b><br>"
        "Built with Python • Streamlit • IBM watsonx.ai</div>"
    )


# ============================================================
# APP
# ============================================================

render_header()
render_hero()

study_material = render_input_workspace()


# ============================================================
# GENERATE STUDY MATERIAL
# ============================================================

st.write("")
_, center, _ = st.columns([2, 3, 2])
with center:
    generate_clicked = st.button(
        "GENERATE STUDY PACK  →",
        type="primary",
        use_container_width=True
    )

if generate_clicked:

    if study_material.strip():

        prompt = build_prompt(study_material)

        with st.spinner("Generating your study material..."):

            try:

                response = model.generate_text(
                    prompt=prompt,
                    params={
                        "max_new_tokens": 2500,
                        "temperature": 0
                    }
                )

                st.session_state["study_response"] = response

            except Exception as e:

                st.session_state.pop("study_response", None)
                render_notice("err", f"Error generating study material: {e}")

    else:

        render_notice("warn", "Please enter some study material first.")


# ============================================================
# RESULTS
# ============================================================

if st.session_state.get("study_response"):
    render_results(st.session_state["study_response"])

render_footer()