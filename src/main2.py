import socket
import selectors
import types
import json

sel = selectors.DefaultSelector()

address = ("localhost", 3335)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(address)
serverSocket.listen(1)

serverSocket.setblocking(False)
sel.register(serverSocket, selectors.EVENT_READ, data=None)

def acceptWrapper(serverSocket):
  serverInput, address = serverSocket.accept()
  print("Nova conexão: ", address)
  serverInput.setblocking(False)
  data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  sel.register(serverInput, events, data=data)

def serviceConnection(key, mask):
  sock = key.fileobj
  data = key.data
  if mask & selectors.EVENT_READ:
      recvData = sock.recv(1024) 
      print("🔴 recvData: ", recvData)
      response = json.loads(recvData.rstrip())
      print("🔴 response: ", response)
      if (not ('message' in response)):
        print("Bem vindo(a), ", response['username'])
      else:
        if response['message'] != 'desconectar':
          data.outb += recvData
        else:
          print('Conexão de fechamento para', data.addr)
          sel.unregister(sock)
          sock.close()
  if mask & selectors.EVENT_WRITE:
    if data.outb:
      print('echoing', repr(data.outb), 'to', data.addr)
      sent = sock.send(data.outb)
      data.outb = data.outb[sent:]        

while True: 
  events = sel.select(timeout=None)
  for key, mask in events:
    if key.data is None:
      acceptWrapper(key.fileobj)
    else:
      serviceConnection(key, mask)

# while True:
#   response = serverInput.recv(1024)
#   response = json.loads(response.rstrip())
#   if (not ('message' in response)):
#     print("Bem vindo(a), ", response['username'])
#   else:
#     if (response['message'] != 'desconectar'):
#       print("Mensagem do cliente: ", response)
#     else:
#       serverSocket.close()
#       break