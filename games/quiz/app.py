
import html
import time
from pathlib import Path

import streamlit as st

from questions import CATEGORIES
from questions_game_logic import (QUESTION_TIME, MAX_SCORE, calculate_points,
                        pick_questions, summarize)

st.set_page_config(page_title="لعبة السعودية الثقافية", page_icon="🇸🇦", layout="centered")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Tajawal:wght@400;500;700&display=swap');
:root{--deep:#0B3D2E;--palm:#006C35;--gold:#C8A24A;--sand:#F1E7D0;--ink:#14201B;}
html,body,.stApp,.stApp *{font-family:'Tajawal',sans-serif;}
h1,h2,h3,.kufi{font-family:'Reem Kufi','Tajawal',sans-serif !important;}
.stApp{direction:rtl;background-color:var(--deep);
 background-image:linear-gradient(135deg,rgba(200,162,74,.07) 25%,transparent 25%),
 linear-gradient(225deg,rgba(200,162,74,.07) 25%,transparent 25%);
 background-size:44px 44px;color:var(--sand);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{max-width:760px;padding-top:2rem;}
.stApp p,.stApp label,.stApp span{color:inherit;}
.stApp [data-testid="stMarkdownContainer"],.stApp [data-testid="stCheckbox"],.stApp [data-testid="stExpander"]{direction:rtl;text-align:right;}
.card,.topbar,.opts,.stats,.score,.hero{direction:rtl;}
.card,.topbar{text-align:right;}
.hero,.hint,.verdict,.score,.stat,.opt{text-align:center;}
.hero{text-align:center;padding:1.6rem 1rem .4rem;}
.hero h1{font-size:clamp(2.2rem,8vw,3.8rem);color:var(--sand);margin:0;line-height:1.25;}
.hero p{color:#cdbf9b;font-size:1.1rem;margin-top:.6rem;}
.band{height:10px;margin:1rem auto;max-width:360px;border-radius:2px;
 background:repeating-linear-gradient(90deg,var(--gold) 0 14px,transparent 14px 20px);opacity:.8;}
.pick{font-family:'Reem Kufi',sans-serif;font-size:1.6rem;margin:.2rem 0 .6rem;color:var(--sand);}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem;margin:1rem 0 1.6rem;}
.stat{border:1px solid rgba(200,162,74,.45);border-radius:6px;padding:.8rem .3rem;text-align:center;}
.stat b{display:block;font-size:1.7rem;color:var(--gold);font-family:'Reem Kufi',sans-serif;}
.stat span{font-size:.85rem;color:#cdbf9b;}
.card{background:var(--sand);color:var(--ink);border-radius:14px;padding:1.4rem 1.5rem;
 border-bottom:5px solid var(--gold);margin-bottom:1.2rem;}
.card .q{font-size:1.5rem;font-weight:700;line-height:1.7;margin:.4rem 0 0;color:var(--ink);}
[data-testid="stFullScreenFrame"]{display:flex !important;justify-content:center !important;width:100% !important;margin-bottom:1.2rem;}
.stImage img{max-height:300px;width:auto;max-width:100%;object-fit:cover;border-radius:12px;border:3px solid var(--gold);}
.noimg{text-align:center;border:2px dashed var(--gold);border-radius:12px;padding:1.4rem;margin-bottom:1.2rem;color:#cdbf9b;}
.chip{display:inline-block;background:var(--palm);color:#fff !important;border-radius:20px;padding:.1rem .8rem;font-size:.85rem;}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;color:var(--sand);}
.timer{height:12px;border-radius:6px;background:rgba(241,231,208,.18);overflow:hidden;margin:.4rem 0 .3rem;}
.timer>div{height:100%;background:var(--gold);transition:width 1s linear;}
.timer.low>div{background:#e2574c;}
.hint{text-align:center;color:#cdbf9b;font-size:.95rem;margin-bottom:1rem;}
.stButton>button{width:100%;border-radius:10px;padding:.7rem 1rem;min-height:3rem;
 background:var(--sand);color:var(--ink);border:2px solid transparent;}
.stButton>button p{font-size:1.1rem;font-weight:500;}
.stButton>button:hover{border-color:var(--gold);color:var(--ink);background:#fff;}
.stButton>button[kind="primary"]{background:var(--gold);color:var(--ink);border:none;min-height:3.4rem;}
.stButton>button[kind="primary"] p{font-size:1.25rem;font-weight:700;}
.stButton>button[kind="primary"]:hover{background:#d8b45c;color:var(--ink);}
.stButton>button:disabled{opacity:.45;}
/* عناصر Streamlit بعرض كامل */
[data-testid="stElementContainer"],.stButton,[data-testid="stCheckbox"]{width:100% !important;}
.stButton>button{width:100% !important;}
/* التصنيفات: كل تصنيف في سطر مستقل، كبير وواضح */
.stCheckbox{background:rgba(241,231,208,.08);border:2px solid rgba(200,162,74,.45);border-radius:14px;
 padding:1.1rem 1.4rem;margin-bottom:.75rem;}
.stCheckbox label{width:100%;cursor:pointer;display:flex;align-items:center;gap:1rem;}
.stCheckbox p{font-size:1.7rem;font-weight:700;color:var(--sand);margin:0;}
.stCheckbox:hover{border-color:var(--gold);}
.stCheckbox:has(input:checked),.stCheckbox:has(label[data-selected="true"]){background:rgba(200,162,74,.24);border-color:var(--gold);}
.stCheckbox label>div:first-of-type{width:1.9rem;height:1.9rem;min-width:1.9rem;border-radius:6px;}
.stCheckbox label[data-selected="true"]>div:first-of-type{background:var(--gold) !important;border-color:var(--gold) !important;}
.stCheckbox label[data-selected="true"] svg polyline{stroke:var(--ink) !important;}
/* خيارات الإجابة: كبيرة ومتساوية الحجم */
.st-key-opts button{min-height:92px;padding:.8rem 1rem;border-radius:12px;background:var(--sand);border:2px solid var(--gold);}
.st-key-opts button p{font-size:1.35rem;font-weight:700;line-height:1.5;color:var(--ink);}
.st-key-opts button:hover{background:#fff;border-color:var(--palm);}
.st-key-opts .stButton,.st-key-opts [data-testid="stButton"],.st-key-opts [data-testid="stElementContainer"]{width:100% !important;}
.st-key-opts button{width:100% !important;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem;}
.opt{min-height:92px;display:flex;align-items:center;justify-content:center;text-align:center;
 border-radius:12px;padding:.8rem 1rem;font-size:1.35rem;font-weight:700;line-height:1.5;
 background:var(--sand);color:var(--ink);border:2px solid var(--gold);}
.opt.right{background:#1f9d57;color:#fff;border-color:#1f9d57;}
.opt.wrong{background:#c0392b;color:#fff;border-color:#c0392b;}
.opt.dim{opacity:.5;}
.verdict{text-align:center;font-size:1.5rem;font-weight:700;margin:.8rem 0 1rem;}
.score{text-align:center;padding:1.4rem 0 .4rem;}
.score .num{font-family:'Reem Kufi',sans-serif;font-size:clamp(4rem,18vw,6.5rem);color:var(--gold);line-height:1;}
.score .of{font-size:1.2rem;color:#cdbf9b;}
@media (max-width:640px){.opts{grid-template-columns:1fr;}.card .q{font-size:1.3rem;}}
@media (prefers-reduced-motion:reduce){.timer>div{transition:none;}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

def init_state():
    defaults = {"screen": "categories", "questions": [], "index": 0, "results": [],
                "q_start": 0.0, "answered": None, "round_cats": []}
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def go(screen):
    if screen == "categories":
        for name in CATEGORIES:
            st.session_state[f"cat_{name}"] = name in st.session_state.round_cats
    st.session_state.screen = screen


def selected_categories():
    return [name for name in CATEGORIES if st.session_state.get(f"cat_{name}", False)]


def set_all_categories(value):
    for name in CATEGORIES:
        st.session_state[f"cat_{name}"] = value


def start_round(cats):
    st.session_state.round_cats = list(cats)
    st.session_state.questions = pick_questions(set(cats))
    st.session_state.index = 0
    st.session_state.results = []
    st.session_state.answered = None
    st.session_state.q_start = time.time()
    go("quiz")


def submit_answer(choice):
    q = st.session_state.questions[st.session_state.index]
    elapsed = time.time() - st.session_state.q_start
    timed_out = choice is None or elapsed > QUESTION_TIME
    is_correct = (not timed_out) and choice == q["answer"]
    record = {"correct": is_correct, "points": calculate_points(elapsed, is_correct),
              "timed_out": timed_out, "choice": choice, "text": q["question"]}
    st.session_state.results.append(record)
    st.session_state.answered = record


def next_question():
    st.session_state.index += 1
    st.session_state.answered = None
    st.session_state.q_start = time.time()
    if st.session_state.index >= len(st.session_state.questions):
        go("result")


def find_image(path_str):
    base = Path(__file__).parent / path_str
    for ext in (base.suffix, ".jpg", ".jpeg", ".png", ".webp"):
        candidate = base.with_suffix(ext)
        if candidate.exists():
            return candidate
    return None


def show_image(q):
    if not q.get("image"):
        return
    found = find_image(q["image"])
    if found:
        st.image(str(found))
    else:
        st.markdown(f'<div class="noimg">🖼️ الصورة غير موجودة: {html.escape(q["image"])}</div>',
                    unsafe_allow_html=True)


# ------------------------------------------------------------------ الشاشات
def categories_screen():
    st.markdown(
        '<div class="hero"><h1>🇸🇦 اعرف السعودية</h1>'
        '<p>لعبة أسئلة ثقافية عن المملكة العربية السعودية</p></div><div class="band"></div>',
        unsafe_allow_html=True)
    st.markdown('<div class="pick">اختر التصنيفات</div>', unsafe_allow_html=True)
    st.button("تحديد جميع التصنيفات", on_click=set_all_categories, args=(True,))

    for name, icon in CATEGORIES.items():
        st.checkbox(f"{icon} {name}", key=f"cat_{name}")

    chosen = selected_categories()
    if not chosen:
        st.markdown('<div class="hint">اختر تصنيفًا واحدًا على الأقل لتبدأ</div>', unsafe_allow_html=True)
    if st.button("ابدأ اللعب", type="primary", disabled=not chosen):
        start_round(chosen)
        st.rerun()


@st.fragment(run_every=1)
def timed_question():
    idx = st.session_state.index
    q = st.session_state.questions[idx]
    elapsed = time.time() - st.session_state.q_start
    if elapsed >= QUESTION_TIME:          
        submit_answer(None)
        st.rerun()
    remaining = QUESTION_TIME - int(elapsed)
    low = "low" if remaining <= 5 else ""
    st.markdown(
        f'<div class="timer {low}"><div style="width:{remaining / QUESTION_TIME * 100}%"></div></div>'
        f'<div class="hint">⏱ {remaining} ثانية</div>'
        f'<div class="card"><span class="chip">{CATEGORIES[q["category"]]} {q["category"]}</span>'
        f'<p class="q">{html.escape(q["question"])}</p></div>', unsafe_allow_html=True)
    show_image(q)
    with st.container(key="opts"):
        cols = st.columns(2)
        for i, option in enumerate(q["options"]):
            if cols[i % 2].button(option, key=f"opt_{idx}_{i}"):
                submit_answer(option)
                st.rerun()


def feedback_view(q, record):
    if record["timed_out"]:
        verdict = "⏱ انتهى الوقت"
    elif record["correct"]:
        verdict = "✅ إجابة صحيحة"
    else:
        verdict = "❌ إجابة خاطئة"
    boxes = ""
    for option in q["options"]:
        if option == q["answer"]:
            css = "right"
        elif option == record["choice"]:
            css = "wrong"
        else:
            css = "dim"
        boxes += f'<div class="opt {css}">{html.escape(option)}</div>'
    st.markdown(
        f'<div class="card"><span class="chip">{CATEGORIES[q["category"]]} {q["category"]}</span>'
        f'<p class="q">{html.escape(q["question"])}</p></div>', unsafe_allow_html=True)
    show_image(q)
    st.markdown(
        f'<div class="verdict">{verdict}</div><div class="opts">{boxes}</div>', unsafe_allow_html=True)
    last = st.session_state.index == len(st.session_state.questions) - 1
    if st.button("عرض النتيجة" if last else "السؤال التالي", type="primary"):
        next_question()
        st.rerun()


def quiz_screen():
    idx = st.session_state.index
    q = st.session_state.questions[idx]
    st.markdown(f'<div class="topbar"><b>السؤال {idx + 1} من {len(st.session_state.questions)}</b></div>',
                unsafe_allow_html=True)
    if st.session_state.answered is None:
        timed_question()
    else:
        feedback_view(q, st.session_state.answered)


def result_screen():
    stats = summarize(st.session_state.results)
    st.markdown(
        f'<div class="hero"><h1>انتهت الجولة</h1></div><div class="band"></div>'
        f'<div class="score"><div class="num">{stats["score"]}</div><div class="of">من {MAX_SCORE} نقطة</div></div>'
        f'<div class="stats">'
        f'<div class="stat"><b>{stats["correct"]}</b><span>إجابات صحيحة</span></div>'
        f'<div class="stat"><b>{stats["wrong"]}</b><span>إجابات خاطئة</span></div>'
        f'<div class="stat"><b>{stats["timeouts"]}</b><span>انتهى وقتها</span></div></div>',
        unsafe_allow_html=True)
    if st.button("العب مرة أخرى", type="primary"):
        start_round(st.session_state.round_cats)
        st.rerun()
    st.button("الرئيسية", on_click=go, args=("categories",))


SCREENS = {"categories": categories_screen, "quiz": quiz_screen, "result": result_screen}

init_state()
SCREENS[st.session_state.screen]()