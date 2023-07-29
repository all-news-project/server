import json
import os.path

from git_db.utils.consts import RepoConsts


def load_data_from_json(file_name: str):
    file_path = os.path.join(RepoConsts.REPO_PATH, file_name)
    return read_json_file(file_path=file_path)


def save_data_to_json(file_name: str, data):
    file_path = os.path.join(RepoConsts.REPO_PATH, file_name)
    save_json_file(file_path=file_path, data=data)


def read_json_file(file_path: str):
    """
    Read json file
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json_file(file_path: str, data: dict, ident: int = 4):
    """
    Saving json file data into path
    :param file_path:
    :param data:
    :param ident:
    :return:
    """
    file = open(file_path, 'w')
    json.dump(data, file, indent=ident)
    # json.dumps(data, file, indent=4)
    file.close()
