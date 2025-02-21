import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
heartbeat_socket = context.socket(zmq.PUSH)

socket.connect("tcp://localhost:5556") # conecta no broker local
heartbeat_socket.connect("tcp://localhost:5557") # conecta no broker local
msg_count = 0
heart_count = 0
heartbeat_interval = 5
last_heartbeat = time.time()

while True:
    # Enviar heartbeat se o intervalo tiver passado
    if time.time() - last_heartbeat > heartbeat_interval:
        heartbeat_socket.send(b"HEARTBEAT")
        heart_count += 1
        last_heartbeat = time.time()
        print(f"Heartbeats enviados: {heart_count}")

    print(f"Mensagem {msg_count}:", end=" ")
    try:
        message = socket.recv(zmq.NOBLOCK)  # Esta chamada não é bloqueante
        socket.send_string("World")
        print(f"{message}")
        msg_count += 1
    except zmq.Again as e:
        # No message received, continue
        pass
    time.sleep(1)  # Aguarde um segundo antes de tentar novamente