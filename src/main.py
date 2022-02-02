import socket
import json
from _thread import *
import threading

users = []

def sendMessageToAllUsers(message):
  return
  for user in users:
    print(user)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(user)
    clientSocket.send(message)

# returns boolean
def handleMessage(response):
  if (not ('message' in response)):
    message = "Bem vindo(a), " + response['username']
    print(message)
    sendMessageToAllUsers(message)
    return True
  else:
    if (response['message'] != 'desconectar'):
      message = response['username'] + ": " + response['message']
      print(message)
      sendMessageToAllUsers(message)
      return True
    else:
      message = response['username'] + "saiu!"
      print(message)
      sendMessageToAllUsers(message)
      return False

def threaded(connection):
  while True:
    data = connection.recv(1024)
    response = json.loads(data.rstrip())
    if (not handleMessage(response)):
      break
    data = data[::-1]
    print("send data")
    connection.send(data)
    print("after send data")
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
    users.append(address)
    print(users)
    start_new_thread(threaded, (serverInput,))
  serverSocket.close()

if __name__ == '__main__':
  main()