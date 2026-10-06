"""
logic.py - منطق اللعبة (الوقت والقرارات والنهايات) بدون أي نصوص أو واجهة.
"""

START_TIME = 60  # دقائق الوقت المتاح للتجهيز


def check_tires(choice, time_left):
    """A: تشيّك وتنسّم الكفرات (-5 دقائق) | B: تتجاهل الإحساس."""
    if choice == "A":
        return time_left - 5, True
    return time_left, False


def choose_road(choice, time_left):
    """A: الطريق الممهّد (-30) | B: الطريق غير الممهّد (-20)."""
    if choice == "A":
        return time_left - 30, "paved"
    return time_left - 20, "unpaved"


def handle_stuck(tire_aired, choice, time_left):
    """
    التغريز في الطريق غير الممهّد.
    الكفرات منسّمة: تطلع السيارة بسرعة بدون خسارة وقت.
    غير منسّمة:
        A: تحاول أكثر (-25) ثم تنتظر مساعدة
        B: تنتظر شخص يساعدك (-15)
    """
    if tire_aired:
        return time_left, False
    return (time_left - 25 if choice == "A" else time_left - 15), True


def help_person(choice, time_left):
    """A: توصّل الشخص (+5 بركة في الوقت) | B: تكمل."""
    return time_left + 5 if choice == "A" else time_left


def get_ending(time_left):
    """تحديد النهاية حسب الوقت المتبقي."""
    if time_left >= 35:
        return "best"
    if time_left > 15:
        return "good"
    return "late"
