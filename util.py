def sort_questions_from_greatest_id(data):
    int_list = []
    for text in data:
        text["id"] = int(text["id"])
        text["submission_time"] = int(text["submission_time"])
        text["view_number"] = int(text["view_number"])
        text["vote_number"] = int(text["vote_number"])
        int_list.append(text)
    sorted_data = sorted(int_list, key=lambda d: d["id"], reverse=True)

    return sorted_data

