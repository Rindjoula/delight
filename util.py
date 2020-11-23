import json 
import requests 

def make_request(url, token):
    """
    Parameters:
    url: url of the request
    token: authorization token

    Returns:
    result of the request
    """

    headers = {"Authorization": "token {}".format(token)}
    x = requests.get(url, headers=headers)
    return json.loads(x.text)


def read_from_json(file_input):
    """
    Parameters: 
    file_input: json file

    Returns:
    data containing in file_input
    """

    with open(file_input) as f:
        data = json.load(f)
    return data


def write_to_json(file_output, list_obj):
    """
    Parameters:
    file_output: json file where the list_obj will be writen
    list_obj: list of objects to be writen
    """

    with open(file_output, "w") as f:
        json.dump(list_obj, f, default=lambda x: x.__dict__)