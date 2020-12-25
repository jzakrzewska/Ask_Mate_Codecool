answers_file = "sample_data/answer.csv"
question_file = "sample_data/question.csv"
id_index = 0
time_index = 1
vote_index = 2
question_id_index = 3
message_index = 4
image_index = 5


def read_dict_from_file(file_name, separator=','):

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

            listed_answers = [element.replace("\n", "").split(separator) for element in lines]
            dict_keys = listed_answers[0]
            dict_answers = listed_answers[1:]
            all_answers = []

            for i in range(len(dict_answers)):
                new_dict = dict(zip(dict_keys,dict_answers[i]))
                all_answers.append(new_dict)
        return all_answers

    except IOError:
        return {}

dicts = read_dict_from_file(question_file)
for dict in dicts:
    print(dict)
#
# def write_dict_to_file(file_name,dict separator=','):
#
#     with open(file_name, "w") as file:
#         for record in dict:
#             row = separator.join(record)
#             file.write(row + "\n")
