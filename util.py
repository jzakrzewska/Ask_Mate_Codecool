

def sort_questions_from_greatest_id(data):
    int_list = []
    for d in data:
        d["id"] = int(d["id"])
        d["submission_time"] = int(d["submission_time"])
        d["view_number"] = int(d["view_number"])
        d["vote_number"] = int(d["vote_number"])
        int_list.append(d)
    sorted_data = sorted(int_list, key= lambda d: d["id"],reverse=True)

    return sorted_data

