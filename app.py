import base64
from pathlib import Path

import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="رحلة نجد",
    page_icon="🌴",
    layout="wide",
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent

ASSETS = BASE_DIR / "assets"

FONTS = ASSETS / "fonts"


# =========================================================
# BASE64
# =========================================================

def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


# =========================================================
# الألعاب
# =========================================================

GAMES = [
    {
        "key": "hero",
        "img": "game1.png",
        "title": "رحلة البطل",
        "desc": "انطلق في مغامرة عبر نجد<br>وأتم التحديات",
        "color": "#8B5E3C",
    },
    {
        "key": "match",
        "img": "game2.png",
        "title": "لعبة المطابقة",
        "desc": "اكتشف الرموز والمعالم<br>السعودية",
        "color": "#2F5D50",
    },
    {
        "key": "quiz",
        "img": "game3.png",
        "title": "لعبة المعلومات",
        "desc": "اختبر معرفتك بالثقافة<br>والتاريخ السعودي",
        "color": "#8B5E3C",
    },
]


# =========================================================
# الصور والخطوط
# =========================================================

bg = b64(ASSETS / "background.png")

frame = b64(ASSETS / "card_frame.png")

saudi_regular = b64(
    FONTS / "SaudiWeb-Regular.woff2"
)

saudi_bold = b64(
    FONTS / "SaudiWeb-Bold.woff2"
)


# =========================================================
# CSS للكروت
# =========================================================

card_css = ""

for g in GAMES:

    card_css += f"""
    /* =====================================================
       CARD
       ===================================================== */

    .st-key-card_{g['key']} {{
        background-image: url("data:image/png;base64,{frame}");

        background-position: center;

        background-size: 100% 100%;

        background-repeat: no-repeat;

        aspect-ratio: 900 / 1440;

        width: 100%;

        box-sizing: border-box;

        padding: 25% 14% 10% 14%;

        display: flex;

        flex-direction: column;
    }}


    /* =====================================================
       GAME IMAGE
       ===================================================== */

    .st-key-card_{g['key']} [data-testid="stImage"] {{
        margin-top: 10px;

        margin-bottom: 1.5rem;

        flex-shrink: 0;

        text-align: center;
    }}


    .st-key-card_{g['key']} [data-testid="stImage"] img {{
        width: 80% !important;

        height: auto !important;

        max-height: 170px;

        object-fit: contain;

        display: block;

        margin-left: auto;

        margin-right: auto;
    }}


    /* =====================================================
       GAME TITLE
       ===================================================== */

    .st-key-card_{g['key']} .card-title {{
        text-align: center;

        font-family: 'Saudi', sans-serif !important;

        font-weight: 700;

        font-size: 1.5rem;

        line-height: 1.35;

        color: #3d2b1a;

        margin: 0.2rem 0 0.3rem 0;

        padding: 0;

        flex-shrink: 0;
    }}


    /* =====================================================
       GAME DESCRIPTION
       ===================================================== */

    .st-key-card_{g['key']} .card-desc {{
        text-align: center;

        font-family: 'Saudi', sans-serif !important;

        font-weight: 400;

        font-size: 1rem;

        line-height: 1.5;

        color: #8a7a68;

        margin: 0;

        padding: 0;

        flex-shrink: 0;
    }}


    /* =====================================================
       BUTTON CONTAINER
       ===================================================== */

    .st-key-card_{g['key']} .st-key-btn_{g['key']} {{
        margin-top: 5rem;

        padding: 0;

        flex-shrink: 0;
    }}


    /* =====================================================
       BUTTON
       ===================================================== */

    .st-key-btn_{g['key']} button {{
        background-color: {g['color']} !important;

        color: #ffffff !important;

        border: none !important;

        border-radius: 999px !important;

        min-height: 42px;

        padding: 0.55rem 1rem;

        font-family: 'Saudi', sans-serif !important;

        font-weight: 700;

        font-size: 1rem;
    }}


    .st-key-btn_{g['key']} button:hover {{
        filter: brightness(1.1);

        color: #ffffff !important;
    }}
    """


