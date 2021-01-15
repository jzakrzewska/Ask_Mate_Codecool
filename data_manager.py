from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection
from datetime import datetime

@connection.connection_handler
def list_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY id
        """

    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor: RealDictCursor, question):
    command = """
        INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image)
        VALUES (%(id)s,%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
    """
    next_id = get_max_id + 1
    param = {
        #"id": next_id,
        'submission_time': datetime.now(),
        'view_number': 0,
        'vote_number': 0,
        'title': question.get('title'),
        "message": question.get("message"),
        "image": "image"
    }

    cursor.execute(command, param)

# @connection.connection_handler
# def get_max_id(cursor: RealDictCursor) -> list:
#     query = """
#         SELECT nextval("id")
#         """
#
#     cursor.execute(query)
#     return cursor.fetchone()

import util

# answers_file = "sample_data/answer.csv"
# question_file = "sample_data/question.csv"
#
#
#
#
# # id_index = 0
# time_index = 1
# # view_index = 2
# # vote_index = 3
# # question_index = 4
# # message_index = 5
# # image_index = 6
#
dictionary_keys_in_memory_question = ["id","submission_time","view_number","vote_number","title","message","image"]
in_memory_question_dictionary_keys = ['Question Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image',]
# #
dictionary_keys_in_memory_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
#
# def read_dict_from_file(file_name, separator=','):
#
#     try:
#         with open(file_name, "r") as file:
#             lines = file.readlines()
#
#             listed_data = [element.replace("\n", "").replace('"', " ").split(separator) for element in lines]
#             dict_keys = listed_data[0]
#             dict_answers = listed_data[1:]
#
#             for sublist in dict_answers:
#                 sublist[time_index] = util.convert_unix_to_date(int(sublist[time_index]))
#             all_data = []
#
#             for i in range(len(dict_answers)):
#
#                 new_dict = dict(zip(dict_keys,dict_answers[i]))
#                 all_data.append(new_dict)
#
#         return all_data
#
#     except IOError:
#         return {}
#
#
# def add_dict_to_file(file_name, dict, separator=','):
#
#     with open(file_name, "a") as file:
#         values = []
#         for key in dict:
#             row = dict[key]
#             values.append(str(row))
#         file.write(separator.join(values) + "\n")
#
# def write_data_to_file(file_name,data,separator=","):
#
#     with open(file_name, "w") as file:
#         headers = (separator.join(data[0].keys()))
#         file.write(headers + "\n")
#         for dictionary in data:
#
#             dictionary['submission_time'] = str(util.convert_date_to_unix(dictionary['submission_time']))
#             dictionary["view_number"] = str(dictionary["view_number"])
#             row = separator.join(dictionary.values())
#             file.write(row + "\n")

dictionary_keys_in_memory_question = ["id","submission_time","view_number","vote_number","title","message","image"]



