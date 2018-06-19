import socket, threading, time
from _socket import SHUT_RDWR, SHUT_RD, SHUT_WR


def accept_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        data = cli_sock.recv(1024)
        data = data.split(' ')
        uname = data[0]
        ip = cli_add[0]
        port = str(cli_add[1])
        CONNECTION_LIST_IP_UNAME[cli_sock] = [uname , cli_add[0] , cli_add[1]]
        print('[User: ' + uname + ']\n[IP: ' + ip + ']\n[Port: ' + port + ']\n')
        for client in CONNECTION_LIST_IP_UNAME:
                if client != cli_sock:
                    client.send('[' + uname + '] just got connected')
        thread_client = threading.Thread(target = broadcast_usr, args=[cli_sock])
        thread_client.start()


def broadcast_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
                b_usr(cli_sock, data)
        except Exception as x:
            print(x)
            break


def b_usr(cs_sock, msg):
    exiting = 'false'
    split_msg = msg.split("> ")
    for client in CONNECTION_LIST_IP_UNAME:
        if split_msg[1].lower() == 'exit':
            exiting = 'true'
            if client != cs_sock:
                client.send(str(CONNECTION_LIST_IP_UNAME[cs_sock][0]) + " has left.")
            else:
                client.send('Thank you for using this chatroom. We hope to see you soon.')
                cs_sock.shutdown(SHUT_RD)
        elif split_msg[1].lower() == 'online':
            if len(CONNECTION_LIST_IP_UNAME) == 1:
                cs_sock.send('No one is online right now')
            if client != cs_sock:
                cs_sock.send('\t{' + str(CONNECTION_LIST_IP_UNAME[client][0]) + '} is online')
        else:
            if client != cs_sock:
                client.send(msg)
            
    if exiting == 'true':
        del CONNECTION_LIST_IP_UNAME[cs_sock]


def list_users():
    for client in CONNECTION_LIST_IP_UNAME:
        for current in CONNECTION_LIST_IP_UNAME:
            if(current != client):
                client.send('\t{' + str(CONNECTION_LIST_IP_UNAME[current][0]) + '} is online')


if __name__ == "__main__":    
    CONNECTION_LIST_IP_UNAME = {}

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(3)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()

    while True:
        if len(CONNECTION_LIST_IP_UNAME) > 0:
            time.sleep(30)
            list_users()