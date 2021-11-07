import socket,os


class CastomServer:
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port
        self.script_path = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def answer_server(self, request_data):
        headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')
        headers_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')
        path = self.script_path + f'{os.sep}view' + request_data.split(' ')[1]
        response = ''

        try:
            with open(path, 'rb') as file:
                response = file.read()

            return headers + response

        except FileNotFoundError:
            # тут эмулируем ошибку 404, если по запросу нужный шаблон страницы не найден
            error_page = ''
            error_page_path = self.script_path + f'{os.sep}view{os.sep}404.html'

            with open(error_page_path, 'rb') as file:
                error_page = file.read()
            
            return headers_404 + error_page
            

    def start_server(self):
        try:
            # устанавливаем подключение сервера и через listen ограничиваем количество подключений до 5
            server = socket.create_server((self.ip, self.port))
            server.listen(5)
            print('server working!')

            while True:
                # получаем клиентский сокет и адрес
                client_socket, addres = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                print(f'customer at the address {addres} joined to server')

                # устанавливаем заголовок и отправляем ответ пользователю
                content = self.answer_server(self, data)
                client_socket.send(content)
                # закрываем соединение
                client_socket.shutdown(socket.SHUT_WR)
        
        # через сочетание клавиш Ctrl+c кладем сервер, если нужно 
        except KeyboardInterrupt:
            server.close()
            print('server shutdown')


if __name__ == '__main__':
    castom_server = CastomServer('127.0.0.1', 2000)
    castom_server.start_server()
