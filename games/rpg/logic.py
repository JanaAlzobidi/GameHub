def check_tires(choice, time_left):
    """
    Handle the tire-check decision.
    A: Check the car and air down the tires.
    B: Ignore the feeling and leave immediately.
    """
    if choice == "A":
        time_left -= 5
        tire_aired = True
    else:
        tire_aired = False
    return time_left, tire_aired


def choose_road(choice, time_left):
    """
    Handle the road choice.
    A: Take the paved road.
    B: Take the unpaved road.
    """
    if choice == "A":
        time_left -= 30
        road = "paved"
    else:
        time_left -= 20
        road = "unpaved"
    return time_left, road


def handle_stuck(tire_aired, choice, time_left):
    """
    Handle what happens if the player takes the unpaved road
    without airing down the tires.
    If the tires were aired down:
        The car gets out quickly،
    If the tires were not aired down:
        A: Try to get the car out yourself.
           but fails, so you still wait for help.
        B: Wait for someone to pass and help.
    """
    if tire_aired:
        return time_left, False
    if choice == "A":
        time_left -= 10
        time_left -= 15
    else:
        time_left -= 15
    return time_left, True


def help_person(choice, time_left):
    """
    Handle the final person's choice.
    A: Give the person a ride.
    B: Continue without helping.
    """
    if choice == "A":
        time_left += 5
    return time_left


def get_ending(time_left):
    """
    Determine the ending based on remaining time.
    """
    if time_left >= 20:
        return "best"
    elif time_left > 0:
        return "good"
    else:
        return "late"
