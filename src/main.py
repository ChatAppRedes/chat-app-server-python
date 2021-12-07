import socket
import json

address = ("localhost", 3335)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(address)
serverSocket.listen(1)
serverInput, address = serverSocket.accept()
print("Nova conexão: ", address)

while True:
  response = serverInput.recv(1024)
  response = json.loads(response.rstrip())
  if (not ('message' in response)):
    print("Bem vindo(a), ", response['username'])
  else:
    if (response['message'] != 'desconectar'):
      print("Mensagem do cliente: ", response)
    else:
      serverSocket.close()
      break