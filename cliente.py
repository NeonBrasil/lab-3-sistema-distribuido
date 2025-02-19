import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

i = 0
while True:
    print(f"Mensagem {i}:", end=" ")
    socket.send(b"Hello")
    mensagem = socket.recv()
    print(f"{mensagem}")
    i += 1

