from flask import Flask, render_template
import data_manager


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/question/<question_id>', methods=['GET'])
def display_a_question(question_id):
    question_dictionary_keys = data_manager.in_memory_question_dictionary_keys
    answers_dictionary_keys = data_manager.in_memory_answer_dictionary_keys

    question = next((item for item in data_manager.read_dictionary_from_file(data_manager.question_file) if item['Question Id'] == question_id), False)
    answers = next((item for item in data_manager.read_dictionary_from_file(data_manager.answers_file) if item['Question Id'] == question_id), False)

    return render_template(
        'question.html',
        question=question,
        answers=answers,
        question_headers = question_dictionary_keys,
        answers_headers = answers_dictionary_keys
    )

if __name__ == '__main__':
    app.run()
