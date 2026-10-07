"""
الملفات:
    memory.py          الواجهة والستايل (الفانكشن run_game)
    game_logic.py      منطق اللعبة (كلاس MemoryGame + بيانات البطاقات)
    board/index.html   لوحة البطاقات
    board/images/      صور البطاقات + back.png (ظهر البطاقة)
    board/fonts/       خط SaudiWeb (Regular + Bold)
    assets/background.png  خلفية اللعبة
"""


def run_game():
    import base64
    from pathlib import Path
    from urllib.parse import quote

    import streamlit as st
    import streamlit.components.v1 as components

    try:  # لما تنستدعى من واجهة رئيسية 
        from . import game_logic
    except ImportError:  # لما تتشغل مباشرة: streamlit run memory.py
        import game_logic
    MemoryGame, CARDS, COLUMNS = game_logic.MemoryGame, game_logic.CARDS, game_logic.COLUMNS

    # أقصى عدد أعمدة تختاره اللعبة تلقائياً لتكبير البطاقات (يرجع لـ COLUMNS لو غير موجود)
    MAX_COLUMNS = getattr(game_logic, "MAX_COLUMNS", COLUMNS)

    BASE_DIR = Path(__file__).resolve().parents[2]
    ASSETS_DIR = BASE_DIR / "assets"
    
    BOARD_DIR = Path(__file__).resolve().parent / "board"
    IMAGES_DIR = ASSETS_DIR / "memory" / "images"
    FONTS_DIR = ASSETS_DIR / "fonts"
    UI_ASSETS = ASSETS_DIR / "ui"

    try:  # لو الواجهة الرئيسية ضبطت الصفحة قبل، نتجاهل
        st.set_page_config(
            page_title="رحلة في ذاكرة الوطن",
            page_icon="🇸🇦",
            layout="wide",
        )
    except Exception:
        pass


    THEME = {
        "bg": "#cfa77a",          
        "panel": "rgba(112, 79, 48, .76)",  
        "panel_strong": "rgba(73, 68, 47, .88)",
        "gold": "#d8b85b",        
        "gold_light": "#f5dda0",
        "cream": "#f7e6c2",     
        "muted": "#e3cda6",     
        "paper_top": "#f8e9c6",
        "paper_bot": "#ecd29b",
        "ink": "#4b3524",         
        "ink_soft": "#7b5b3b",
        "edge": "#4b3524",       
        "olive": "#66774f",
        "olive_dark": "#465632",
    }

    FONT_STACK = "'SaudiWeb', 'IBM Plex Sans Arabic', 'Segoe UI', Tahoma, sans-serif"


    def svg_uri(svg: str) -> str:
        """يحوّل SVG نصي لـ url() يصلح داخل CSS."""
        return 'url("data:image/svg+xml;utf8,' + quote(svg, safe=" =:/,.;()'-") + '")'


    # ---------- رسومات صغيرة ----------
    DIAMOND = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">'
        '<path d="M10 1 19 10 10 19 1 10Z" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<path d="M10 5.2 14.8 10 10 14.8 5.2 10Z" fill="{c}"/></svg>'
    )


    DUNES = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 110" preserveAspectRatio="none">'
        '<path d="M0 110V78C70 58 120 92 200 72S330 58 400 80V110Z" fill="#b98b52" opacity=".22"/>'
        '<path d="M0 110V92C90 76 150 104 240 88S350 80 400 94V110Z" fill="#a67a45" opacity=".20"/>'
        '<g stroke="#7a5a35" stroke-linecap="round" fill="none" opacity=".30">'
        '<path d="M40 108C38 90 42 72 48 56" stroke-width="3"/>'
        '<path d="M48 56C36 46 24 48 14 58M48 56C40 42 30 38 20 40M48 56C52 42 60 36 70 36M48 56C60 48 72 50 80 60" stroke-width="2.4"/>'
        '<path d="M352 108C354 92 350 78 346 66" stroke-width="3"/>'
        '<path d="M346 66C336 58 326 60 318 68M346 66C344 54 352 46 362 44M346 66C356 60 366 62 374 70" stroke-width="2.4"/>'
        '</g></svg>'
    )

    ICON_STAR = (
        '<svg viewBox="0 0 24 24"><polygon fill="#f3d58a" points="12,2.8 14.8,8.9 21.4,9.6 16.5,14.1 17.9,20.6 12,17.3 6.1,20.6 7.5,14.1 2.6,9.6 9.2,8.9"/></svg>'
    )
    ICON_GAMEPAD = (
        '<svg viewBox="0 0 24 24"><path fill="#f3d58a" d="M7.2 7.6h9.6a5.2 5.2 0 0 1 5 3.9l1 3.9a2.7 2.7 0 0 1-4.6 2.5L15.8 15H8.2l-2.4 2.9a2.7 2.7 0 0 1-4.6-2.5l1-3.9a5.2 5.2 0 0 1 5-3.9Z"/>'
        '<path d="M7.6 10.4v3.2M6 12h3.2" stroke="#3f2c1c" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="15.6" cy="11" r="1" fill="#3f2c1c"/><circle cx="18" cy="13" r="1" fill="#3f2c1c"/></svg>'
    )
    ICON_PUZZLE = (
        '<svg viewBox="0 0 24 24"><g transform="rotate(45 12 12)" fill="#f3d58a">'
        '<rect x="9" y="2.5" width="6" height="19" rx="3"/><rect x="2.5" y="9" width="19" height="6" rx="3"/></g>'
        '<circle cx="12" cy="12" r="2" fill="#3f2c1c"/></svg>'
    )
    ICON_BULB = (
        '<svg viewBox="0 0 24 24"><path fill="#f3d58a" d="M12 2.6a6.6 6.6 0 0 0-3.6 12.1c.7.5 1.1 1.2 1.1 2v.6h5v-.6c0-.8.4-1.5 1.1-2A6.6 6.6 0 0 0 12 2.6Z"/>'
        '<rect x="9.6" y="18.6" width="4.8" height="1.8" rx=".9" fill="#f3d58a"/><rect x="10.4" y="21" width="3.2" height="1.4" rx=".7" fill="#f3d58a"/></svg>'
    )
    ICON_TROPHY = (
        '<svg viewBox="0 0 24 24"><path fill="#f3d58a" d="M7 3h10v5a5 5 0 0 1-10 0V3Z"/>'
        '<path d="M7 5H3.5c0 3 1.5 4.6 3.6 4.9M17 5h3.5c0 3-1.5 4.6-3.6 4.9" stroke="#f3d58a" stroke-width="1.6" fill="none"/>'
        '<rect x="10.8" y="12.5" width="2.4" height="4" fill="#f3d58a"/><rect x="7.5" y="16.5" width="9" height="3" rx="1.2" fill="#f3d58a"/></svg>'
    )

    EMBLEM = (
        '<svg class="emblem" viewBox="0 0 64 64" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        '<g stroke="#4b3524" stroke-width="3.2"><path d="M9 57 46 37"/><path d="M55 57 18 37"/></g>'
        '<g fill="#4b3524"><circle cx="9" cy="57" r="2.4"/><circle cx="55" cy="57" r="2.4"/></g>'
        '<path d="M32 40V27" stroke="#4b3524" stroke-width="3.6"/>'
        '<g stroke="#3d5a33" stroke-width="3.2">'
        '<path d="M32 27C25 19 15 19 8 25"/><path d="M32 27C27 16 21 11 12 11"/><path d="M32 27C32 17 32 11 32 5"/>'
        '<path d="M32 27C37 16 43 11 52 11"/><path d="M32 27C39 19 49 19 56 25"/></g></svg>'
    )
    ICON_REFRESH_BTN = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<circle cx="16" cy="16" r="15" fill="#f4e2b6" stroke="#cfa95c" stroke-width="1.5"/>'
        '<path d="M22.2 12.2A7.4 7.4 0 1 0 23.4 17" fill="none" stroke="#4b3524" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M22.8 7.6v5.4h-5.4" fill="none" stroke="#4b3524" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


    @st.cache_resource
    def background_css():
        """يحوّل صورة الخلفية لـ CSS (data URI) عشان Streamlit ما يخدم الملفات مباشرة."""
        path = UI_ASSETS / "background.png"
        if not path.exists():
            return ""
        data = base64.b64encode(path.read_bytes()).decode()
        return (
            "background-image: url('data:image/png;base64," + data + "');"
            "background-repeat: no-repeat;"
            "background-position: center center;"
            "background-size: cover;"
            "background-attachment: fixed;"
        )


    @st.cache_resource
    def font_css():
        """يضمّن خط SaudiWeb (Regular + Bold) داخل الصفحة."""
        rules = []
        for weight, name in ((400, "SaudiWeb-Regular.woff2"), (700, "SaudiWeb-Bold.woff2")):
            path = FONTS_DIR / name
            if path.exists():
                data = base64.b64encode(path.read_bytes()).decode()
                rules.append(
                    "@font-face{font-family:'SaudiWeb';font-style:normal;font-weight:%d;"
                    "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % (weight, data)
                )
        return "\n".join(rules)


    STYLE = """
    <style>
    __fonts__

    :root {
        --bg: __bg__;
        --panel: __panel__;
        --panel-strong: __panel_strong__;
        --gold: __gold__;
        --gold-light: __gold_light__;
        --cream: __cream__;
        --muted: __muted__;
        --ink: __ink__;
        --ink-soft: __ink_soft__;
        --panel-w: 500px;
    }

    /* ===== الخط ===== */
    html, body, .stApp,
    .stApp p, .stApp div, .stApp span, .stApp button, .stApp label,
    .stApp h1, .stApp h2, .stApp h3 {
        font-family: __font_stack__;
    }
    .stApp [data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded', sans-serif !important; }
    html, body { background-color: var(--bg); }

    /* ===== الخلفية ===== */
    .stApp {
        background-color: var(--bg);
        __background__
        color: var(--cream);
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section.main {
        background: transparent !important;
    }

    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 0.6rem !important;
        padding-bottom: 0.4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }

    /* ===== ترتيب الأعمدة ===== */
    [data-testid="stHorizontalBlock"] { align-items: center; }
    [data-testid="stColumn"] { min-width: 0 !important; }
    [data-testid="stColumn"] [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="stColumn"] [data-testid="stElementContainer"],
    [data-testid="stColumn"] .stMarkdown { margin: 0 !important; }

    /* ===== بطاقات اللوحة اليمين (ورق رملي بإطار بني) ===== */
    .panel {
        display: flex;
        flex-direction: column;
        gap: 10px;
        direction: rtl;
        max-width: var(--panel-w);
        margin: 0 auto;
        font-size: clamp(13px, 1vw, 18px);   
    }

    .hero, .stat, .fact {
        position: relative;
        background: linear-gradient(180deg, __paper_top__ 0%, __paper_bot__ 100%);
        border: 2px solid __edge__;
        border-radius: 20px;
        box-shadow:
            inset 0 0 0 3px rgba(255, 244, 214, .78),
            inset 0 0 0 4px rgba(123, 91, 59, .45),
            0 8px 18px rgba(55, 37, 22, .30);
        color: var(--ink);
    }
    .hero::before, .hero::after,
    .stat::before, .stat::after,
    .fact::before, .fact::after {
        content: "";
        position: absolute;
        top: 10px;
        width: 12px; height: 12px;
        background: __diamond_brown__ center / contain no-repeat;
        opacity: .7;
        pointer-events: none;
    }
    .hero::before, .stat::before, .fact::before { left: 13px; }
    .hero::after,  .stat::after,  .fact::after  { right: 13px; }

    /* العنوان */
    .hero {
        display: flex; align-items: center; justify-content: center; gap: 12px;
        padding: 14px 40px;
        min-height: 4em;
    }
    .hero::before, .hero::after { top: 50%; margin-top: -6px; }
    .hero h1 {
        flex: 1;
        margin: 0; padding: 0;
        font-size: 1.65em; font-weight: 700; line-height: 1.35;
        color: var(--ink);
        text-align: center;
    }
    .hero .emblem { width: 3em; height: 3em; flex: none; }

    /* مربعات النقاط */
    .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

    .stat {
        padding: 12px 10px 14px;
        text-align: center;
        overflow: hidden;
        background:
            __dunes__ bottom center / 100% 62% no-repeat,
            linear-gradient(180deg, __paper_top__ 0%, __paper_bot__ 100%);
    }
    .stat.score { grid-column: 1 / -1; padding: 14px 10px 16px; }

    .stat .head {
        display: flex; align-items: center; justify-content: center; gap: 9px;
        color: var(--ink-soft); font-size: 1.15em; font-weight: 700;
        margin-bottom: 4px;
    }
    .stat .icon {
        width: 2.5em; height: 2.5em; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        background: radial-gradient(circle at 35% 28%, #7a5a3c, #3f2c1c 72%);
        border: 2px solid rgba(243, 213, 138, .55);
        box-shadow: 0 2px 6px rgba(55, 37, 22, .45);
    }
    .stat .icon svg { width: 1.3em; height: 1.3em; display: block; }
    .stat .value { color: var(--ink); font-size: 2.15em; font-weight: 700; line-height: 1.15; }
    .stat.score .value { font-size: 3.3em; }

    /* السكور + الحركة (+50 / -5) */
    .score-row { display: flex; align-items: center; justify-content: center; gap: 6px; }
    .score-row::before { content: ""; width: 3.6em; }
    .delta {
        width: 3.6em; text-align: start; direction: ltr;
        font-size: 1.7em; font-weight: 700; opacity: 0; pointer-events: none;
        text-shadow: 0 1px 0 rgba(255, 244, 214, .85);
    }
    .delta.plus  { color: #2f7d3a; }
    .delta.minus { color: #b3261e; }
    .delta.plus.a  { animation: popUpA 1.4s ease-out forwards; }
    .delta.plus.b  { animation: popUpB 1.4s ease-out forwards; }
    .delta.minus.a { animation: dropA 1.4s ease-out forwards; }
    .delta.minus.b { animation: dropB 1.4s ease-out forwards; }

    @keyframes popUpA { 0% {opacity:0; transform: translateY(14px) scale(.5);} 18% {opacity:1; transform: translateY(0) scale(1.25);} 35% {transform: scale(1);} 75% {opacity:1; transform: translateY(-10px);} 100% {opacity:0; transform: translateY(-28px);} }
    @keyframes popUpB { 0% {opacity:0; transform: translateY(14px) scale(.5);} 18% {opacity:1; transform: translateY(0) scale(1.25);} 35% {transform: scale(1);} 75% {opacity:1; transform: translateY(-10px);} 100% {opacity:0; transform: translateY(-28px);} }
    @keyframes dropA { 0% {opacity:0; transform: translateY(-14px) scale(.7);} 15% {opacity:1; transform: translateY(0) scale(1.1);} 25% {transform: translateX(-6px);} 35% {transform: translateX(6px);} 45% {transform: translateX(-4px);} 55% {transform: translateX(0);} 75% {opacity:1;} 100% {opacity:0; transform: translateY(22px);} }
    @keyframes dropB { 0% {opacity:0; transform: translateY(-14px) scale(.7);} 15% {opacity:1; transform: translateY(0) scale(1.1);} 25% {transform: translateX(-6px);} 35% {transform: translateX(6px);} 45% {transform: translateX(-4px);} 55% {transform: translateX(0);} 75% {opacity:1;} 100% {opacity:0; transform: translateY(22px);} }

    /* ===== المعلومة ===== */
    .fact { padding: 12px 22px 14px; text-align: right; }
    .fact .fact-title {
        display: flex; align-items: center; justify-content: center; gap: 8px;
        color: var(--ink-soft); font-size: 1.15em; font-weight: 700; margin-bottom: 6px;
    }
    .fact .icon {
        width: 2em; height: 2em; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        background: radial-gradient(circle at 35% 28%, #7a5a3c, #3f2c1c 72%);
        border: 2px solid rgba(243, 213, 138, .55);
    }
    .fact .icon svg { width: 1.1em; height: 1.1em; display: block; }
    .fact .fact-body {
        font-size: 1.08em; line-height: 1.8; color: var(--ink);
        max-height: max(80px, calc(100vh - 640px));
        overflow-y: auto;
        padding-left: 4px;
        scrollbar-width: thin;
        scrollbar-color: rgba(75, 53, 36, .5) transparent;
    }

    /* ===== الفوز ===== */
    .win {
        position: relative;
        background: linear-gradient(180deg, __olive__, __olive_dark__);
        border: 2px solid __edge__;
        border-radius: 20px;
        box-shadow: inset 0 0 0 3px rgba(226, 190, 100, .55), 0 8px 18px rgba(55, 37, 22, .30);
        padding: 12px 14px;
        text-align: center;
    }
    /*تخفي المعلومة لما يطلع صندوق الفوز*/
    @media (max-height: 760px) { .panel.won .fact { display: none; } }
    .win .trophy { width: 34px; height: 34px; display: block; margin: 0 auto 2px; }
    .win h2, .win p { margin: 0; color: #f8e9c6 !important; }
    .win h2 { font-size: 1.4em; font-weight: 700; }
    .win p { font-size: 1.05em; }

    /* ===== زر لعبة جديدة ===== */
    div.stButton, div[data-testid="stButton"] {
        max-width: var(--panel-w);
        width: 100%;
        margin: 0 auto !important;
    }
    div.stButton > button, div[data-testid="stButton"] > button {
        position: relative;
        width: 100%;
        min-height: clamp(58px, 3.8vw, 76px);
        border-radius: 20px;
        background:
            __diamond_gold__ right 16px center / 13px no-repeat,
            __diamond_gold__ left 16px center / 13px no-repeat,
            linear-gradient(180deg, __olive__ 0%, __olive_dark__ 100%) !important;
        border: 2px solid __edge__ !important;
        box-shadow:
            inset 0 0 0 3px rgba(226, 190, 100, .60),
            inset 0 0 0 4px rgba(40, 30, 15, .35),
            0 8px 18px rgba(55, 37, 22, .32);
        color: #f8e9c6 !important;
        transition: filter .15s, transform .08s;
    }
    div.stButton > button p, div[data-testid="stButton"] > button p {
        display: flex; align-items: center; justify-content: center; gap: 12px;
        margin: 0; color: #f8e9c6 !important;
        font-size: clamp(19px, 1.4vw, 26px); font-weight: 700;
    }
    div.stButton > button p::before, div[data-testid="stButton"] > button p::before {
        content: "";
        width: 1.6em; height: 1.6em; flex: none;
        background: __refresh__ center / contain no-repeat;
    }
    div.stButton > button:hover, div[data-testid="stButton"] > button:hover {
        filter: brightness(1.1);
        border-color: __edge__ !important;
        color: #fff3c4 !important;
    }
    div.stButton > button:active, div[data-testid="stButton"] > button:active { transform: translateY(1px); }
    div.stButton > button:focus:not(:active), div[data-testid="stButton"] > button:focus:not(:active) {
        border-color: __edge__ !important;
        box-shadow:
            inset 0 0 0 3px rgba(226, 190, 100, .60),
            inset 0 0 0 4px rgba(40, 30, 15, .35),
            0 8px 18px rgba(55, 37, 22, .32);
    }

    hr, [data-testid="stDivider"] { border-color: rgba(245, 221, 160, .35) !important; }
    [data-testid="stCaptionContainer"], .stCaption, small { color: var(--muted) !important; }
    </style>
    """

    for key, value in THEME.items():
        STYLE = STYLE.replace(f"__{key}__", value)
    STYLE = (
        STYLE.replace("__fonts__", font_css())
        .replace("__font_stack__", FONT_STACK)
        .replace("__background__", background_css())
        .replace("__diamond_brown__", svg_uri(DIAMOND.format(c="#4b3524")))
        .replace("__diamond_gold__", svg_uri(DIAMOND.format(c="#e6c36a")))
        .replace("__dunes__", svg_uri(DUNES))
        .replace("__refresh__", svg_uri(ICON_REFRESH_BTN))
    )

    st.markdown(STYLE, unsafe_allow_html=True)

    # مكوّن اللوحة: يعرض البطاقات ويرجع لبايثون رقم البطاقة اللي انضغطت
    board_component = components.declare_component(
        "saudi_memory_board", path=str(BOARD_DIR)
    )

    # =========================
    # Game state
    # =========================
    if "game" not in st.session_state:
        st.session_state.game = MemoryGame()
        st.session_state.last_nonce = None

    game: MemoryGame = st.session_state.game

    # =========================
    # Header
    # =========================
    board_col, info_col = st.columns([3.1, 1], gap="medium")

    # ---------- يمين الشاشة: النقاط والمعلومة والمحاولات ----------
    with info_col:
        # حركة +50 / -5 جنب السكور 
        delta_html = ""
        if game.last_delta:
            kind = "plus" if game.last_delta > 0 else "minus"
            sign = "+" if game.last_delta > 0 else "-"
            phase = "a" if game.delta_id % 2 else "b"
            delta_html = f'<span class="delta {kind} {phase}">{sign}{abs(game.last_delta)}</span>'
        else:
            delta_html = '<span class="delta"></span>'

        fact_html = ""
        if game.fact:
            fact_text = game.fact.replace("✨", "").strip()
            fact_html = (
                '<div class="fact">'
                f'<div class="fact-title"><span class="icon">{ICON_BULB}</span>معلومة</div>'
                f'<div class="fact-body">{fact_text}</div>'
                '</div>'
            )

        win_html = ""
        if game.game_over:
            win_html = f"""
            <div class="win">
                <span class="trophy">{ICON_TROPHY.replace('<svg ', '<svg width="34" height="34" ')}</span>
                <h2>مبروك! أكملتِ اللعبة</h2>
                <p>جمعتِ جميع الرموز السعودية.</p>
            </div>"""

        st.markdown(
            f"""
            <div class="panel{' won' if game.game_over else ''}">
                <div class="hero"><h1>رحلة في ذاكرة الوطن</h1>{EMBLEM}</div>
                <div class="stats">
                    <div class="stat score">
                        <div class="head"><span class="icon">{ICON_STAR}</span>النقاط</div>
                        <div class="score-row"><span class="value">{game.score}</span>{delta_html}</div>
                    </div>
                    <div class="stat">
                        <div class="head"><span class="icon">{ICON_GAMEPAD}</span>المحاولات</div>
                        <div class="value">{game.moves}</div>
                    </div>
                    <div class="stat">
                        <div class="head"><span class="icon">{ICON_PUZZLE}</span>المطابقات</div>
                        <div class="value"><span dir="ltr">{len(game.matched)} / {len(CARDS)}</span></div>
                    </div>
                </div>
                {fact_html}
                {win_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # مسافة بين اللوحة وزر «لعبة جديدة»
        st.markdown('<div style="height: 45px"></div>', unsafe_allow_html=True)

        if st.button("لعبة جديدة", use_container_width=True):
            st.session_state.game = MemoryGame()
            st.rerun()


    # ---------- يسار الشاشة: البطاقات ----------
    def image_data_url(path: Path) -> str | None:
        if not path.exists():
            return None

        data = base64.b64encode(path.read_bytes()).decode()

        if path.suffix.lower() == ".png":
            mime = "image/png"
        elif path.suffix.lower() in {".jpg", ".jpeg"}:
            mime = "image/jpeg"
        else:
            mime = "application/octet-stream"

        return f"data:{mime};base64,{data}"

    def font_data_url(path: Path) -> str | None:
        if not path.exists():
            return None

        data = base64.b64encode(path.read_bytes()).decode()
        return f"data:font/woff2;base64,{data}"

    cards_payload = game.board_payload(IMAGES_DIR)

    for card in cards_payload:
        if card["image"]:
            card["image"] = image_data_url(IMAGES_DIR / card["image"])

    back_image = image_data_url(IMAGES_DIR / "back.png")
    regular_font = font_data_url(FONTS_DIR / "SaudiWeb-Regular.woff2")
    bold_font = font_data_url(FONTS_DIR / "SaudiWeb-Bold.woff2")

    with board_col:
        event = board_component(
            cards=cards_payload,
            columns=COLUMNS,
            max_columns=MAX_COLUMNS,
            back_image=back_image,
            regular_font=regular_font,
            bold_font=bold_font,
            pending_hide=game.pending_hide,
            game_over=game.game_over,
            key="board",
            default=None,
        )

        # الحدث الجديد فقط (الـ nonce يمنع معالجة نفس الضغطة مرتين)
        if event and event.get("nonce") != st.session_state.last_nonce:
            st.session_state.last_nonce = event.get("nonce")
            if event.get("type") == "flip":
                game.select(int(event["index"]))
            elif event.get("type") == "hide":
                game.hide_pending()
            st.rerun()


if __name__ == "__main__":
    run_game()
