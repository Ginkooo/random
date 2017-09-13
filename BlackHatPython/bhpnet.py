#!/usr/bin/env python3

import sys
import socket
import subprocess
from threading import Thread
from io import BufferedReader
from functools import namedtuple
from argparse import ArgumentParser


args = None


def parse_args() -> object:
    """
    parses command line params

    :return: object containing command line parameters
    :rtype: object
    """
    ap = ArgumentParser(description='Simple netcat-like program')
    ap.add_argument('-t', dest='host', required=True,
                    help='target host name or ip', type=str)
    ap.add_argument('-p', dest='port', required=True,
                    help='target port number', type=int)
    ap.add_argument('-l', '--listen', action='store_true', dest='listen',
                    help='listens for incomming connections on [host]:[port]')
    ap.add_argument('-e', '--execute', dest='execute_file_path',
                    help='executes file, when it is recieved')
    ap.add_argument('-c', '--command', action='store_true', dest='command',
                    help='initialize command line')
    ap.add_argument('-u', '--upload', dest='upload_file_path',
                    help='sends file and saves it in [destination]')
    return ap.parse_args()


def run_server_loop(target: object) -> None:
    """
    listens for connections on port and interface of the target

    :param target: object containing port and host properties
    :type target: object

    :rtype: None
    """
    client = socket.socket()
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind((target.host, target.port))
    client.listen()
    conn, addr = client.accept()
    thread = Thread(target=server_input_handler, args=(conn, args.command))
    thread.start()
    while True:
            msg = input().encode()
            print(msg, end='')


def execute_command(data: str) -> None:
    data = data.strip()
    try:
        result = subprocess.check_output(data, shell=True)
    except Exception as err:
        result = str(err).encode() + b'\n'
    return result


def server_input_handler(client: socket.socket, execute: bool=False):
    while True:
        try:
            data = client.recv(4096).decode()
            if execute:
                data = execute_command(data)
                client.sendall(data)
            print(data, end='')
        except Exception as err:
            pass


def run_client_loop(target: object) -> None:
    client = socket.socket()
    client.connect((target.host, target.port))
    thread = Thread(target=server_input_handler, args=(client,))
    thread.start()
    while True:
        try:
            msg = input().encode() + b'\n'
            client.sendall(msg)
        except:
            client.close()
            exit(1)


def main():
    global args
    args = parse_args()

    client_condition = not args.listen and args.port > 0
    listen_condition = args.listen and args.port > 0

    target = namedtuple('target', ('host', 'port'))
    target.host = args.host
    target.port = args.port

    if client_condition:
        print('Clienting')
        run_client_loop(target)
    elif listen_condition:
        print('Listening')
        run_server_loop(target)


if __name__ == '__main__':
    main()
