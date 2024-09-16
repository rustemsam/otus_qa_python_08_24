import csv
import json
import os.path

FILES_DIR = os.path.dirname(__file__)


def get_path(filename: str) -> str:
    return os.path.join(FILES_DIR, filename)


def read_books_from_csv(csv_file: str) -> list:
    with open(get_path(csv_file), newline="") as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)

        books = []
        for row in csv_reader:
            row_dict = dict(zip(header, row))
            book = {
                "title": row_dict.get("Title", "Unknown"),
                "author": row_dict.get("Author", "Unknown"),
                "pages": int(row_dict.get("Pages", 0)),
                "genre": row_dict.get("Genre", "Unknown"),
            }
            books.append(book)
    return books


def read_users_from_json(json_file: str) -> list:
    with open(get_path(json_file), "r") as f:
        users = json.load(f)
    return users


def distribute_books_among_users(users: list, books: list) -> list:
    result_list = []

    num_users = len(users)
    num_books = len(books)

    basic_books_per_user = num_books // num_users
    extra_books = num_books % num_users

    start_index = 0

    for i, user in enumerate(users):
        result = {
            "name": user["name"],
            "gender": user["gender"],
            "address": user["address"],
            "age": user["age"],
            "books": [],
        }

        end_index = start_index + basic_books_per_user + (1 if i < extra_books else 0)
        result["books"] = books[start_index:end_index]
        start_index = end_index
        result_list.append(result)

    return result_list


def write_result_to_json(result_list: list, output_file: str):
    with open(output_file, "a") as f:
        json.dump(result_list, f, indent=4)


def parse_json_csv(csv_file: str, json_file: str, output_file: str = "result.json"):
    books = read_books_from_csv(csv_file)
    users = read_users_from_json(json_file)

    result_list = distribute_books_among_users(users, books)
    write_result_to_json(result_list, output_file)


if __name__ == "__main__":
    csv_file = "books.csv"
    json_file = "users.json"
    output_file = "result.json"
parse_json_csv(csv_file, json_file, output_file)
