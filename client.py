import socket, threading

def send(uname):
    cli_sock.send(uname)
    while True:
        msg = raw_input('\nMe > ')
        data = uname + '> ' + msg
        cli_sock.send(data)

def receive():
    while True:
        data = cli_sock.recv(1024)
        data = data.split('\t')
        data = ''.join(data)
        data = data.split('\n')
        data = ' '.join(data)
        if '{' in data:
            data = data.split('\n')
            data = ''.join(data)
            data = data.replace('online{', 'online\n\t\t\t\t{')
            print ('\t\t\t\t' + data)
        else:
            print ('\t' + data)

if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    uname = raw_input('Enter your name to enter the chat > ')

    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...\n\nEnter \'exit\' to quit the app...\nEnter \'online\' to get a list of online members ')
    
    thread_send = threading.Thread(target = send,args=[uname])
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()