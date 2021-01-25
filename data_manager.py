from psycopg2 import sql
from psycopg2._psycopg import cursor
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
def list_questions_sorted(cursor: RealDictCursor, order_option):
    query = sql.SQL("""
            SELECT *
            FROM question
            ORDER BY {}
            """).format(sql.Identifier(order_option))

    cursor.execute(query, {'order_option': order_option})
    return cursor.fetchall()


@connection.connection_handler
def list_questions_sorted_votes(cursor: RealDictCursor):
    query = """
            SELECT *
            FROM question
            ORDER BY vote_number
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor: RealDictCursor, question, image_path=""):
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
        "image": image_path
    }

    cursor.execute(command, param)


@connection.connection_handler
def add_answer_by_question_id(cursor: RealDictCursor, question_id, answer,image_path=""):
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
        "image": image_path
    }

    cursor.execute(command, param)


@connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        SELECT id, view_number, vote_number, title, message, image
        FROM question
        WHERE id = %(id)s
        """

    param = {'id': question_id}
    cursor.execute(query,param)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = %(id)s
        """
    param = {'id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def get_answer_by_id(cursor: RealDictCursor, id) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE id = %(id)s
        """
    param = {'id': id}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def delete_question_by_id(cursor: RealDictCursor, question_id):

    return cursor.execute("DELETE FROM question WHERE id = %s", (question_id,))

@connection.connection_handler
def edit_question_by_id(cursor: RealDictCursor, question):
    command = """
            UPDATE question
            SET title = %(title)s, message = %(message)s
            WHERE id = %(id)s        
            """
    param = {"id": question["id"],
             "title": question["title"],
             "message": question["message"]}
    return cursor.execute(command, param)

@connection.connection_handler
def edit_answer_by_id(cursor: RealDictCursor, answer, question_id):


    command = """
            UPDATE answer
            SET message = %(message)s
            WHERE id = %(id)s  AND question_id = %(question_id)s     
            """
    param = {"id": answer["id"],
             "message": answer["message"],
             "question_id": question_id}

    return cursor.execute(command, param)




@connection.connection_handler
def delete_answer_by_question_id(cursor: RealDictCursor, id, question_id):

    return cursor.execute("DELETE FROM answer WHERE id = %s AND question_id = %s", (id, question_id,))

@connection.connection_handler
def update_view_number(cursor: RealDictCursor, id):

    return cursor.execute("UPDATE question SET view_number = view_number + 1 WHERE id = %s", (id,))

@connection.connection_handler
def vote_up_answer(cursor: RealDictCursor, id, question_id):

    return cursor.execute("UPDATE answer SET vote_number = vote_number + 1 WHERE id = %s AND question_id = %s",(id,question_id))

@connection.connection_handler
def vote_down_answer(cursor: RealDictCursor, id, question_id):

    return cursor.execute("UPDATE answer SET vote_number = vote_number - 1 WHERE id = %s AND question_id = %s",(id,question_id))


@connection.connection_handler
def vote_up_question(cursor: RealDictCursor, id):

    return cursor.execute("UPDATE question SET vote_number = vote_number + 1 WHERE id = %s",(id,))

@connection.connection_handler
def vote_down_question(cursor: RealDictCursor, id):

    return cursor.execute("UPDATE question SET vote_number = vote_number - 1 WHERE id = %s",(id,))


@connection.connection_handler
def search_by_phase_question(cursor: RealDictCursor, phase) -> list:
    query = """
    SELECT * 
    FROM question 
    WHERE title LIKE %(phase)s OR message LIKE %(phase)s
    """
    param = {'phase': f"%{phase}%"}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def search_by_phase_answer(cursor: RealDictCursor, phase) -> list:
    query = """
    SELECT * 
    FROM answer 
    WHERE message LIKE %(phase)s
    """
    param = {'phase': f"%{phase}%"}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def get_comment_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
    SELECT id, message, submission_time, edited_count FROM comment
    WHERE question_id = %(id)s
    """
    param = {'id': question_id}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id) -> list:
    query = """
    SELECT id, message, submission_time, edited_count FROM comment
    WHERE id = %(id)s
    """
    param = {'id': id}
    cursor.execute(query, param)
    return cursor.fetchall()






@connection.connection_handler
def add_comment_to_question(cursor: RealDictCursor, question_id, comment):
    command = """
            INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count)
            VALUES (DEFAULT, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
        """

    param = {
        "id": id,
        'question_id': question_id,
        'answer_id': None,
        'message': comment.get('message'),
        'submission_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'edited_count': 0
    }

    cursor.execute(command, param)


@connection.connection_handler
def edit_question_comment_by_id(cursor: RealDictCursor,comment):

    command = """
            UPDATE comment
            SET message = %(message)s, edited_count = %(edited_count)s + 1
            WHERE id = %(id)s"""

    param = {"id": comment["id"],
             "message": comment["message"],
             "edited_count": comment["edited_count"]}

    return cursor.execute(command, param)

@connection.connection_handler
def delete_comment_by_question_id(cursor: RealDictCursor, id, question_id):
    command = """
    DELETE from comment
    WHERE id = %(id)s AND question_id = %(question_id)s
    """
    param = {
        "id": id,
        "question_id": question_id
    }
    return cursor.execute(command,param)

dictionary_keys_in_memory_question = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
dictionary_keys_in_memory_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
dictionary_keys_in_memory_comments = ['id', 'message', 'submission_time', 'edited_count']


