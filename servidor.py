import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5556") # conecta no broker local
msg_count = 0

while True:
    print(f"Mensagem {msg_count}:", end=" ")
    message = socket.recv()
    socket.send_string("World")
    print(f"{message}")
    msg_count += 1
