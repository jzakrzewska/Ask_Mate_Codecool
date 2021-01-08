import time
from datetime import datetime

import data_manager

def sort_questions_from_greatest_id(data):
    int_list = []
    for text in data:
        text["id"] = int(text["id"])
        #text["view_number"] = int(text["view_number"])
        #text["vote_number"] = int(text["vote_number"])
        int_list.append(text)
    sorted_data = sorted(int_list, key=lambda d: d["id"], reverse=True)

    return sorted_data

def convert_unix_to_date(data):
    local_time = time.ctime(data)
    return local_time

def convert_date_to_unix(data):
    time = datetime.strptime(data, "%a %b %d %H:%M:%S %Y")
    unix_time = int(datetime.timestamp(time))

    return unix_time

def greatest_id(file):
    questions = sort_questions_from_greatest_id(file)
    return max([question["id"] for question in questions])


# def greatest_id(file):
#     all_data = data_manager.read_dict_from_file(file)
#     return max([user["id"] for user in all_data])


def finding_by_id(file, id_in_file, given_id):
    return next((item for item in file if item[id_in_file] == given_id), False)


def voting_answer(answer_id, operator):
    answers = data_manager.read_dict_from_file(data_manager.answers_file)
    answer = finding_by_id(answers, 'id', answer_id)

    answers_after_deletion = list(item for item in answers if item["id"] != answer_id)
    data_manager.write_data_to_file(data_manager.answers_file, answers_after_deletion)

    if operator == '+':
        answer['vote_number'] = str(int(answer['vote_number']) + 1)
    elif operator == '-':
        answer['vote_number'] = str(int(answer['vote_number']) - 1)
    else:
        raise ValueError('Invalid operator, try + or -')

    answer['submission_time'] = convert_date_to_unix(answer['submission_time'])

    data_manager.add_dict_to_file(data_manager.answers_file, answer)


def voting_question(question_id,operator):
    questions = data_manager.read_dict_from_file(data_manager.question_file)
    question = finding_by_id(questions, 'id', question_id)

    questions_after_voting = list(item for item in questions if item != question)
    data_manager.write_data_to_file(data_manager.question_file, questions_after_voting)

    if operator == '+':
        question['vote_number'] = str(int(question['vote_number']) + 1)
    elif operator == '-':
        question['vote_number'] = str(int(question['vote_number']) - 1)
    else:
        raise ValueError('Invalid operator, try + or -')

    question['submission_time'] = convert_date_to_unix(question['submission_time'])

    data_manager.add_dict_to_file(data_manager.question_file, question)

    questions = sort_questions_from_greatest_id(data_manager.read_dict_from_file(data_manager.question_file))