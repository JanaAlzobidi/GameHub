"""
رحلة الشهب 🌠  |  Meteor Night - a short Saudi-themed story game
Run:  streamlit run game.py

الملفات:
  game.py   -> الواجهة والتصميم وتشغيل اللعبة (هذا الملف)
  story.py  -> نصوص القصة
  logic.py  -> منطق اللعبة (الوقت والقرارات والنهايات)

Images: put them in an "images" folder next to this file.
The scene -> file name mapping is in SCENE_IMAGES (search for it below).
"""
import base64
from pathlib import Path

import streamlit as st

from logic import (START_TIME, check_tires, choose_road, handle_stuck,
                   help_person, get_ending)
from story import (GAME_TITLE, TAGLINE, PROLOGUE, TIRE_EVENT, TIRE_CHECKED,
                   ROAD_EVENT, PAVED_RESULT, UNPAVED_AIRED, UNPAVED_NOT_AIRED,
                   STUCK_EVENT, STUCK_TRY, HELP_RESULT, PERSON_EVENT,
                   PERSON_HELPED, ENDINGS, CHAPTERS, SCENE_HINTS)

st.set_page_config(page_title=GAME_TITLE, page_icon="🌠", layout="centered")

# ───────────────────────── IMAGES (folder "images" next to this file) ─────────────────────────
IMAGES_DIR = Path(__file__).parent.parent / "assets"

# اسم المشهد  ->  اسم ملف الصورة داخل مجلد images
# أي مشهد ما له صورة هنا (أو الملف مو موجود) يستخدم الرسمة المدمجة بدلًا منها.
SCENE_IMAGES = {
     "title":      "الواجهة2.jpg",
    # المقدمة: p1 و p2 و p3 لسا ما لها صور → تظهر مكانها لوحة Placeholder
    # (صمم الصورة وسمّها بنفس الاسم هنا وحطها في مجلد images)
    "p1":         "زحمه الطرق.jpg",
    "p2":         "تخطيط2.jpg",
    "p3":         "تقويم.jpg",
    "p4":         "غفوه2.jpg",
    "p5":         "الاستيقاظ متأخرا.jpg",
    "p6":         "الانطلاق2.jpg",
    # الأحداث
    "tire":       "طريق حاره.jpg",
    "tire_ok":    "قيادة السيارة في طريق البر والتعامل مع الكفرات والطرق.jpg",
    "road":       "طريق مختصر.jpg",
    "paved":      "قيادة السيارة في طريق البر والتعامل مع الكفرات والطرق.jpg",
    "stuck":      "التغريز في رمال الصحراء.jpg",
    "aired":      "التغريز في رمال الصحراء.jpg",
    "help":       "مساعده بعد التغريز.jpg",
    "person":     "استغاثه بدون شهب.jpg",
    "person_ok":  "استغاثه بدون شهب.jpg",
    # النهايات
    "best":       "نهايه مثاليه.jpg",
    "best_win":   "فوز الصوره.jpg",
    "good":       "التأمل وتصوير النجوم (عند التأخر أو ضيق الوقت).jpg",
    "late":       "التأمل وتصوير النجوم (عند التأخر أو ضيق الوقت).jpg",
}


@st.cache_data(show_spinner=False)
def _b64(path_str, mtime):
    return base64.b64encode(Path(path_str).read_bytes()).decode()


def show_scene(key):
    name = SCENE_IMAGES.get(key)
    path = IMAGES_DIR / name if name else None
    if path and path.exists():
        ext = path.suffix.lower().lstrip(".")
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        data = _b64(str(path), path.stat().st_mtime)
        st.markdown(f'<div class="frame"><img src="data:{mime};base64,{data}"></div>', unsafe_allow_html=True)
    else:
        fname = name or f"{key}.jpg"
        hint = SCENE_HINTS.get(key, "")
        st.markdown(f'<div class="ph"><div class="ph-ic">🖼️</div><div class="ph-t">مكان الصورة · {key}</div>'
                    f'<div class="ph-h">{hint}</div><code>images/{fname}</code></div>', unsafe_allow_html=True)


