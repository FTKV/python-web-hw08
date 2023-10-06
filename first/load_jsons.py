import json
import pathlib

from connect import db_name, client_mongo
from models import Author, Quote


exec(f"db = client_mongo.{db_name}")


model_file_dict = {"authors": Author, "quotes": Quote}


if __name__ == '__main__':
    list_files = pathlib.Path('.').joinpath("first/json").glob('*.json')
    authors =[]
    for file in list_files:
        with open(file, 'r', encoding="utf-8") as fh:
            collection = db.create_collection(file.stem)
            json_list = json.load(fh)
            for json_file in json_list:
                print(file.stem[:-1].capitalize())
                if file.stem != "authors":
                    json_file["author"] = list(filter(lambda n: n["fullname"] == json_file["author"], authors))[0]
                object = model_file_dict[file.stem](**json_file).save()
                if file.stem == "authors":
                    authors.append(object)
