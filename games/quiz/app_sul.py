import base64
import html
import time
from pathlib import Path

import streamlit as st

try:
    from .questions import CATEGORIES
    from .questions_game_logic import (
        QUESTION_TIME, MAX_SCORE, calculate_points,
        pick_questions, summarize
    )
except ImportError:
    from questions import CATEGORIES
    from questions_game_logic import (
        QUESTION_TIME, MAX_SCORE, calculate_points,
        pick_questions, summarize
    )

QUIZ_DIR = Path(__file__).resolve().parent

ASSETS_DIR = QUIZ_DIR.parents[1] / "assets"
QUIZ_ASSETS = ASSETS_DIR / "quiz"

CSS = """
<style>
.st-key-quiz{max-width:760px;margin:0 auto;direction:rtl;text-align:right;color:#3d2b1a;}
.st-key-quiz,.st-key-quiz p,.st-key-quiz label,.st-key-quiz span,.st-key-quiz div,
.st-key-quiz button{font-family:'Saudi','Tajawal',sans-serif !important;}
.st-key-quiz [data-testid="stMarkdownContainer"],.st-key-quiz [data-testid="stCheckbox"]{direction:rtl;text-align:right;}
.st-key-quiz .hero,.st-key-quiz .hint,.st-key-quiz .verdict,.st-key-quiz .score,.st-key-quiz .stat,
.st-key-quiz .opt{text-align:center;}

/* عناوين الشاشات */
.st-key-quiz .hero{padding:.2rem 0 .2rem;}
.st-key-quiz .hero .t{font-weight:700;font-size:clamp(2rem,7vw,3rem);color:#8B5E3C;line-height:1.25;margin:0;}
.st-key-quiz .hero .s{color:#5a4632;font-size:1.2rem;margin-top:.2rem;}
.st-key-quiz .band{height:10px;margin:.8rem auto 1.2rem;max-width:320px;border-radius:2px;
 background:repeating-linear-gradient(90deg,#8B5E3C 0 14px,transparent 14px 20px);opacity:.65;}
.st-key-quiz .pick{font-weight:700;font-size:1.6rem;margin:.2rem 0 .7rem;color:#3d2b1a;}

/* بطاقة السؤال */
.st-key-quiz .qcard{background:rgba(255,250,238,.9);border:2px solid rgba(139,94,60,.5);
 border-bottom:6px solid #8B5E3C;border-radius:22px;padding:1.3rem 1.6rem 1.4rem;margin-bottom:1.2rem;
 box-shadow:0 8px 24px rgba(90,60,30,.18);}
.st-key-quiz .qcard .q{font-size:1.55rem;font-weight:700;line-height:1.7;margin:.5rem 0 0;color:#3d2b1a;}
.st-key-quiz .chip{display:inline-block;background:#8B5E3C;color:#fff8ea !important;border-radius:999px;
 padding:.15rem 1rem;font-size:.9rem;box-shadow:0 2px 6px rgba(90,60,30,.25);}
.st-key-quiz .topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;
 font-size:1.15rem;color:#3d2b1a;}

/* المؤقت */
.st-key-quiz .timer{height:12px;border-radius:999px;background:rgba(139,94,60,.22);overflow:hidden;margin:.4rem 0 .3rem;}
.st-key-quiz .timer>div{height:100%;background:#8B5E3C;border-radius:999px;transition:width 1s linear;}
.st-key-quiz .timer.low>div{background:#9c4a22;}
.st-key-quiz .hint{color:#5a4632;font-size:1rem;margin-bottom:1rem;}

/* الصورة */
.st-key-quiz [data-testid="stFullScreenFrame"],.st-key-quiz [data-testid="stImage"]{
 display:flex !important;justify-content:center !important;width:100% !important;margin-bottom:1.2rem;}
.st-key-quiz .stImage img,.st-key-quiz [data-testid="stImage"] img{max-height:300px;width:auto;max-width:100%;
 object-fit:cover;border-radius:16px;border:3px solid #8B5E3C;}
.st-key-quiz .noimg{text-align:center;border:2px dashed #8B5E3C;border-radius:16px;padding:1.4rem;
 margin-bottom:1.2rem;color:#5a4632;}

/* الأزرار: نفس شكل أزرار الواجهة الرئيسية (حبّة بنية) */
.st-key-quiz [data-testid="stElementContainer"],.st-key-quiz .stButton,.st-key-quiz [data-testid="stCheckbox"]{width:100% !important;}
.st-key-quiz .stButton>button{width:100% !important;border-radius:999px;padding:.6rem 1rem;min-height:3rem;
 background:#fff8ea !important;color:#3d2b1a !important;border:2px solid #8B5E3C !important;box-shadow:none;}
.st-key-quiz .stButton>button p{font-size:1.1rem;font-weight:700;color:inherit !important;}
.st-key-quiz .stButton>button:hover{background:#f1e0c2 !important;border-color:#3d2b1a !important;color:#3d2b1a !important;}
.st-key-quiz .stButton>button[kind="primary"],.st-key-quiz .stButton>button[data-testid="stBaseButton-primary"]{
 background:#8B5E3C !important;color:#fff !important;border:none !important;min-height:3.3rem;}
.st-key-quiz .stButton>button[kind="primary"] p,.st-key-quiz .stButton>button[data-testid="stBaseButton-primary"] p{
 font-size:1.25rem;color:#fff !important;}
.st-key-quiz .stButton>button[kind="primary"]:hover,.st-key-quiz .stButton>button[data-testid="stBaseButton-primary"]:hover{
 background:#8B5E3C !important;filter:brightness(1.12);color:#fff !important;}
.st-key-quiz .stButton>button:disabled{opacity:.45;}

/* التصنيفات: كل تصنيف في سطر مستقل */
.st-key-quiz .stCheckbox label{
    width:100%;
    cursor:pointer;
    display:flex;
    align-items:center;
    gap:1rem;
}

.st-key-quiz .stCheckbox p{
    flex:1;
    width:auto;
    font-size:1.6rem;
    font-weight:700;
    color:#3d2b1a;
    margin:0;
    white-space:nowrap;
}

.st-key-quiz .stCheckbox:hover{
    border-color:#8B5E3C;
}

.st-key-quiz .stCheckbox:has(input:checked),
.st-key-quiz .stCheckbox:has(label[data-selected="true"]){
    background:rgba(241,224,194,.97);
    border-color:#8B5E3C;
}
/* خيارات الإجابة: كبيرة ومتساوية الحجم */
.st-key-quiz_opts button{min-height:92px;padding:.8rem 1rem;border-radius:20px !important;}
.st-key-quiz_opts button p{font-size:1.3rem !important;line-height:1.5;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem;direction:rtl;}
.st-key-quiz .opt{min-height:92px;display:flex;align-items:center;justify-content:center;
 border-radius:20px;padding:.8rem 1rem;font-size:1.3rem;font-weight:700;line-height:1.5;
 background:#fff8ea;color:#3d2b1a;border:2px solid #8B5E3C;}
.st-key-quiz .opt.right{background:linear-gradient(180deg,#9b6a42,#8B5E3C);color:#fff8ea;border-color:#8B5E3C;box-shadow:0 6px 16px rgba(139,94,60,.35);}
.st-key-quiz .opt.wrong{background:linear-gradient(180deg,#4a3623,#3d2b1a);color:#f1e7d0;border-color:#3d2b1a;}
.st-key-quiz .opt.right::before,.st-key-quiz .opt.wrong::before{font-size:1.3rem;margin-inline-end:.7rem;}
.st-key-quiz .opt.right::before{content:"✓";}
.st-key-quiz .opt.wrong::before{content:"✕";}
.st-key-quiz .vmark{display:inline-flex;align-items:center;justify-content:center;width:2.2rem;height:2.2rem;border-radius:50%;
 background:#8B5E3C;color:#fff8ea;font-size:1.2rem;margin-inline-start:.6rem;vertical-align:middle;}
.st-key-quiz .vmark.bad{background:#3d2b1a;}
.st-key-quiz .opt.dim{opacity:.5;}
.st-key-quiz .verdict{font-size:1.6rem;font-weight:700;margin:.8rem 0 1rem;color:#3d2b1a;}

/* النتيجة */
.st-key-quiz .score{padding:1rem 0 .4rem;}
.st-key-quiz .score .num{font-weight:700;font-size:clamp(4rem,18vw,6.5rem);color:#8B5E3C;line-height:1.1;}
.st-key-quiz .score .of{font-size:1.2rem;color:#5a4632;}
.st-key-quiz .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin:1rem 0 1.6rem;}
.st-key-quiz .stat{background:rgba(255,250,238,.88);border:2px solid rgba(139,94,60,.5);border-radius:18px;padding:.9rem .3rem;}
.st-key-quiz .stat b{display:block;font-size:1.9rem;color:#8B5E3C;}
.st-key-quiz .stat span{font-size:.95rem;color:#5a4632;}
@media (max-width:640px){.opts{grid-template-columns:1fr;}.st-key-quiz .qcard .q{font-size:1.3rem;}}
@media (prefers-reduced-motion:reduce){.st-key-quiz .timer>div{transition:none;}}
</style>
"""

