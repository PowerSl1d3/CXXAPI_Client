from client import Client
import magic
import time


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
    username = 'admin'
    password = 'admin'
    client = Client(url=url, username=username, password=password)
    #print(client.get_todolist())
    #print(client.post_todo("Hello world!"))
    #print(client.update_todo(1, "New todo"))
    #print(client.delete_todo(1))
    print(client.post_file('/home/olegaksenenko/Desktop/git/CXXAPI_Client/HelloWorld.cpp',
                           magic.from_file('/home/olegaksenenko/Desktop/git/CXXAPI_Client/HelloWorld.cpp')))
    file_list = client.get_file_list()
    print(file_list)
    print(client.get_file(file_list[0][1], file_list[0][2]))
    print(client.delete_file(file_list[0][1], file_list[0][2]))

