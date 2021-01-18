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
        
        VALUES (DEFAULT,%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
        
    
    """
    param = {
        "id": id,
        'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'view_number': 0,
        'vote_number': 0,
        'title': question.get('title'),
        "message": question.get("message"),
        "image": question.get("image.filename")
    }

    cursor.execute(command, param)

@connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        SELECT view_number, vote_number, title, message, image
        FROM question
        WHERE id = %(id)s
        """

    param = {'id': question_id}
    cursor.execute(query,param)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        SELECT submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = %(id)s
        """
    param = {'id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def delete_question_by_id(cursor: RealDictCursor, question_id):

    return cursor.execute("DELETE FROM question WHERE id = %s", (question_id,))


@connection.connection_handler
def add_answer_by_question_id(cursor: RealDictCursor, question_id, answer):
    command = """
        INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)

        VALUES (DEFAULT,%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
    """

    param = {
        "id": id,
        'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'vote_number': 0,
        'question_id': question_id,
        "message": answer.get("message"),
        "image": answer.get("image.filename")
    }

    cursor.execute(command, param)


dictionary_keys_in_memory_question = ["id","submission_time","view_number","vote_number","title","message","image"]
dictionary_keys_in_memory_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']



