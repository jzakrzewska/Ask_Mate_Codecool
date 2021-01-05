import time

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


def greatest_id(file):
    questions = sort_questions_from_greatest_id(file)
    return max([question["id"] for question in questions])


def get_question(question_id):
    for line in data_manager.read_dict_from_file(data_manager.question_file):
        if line['id'] == question_id:

            return line

    return None

# def greatest_id(file):
#     all_data = data_manager.read_dict_from_file(file)
#     return max([user["id"] for user in all_data])
