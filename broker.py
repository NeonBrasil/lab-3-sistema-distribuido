import zmq
import time

context = zmq.Context()
poller = zmq.Poller()

client_socket = context.socket(zmq.ROUTER)
client_socket.bind("tcp://*:5555")
poller.register(client_socket, zmq.POLLIN)
client_count = 0

server_socket = context.socket(zmq.DEALER)
server_socket.bind("tcp://*:5556")
poller.register(server_socket, zmq.POLLIN)
server_count = 0

# Socket para receber heartbeats
heartbeat_socket = context.socket(zmq.PULL)
heartbeat_socket.bind("tcp://*:5557")
poller.register(heartbeat_socket, zmq.POLLIN)

last_heartbeat = time.time()
heartbeat_timeout = 10  # Timeout de 10 segundos para heartbeats

while True:
    socks = dict(poller.poll())

    if socks.get(client_socket) == zmq.POLLIN:
        client_count += 1
        message = client_socket.recv()
        more = client_socket.getsockopt(zmq.RCVMORE)
        if more:
            server_socket.send(message, zmq.SNDMORE)
        else:
            server_socket.send(message)
        print(f"Client messages: {client_count}")

    if socks.get(server_socket) == zmq.POLLIN:
        server_count += 1
        message = server_socket.recv()
        more = server_socket.getsockopt(zmq.RCVMORE)
        if more:
            client_socket.send(message, zmq.SNDMORE)
        else:
            client_socket.send(message)
        print(f"Server messages: {server_count}")

    if socks.get(heartbeat_socket) == zmq.POLLIN:
        heartbeat = heartbeat_socket.recv()
        if heartbeat == b"HEARTBEAT":
            last_heartbeat = time.time()
            print("Received heartbeat from server")

    # Verificar se o heartbeat foi recebido dentro do timeout
    if time.time() - last_heartbeat > heartbeat_timeout:
        print("Server heartbeat timeout")
        # Aqui você pode adicionar lógica para lidar com a falha do servidor