# =========================================================
# CSS العام
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       SAUDI REGULAR FONT
       ===================================================== */

    @font-face {{
        font-family: 'Saudi';

        src: url(
            "data:font/woff2;base64,{saudi_regular}"
        ) format("woff2");

        font-weight: 400;

        font-style: normal;

        font-display: swap;
    }}


    /* =====================================================
       SAUDI BOLD FONT
       ===================================================== */

    @font-face {{
        font-family: 'Saudi';

        src: url(
            "data:font/woff2;base64,{saudi_bold}"
        ) format("woff2");

        font-weight: 700;

        font-style: normal;

        font-display: swap;
    }}


    /* =====================================================
       GLOBAL
       ===================================================== */

    html,
    body,
    [class*="css"],
    .stApp {{
        font-family: 'Saudi', sans-serif !important;

        direction: rtl;
    }}


    /* =====================================================
       BACKGROUND
       ===================================================== */

    .stApp {{
        background-image:
            url("data:image/png;base64,{bg}");

        background-size: cover;

        background-position: center;

        background-attachment: fixed;
    }}


    /* =====================================================
       HIDE STREAMLIT UI
       ===================================================== */

    header[data-testid="stHeader"],
    #MainMenu,
    footer {{
        display: none;
    }}


    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    .block-container {{
        padding-top: 2.5rem;

        max-width: 1100px;
    }}


    /* =====================================================
       WEBSITE TITLE
       رحلة نجد
       ===================================================== */

    .game-title {{
        text-align: center;

        font-family: 'Saudi', sans-serif !important;

        font-weight: 700 !important;

        font-size: 4rem !important;

        color: #8B5E3C !important;

        margin: 0;

        line-height: 1.2;
    }}


    /* =====================================================
       WEBSITE SUBTITLE
       ===================================================== */

    .game-sub {{
        text-align: center;

        font-family: 'Saudi', sans-serif !important;

        font-weight: 400;

        color: #5a4632;

        font-size: 1.3rem;

        margin-top: 0.2rem;

        margin-bottom: 1.5rem;
    }}


    /* =====================================================
       CARD IMAGE
       ===================================================== */

    .stImage img {{
        border-radius: 14px;
    }}


    {card_css}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# التنقل
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


def go(page: str):

    st.session_state.page = page


# =========================================================
# الصفحة الرئيسية
# =========================================================

if st.session_state.page == "home":

    # =====================================================
    # اسم الموقع
    # =====================================================

    st.markdown(
        '<h1 class="game-title">🌴 رحلة نجد</h1>',
        unsafe_allow_html=True,
    )


    # =====================================================
    # الوصف تحت اسم الموقع
    # =====================================================

    st.markdown(
        '<div class="game-sub">ثلاث ألعاب .. تراث واحد</div>',
        unsafe_allow_html=True,
    )


    # Streamlit يرتب الأعمدة من اليسار إلى اليمين
    # لذلك نعكس الألعاب حتى تظهر رحلة البطل على اليمين

    cols = st.columns(
        3,
        gap="small"
    )


    for col, g in zip(
        cols,
        reversed(GAMES)
    ):

        with col:

            with st.container(
                key=f"card_{g['key']}"
            ):

                # =================================================
                # أيقونة اللعبة
                # =================================================

                st.image(
                    str(
                        ASSETS / g["img"]
                    ),
                    use_container_width=True,
                )


                # =================================================
                # اسم اللعبة
                # =================================================

                st.markdown(
                    f'<div class="card-title">{g["title"]}</div>',
                    unsafe_allow_html=True,
                )


                # =================================================
                # وصف اللعبة
                # =================================================

                st.markdown(
                    f'<div class="card-desc">{g["desc"]}</div>',
                    unsafe_allow_html=True,
                )


                # =================================================
                # زر اللعبة
                # =================================================

                with st.container(
                    key=f"btn_{g['key']}"
                ):

                    st.button(
                        "ابدأ اللعبة  ‹",

                        key=f"button_{g['key']}",

                        use_container_width=True,

                        on_click=go,

                        args=(g["key"],),
                    )


# =========================================================
# صفحات الألعاب
# =========================================================

else:

    game = next(
        g
        for g in GAMES
        if g["key"] == st.session_state.page
    )


    st.markdown(
        f'<h1 class="game-title">{game["title"]}</h1>',
        unsafe_allow_html=True,
    )


    st.info(
        "هنا يجي كود اللعبة 🎮"
    )


    st.button(
        "← رجوع للرئيسية",

        on_click=go,

        args=("home",),
    )
