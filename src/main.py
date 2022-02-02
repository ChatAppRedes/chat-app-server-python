import socket
import json
from _thread import *
import threading

def threaded(connection):
  while True:
    data = connection.recv(1024)
    response = json.loads(data.rstrip())
    if (not ('message' in response)):
      print("Bem vindo(a), ", response['username'])
    else:
      if (response['message'] != 'desconectar'):
        print(response['username'], ": ", response['message'])
      else:
        print(response['username'], "saiu!")
        break
    data = data[::-1]
    connection.send(data)
  connection.close()

def main():
  address = ("localhost", 3335)
  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.bind(address)
  serverSocket.listen(5)
  while True:
    print("Aguardando novas conexões")
    serverInput, address = serverSocket.accept()
    print("After accept")
    print("Nova conexão: ", address)
    start_new_thread(threaded, (serverInput,))
  serverSocket.close()

if __name__ == '__main__':
  main()