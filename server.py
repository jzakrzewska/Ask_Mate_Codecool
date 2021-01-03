from flask import Flask, render_template, url_for, request, redirect

import time
import data_manager
import util

app = Flask(__name__)
answers_file = "sample_data/answer.csv"
question_file = "sample_data/question.csv"


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/list")
def list_questions():
    dictionary_keys = data_manager.dictionary_keys_in_memory
    questions = util.sort_questions_from_greatest_id(data_manager.read_dict_from_file(data_manager.question_file))

    return render_template("list_questions.html", headers=dictionary_keys, stories=questions)


@app.route("/add", methods=["GET"])
def add_question_get():
    return render_template("request_form.html")


@app.route("/add", methods=["POST"])
def add_question_post():
    data = {"id": util.greatest_id(data_manager.read_dict_from_file(question_file)) + 1,
            "submission_time": int(time.time()),
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
            "image": ""}
    print(data)
    data_manager.write_dict_to_file(question_file, data)
    return redirect(url_for("index"))

@app.route('/question/<question_id>', methods=['GET'])
def display_a_question(question_id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer

    question = next((item for item in data_manager.read_dict_from_file(data_manager.question_file) if item['id'] == question_id), False)
    answers = next((item for item in data_manager.read_dict_from_file(data_manager.answers_file) if item['id'] == question_id), False)

    return render_template(
        'question.html',
        question=question,
        answers=answers,
        question_headers = question_dictionary_keys,
        answers_headers = answers_dictionary_keys
    )


if __name__ == "__main__":
    app.run()