class _State:
    _P = "quiz_"

    def __getattr__(self, name):
        try:
            return st.session_state[self._P + name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        st.session_state[self._P + name] = value


S = _State()


def init_state():
    defaults = {"screen": "categories", "questions": [], "index": 0, "results": [],
                "q_start": 0.0, "answered": None, "round_cats": []}
    for key, value in defaults.items():
        st.session_state.setdefault("quiz_" + key, value)


def go(screen):
    if screen == "categories":
        for name in CATEGORIES:
            st.session_state[f"quiz_cat_{name}"] = name in S.round_cats
    S.screen = screen


def selected_categories():
    return [name for name in CATEGORIES if st.session_state.get(f"quiz_cat_{name}", False)]


def set_all_categories(value):
    for name in CATEGORIES:
        st.session_state[f"quiz_cat_{name}"] = value


def start_round(cats):
    S.round_cats = list(cats)
    S.questions = pick_questions(set(cats))
    S.index = 0
    S.results = []
    S.answered = None
    S.q_start = time.time()
    go("quiz")


def submit_answer(choice):
    q = S.questions[S.index]
    elapsed = time.time() - S.q_start
    timed_out = choice is None or elapsed > QUESTION_TIME
    is_correct = (not timed_out) and choice == q["answer"]
    record = {"correct": is_correct, "points": calculate_points(elapsed, is_correct),
              "timed_out": timed_out, "choice": choice, "text": q["question"]}
    S.results.append(record)
    S.answered = record


def next_question():
    S.index += 1
    S.answered = None
    S.q_start = time.time()
    if S.index >= len(S.questions):
        go("result")


def find_image(path_str):
    base = QUIZ_ASSETS / Path(path_str).name

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


def categories_screen():
    st.markdown(
        '<div class="hero"><div class="s">لعبة أسئلة ثقافية عن المملكة العربية السعودية</div></div>'
        '<div class="band"></div>',
        unsafe_allow_html=True)
    st.markdown('<div class="pick">اختر التصنيفات</div>', unsafe_allow_html=True)
    st.button("تحديد جميع التصنيفات", key="quiz_select_all", on_click=set_all_categories, args=(True,))

    for name, icon in CATEGORIES.items():
        st.checkbox(f"{icon} {name}", key=f"quiz_cat_{name}")

    chosen = selected_categories()
    if not chosen:
        st.markdown('<div class="hint">اختر تصنيفًا واحدًا على الأقل لتبدأ</div>', unsafe_allow_html=True)
    if st.button("ابدأ اللعب", key="quiz_start", type="primary", disabled=not chosen):
        start_round(chosen)
        st.rerun()


@st.fragment(run_every=1)
def timed_question():
    idx = S.index
    q = S.questions[idx]
    elapsed = time.time() - S.q_start
    if elapsed >= QUESTION_TIME:
        submit_answer(None)
        st.rerun()
    remaining = QUESTION_TIME - int(elapsed)
    low = "low" if remaining <= 5 else ""
    st.markdown(
        f'<div class="timer {low}"><div style="width:{remaining / QUESTION_TIME * 100}%"></div></div>'
        f'<div class="hint">⏱ {remaining} ثانية</div>'
        f'<div class="qcard"><span class="chip">{CATEGORIES[q["category"]]} {q["category"]}</span>'
        f'<p class="q">{html.escape(q["question"])}</p></div>', unsafe_allow_html=True)
    show_image(q)
    with st.container(key="quiz_opts"):
        cols = st.columns(2)
        for i, option in enumerate(q["options"]):
            if cols[i % 2].button(option, key=f"quiz_opt_{idx}_{i}"):
                submit_answer(option)
                st.rerun()


def feedback_view(q, record):
    if record["timed_out"]:
        verdict = 'انتهى الوقت<span class="vmark bad">✕</span>'
    elif record["correct"]:
        verdict = 'إجابة صحيحة<span class="vmark">✓</span>'
    else:
        verdict = 'إجابة خاطئة<span class="vmark bad">✕</span>'
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
        f'<div class="qcard"><span class="chip">{CATEGORIES[q["category"]]} {q["category"]}</span>'
        f'<p class="q">{html.escape(q["question"])}</p></div>', unsafe_allow_html=True)
    show_image(q)
    st.markdown(
        f'<div class="verdict">{verdict}</div><div class="opts">{boxes}</div>', unsafe_allow_html=True)
    last = S.index == len(S.questions) - 1
    if st.button("عرض النتيجة" if last else "السؤال التالي", key="quiz_next", type="primary"):
        next_question()
        st.rerun()


