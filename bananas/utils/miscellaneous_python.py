def multiple_key_delete(dictionary, key_list):
    for key in key_list:
        if key in dictionary:
            del dictionary[key]


