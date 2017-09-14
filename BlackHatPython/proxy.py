#!/usr/bin/env python3

# ========================================================
# Program listening for packets on local host and port,  |
# frowarding them to remote                              |
# ========================================================

import socket
from argparse import ArgumentParser
from threading import Thread
from queue import Queue
from functools import namedtuple


def parse_args() -> object:
    ap = ArgumentParser()

    local = ap.add_argument_group('local')
    local.add_argument('local_host')
    local.add_argument('local_port', type=int)

    remote = ap.add_argument_group('remote')
    remote.add_argument('remote_host')
    remote.add_argument('remote_port', type=int)

    return ap.parse_args()


def listen_and_save(conn: socket.socket, queue: Queue):
    while True:
        data = b''
        while True:
            recieved = conn.recv(4096)
            data += recieved
            if len(recieved) < 4096:
                break
        queue.put(data)


def listen_for_packets(target: object, queue: Queue) -> None:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((target.host, target.port))
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = Thread(target=listen_and_save,
                        args=(conn, queue))
        thread.start()


def send_packets(target: object, queue: Queue):
    s = socket.socket()
    s.connect((target.host, target.port))
    while True:
        s.sendall(queue.get())


def main():
    args = parse_args()
    local = namedtuple('local', ('host', 'port'))
    local.host = args.local_host
    local.port = args.local_port

    remote = namedtuple('remote', ('host', 'port'))
    remote.host = args.remote_host
    remote.port = args.remote_port

    queue = Queue()

    listen_thread = Thread(target=listen_for_packets,
                           args=(local, queue))
    listen_thread.start()

    send_packets(target=remote, queue=queue)


if __name__ == '__main__':
    main()
