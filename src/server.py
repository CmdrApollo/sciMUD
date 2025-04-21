import sys
import socket
import selectors
import types

from game import Game

sel = selectors.DefaultSelector()

games = {}

def accept_wrapper(sock):
    conn, addr = sock.accept()
    
    print(f"Accepted connection from {addr}")
    
    conn.setblocking(False)
    
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)
    
    games.update({ addr: Game() })

def service_connection(key, mask) -> None:
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)

        if recv_data:
            text = recv_data.decode('utf-8')
            
            name = sock.getpeername()
            
            if name in games:
                current_game = games[name]

                current_game.parse(text)
                output = current_game.update()
            else:
                output = "An error occured with the server."
            
            out_data = output.encode('utf-8')
            sent = sock.send(out_data)
            data.outb = data.outb[sent:]
        else:
            try:
                games.pop(sock.getpeername())
            except KeyError:
                # this shouldn't happen but whatever
                pass

            print(f"Closing connection to {data.addr}.")
            sel.unregister(sock)
            sock.close()

# user must pass in host and port through the terminal
# when running the program (127.0.0.1, 65432) is what
# i have been using
host, port = sys.argv[1], int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen()

sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, shutting down server.")
finally:
    sel.close()