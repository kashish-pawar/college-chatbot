from rapidfuzz import fuzz
import json
import re

# Function to clean user input and pattern questions
def clean_text(text):
    return re.sub(r'\W+', ' ', text.lower()).strip()

# Load JSON data from file
with open('database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Function to get the most relevant answer based on user input
def get_dynamic_answer(user_input):
    highest_score = 0
    best_answer = "Sorry, I couldn't understand your question. Please try again."

    user_input_clean = clean_text(user_input)

    for item in data:
        for pattern_entry in item['patterns']:
            pattern_clean = clean_text(pattern_entry['question'])
            score = fuzz.token_set_ratio(user_input_clean, pattern_clean)

            if score > highest_score and score > 70:  # You can adjust this threshold
                highest_score = score
                best_answer = pattern_entry['response']

    return best_answer

# For testing purpose
if __name__ == "__main__":
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = get_dynamic_answer(query)
        print("Bot:", response)
