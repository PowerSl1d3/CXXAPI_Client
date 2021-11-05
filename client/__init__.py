import requests
from urllib.parse import urljoin


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

    def get_todolist(self) -> [(int, str)]:
        response = requests.get(urljoin(self.url, self.DEFAULT_TODO_ROUTE), json={"token": self.token})
        content = map(lambda x: x.split("#"), filter(None, response.text.split("\n")))
        answer = []

        for todo_id, todo_text in content:
            answer.append((int(todo_id), todo_text))
        return answer

    def post_todo(self, text: str) -> str:
        post_body = {"token": self.token, "text": text}
        response = requests.post(urljoin(self.url, self.DEFAULT_TODO_ROUTE), json=post_body)
        return response.text

    def update_todo(self, todo_id: int, new_text: str) -> str:
        post_body = {"token": self.token, "text": new_text}
        response = requests.put(urljoin(self.url, self.DEFAULT_TODO_ROUTE + "/" + str(todo_id)), json=post_body)
        return response.text

    def delete_todo(self, todo_id: int) -> str:
        post_body = {"token": self.token}
        response = requests.delete(urljoin(self.url, self.DEFAULT_TODO_ROUTE + "/" + str(todo_id)), json=post_body)
        return response.text

    def post_file(self, filename: str, file_type: str) -> str:
        with open(filename, 'r') as file:
            response = requests.post(urljoin(self.url, self.DEFAULT_FILES_ROUTE),
                                     headers={"token": self.token, "filename": filename.split("/")[-1],
                                              "Content-Type": file_type},
                                     json={"content": file.read()})
        return response.text

    def get_file_list(self) -> [(int, str, str)]:
        response = requests.get(urljoin(self.url, self.DEFAULT_FILES_ROUTE), headers={"token": self.token})
        content = map(lambda x: x.split("#"), filter(None, response.text.split("\n")))
        answer = []

        for file_id, filename, file_type in content:
            answer.append((int(file_id), filename, file_type))
        return answer

    def get_file(self, filename: str, file_type: str) -> str:
        response = requests.get(urljoin(self.url, self.DEFAULT_FILES_ROUTE + "/" + filename),
                                headers={"token": self.token, "Content-Type": file_type})
        with open(filename, mode="w") as new_file:
            new_file.write(response.text)
        return "File downloaded!"

    def delete_file(self, filename: str, file_type: str) -> str:
        response = requests.delete(urljoin(self.url, self.DEFAULT_FILES_ROUTE + "/" + filename.split("/")[-1]),
                                   headers={"token": self.token, "Content-Type": file_type})

        return response.text
