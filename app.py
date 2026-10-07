import base64
from pathlib import Path

import streamlit as st


# إعدادات الصفحة

st.set_page_config(
    page_title="مِنّا وفينا",
    page_icon="🌴",
    layout="wide",
)


# المسارات

BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"
FONTS = ASSETS / "fonts"


# تحويل الملفات إلى ترميز قاعدة 64

def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


# الألعاب
# دانية مسؤولة عن لعبة
# رغد مسؤولة عن لعبة "لعبة المطابقة"
# سليمان مسؤول عن لعبة "لعبة المعلومات"

GAMES = [
    {
        "key": "hero",
        "img": "game1.png",
        "title": "موعد مع الشهب",
        "desc": "انطلق في رحلة لمطاردة الشهب<br>والتقط لقطتك قبل فوات الأوان",
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


# الصور والخطوط

bg = b64(ASSETS / "background.png")
frame = b64(ASSETS / "card_frame.png")

saudi_regular = b64(
    FONTS / "SaudiWeb-Regular.woff2"
)

saudi_bold = b64(
    FONTS / "SaudiWeb-Bold.woff2"
)


# تنسيق بطاقات الألعاب

card_css = ""

for g in GAMES:

    card_css += f"""
    /* =====================================================
       بطاقة اللعبة
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
       صورة اللعبة
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
       اسم اللعبة
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
       وصف اللعبة
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
       حاوية زر اللعبة
       ===================================================== */

    .st-key-card_{g['key']} .st-key-btn_{g['key']} {{
        margin-top: 5rem;
        padding: 0;
        flex-shrink: 0;
    }}


    /* =====================================================
       زر اللعبة
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


# التنسيق العام للموقع

st.markdown(
    f"""
    <style>

    /* =====================================================
       الخط السعودي العادي
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
       الخط السعودي العريض
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
       التنسيق العام
       ===================================================== */

    html,
    body,
    [class*="css"],
    .stApp {{
        font-family: 'Saudi', sans-serif !important;
        direction: rtl;
    }}


    /* =====================================================
       خلفية الموقع
       ===================================================== */

    .stApp {{
        background-image:
            url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}


    /* =====================================================
       إخفاء عناصر Streamlit
       ===================================================== */

    header[data-testid="stHeader"],
    #MainMenu,
    footer {{
        display: none;
    }}


    /* =====================================================
       الحاوية الرئيسية
       ===================================================== */

    .block-container {{
        padding-top: 2.5rem;
        max-width: 1100px;
    }}


    /* =====================================================
       اسم الموقع
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
       الوصف تحت اسم الموقع
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
       صور الألعاب
       ===================================================== */

    .stImage img {{
        border-radius: 14px;
    }}


    /* =====================================================
       تنسيقات بطاقات الألعاب
       ===================================================== */

    {card_css}

    </style>
    """,
    unsafe_allow_html=True,
)


# التنقل بين الصفحات

if "page" not in st.session_state:
    st.session_state.page = "home"


def go(page: str):
    st.session_state.page = page


# الصفحة الرئيسية

if st.session_state.page == "home":

    # اسم الموقع

    st.markdown(
        '<h1 class="game-title">مِنّا وفينا</h1>',
        unsafe_allow_html=True,
    )


    # الوصف الموقع

    st.markdown(
        '<div class="game-sub">ثلاث ألعاب .. تراث واحد</div>',
        unsafe_allow_html=True,
    )


    # ترتيب بطاقات الألعاب

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

                # أيقونة اللعبة

                st.image(
                    str(
                        ASSETS / g["img"]
                    ),
                    use_container_width=True,
                )


                # اسم اللعبة

                st.markdown(
                    f'<div class="card-title">{g["title"]}</div>',
                    unsafe_allow_html=True,
                )


                # وصف اللعبة

                st.markdown(
                    f'<div class="card-desc">{g["desc"]}</div>',
                    unsafe_allow_html=True,
                )


                # زر اللعبة

                with st.container(
                    key=f"btn_{g['key']}"
                ):

                    st.button(
                        "ابدأ اللعبة ‹",
                        key=f"button_{g['key']}",
                        use_container_width=True,
                        on_click=go,
                        args=(g["key"],),
                    )


# صفحات الألعاب

else:

    game = next(
        g
        for g in GAMES
        if g["key"] == st.session_state.page
    )


    # اسم اللعبة

    st.markdown(
        f'<h1 class="game-title">{game["title"]}</h1>',
        unsafe_allow_html=True,
    )


    # مكان إضافة كود الألعاب
    #  تكون اللعبة الي اختارها اللاعب game["key"] قيمة

    if game["key"] == "hero":

        # =================================================
        # كود دانية
        # لعبة موعد مع الشهب
        # =================================================

        st.info(
            "هنا يجي كود لعبة موعد مع الشهب"
        )


    elif game["key"] == "match":

        # =================================================
        # كود رغد
        # لعبة المطابقة
        # =================================================

        st.info(
            "هنا يجي كود لعبة المطابقة"
        )


    elif game["key"] == "quiz":

        # =================================================
        # كود سليمان
        # لعبة المعلومات
        # =================================================

        st.info(
            "هنا يجي كود لعبة المعلومات"
        )


    # زر الرجوع للصفحة الرئيسية

    st.button(
        "← رجوع للرئيسية",
        on_click=go,
        args=("home",),
    )
