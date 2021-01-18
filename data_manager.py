from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import connection
import datetime

@connection.connection_handler
def get_id(cursor: RealDictCursor) -> list:
    query = """
            SELECT MAX(id) + 1  FROM question"""
    cursor.execute(query)


    return cursor.fetchall()



@connection.connection_handler
def get_question(cursor: RealDictCursor) -> list:
    query = """
            SELECT id, image, message, title, vote_number, view_number, submission_time
            FROM question
            ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def add_question(cursor: RealDictCursor, question) -> list:

    command = """
            INSERT INTO question (id, image, message, title, vote_number, view_number, submission_time)
            VALUES (DEFAULT ,%(image)s,%(message)s,%(title)s,%(vote_number)s,%(view_number)s,%(submission_time)s);"""
    param = {'id': id,
             'image': question.get("image"),
             'message': question.get("message"),
             'title': question.get("title"),
             'vote_number': 0,
             'view_number': 0,
             'submission_time': datetime.datetime.now()}
    cursor.execute(command, param)

@connection.connection_handler
def edit_question(cursor: RealDictCursor, title, message, question_id):
    command = """UPDATE question SET title = %(title)s , message = %(message) WHERE id = %(id)s;"""
    param = {'message': message, "title": title, "id": question_id}
    cursor.execute(command, param)

@connection.connection_handler
def del_question(cursor: RealDictCursor, id: int):
    command = """
            DELETE
            FROM question
            WHERE id = %(id)s
     """
    param = {"id": id}
    cursor.execute(command, param)




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
in_memory_question_dictionary_keys = [
     'Question Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
# # ]
# #
# dictionary_keys_in_memory_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
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
#

