from flask import Flask, render_template, url_for, request, redirect

import os
import time

from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor

import data_manager
import util

app = Flask(__name__)
answers_file = "sample_data/answer.csv"
question_file = "sample_data/question.csv"

#dodać folder static
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FOLDER = 'static/images/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, TARGET_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def list_questions():
    dictionary_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    question = data_manager.get_question()

    return render_template("list_questions.html", headers=dictionary_keys, stories=question)


@app.route("/add", methods=["GET"])
def add_question_get():
    return render_template("request_form.html")



app.config["IMAGE_UPLOADS"] = "/Users/admin/cc_projects/Ask_Mate_Codecool/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


@app.route("/add-question", methods=["GET", "POST"])
def add_question_post():
    if request.method == "POST":
        question = request.form
        data_manager.add_question(question)
        return redirect('/')
    return render_template("/request_form.html")

    return redirect(url_for("list_questions"))


@app.route("/add/upload-image", methods=["GET", "POST"])
def upload_image():
    return render_template("request_form.html")

@app.route("/question-edit/<question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    message = "String"
    title = "Title"
    data_manager.edit_question(title, message, question_id)
    render_template("edit_question.html")


# @app.route('/question/<question_id>', methods=['GET'])
# def display_a_question(question_id):
#     question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
#     answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
#     questions = data_manager.read_dict_from_file(data_manager.question_file)
#     answers = data_manager.read_dict_from_file(data_manager.answers_file)
#
#     question = util.finding_by_id(questions, 'id', question_id)
#
#     answers = list(
#         item for item in answers if item['question_id'] == question_id)
#     question["view_number"] = int(question.get("view_number", 0)) + 1
#     data_manager.write_data_to_file(data_manager.question_file, questions)
#
#     return render_template(
#         'question.html',
#         question=question,
#         answers=answers,
#         question_headers=question_dictionary_keys,
#         answers_headers=answers_dictionary_keys
#     )


@app.route('/question/<question_id>/delete', methods=["GET"])
def delete_a_question_get(question_id):
    data_manager.del_question(question_id)
    return redirect(url_for("list_questions.html"))



@app.route("/question/<question_id>/add_new_answer", methods=["GET"])
def add_new_answer_get(question_id):
    question = next(
        (item for item in data_manager.read_dict_from_file(data_manager.question_file) if item['id'] == question_id),
        False)
    return render_template("add_new_answer.html", question=question)


@app.route("/question/<question_id>/add_new_answer", methods=["POST"])
def add_new_answer(question_id):
    answer = {"id": util.greatest_id(data_manager.read_dict_from_file(answers_file)) + 1,
              "submission_time": int(time.time()),
              "vote_number": 0,
              "question_id": question_id,
              "message": request.form.get("message"),
              "image": ""
              }
    data_manager.add_dict_to_file(answers_file, answer)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["GET"])
def delete_an_answer(answer_id, question_id):
    answers = data_manager.read_dict_from_file(data_manager.answers_file)

    answers_after_deletion = list(d for d in answers if d["id"] != answer_id)
    data_manager.write_data_to_file(data_manager.answers_file, answers_after_deletion)

    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote_up/<question_id>', methods=['GET'])
def vote_up_answer(answer_id, question_id):
    util.voting_answer(answer_id, '+')

    return redirect(url_for('display_a_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down/<question_id>', methods=['GET'])
def vote_down_answer(answer_id, question_id):
    util.voting_answer(answer_id, '-')

    return redirect(url_for('display_a_question', question_id=question_id))


@app.route('/question/<question_id>/vote_up', methods=['GET'])
def vote_question_up(question_id):
    util.voting_question(question_id, '+')

    return redirect(url_for('list_questions'))

@app.route('/question/<question_id>/vote_down', methods=['GET'])
def vote_question_down(question_id):
    util.voting_question(question_id, '-')

    return redirect(url_for('list_questions'))


if __name__ == "__main__":
    app.run()
