import util

answers_file = "sample_data/answer.csv"
question_file = "sample_data/question.csv"




# id_index = 0
time_index = 1
# view_index = 2
# vote_index = 3
# question_index = 4
# message_index = 5
# image_index = 6

dictionary_keys_in_memory_question = ["id","submission_time","view_number","vote_number","title","message","image"]
# in_memory_question_dictionary_keys = [
#     'Question Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image',
# ]
#
dictionary_keys_in_memory_answer = ['answer id', 'submission time', 'vote number', 'question id', 'message', 'image']

def read_dict_from_file(file_name, separator=','):

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

            listed_data = [element.replace("\n", "").replace('"', " ").split(separator) for element in lines]
            dict_keys = listed_data[0]
            dict_answers = listed_data[1:]

            for sublist in dict_answers:
                sublist[time_index] = util.convert_unix_to_date(int(sublist[time_index]))
            all_data = []

            for i in range(len(dict_answers)):

                new_dict = dict(zip(dict_keys,dict_answers[i]))
                all_data.append(new_dict)

        return all_data

    except IOError:
        return {}


def write_dict_to_file(file_name, dict, separator=','):

    with open(file_name, "a") as file:
        values = []
        for key in dict:
            row = dict[key]
            values.append(str(row))
        file.write(separator.join(values) + "\n")

