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

    data_manager.add_dict_to_file(question_file, data)
    return redirect(url_for("index"))

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

@app.route('/question/<question_id>/delete', methods=["GET"])
def delete_a_question_get(question_id):
    dictionary_keys = data_manager.dictionary_keys_in_memory_question
    questions = data_manager.read_dict_from_file(data_manager.question_file)
    answers = data_manager.read_dict_from_file(data_manager.answers_file)

    question_to_delete = next((item for item in questions if item['id'] == question_id), False)

    questions_after_deletion = list(d for d in questions if d != question_to_delete)
    answers_after_deletion = list(item for item in answers if item['question_id'] != question_id)

    data_manager.write_data_to_file(data_manager.question_file, questions_after_deletion)
    data_manager.write_data_to_file(data_manager.answers_file, answers_after_deletion)

    questions = util.sort_questions_from_greatest_id(data_manager.read_dict_from_file(data_manager.question_file))

    return render_template("list_questions.html", headers=dictionary_keys, stories=questions)


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
    data_manager.add_dict_to_file(answers_file, answer)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["GET"])
def delete_an_answer(answer_id,question_id):
    answers = data_manager.read_dict_from_file(data_manager.answers_file)

    answers_after_deletion = list(d for d in answers if d["id"] != answer_id)
    data_manager.write_data_to_file(data_manager.answers_file, answers_after_deletion)

    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote_up', methods=['GET'])
def vote_up_answer(answer_id):
    answers = data_manager.read_dict_from_file(data_manager.answers_file)
    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer

    answer = next((item for item in data_manager.read_dict_from_file(data_manager.answers_file) if item['id'] == answer_id), False)
    answer['vote_number'] = answer['vote_number'] + 1

    data_manager.add_data_to_file(data_manager.answers_file, answer)

if __name__ == "__main__":
    app.run()
