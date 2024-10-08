from flask import Flask, render_template, request, redirect, url_for
import random
import webbrowser
import time
app = Flask(__name__)

words = ['PYTHON', 'FLASK', 'WEB', 'PROGRAMMING', 'HANGMAN', 'GAME', 'DEVELOPMENT', 'SERVER', 'DATABASE', 'FRAMEWORK', 'SOFTWARE', 'ENGINEER', 'COMPUTER', 'SCIENCE', 'INFORMATION', 'TECHNOLOGY', 'SECURITY', 'NETWORK', 'INTERNET', 'APPLICATION', 'INTERFACE', 'MOBILE', 'DESKTOP', 'LAPTOP', 'CODING', 'ALGORITHM', 'CLOUD', 'COMPUTING', 'BLOCKCHAIN', 'CRYPTOGRAPHY']

hidden_word = ''
guessed_letters = []
attempts = 0

@app.route('/')
def home():
    return redirect(url_for('hangman_game'))

@app.route('/hangman_game')
def hangman_game():
    global hidden_word, guessed_letters, attempts
    hidden_word = random.choice(words)
    guessed_letters = []
    attempts = 0
    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)

# TODO TASK 1 (DONE)
#  Implement logic that correctly processes the hidden_word and guessed_letters and
#  returns a string with letters revealed or hidden based on user guesses.
def get_display_word():
    global hidden_word, guessed_letters
    return ''.join([letter if letter in guessed_letters else ' _ ' for letter in hidden_word])

# TODO TASK 2 (DONE)
#  Ensure that guesses are only added if they haven’t already been guessed.
#  Ensure that the function returns True for correct guesses and False for incorrect guesses.
def check_correct_guess(input_letter):
    global guessed_letters
    input_letter = input_letter.upper()
    if input_letter not in guessed_letters:
        guessed_letters.append(input_letter)
        return input_letter in hidden_word
    return False

# TODO TASK 3 (DONE)
#  Implement the logic that tracks the number of attempts and determines if
#  the player has lost (attempts ≥ 6).
def check_lose():
    global attempts
    return attempts >= 6

# TODO TASK 4 (DONE)
#  Ensure that the function correctly checks if all letters in hidden_word are
#  in the guessed_letters.
def check_win():
    global hidden_word, guessed_letters
    return all(letter in guessed_letters for letter in hidden_word)

@app.route('/guess', methods=['POST'])
def guess():
    global hidden_word, attempts

    guessed_letter = request.form['letter']

    if not check_correct_guess(guessed_letter):
        attempts += 1

    if check_lose():
        return render_template('lose.html', word=hidden_word)

    if check_win():
        return render_template('win.html', word=hidden_word)

    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)

if __name__ == '__main__':
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    webbrowser.open_new(url)
    app.run(debug=True, port=port)
