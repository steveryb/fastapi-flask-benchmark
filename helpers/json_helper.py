import random
import string
import json


def generate_people(num_lines=100) -> str:
    """
    Generate a json file to be used with
    :param num_lines: number of lines to generate
    :return: a json blob, with num_lines number of objects, each containing an object with a name (str) and age (int)
    """

    records = [{
        "name": "".join(random.choice(string.ascii_letters) for _ in range(10)),
        "age": random.randint(0, 10000000000)
    } for _ in range(num_lines)]
    return json.dumps({"people": records})