def quiz_screen():
    idx = S.index
    q = S.questions[idx]
    st.markdown(f'<div class="topbar"><b>السؤال {idx + 1} من {len(S.questions)}</b></div>',
                unsafe_allow_html=True)
    if S.answered is None:
        timed_question()
    else:
        feedback_view(q, S.answered)


def result_screen():
    stats = summarize(S.results)
    st.markdown(
        f'<div class="hero"><div class="t">انتهت الجولة</div></div><div class="band"></div>'
        f'<div class="score"><div class="num">{stats["score"]}</div><div class="of">من {MAX_SCORE} نقطة</div></div>'
        f'<div class="stats">'
        f'<div class="stat"><b>{stats["correct"]}</b><span>إجابات صحيحة</span></div>'
        f'<div class="stat"><b>{stats["wrong"]}</b><span>إجابات خاطئة</span></div>'
        f'<div class="stat"><b>{stats["timeouts"]}</b><span>انتهى وقتها</span></div></div>',
        unsafe_allow_html=True)
    if st.button("العب مرة أخرى", key="quiz_again", type="primary"):
        start_round(S.round_cats)
        st.rerun()
    st.button("اختيار التصنيفات", key="quiz_to_categories", on_click=go, args=("categories",))


SCREENS = {"categories": categories_screen, "quiz": quiz_screen, "result": result_screen}


