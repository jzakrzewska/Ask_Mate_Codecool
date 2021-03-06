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

sort_options = ["id", "submission_time", "view_number", "vote_number", "title", "message",]




@app.route("/")
def list_questions():
    dictionary_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    order_option = request.args.get("sort_list")
    if order_option:
        question_detail = data_manager.list_questions_sorted(order_option)
    else:
        question_detail = data_manager.list_questions()

    return render_template("list_questions.html", headers=dictionary_keys, stories=question_detail)


@app.route("/add", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question = request.form
        image = request.files["image"]

        if image.filename != "":
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))

        else:
            image.filename = "no image"

        data_manager.add_question(question,"/images/" + image.filename)

        return redirect("/")
    return render_template("request_form.html", question=None)

@app.route("/edit/<id>", methods=["GET","POST"])
def edit_question(id):
    if request.method == "POST":
        question = dict(request.form)
        data_manager.edit_question_by_id(question)
        return redirect(url_for("display_a_question",id=id))

    else:
        question = data_manager.get_question_by_id(id)[0]
        return render_template("request_form.html", question=question)

@app.route("/answer/<answer_id>/edit/<id>", methods=["GET","POST"])
def edit_answer(answer_id, id):

    if request.method == "POST":
        answer = request.form
        question = data_manager.get_question_by_id(id)
        data_manager.edit_answer_by_id(answer,id)
        return redirect(url_for("display_a_question",id=id, answer_id=answer_id,answer=answer,question=question))

    else:
        answer = data_manager.get_answer_by_id(answer_id)[0]
        question = data_manager.get_question_by_id(id)
        return render_template("add_new_answer.html", question=question,id=id,answer=answer)

@app.route('/question/<id>', methods=['GET'])
def display_a_question(id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    question_to_display = data_manager.get_question_by_id(id)

    data_manager.update_view_number(id)

    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)

    comments_dictionary_keys = data_manager.dictionary_keys_in_memory_comments
    question_comments = data_manager.get_comment_by_question_id(id)

    return render_template(
        'question.html',
        question=question_to_display,
        answers=answers,
        id=id,
        question_headers=question_dictionary_keys,
        answers_headers=answers_dictionary_keys,
        comments_headers=comments_dictionary_keys,
        question_comments=question_comments,
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
        data_manager.add_answer_by_question_id(id, answer,"/images/" + image.filename)

        return redirect(url_for("display_a_question",
                            answers=answers,
                            question=question,
                            id=id,
                            question_headers=question_dictionary_keys,
                            answers_headers=answers_dictionary_keys))
    return render_template("add_new_answer.html", question=question,id=id,answer=None)


@app.route('/answer/<answer_id>/up/<id>', methods=['GET'])
def vote_answer_up(answer_id, id):
    data_manager.vote_up_answer(answer_id,id)
    return redirect(url_for('display_a_question',
                            id=id,
                            answer_id=answer_id))


@app.route('/answer/<answer_id>/down/<id>', methods=['GET'])
def vote_answer_down(answer_id, id):
    data_manager.vote_down_answer(answer_id,id)
    return redirect(url_for('display_a_question',
                            id=id,
                            answer_id=answer_id))


@app.route('/question/<id>/up', methods=['GET'])
def vote_question_up(id):
    data_manager.vote_up_question(id)
    return redirect(url_for('list_questions'))


@app.route('/question/<id>/down', methods=['GET'])
def vote_question_down(id):
    data_manager.vote_down_question(id)
    return redirect(url_for('list_questions'))


@app.route('/search', methods=['GET'])
def search_by_phase():
    message = request.args.get("q")
    result_question = data_manager.search_by_phase_question(message)
    result_answer = data_manager.search_by_phase_answer(message)

    return render_template('search.html', questions=result_question, answers=result_answer)


@app.route("/question/<id>/add_new_comment", methods=["GET", "POST"])
def add_new_comment_to_question(id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    comments_dictionary_keys = data_manager.dictionary_keys_in_memory_comments

    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)

    question = data_manager.get_question_by_id(id)
    question_comments = data_manager.get_comment_by_question_id(id)

    if request.method == "POST":
        comment = request.form

        data_manager.add_comment_to_question(id, comment)

        return redirect(url_for("display_a_question",
                            answers=answers,
                            question=question,
                            id=id,
                            question_headers=question_dictionary_keys,
                            answers_headers=answers_dictionary_keys,
                            comments_headers=comments_dictionary_keys,
                            question_comments=question_comments,
                            ))
    return render_template("request_form_comment.html", question=question, id=id, comment=None)

@app.route("/<comment_id>/edit/<id>", methods=["GET","POST"])
def edit_question_comment(comment_id, id):

    if request.method == "POST":
        comment = request.form
        question = data_manager.get_question_by_id(id)
        data_manager.edit_question_comment_by_id(comment)
        return redirect(url_for("display_a_question", id=id, comment_id=comment_id, comment=comment, question=question))

    else:
        comment = data_manager.get_comment_by_id(comment_id)[0]
        question = data_manager.get_question_by_id(id)
        return render_template("request_form_comment.html", question=question, id=id, comment=comment)


@app.route("/<comment_id>/delete/<id>", methods=["GET"])
def delete_a_question_comment(comment_id, id):
    question_dictionary_keys = data_manager.dictionary_keys_in_memory_question
    question_to_display = data_manager.get_question_by_id(id)

    answers_dictionary_keys = data_manager.dictionary_keys_in_memory_answer
    answers = data_manager.get_answer_by_question_id(id)

    comments_dictionary_keys = data_manager.dictionary_keys_in_memory_comments
    question_comments = data_manager.get_comment_by_question_id(id)

    data_manager.delete_comment_by_question_id(comment_id, id)


    return redirect(url_for("display_a_question", comment_id=comment_id, id=id,
                            question_headers=question_dictionary_keys,
                            answers_headers=answers_dictionary_keys,
                            question=question_to_display,
                            answers=answers,
                            comments_headers=comments_dictionary_keys,
                            question_comments=question_comments))


if __name__ == "__main__":
    app.run()
