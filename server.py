from flask import Flask, render_template, url_for, request, redirect

import os
import time
import data_manager
import util

app = Flask(__name__)
answers_file = "sample_data/answer.csv"
question_file = "sample_data/question.csv"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FOLDER = 'static/images/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, TARGET_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.gif']






@app.route("/")
def list_questions():
    dictionary_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]

    question_detail = data_manager.list_questions()
    return render_template("list_questions.html", headers=dictionary_keys, stories=question_detail)


@app.route("/add", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = request.form

        image = request.files["image"]

        if image.filename != "":
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))
            image_name = "images/" + image.filename
        else:
            image.filename = "no image"
        data_manager.add_question(question)
        return redirect("/")
    return render_template("request_form.html")



@app.route('/question/<id>', methods=['GET'])
def display_a_question(id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    question_to_display = data_manager.get_question_by_id(id)
    data_manager.update_view_number(id)
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)



    return render_template(
        'question.html',
        question=question_to_display,
        answers=answers,
        id=id,
        question_headers=question_dictionary_keys,
        answers_headers=answers_dictionary_keys
    )


@app.route('/question/delete/<id>', methods=["GET"])
def delete_a_question(id):
    data_manager.delete_question_by_id(id)
    return redirect(url_for("list_questions"))

@app.route("/answer/<answer_id>/delete/<id>", methods=["GET"])
def delete_an_answer(answer_id, id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    question_to_display = data_manager.get_question_by_id(id)
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)
    data_manager.delete_answer_by_question_id(answer_id, id)
    return redirect(url_for("display_a_question", answer_id=answer_id, id=id,
                            question_headers=question_dictionary_keys,
                            answers_headers=answers_dictionary_keys,
                            question=question_to_display,
                            answers=answers))

@app.route("/question/<id>/add_new_answer", methods=["GET", "POST"])
def add_new_answer(id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)
    question = data_manager.get_question_by_id(id)
    if request.method == "POST":

        answer = request.form

        image = request.files["image"]
        if image.filename != "":
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))
            image_name = "images/" + image.filename
        else:
            image.filename = "no image"
        data_manager.add_answer_by_question_id(id, answer)

        return redirect(url_for("display_a_question",
                            answers=answers,
                            question=question,
                            id=id,
                            question_headers=question_dictionary_keys,
                            answers_headers=answers_dictionary_keys))
    return render_template("add_new_answer.html", question=question,id=id)






#
# @app.route('/answer/<answer_id>/vote_up/<question_id>', methods=['GET'])
# def vote_up_answer(answer_id, question_id):
#     util.voting_answer(answer_id, '+')
#
#     return redirect(url_for('display_a_question', question_id=question_id))
#
#
# @app.route('/answer/<answer_id>/vote_down/<question_id>', methods=['GET'])
# def vote_down_answer(answer_id, question_id):
#     util.voting_answer(answer_id, '-')
#
#     return redirect(url_for('display_a_question', question_id=question_id))
#
#
# @app.route('/question/<question_id>/vote_up', methods=['GET'])
# def vote_question_up(question_id):
#     util.voting_question(question_id, '+')
#
#     return redirect(url_for('list_questions'))
#
# @app.route('/question/<question_id>/vote_down', methods=['GET'])
# def vote_question_down(question_id):
#     util.voting_question(question_id, '-')
#
#     return redirect(url_for('list_questions'))


if __name__ == "__main__":
    app.run()
