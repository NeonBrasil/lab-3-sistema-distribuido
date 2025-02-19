import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555") # conecta no broker local

msg_count = 0
while True:
    print(f"Mensagem {msg_count}:", end=" ")
    socket.send(b"Hello") # envia mensagem (request)
    mensagem = socket.recv() # recebe mensagem (reply)
    print(f"{mensagem}")
    msg_count += 1
