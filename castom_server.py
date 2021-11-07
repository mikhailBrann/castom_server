import socket

# устанавливаем подключение сервера и через listen ограничиваем количество подключений до 5
server = socket.create_server(('127.0.0.1', 2000))
server.listen(5)

# получаем клиентский сокет и адрес
client_socket, addres = server.accept()
data = client_socket.recv(1024).decode('utf-8')

# устанавливаем заголовок и отправляем ответ пользователю
headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')
content = 'connect to server sucefull!'.encode('utf-8')
server_answer = client_socket.send(headers + content)


