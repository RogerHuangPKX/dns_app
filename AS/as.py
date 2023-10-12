import socket

AS_DATABASE = {}

UDP_IP = "0.0.0.0"
UDP_PORT = 53533

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    data_str = data.decode()

    if "VALUE=" in data_str:
        parts = data_str.split("\n")
        name = parts[1].split("=")[1]
        value = parts[2].split("=")[1]
        AS_DATABASE[name] = value
    else:
        name = data_str.split("\n")[1].split("=")[1]
        ip = AS_DATABASE.get(name, None)
        if ip:
            response = f"TYPE=A\nNAME={name}\nVALUE={ip}\nTTL=10\n"
            sock.sendto(response.encode(), addr)
