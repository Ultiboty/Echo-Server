from socket import *
import threading, time, select, random, string
QUIT = False  # static var for every thread to know when server is shutting down
First = True

def get_open_port():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def start_server(addr):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(addr)
    server.listen(2)
    return server


def broadcast_server_info(info):
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while not QUIT:
        udp_socket.sendto(bytes(info, 'utf-8'), ('255.255.255.255', 50008))
        time.sleep(1)
    udp_socket.close()


def shut_down(writable,s):
    print('\nEXIT COMMAND, SHUTTING DOWN SERVER, COMMAND FROM:', s.getpeername())
    for sock in writable:
        sock.send('SERVER SHUTTING DOWN'.encode('utf-8'))
    global QUIT
    QUIT = True


def main():
    start_time = time.time()
    missions = ('go for a short walk around the neighborhood', 'go drink a glass of water, and after u drink it fill another glass to be by your side',
                'posture check, sit correctly and straighten your back',
                'do a phone call to someone u have not talked to in some time (friend / grandparents / family member / etc.)',
                'pick a book from your home that u did not read and read 10-15 pages', 'clean your room','open a random wikipedia page and read about it link: https://wikiroulette.co/',
                'learn how to cook something healthy link: https://www.bbcgoodfood.com/recipes/collection/quick-and-healthy-recipes',
                'Do a random act of kindness, can be for a family member, a friend, or even a complete stranger :)',
                'go out with your friends (basketball, movie, etc.)')
    exit_password = ''.join([random.choice(string.ascii_letters) for i in range(10)])
    port = get_open_port()
    ip = '192.168.0.106'
    addr = (ip, port)
    server = start_server(addr)
    broadcast_thread = threading.Thread(target=broadcast_server_info, args=(ip+str(port),))
    broadcast_thread.start()
    inputs = [server]  # list of connections we receive messages/requests from
    outputs = []  # list of the messages we are sending
    print('starting server on:', server.getsockname())
    global QUIT
    while not QUIT:
        readable, writable, exceptional = select.select(
            inputs, outputs, [])
        for sock in readable:
            if sock is server:
                connection, client_address = sock.accept()
                print("starting session from:", client_address)
                inputs.append(connection)
                outputs.append(connection)
            else:
                try:
                    data = sock.recv(1024).decode('utf-8')
                    if not data or data == 'exit':
                        print(sock.getpeername(), 'is exiting the session')
                        sock.send('exiting the session'.encode('utf-8'))
                        inputs.remove(sock)
                        outputs.remove(sock)
                        sock.close()
                    elif data == 'quit-'+exit_password:
                        shut_down(writable, sock)
                        break
                    elif sock in writable:
                        if data == 'time':
                            sock.send(time.strftime('%H:%M:%S').encode('utf-8'))
                        elif data == 'mission':
                            sock.send((missions[random.randint(0, 9)]).encode('utf-8'))
                        elif data == 'people':
                            sock.send(str(len(inputs)-1).encode('utf-8'))
                        elif data == 'run time':
                            sock.send(str(time.time()-start_time).encode('utf-8'))
                        else:
                            global First
                            if First:
                                reply = 'Echo: '+data + (', THE ADMIN PASSWORD IS: ' + exit_password)
                                First = False
                            else:
                                reply = 'Echo: ' + data
                            sock.send(reply.encode('utf-8'))
                        print('received:', data, 'from:', sock.getpeername())
                except:
                    print(sock.getpeername(), 'is exiting the session')
                    inputs.remove(sock)
                    outputs.remove(sock)
                    sock.close()
        for sock in exceptional:
            print(sock.getpeername(), 'is exiting the session')
            inputs.remove(sock)
            outputs.remove(sock)
            sock.close()
    server.close()


if __name__ == '__main__':
    main()