# ───────────────────────── STYLE (RPG × Saudi theme) ─────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Aref+Ruqaa:wght@700&display=swap');
:root{ --gold:#D4AF37; --gold2:#F3DC8A; --gold-dim:rgba(212,175,55,.35);
       --g0:#010806; --g1:#03150e; --g2:#072a1c; --g3:#0d4a31; --panel:rgba(2,12,8,.93); --ink:#E4DDC3; --mist:rgba(127,214,192,.16); --imgmax:58vh; }
html, body, .stApp, [class*="css"], button { font-family:'Tajawal',sans-serif !important; }
.stApp{
  direction:rtl; color:var(--ink);
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cg fill='none' stroke='%23D4AF37' stroke-opacity='.10' stroke-width='1'%3E%3Crect x='25' y='25' width='40' height='40'/%3E%3Crect x='25' y='25' width='40' height='40' transform='rotate(45 45 45)'/%3E%3Ccircle cx='45' cy='45' r='9'/%3E%3C/g%3E%3C/svg%3E"),
    radial-gradient(ellipse at 50% -15%, var(--g3) 0%, var(--g2) 22%, var(--g1) 50%, var(--g0) 100%);
  background-attachment: fixed;
}
.stApp::before{ content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,.85) 100%); }
.stApp::after{ content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(1.6px 1.6px at 8% 12%, #fff, transparent), radial-gradient(1.2px 1.2px at 22% 38%, #F3DC8A, transparent),
    radial-gradient(1.8px 1.8px at 35% 9%, #fff, transparent), radial-gradient(1.2px 1.2px at 48% 27%, #fff, transparent),
    radial-gradient(1.6px 1.6px at 63% 14%, #F3DC8A, transparent), radial-gradient(1.2px 1.2px at 77% 33%, #fff, transparent),
    radial-gradient(1.8px 1.8px at 90% 10%, #fff, transparent), radial-gradient(1.2px 1.2px at 14% 72%, #fff, transparent),
    radial-gradient(1.6px 1.6px at 55% 82%, #F3DC8A, transparent), radial-gradient(1.2px 1.2px at 93% 66%, #fff, transparent),
    radial-gradient(ellipse 60% 22% at 20% 92%, var(--mist), transparent), radial-gradient(ellipse 55% 20% at 85% 78%, var(--mist), transparent);
  animation:breathe 7s ease-in-out infinite alternate; }
@keyframes breathe{ from{opacity:.35;} to{opacity:1;} }
#MainMenu, footer, header{ visibility:hidden; }
.block-container{ max-width:780px; padding-top:.6rem; padding-bottom:1rem; position:relative; z-index:1; }

/* Logo */
.logo{ text-align:center; margin:0 0 10px; }
.logo.compact{ position:fixed; top:8px; right:22px; z-index:20; margin:0; text-align:right; }
.logo.compact h1{ font-size:1.6rem; margin:0; }
.logo.compact .sub{ display:none; }
.stApp:has(.logo.compact) .block-container{ padding-top:.4rem; }
[data-testid="stElementContainer"]:has(.logo.compact){ height:0; margin-bottom:-1rem; }
@media (max-width:1150px){ .logo.compact{ position:static; margin-bottom:2px; } }
.logo .orn{ color:var(--gold); letter-spacing:4px; font-size:1rem; opacity:.9; }
.logo h1{ font-family:'Aref Ruqaa','Tajawal',serif !important; font-size:2.6rem; margin:0; line-height:1.3;
  background:linear-gradient(180deg,#fff6c9,var(--gold) 55%,#9a7a1c); -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; filter:drop-shadow(0 2px 6px rgba(0,0,0,.8)) drop-shadow(0 0 14px rgba(212,175,55,.35)); }
.logo .sub{ color:var(--gold2); font-size:.95rem; font-weight:500; }

/* Scene image */
[data-testid="stImage"] img, .frame{
  border:3px solid var(--gold); border-radius:6px; outline:1px solid var(--gold-dim); outline-offset:6px;
  box-shadow:0 0 0 6px rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.65), 0 0 24px rgba(212,175,55,.18); }
.frame{ overflow:hidden; margin:4px 0 12px; }
[data-testid="stElementContainer"]:has([data-testid="stImage"]), [data-testid="stImage"], [data-testid="stImageContainer"]{
  width:100% !important; max-width:100% !important; }
[data-testid="stImage"]{ margin-bottom:10px; padding:0; display:flex; justify-content:center; }
.card p{ margin:0; }
.frame{ width:100%; box-sizing:border-box; aspect-ratio:16/9; max-height:var(--imgmax); }
.frame img{ width:100%; height:100%; object-fit:cover; display:block; filter:brightness(.84) contrast(1.07) saturate(.85); }
.ph{ width:100%; box-sizing:border-box; aspect-ratio:16/9; max-height:var(--imgmax); margin:4px 0 12px; border:2px dashed var(--gold); border-radius:6px; background:rgba(2,12,8,.65);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px; text-align:center;
  box-shadow:inset 0 0 40px rgba(0,0,0,.6); }
.ph-ic{ font-size:2.4rem; opacity:.8; } .ph-t{ color:var(--gold); font-weight:800; font-size:1.05rem; }
.ph-h{ color:var(--ink); opacity:.75; font-size:.9rem; }
.ph code{ direction:ltr; unicode-bidi:isolate; color:var(--gold2); background:rgba(212,175,55,.1); border:1px solid var(--gold-dim);
  border-radius:4px; padding:1px 10px; font-size:.8rem; margin-top:4px; }
[data-testid="stImage"] img{ width:100% !important; box-sizing:border-box; height:min(56.25cqw, var(--imgmax)) !important; aspect-ratio:auto; max-height:none; object-fit:cover; }

[data-testid="stImage"] img{ filter:brightness(.84) contrast(1.07) saturate(.85);
  animation:emerge 1.5s ease both, lantern 5s ease-in-out infinite alternate; }
.frame{ animation:fadein 1.2s ease both, lantern 5s ease-in-out infinite alternate; }
@keyframes emerge{ from{opacity:0; filter:brightness(.15) blur(5px);} to{opacity:1; filter:brightness(.84) contrast(1.07) saturate(.85);} }
@keyframes fadein{ from{opacity:0;} to{opacity:1;} }
@keyframes lantern{
  from{ box-shadow:0 0 0 6px rgba(0,0,0,.5), 0 12px 34px rgba(0,0,0,.85), 0 0 16px rgba(212,175,55,.10); }
  to{ box-shadow:0 0 0 6px rgba(0,0,0,.5), 0 12px 34px rgba(0,0,0,.85), 0 0 44px rgba(212,175,55,.30), 0 0 100px rgba(18,96,63,.45); } }
.logo h1{ animation:glowtitle 4.5s ease-in-out infinite alternate; }
@keyframes glowtitle{
  from{ filter:drop-shadow(0 2px 6px rgba(0,0,0,.9)) drop-shadow(0 0 6px rgba(212,175,55,.15)); }
  to{ filter:drop-shadow(0 2px 6px rgba(0,0,0,.9)) drop-shadow(0 0 22px rgba(212,175,55,.55)); } }

/* HUD: a gold timeline from 8:00 (right) to 9:00 (left) */
.hud{ --c:#F3DC8A; --glow:rgba(212,175,55,.85); position:relative; padding:2px 4px 10px; margin-bottom:10px; }
.hud::after{ content:""; position:absolute; bottom:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg, transparent, var(--gold-dim), transparent); }
.hud-top{ display:flex; justify-content:space-between; align-items:baseline; }
.chapter{ color:var(--gold2); opacity:.7; font-size:.85rem; letter-spacing:.5px; }
.chapter::before{ content:"✦ "; color:var(--gold); }
.timelbl{ color:var(--ink); opacity:.85; font-size:.85rem; display:flex; align-items:baseline; gap:6px; }
.tnum{ font-family:'Aref Ruqaa','Tajawal',serif !important; font-size:1.7rem; line-height:1; color:var(--c); text-shadow:0 0 12px var(--glow); }
.tl{ display:flex; align-items:center; gap:12px; margin:10px 0 12px; }
.tl-lbl{ color:var(--gold); font-size:.8rem; font-weight:700; white-space:nowrap; }
.tl-lbl::before{ content:"◆ "; font-size:.65rem; }
.track{ position:relative; flex:1; height:2px; background:rgba(212,175,55,.25); border-radius:2px; }
.tick{ position:absolute; top:-5px; width:1px; height:12px; background:var(--gold-dim); }
.fill{ position:relative; z-index:2; height:2px; border-radius:2px; transition:width .9s ease;
  background:linear-gradient(270deg, rgba(212,175,55,.3), var(--c)); box-shadow:0 0 9px var(--glow); }
.fill::after{ content:""; position:absolute; left:-6px; top:50%; width:11px; height:11px; background:#fff6c9;
  transform:translateY(-50%) rotate(45deg); box-shadow:0 0 8px 2px var(--glow), 0 0 22px 6px var(--glow);
  animation:ember 2.4s ease-in-out infinite alternate; }
@keyframes ember{ from{ opacity:.65; box-shadow:0 0 6px 1px var(--glow), 0 0 14px 3px var(--glow); }
                  to{ opacity:1; box-shadow:0 0 9px 3px var(--glow), 0 0 26px 8px var(--glow); } }
.chips{ display:flex; flex-wrap:wrap; align-items:center; }
.chip{ color:var(--ink); opacity:.65; font-size:.8rem; }
.chip + .chip::before{ content:"·"; margin:0 9px; color:var(--gold); }

/* Dialogue box */
.card{ position:relative; background:var(--panel); border:2px solid var(--gold); border-radius:8px; padding:20px 24px 14px;
  margin:22px 0 12px; font-size:1.05rem; line-height:1.85; color:var(--ink); direction:rtl; text-align:right;
  box-shadow:inset 0 0 0 4px rgba(0,0,0,.55), inset 0 0 0 5px var(--gold-dim), 0 8px 24px rgba(0,0,0,.6);
  animation:rise .55s ease both; }
.card::before,.card::after{ content:"❖"; position:absolute; color:var(--gold); font-size:.95rem; background:var(--g0); padding:0 4px; }
.card::before{ bottom:-12px; left:18px; } .card::after{ bottom:-12px; right:18px; }
.nameplate{ position:absolute; top:-17px; right:22px; background:linear-gradient(180deg,var(--gold2),var(--gold) 60%,#9a7a1c);
  color:#1b1405; font-weight:800; font-size:.9rem; padding:3px 22px; border-radius:4px; border:1px solid #6e5410;
  box-shadow:0 3px 8px rgba(0,0,0,.6); }
.card h3{ color:var(--gold); font-family:'Aref Ruqaa','Tajawal',serif !important; font-size:1.9rem; margin:4px 0 8px; text-align:center; }
.card.end{ border-color:var(--gold2); box-shadow:inset 0 0 0 4px rgba(0,0,0,.55), inset 0 0 0 5px var(--gold), 0 0 34px rgba(212,175,55,.35), 0 8px 24px rgba(0,0,0,.6); }
@keyframes rise{ from{opacity:0; transform:translateY(14px); filter:blur(7px);} to{opacity:1; transform:none; filter:none;} }

/* Choice / action buttons */
.stButton > button{ width:100%; direction:rtl; text-align:center; color:var(--ink); font-size:1rem; font-weight:700;
  padding:.55rem 1.1rem; border-radius:6px; border:2px solid var(--gold-dim);
  background:linear-gradient(180deg,rgba(10,52,35,.9),rgba(2,14,9,.97)); box-shadow:0 3px 12px rgba(0,0,0,.7);
  transition:all .18s ease; }
.stButton > button p{ font-size:1rem; }
.stButton > button:hover{ border-color:var(--gold); color:#1b1405; transform:translateX(-4px);
  background:linear-gradient(180deg,var(--gold2),var(--gold)); box-shadow:0 0 18px rgba(212,175,55,.55); }
.stButton > button:hover p{ color:#1b1405; }
.stButton > button:focus:not(:active){ border-color:var(--gold); color:var(--ink); }
.stButton{ margin-bottom:4px; }
[data-testid="stColumn"] .stButton > button, [data-testid="column"] .stButton > button{ min-height:4.2rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── STATE ─────────────────────────
S = st.session_state

def reset():
    S.update(stage="title", i=0, time=START_TIME, aired=False, road=None, r_img="", r_texts=[], r_next="")

if "stage" not in S:
    reset()

def go(stage):
    S.stage = stage

def show(img, texts, nxt):
    S.update(stage="result", r_img=img, r_texts=texts, r_next=nxt)

def start():
    reset(); S.stage = "prologue"

def next_prologue():
    S.i += 1
    if S.i >= len(PROLOGUE):
        go("tire")

def pick_tire(c):
    S.time, S.aired = check_tires(c, S.time)
    if c == "A":
        show("tire_ok", [TIRE_CHECKED], "road")
    else:
        go("road")

def pick_road(c):
    S.time, S.road = choose_road(c, S.time)
    if S.road == "paved":
        show("paved", [PAVED_RESULT], "person")
    elif S.aired:
        S.time, _ = handle_stuck(True, None, S.time)
        show("aired", [UNPAVED_AIRED], "person")
    else:
        go("stuck")

def pick_stuck(c):
    S.time, _ = handle_stuck(False, c, S.time)
    show("help", ([STUCK_TRY] if c == "A" else []) + [HELP_RESULT], "person")

def pick_person(c):
    S.time = help_person(c, S.time)
    if c == "A":
        show("person_ok", [PERSON_HELPED], "ending")
    else:
        go("ending")

# ───────────────────────── UI HELPERS ─────────────────────────
def banner(compact=False):
    st.markdown(f'<div class="logo{" compact" if compact else ""}"><h1>{GAME_TITLE}</h1>'
                f'<div class="sub">{TAGLINE}</div></div>', unsafe_allow_html=True)

def hud():
    t = max(S.time, 0)
    pct = min(max((START_TIME - S.time) / START_TIME * 100, 0), 100)  # how far along 8:00 → 9:00
    key = S.r_img if S.stage == "result" else S.stage
    chips = ""
    if key != "tire":
        chips += f'<span class="chip">🛞 الكفرات: {"منسّمة" if S.aired else "عادية"}</span>'
    if S.road:
        chips += f'<span class="chip">🛣️ الطريق: {"ممهّد" if S.road == "paved" else "رملي"}</span>'
    ticks = "".join(f'<i class="tick" style="right:{x}%"></i>' for x in (20, 40, 60, 80))
    st.markdown(f'<div class="hud"><div class="hud-top"><span class="chapter">{CHAPTERS.get(key, "")}</span>'
                f'<span class="timelbl">الوقت المتبقي <span class="tnum">{t}</span> دقيقة</span></div>'
                f'<div class="tl"><span class="tl-lbl">٨:٠٠</span>'
                f'<div class="track">{ticks}<div class="fill" style="width:{pct}%"></div></div>'
                f'<span class="tl-lbl">٩:٠٠</span></div>'
                f'<div class="chips">{chips}</div></div>', unsafe_allow_html=True)

def card(text, title=None, cls="", name="الراوي"):
    body = text.replace("\n", "<br>")
    head = f"<h3>{title}</h3>" if title else ""
    st.markdown(f'<div class="card {cls}"><div class="nameplate">{name}</div>{head}{body}</div>', unsafe_allow_html=True)

def choices(options, callback):
    cols = st.columns(len(options))
    for col, (k, label) in zip(cols, options.items()):
        letter = "أ" if k == "A" else "ب"
        with col:
            st.button(f"◆  {letter} · {label}", key=f"{S.stage}_{k}", on_click=callback, args=(k,))

# ───────────────────────── SCREENS ─────────────────────────
banner(S.stage != "title")
stage = S.stage

if stage == "title":
    show_scene("title")
    st.button("🚗 ابدأ الطلعة", on_click=start)

elif stage == "prologue":
    key, text = PROLOGUE[S.i]
    show_scene(key)
    card(text)
    st.button("التالي ◀", on_click=next_prologue)

elif stage == "tire":
    hud(); show_scene("tire"); card(TIRE_EVENT[0]); choices(TIRE_EVENT[1], pick_tire)

elif stage == "road":
    hud(); show_scene("road"); card(ROAD_EVENT[0]); choices(ROAD_EVENT[1], pick_road)

elif stage == "stuck":
    hud(); show_scene("stuck"); card(UNPAVED_NOT_AIRED); choices(STUCK_EVENT, pick_stuck)

elif stage == "person":
    hud(); show_scene("person"); card(PERSON_EVENT[0]); choices(PERSON_EVENT[1], pick_person)

elif stage == "result":
    hud(); show_scene(S.r_img)
    for t in S.r_texts:
        card(t)
    st.button("التالي ◀", on_click=go, args=(S.r_next,))

elif stage == "ending":
    end = get_ending(S.time)
    title, text = ENDINGS[end]
    show_scene(end)
    card(text, title, "end", name="النهاية")
    if end == "best":
        show_scene("best_win")
    st.markdown(f'<div class="chips" style="justify-content:center;margin-bottom:12px"><span class="chip">⏱ الوقت المتبقي عند الوصول: {max(S.time, 0)} دقيقة</span></div>', unsafe_allow_html=True)
    st.button("🔄 العب مرة ثانية", on_click=reset)
