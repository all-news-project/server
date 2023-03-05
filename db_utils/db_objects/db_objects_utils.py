def get_db_object_from_dict(object_dict: dict, class_instance) -> object:
    """
    Getting a database dictionary and a class and return the database object

    # example of use:
    article = get_db_object_from_dict(object_dict=article_dict, class_instance=Article)

    :param object_dict:
    :param class_instance:
    :return:
    """
    if "_id" in object_dict.keys():
        object_dict.pop("_id", None)
    obj = class_instance(**object_dict)
    return obj
