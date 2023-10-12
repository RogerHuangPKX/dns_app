from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

def query_as_for_ip(hostname):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msg = f"TYPE=A\nNAME={hostname}\n"
        s.sendto(msg.encode(), ('127.0.0.1', 53533))
        data, _ = s.recvfrom(1024)
        return data.decode().split("VALUE=")[1].split(" ")[0]

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    
    if not all([hostname, fs_port, number]):
        return jsonify({'error': 'Missing parameters'}), 400

    ip = query_as_for_ip(hostname)

    fs_response = requests.get(f'http://{ip}:{fs_port}/fibonacci', params={'number': number})

    if fs_response.status_code == 200:
        return fs_response.json(), 200
    else:
        return jsonify({'error': 'FS server error'}), 500

if __name__ == '__main__':
    app.run(port=8080)
