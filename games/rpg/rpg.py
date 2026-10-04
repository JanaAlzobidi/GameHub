
from logic import (
    check_tires,
    choose_road,
    handle_stuck,
    help_person,
    get_ending
)

from story import (
    prologue,
    tire_event,
    tire_checked,
    tire_ignored,
    road_event,
    paved_result,
    unpaved_aired_result,
    unpaved_not_aired_result,
    stuck_event,
    stuck_try_result,
    help_result,
    person_event,
    person_helped_result,
    person_ignored_result,
    endings
)


# =========================
# GAME SETUP
# =========================

time_left = 60


# =========================
# PROLOGUE
# =========================

print("\n🌌 DESERT NIGHT 🌌")

for scene in prologue:
    print("\n" + scene)
    input("\nاضغط Enter للمتابعة...")


# =========================
# EVENT 1 — TIRES
# =========================

print("\n" + tire_event["text"])

for key, choice in tire_event["choices"].items():
    print(f"{key} - {choice}")

choice = input("\nاختيارك: ").upper()

time_left, tire_aired = check_tires(choice, time_left)

if choice == "A":
    print("\n" + tire_checked)
else:
    print("\n" + tire_ignored)

input("\nاضغط Enter للمتابعة...")


# =========================
# EVENT 2 — ROAD
# =========================

print("\n" + road_event["text"])

for key, choice in road_event["choices"].items():
    print(f"{key} - {choice}")

choice = input("\nاختيارك: ").upper()

time_left, road = choose_road(choice, time_left)

if choice == "A":
    print("\n" + paved_result)

else:
    if tire_aired:
        print("\n" + unpaved_aired_result)

    else:
        print("\n" + unpaved_not_aired_result)

        for key, choice_text in stuck_event["choices"].items():
            print(f"{key} - {choice_text}")

        stuck_choice = input("\nاختيارك: ").upper()

        time_left, got_help = handle_stuck(
            tire_aired,
            stuck_choice,
            time_left
        )

        if stuck_choice == "A":
            print("\n" + stuck_try_result)
            print("\n" + help_result)
        else:
            print("\n" + help_result)

input("\nاضغط Enter للمتابعة...")


# =========================
# EVENT 3 — PERSON
# =========================

print("\n" + person_event["text"])

for key, choice in person_event["choices"].items():
    print(f"{key} - {choice}")

choice = input("\nاختيارك: ").upper()

time_left = help_person(choice, time_left)

if choice == "A":
    print("\n" + person_helped_result)
else:
    print("\n" + person_ignored_result)

input("\nاضغط Enter للمتابعة...")


# =========================
# ENDING
# =========================

ending = get_ending(time_left)

print("\n" + "=" * 40)
print("📸 النتيجة")
print("=" * 40)

print("\n" + endings[ending])

print(f"\nالوقت المتبقي: {time_left} دقيقة")