def show_quiz_game():
    """يعرض لعبة المعلومات داخل صفحة اللعبة في app.py."""
    init_state()

    # لو اللاعب طلع من اللعبة في منتصف سؤال ورجع بعد انتهاء وقته، نبدأ من اختيار التصنيفات
    if (S.screen == "quiz" and S.answered is None
            and time.time() - S.q_start > QUESTION_TIME + 1):
        go("categories")

    st.markdown(CSS, unsafe_allow_html=True)
    with st.container(key="quiz"):
        SCREENS[S.screen]()


ASSETS = QUIZ_DIR.parents[1] / "assets"
if not (ASSETS / "background.png").exists():
    ASSETS = QUIZ_DIR / "assets"
FONTS = ASSETS / "fonts"


@st.cache_data(show_spinner=False)
def _b64(path_str, mtime):
    return base64.b64encode(Path(path_str).read_bytes()).decode()


def _asset_b64(path):
    return _b64(str(path), path.stat().st_mtime) if path.exists() else None


def apply_site_theme():
    css = ""
    for fname, weight in (("SaudiWeb-Regular.woff2", 400), ("SaudiWeb-Bold.woff2", 700)):
        data = _asset_b64(FONTS / fname)
        if data:
            css += (f"@font-face{{font-family:'Saudi';font-style:normal;font-weight:{weight};"
                    f"font-display:swap;src:url(data:font/woff2;base64,{data}) format('woff2');}}\n")
    bg = _asset_b64(ASSETS / "background.png")
    if bg:
        css += (f".stApp{{background-image:url('data:image/png;base64,{bg}');"
                "background-size:cover;background-position:center;background-attachment:fixed;}\n")
    css += """
    html,body,[class*="css"],.stApp{font-family:'Saudi','Tajawal',sans-serif !important;direction:rtl;}
    .stApp{background-color:#f1dfc3;}
    header[data-testid="stHeader"],#MainMenu,footer{display:none;}
    .block-container{padding-top:2.5rem;max-width:1100px;}
    .game-title{text-align:center;font-weight:700 !important;font-size:4rem !important;color:#8B5E3C !important;
      margin:0;line-height:1.2;font-family:'Saudi','Tajawal',sans-serif !important;}
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def run_standalone():
    """يشغّل لعبة المعلومات كموقع مستقل (نفس صفحة اللعبة في الواجهة الرئيسية)."""
    st.set_page_config(page_title="لعبة المعلومات", page_icon="🇸🇦", layout="wide")
    apply_site_theme()
    st.markdown('<h1 class="game-title">لعبة المعلومات</h1>', unsafe_allow_html=True)
    show_quiz_game()


if __name__ == "__main__":
    run_standalone()
