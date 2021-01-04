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
def add_user_story_get():
    return render_template("request_form.html", story=None)


@app.route("/add", methods=["POST"])
def add_user_story_post():
    data = dict(request.form)
    data["view number"] = 0
    data["id"] = util.greatest_id() + 1
    data["submission time"] = time.time()
    data_manager.write_dict_to_file(question_file, data)
    return redirect(url_for(list_questions))


if __name__ == "__main__":
    app.run()
