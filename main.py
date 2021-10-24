from client import Client


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
    username = 'admin'
    password = 'admin'
    client = Client(url=url, username=username, password=password)
    print(client.get_todolist())
    print(client.post_todo("Hello world!"))
    print(client.update_todo(1, "New todo"))
    print(client.delete_todo(1))
