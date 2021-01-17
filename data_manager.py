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
        'submission_time': datetime.now(),
        'view_number': 0,
        'vote_number': 0,
        'title': question.get('title'),
        "message": question.get("message"),
        "image": question.get("image.filename")
    }

    cursor.execute(command, param)

@connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, id) -> list:
    query = """
        SELECT view_number, vote_number, title, message, image
        FROM question
        WHERE id = %(id)s
        """
    param = {'id': id}
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

dictionary_keys_in_memory_question = ["id","submission_time","view_number","vote_number","title","message","image"]
dictionary_keys_in_memory_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']



