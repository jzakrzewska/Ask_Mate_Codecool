answers_file = 'sample_data/answer.csv'
question_file = 'sample_data/question.csv'


in_memory_question_dictionary_keys = [
    'Question Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image',
]

in_memory_answer_dictionary_keys = [
    'Answer Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image',
]


def read_dictionary_from_file(file_name, separator=','):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            listed_data = [element.replace('\n', '').split(separator) for element in lines]
            dictionary_keys = listed_data[0]
            dictionary_elements = listed_data[1:]
            all_data = []

            for element in range(len(dictionary_elements)):
                new_dictionary = dict(zip(dictionary_keys, dictionary_elements[element]))
                all_data.append(new_dictionary)

        return all_data

    except IOError:
        return {}

