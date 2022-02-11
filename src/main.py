import socket
import json
from _thread import *
import threading

users = []

def sendMessageToAllUsers(message):
  for user in users:
    try:
      # user.send(message.encode())
      user.send((message + "\n").encode())
      print("Message sent to", user)
    except: 
      users.remove(user)

# returns boolean
def handleMessage(response):
  if ('receiver' in response):
    print("Receiver in ")
    if (response['receiver']):
      print("Receiver")
      return True

  if (not ('message' in response)):
    message = "Bem vindo(a), " + response['username']
    print(message)
    responseToUsers = {
      "message": "welcome",
      "username": response['username']
    }
    sendMessageToAllUsers(json.dumps(responseToUsers))
    return True
  else:
    if (response['message'] != 'quit'):
      message = response['username'] + ": " + response['message']
      print(message)
      sendMessageToAllUsers(json.dumps(response))
      return True
    else:
      message = response['username'] + " saiu!"
      print(message)
      responseToUsers = {
        "message": "quit",
        "username": response['username']
      }
      sendMessageToAllUsers(json.dumps(responseToUsers))
      return False

def threaded(connection):
  while True:
    data = connection.makefile().readline()
    dataWithoutLineBreak = data.replace('\n', '')
    response = json.loads(dataWithoutLineBreak)
    print(response)
    response = json.loads(data.rstrip())
    if (not handleMessage(response)):
      break
    data = data[::-1]
    # print("send data")
    # connection.send(data)
    # print("after send data")
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
    users.append(serverInput)
    print(users)
    start_new_thread(threaded, (serverInput,))
  serverSocket.close()

if __name__ == '__main__':
  main()