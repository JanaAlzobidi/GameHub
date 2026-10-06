# Import the random module to select questions and shuffle options randomly.
import random

# Import the QUESTIONS list from the questions.py file.
from questions import QUESTIONS

# here are fixed values used throughout the game.
QUESTION_TIME = 30                    # Time limit for each question
ROUND_SIZE = 5                        # Number of questions in each round
MAX_POINTS = 3                        # Maximum points for one question
MAX_SCORE = ROUND_SIZE * MAX_POINTS   # Maximum score for one round

# Check if the question's category is in the selected categories
in_selected = lambda question, cats: question["category"] in cats

# This function calculates points based on answer time and correctness.
def calculate_points(elapsed, is_correct):

    # Wrong answer = 0 points.
    if not is_correct:
        return 0

    # Correct answer = points based on speed (seconds).
    if elapsed <= 10:
        return 3     
    elif elapsed <= 20:
        return 2        
    elif elapsed <= QUESTION_TIME:
        return 1       
    else:
        return 0        

# This function return a copy of the question with shuffled options.
def shuffle_options(question):

    options = question["options"][:]     # Copy the options
    random.shuffle(options)              # Shuffle the options

    new_question = question.copy()       # Copy the question
    new_question["options"] = options    # Add the shuffled options
    return new_question                  # Return the new question


# This function select questions for the game round
def pick_questions(selected, count=ROUND_SIZE):

    pool = []
    for q in QUESTIONS:
        if in_selected(q, selected): # Check if the question category was selected
            pool.append(q)
    
    # Set the number of questions, using all available questions if there are fewer.
    how_many = count
    if len(pool) < count:
        how_many = len(pool)

    # Select questions randomly from the available questions
    chosen = random.sample(pool, how_many)

    # Creates a list of selected questions, shuffles their options, and returns the final list.
    result = []
    for q in chosen:
        result.append(shuffle_options(q))
    return result


def summarize(results):

    correct = 0      # Count correct answers.
    timeouts = 0     # Count timed-out questions.
    score = 0        # Calculate the total score.

    # Go through all question results.
    for r in results:
        score = score + r["points"]
        if r["correct"]:
            correct = correct + 1
        if r["timed_out"]:
            timeouts = timeouts + 1
    
    # Calculate wrong answers
    wrong = len(results) - correct 
    
    return {
        "correct": correct,
        "wrong": wrong,
        "timeouts": timeouts,
        "score": score,
    }