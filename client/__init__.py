import requests
from urllib.parse import urljoin


class Task:
    def __init__(self, task_id: int, task_text: str):
        self.id = task_id
        self.text = task_text

    def __str__(self) -> str:
        return f"ID: {self.id}\n" \
               f"TASK TEXT: {self.text}"


class File:
    def __init__(self, file_id: int, filename: str, file_type: str):
        self.id = file_id
        self.name = filename
        self.type = file_type

    def __str__(self):
        return f"ID: {self.id}\n" \
               f"FILENAME: {self.name}\n" \
               f"FYLE_TYPE: {self.type}"


class ServerError(Exception):
    pass


class Client:

    def __init__(self, username: str, password: str, url: str):
        self.url = url
        self.authentication = {
            "username": username,
            "password": password
        }
        self.DEFAULT_USER_ROUTE = "/user"
        self.DEFAULT_TODO_ROUTE = "/todo"
        self.DEFAULT_FILES_ROUTE = "/files"

        self.token = requests.post(urljoin(url, self.DEFAULT_USER_ROUTE), json=self.authentication).json()["token"]

    def create_user(self, username: str, password: str) -> str:
        self.authentication = {
            "username": username,
            "password": password
        }

        self.token = requests.post(urljoin(self.url, self.DEFAULT_USER_ROUTE), json=self.authentication).json()["token"]
        return self.token

    def get_todolist(self) -> [Task]:
        response = requests.get(urljoin(self.url, self.DEFAULT_TODO_ROUTE), json={"token": self.token})
        if response.status_code == 404:
            raise ServerError(response.text)
        content = map(lambda x: x.split("#"), filter(None, response.text.split("\n")))
        answer = []

        for todo_id, todo_text in content:
            answer.append(Task(int(todo_id), todo_text))
        return answer

    def post_todo(self, text: str) -> str:
        post_body = {"token": self.token, "text": text}
        response = requests.post(urljoin(self.url, self.DEFAULT_TODO_ROUTE), json=post_body)
        if response.status_code == 404:
            raise ServerError(response.text)

        return response.text

    def update_todo(self, todo_id: int, new_text: str) -> str:
        post_body = {"token": self.token, "text": new_text}
        response = requests.put(urljoin(self.url, self.DEFAULT_TODO_ROUTE + "/" + str(todo_id)), json=post_body)
        if response.status_code == 404:
            raise ServerError(response.text)
        return response.text

    def delete_todo(self, todo_id: int) -> str:
        post_body = {"token": self.token}
        response = requests.delete(urljoin(self.url, self.DEFAULT_TODO_ROUTE + "/" + str(todo_id)), json=post_body)
        if response.status_code == 404:
            raise ServerError(response.text)
        return response.text

    def post_file(self, filename: str, file_type: str) -> str:
        with open(filename, 'r') as file:
            response = requests.post(urljoin(self.url, self.DEFAULT_FILES_ROUTE),
                                     headers={"token": self.token, "filename": filename.split("/")[-1],
                                              "Content-Type": file_type},
                                     json={"content": file.read()})
            if response.status_code == 404:
                raise ServerError(response.text)
        return response.text

    def get_file_list(self) -> [File]:
        response = requests.get(
            urljoin(self.url, self.DEFAULT_FILES_ROUTE), headers={"token": self.token}
        )
        if response.status_code == 404:
            raise ServerError(response.text)
        content = map(lambda x: x.split("#"), filter(None, response.text.split("\n")))
        answer = []

        for file_id, filename, file_type in content:
            answer.append(File(int(file_id), filename, file_type))
        return answer

    def get_file(self, filename: str, file_type: str) -> str:
        response = requests.get(urljoin(self.url, self.DEFAULT_FILES_ROUTE + "/" + filename),
                                headers={"token": self.token, "Content-Type": file_type})
        if response.status_code == 404:
            raise ServerError(response.text)
        with open(filename, mode="w") as new_file:
            new_file.write(response.text)
        return "File downloaded!"

    def delete_file(self, filename: str, file_type: str) -> str:
        response = requests.delete(urljoin(self.url, self.DEFAULT_FILES_ROUTE + "/" + filename.split("/")[-1]),
                                   headers={"token": self.token, "Content-Type": file_type})
        if response.status_code == 404:
            raise ServerError(response.text)

        return response.text
