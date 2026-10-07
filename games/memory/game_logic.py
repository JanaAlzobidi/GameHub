"""
منطق لعبة البطاقات المتطابقة (بدون أي كود واجهة).
الكلاس MemoryGame يدير: البطاقات، النقاط، المحاولات، والمعلومة (الإشعار).
"""

import random
from pathlib import Path

# ---------------------------------------------------------------
# بيانات البطاقات (collection): كل بطاقة dict
# "image" = اسم الملف داخل board/images
# ---------------------------------------------------------------
CARDS = [
    {
        "id": "dallah",
        "name": "الدلة",
        "image": "dallah.png",
        "fact": "رمز الضيافة والكرم السعودي، والقهوة السعودية مدرجة ضمن تراث اليونسكو",
    },
    {
        "id": "dates",
        "name": "التمور",
        "image": "dates.png",
        "fact": "رمز الشموخ والعطاء، وتضم المملكة أكثر من 30 مليون نخلة تنتج أجود التمور",
    },
    {
        "id": "incense",
        "name": "البخور",
        "image": "incense.png",
        "fact": "تعبير عن الترحيب والاحتفاء بالضيوف ورائحة المجالس السعودية الأصيلة",
    },
    {
        "id": "bisht",
        "name": "البشت",
        "image": "bisht.png",
        "fact": "رمز الهيبة والأصالة في المناسبات والاحتفالات الرسمية والوطنية",
    },
    {
        "id": "horse",
        "name": "الخيل",
        "image": "horse.png",
        "fact":"تتميز الخيول العربية بجمالها وسرعتها، ولها تاريخ ممتد في الجزيرة العربية",
    },
    {
        "id": "falcon",
        "name": "الصقر",
        "image": "falcon.png",
        "fact": "تُعبّر الصقارة عن القوة والأصالة، وتعتبر رياضة تراثية عريقة في المملكة",
    },
    {
        "id": "alula",
        "name": "العلا",
        "image": "alula.png",
        "fact": "معلم أثري شهير في العُلا، نحته النبطيون في صخرة واحدة جبلية منفردة",
    },
    {
        "id": "diriyah",
        "name": "الدرعية",
        "image": "diriyah.png",
        "fact": "مهد الدولة السعودية الأولى ومسجل في قائمة التراث العالمي لليونسكو",
    },
    {
        "id": "shms",
        "name": "شمس",
        "image": "shms.png",
        "fact":"مهمة “شمس” أول مهمة وطنية متخصصة في رصد طقس الفضاء تمت كتعاون بين وكالة الفضاء السعودية و ناسا ضمن برنامج آرتميس لارسل  القمر الصناعي “شمس” الذي يساعد في تعزيز اسدامة القطاعات الحيوية المرتبطة بالفضاء كالملاحة",
    },
    {
        "id": "space",
        "name": "السعودية نحو الفضاء",
        "image": "space.png",
        "fact": "مهمة “السعودية نحو الفضاء” احدى مهام برنامج السعودية لرواد الفضاء، حيث تم فيها إرسال رائد الفضاء علي القرني ورائدة فضاء ريانة برناوي كأول رائدة فضاء سعودية، أتما خلال الرحلة 11 تجربة بحثية وعلمية في بيئة الجاذبية الصغرى” وبراءة اختراع دولية"
    },
    {
        "id": "khaleeji 27",
        "name": "كأس االخليج",
        "image": "khaleeji.png",
        "fact": "أُقيمت أول بطولة لكأس الخليج عام 1970 في البحرين، وكانت بمشاركة 4 منتخبات فقط (السعودية، الكويت، البحرين، قطر)",
    },
    {
        "id": "majed",
        "name": "ماجد عبدالله",
        "image": "majed.png",
        "fact": "ماجد عبدالله الهداف التاريخي للمنتخب السعودي في كأس الخليج تاريخيًا",
    },
]

# عدد البطاقات في كل صف 
COLUMNS = 6
# أقصى عدد أعمدة تسمح اللعبة تختاره تلقائياً 
MAX_COLUMNS = 8

# قيم اللعب
MATCH_SCORE = 50
WIN_BONUS_SCORE = 500
MISS_PENALTY = 5


class MemoryGame:
    """حالة لعبة واحدة."""

    def __init__(self):
        deck = []
        for card in CARDS:                 
            deck.append(card)
            deck.append(card)
        random.shuffle(deck)

        self.deck = deck                   
        self.flipped = []                  # list: البطاقات المكشوفة في المحاولة الحالية
        self.matched = set()               # set: أرقام (id) الأزواج المتطابقة
        self.score = 0
        self.moves = 0
        self.message = ""
        self.last_delta = 0                # +50 / -5 لآخر محاولة (للحركة جنب السكور)
        self.delta_id = 0                  # عداد المحاولات
        self.fact = ""
        self.pending_hide = False          # True = بطاقتين غير متطابقتين ظاهرتين وتنتظران الإخفاء
        self.game_over = False

    # ---------- مساعدات ----------
    def is_open(self, index):
        return index in self.flipped or self.deck[index]["id"] in self.matched

    def hide_pending(self):
        """يخفي البطاقتين غير المتطابقتين (إذا كان فيه شيء ينتظر الإخفاء)."""
        if self.pending_hide:
            self.flipped = []
            self.pending_hide = False

    # ---------- قلب بطاقة ----------
    def select(self, index):
        if self.game_over or not (0 <= index < len(self.deck)):
            return

        # لو فيه بطاقتين غير متطابقتين ظاهرتين: تختفي قبل ما تفتح الجديدة
        self.hide_pending()

        card = self.deck[index]
        if card["id"] in self.matched or index in self.flipped:   # condition
            return

        self.flipped.append(index)
        if len(self.flipped) < 2:
            return

        # صار عندنا بطاقتين -> نفحص
        self.moves += 1
        first = self.deck[self.flipped[0]]
        second = self.deck[self.flipped[1]]

        if first["id"] == second["id"]:
            self.matched.add(first["id"])
            self.score += MATCH_SCORE
            self.fact = f"✨ {first['name']}: {first['fact']}"
            self.last_delta = MATCH_SCORE
            self.delta_id += 1
            self.flipped = []

            if len(self.matched) == len(CARDS):
                self.score += WIN_BONUS_SCORE
                self.game_over = True
        else:
            self.score = max(0, self.score - MISS_PENALTY)
            self.last_delta = -MISS_PENALTY
            self.delta_id += 1
            self.pending_hide = True

    # ---------- بيانات اللوحة للواجهة ----------
    def board_payload(self, images_dir):
        images_dir = Path(images_dir)
        payload = []
        for i, card in enumerate(self.deck):
            image_file = card["image"] if (images_dir / card["image"]).exists() else None
            payload.append({
                "name": card["name"],
                "image": image_file,
                "open": self.is_open(i),
                "matched": card["id"] in self.matched,
            })
        return payload
