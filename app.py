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
    dictionary_keys = data_manager.dictionary_keys_in_memory_question
    questions = util.sort_questions_from_greatest_id(data_manager.read_dict_from_file(data_manager.question_file))

    return render_template("list_questions.html", headers=dictionary_keys, stories=questions)


@app.route("/add", methods=["GET"],)
def add_question_get():
    return render_template("request_form.html", question=None)


@app.route("/add", methods=["POST"])
def add_question_post():
    data = {"id": util.greatest_id(data_manager.read_dict_from_file(question_file)) + 1,
            "submission_time": int(time.time()),
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
            "image": ""}

    data_manager.write_dict_to_file(question_file, data)
    return redirect(url_for("index"))


@app.route('/edit/<question_id>', methods=["GET"])
def edit_question_get(question_id):

    question_id = int(question_id)
    question = util.get_question(question_id)
    print(question)
    if question is None:
        return redirect(url_for("index"))

    return render_template("request_form.html", question=question)


@app.route("/edit/<question_id>", methods=["POST"])
def edit_question_post(question_id):
    question_id = int(question_id)
    question = util.get_question(question_id)

    question["title"] = request.form.get("title")
    question["message"] = request.form.get("message")
    question["submission_time"] = int(time.time())
    data_manager.update_dic_in_file(question_file, question)
    return redirect(url_for("list_questions"))


@app.route('/question/<question_id>', methods=['GET'])
def display_a_question(question_id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer

    question = next((item for item in data_manager.read_dict_from_file(data_manager.question_file) if item['id'] == question_id), False)

    answers = list(item for item in data_manager.read_dict_from_file(answers_file) if item['question_id'] == question_id)

    return render_template(
        'question.html',
        question=question,
        answers=answers,
        question_headers=question_dictionary_keys,
        answers_headers=answers_dictionary_keys
    )

@app.route("/question/<question_id>/add_new_answer", methods=["GET"])
def add_new_answer_get(question_id):
    question = next((item for item in data_manager.read_dict_from_file(data_manager.question_file) if item['id'] == question_id), False)
    return render_template("add_new_answer.html", question=question)



@app.route("/question/<question_id>/add_new_answer", methods=["POST"])
def add_new_answer(question_id):
    question = next((item for item in data_manager.read_dict_from_file(data_manager.question_file) if item['id'] == question_id), False)

    answer = {"id": util.greatest_id(data_manager.read_dict_from_file(answers_file)) + 1,
              "submission_time": int(time.time()),
              "vote_number": 0,
              "question_id": question_id,
              "message": request.form.get("message"),
              "image": ""
              }
    data_manager.write_dict_to_file(answers_file, answer)
    return redirect(url_for("display_a_question",question_id=question_id))

if __name__ == "__main__":
    app.run()
