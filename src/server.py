import sys
import socket
import selectors
import types

from world import World
from player import Player
import config

sel = selectors.DefaultSelector()

world = World()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    
    print(f"Accepted connection from {addr}")
    
    conn.setblocking(False)
    
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
    world.players.update({ addr: Player(world) })

def service_connection(key, mask) -> None:
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)

        if recv_data:
            text = recv_data.decode('utf-8')
            
            name = sock.getpeername()
            
            if name in world.players:
                current_player = world.players[name]

                output = current_player.parse(text)
            else:
                output = "An error occured with the server."
            
            out_data = output.encode('utf-8')
            sent = sock.send(out_data)
            data.outb = data.outb[sent:]
        else:
            try:
                world.players.pop(sock.getpeername())
            except KeyError:
                # this shouldn't happen but whatever
                pass

            print(f"Closing connection to {data.addr}.")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        try:
            name = sock.getpeername()
            
            if name in world.players:
                current_player = world.players[name]

                output = current_player.prompt()
            else:
                output = "An error occured with the server."
                
            out_data = output.encode('utf-8')
            sent = sock.send(out_data)
            data.outb = data.outb[sent:]
        except OSError:
            pass

host = config.host
port = config.port

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