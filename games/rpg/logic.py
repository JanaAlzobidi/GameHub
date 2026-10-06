"""
logic.py - منطق اللعبة (الوقت والقرارات والنهايات) بدون أي نصوص أو واجهة.
"""

START_TIME = 60  # دقائق الوقت المتاح للتجهيز


def check_tires(choice, time_left):
    """
    معالجة قرار فحص الكفرات.
    A: تفحص السيارة وتنسّم الكفرات.
    B: تتجاهل الإحساس وتنطلق مباشرة.
    """
    if choice == "A":
        return time_left - 5, True
    return time_left, False


def choose_road(choice, time_left):
    """
    معالجة اختيار الطريق.
    A: تأخذ الطريق الممهّد.
    B: تأخذ الطريق غير الممهّد.
    """
    if choice == "A":
        return time_left - 30, "paved"
    return time_left - 20, "unpaved"


def handle_stuck(tire_aired, choice, time_left):
    """
    معالجة ما يحدث إذا أخذ اللاعب الطريق غير الممهّد
    بدون تنسيم الكفرات.
    إذا كانت الكفرات منسّمة:
        تخرج السيارة بسرعة.
    إذا لم تكن الكفرات منسّمة:
        A: تحاول إخراج السيارة بنفسك،
           لكنك تفشل، فتضطر لانتظار المساعدة في النهاية.
        B: تنتظر مرور شخص يساعدك.
    """
    if tire_aired:
        return time_left, False
    return (time_left - 25 if choice == "A" else time_left - 15), True


def help_person(choice, time_left):
    """
    معالجة قرار اللاعب الأخير تجاه الشخص الواقف في الطريق.
    A: توصّل الشخص.
    B: تكمل طريقك بدون مساعدته.
    """
    return time_left + 5 if choice == "A" else time_left


def get_ending(time_left):
    """
    تحديد النهاية بناءً على الوقت المتبقي.
    """
    if time_left >= 35:
        return "best"
    if time_left > 15:
        return "good"
    return "late"
