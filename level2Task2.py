from Flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Path to store quizzes
QUIZ_FILE = 'quizzes.json'

# Load quizzes from file
def load_quizzes():
    if os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save quizzes to file
def save_quizzes(quizzes):
    with open(QUIZ_FILE, 'w') as f:
        json.dump(quizzes, f, indent=4)

# Route for home page
@app.route('/')
def index():
    quizzes = load_quizzes()
    return render_template('index.html', quizzes=quizzes)

# Route for creating a quiz
@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        questions = request.form.getlist('question')
        options = request.form.getlist('options')
        answers = request.form.getlist('answer')

        quizzes = load_quizzes()
        quizzes[title] = {'questions': []}

        for i in range(len(questions)):
            quiz_question = {
                'question': questions[i],
                'options': options[i].split(','),
                'answer': answers[i]
            }
            quizzes[title]['questions'].append(quiz_question)

        save_quizzes(quizzes)
        return redirect(url_for('index'))

    return render_template('create_quiz.html')

# Route for taking a quiz
@app.route('/take_quiz/<quiz_title>', methods=['GET', 'POST'])
def take_quiz(quiz_title):
    quizzes = load_quizzes()
    quiz = quizzes.get(quiz_title)

    if request.method == 'POST':
        score = 0
        for i, question in enumerate(quiz['questions']):
            if request.form[f'answer{i}'] == question['answer']:
                score += 1
        return render_template('result.html', score=score, total=len(quiz['questions']))

    return render_template('take_quiz.html', quiz_title=quiz_title, quiz=quiz)

if __name__ == '__main__':
    app.run(debug=True)
