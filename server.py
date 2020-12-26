from flask import Flask, render_template

import data_manager
import util

app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")# questions = questions)


@app.route("/list")
def list_questions():
    dictionary_keys = data_manager.dictionary_keys_in_memory
    questions = util.sort_questions_from_greatest_id(data_manager.read_dict_from_file(data_manager.question_file))

    return render_template("list_questions.html", headers=dictionary_keys, stories=questions)

if __name__ == "__main__":
    app.run()
