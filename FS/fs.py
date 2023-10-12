from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def register_with_as(hostname, ip):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
        s.sendto(msg.encode(), ('127.0.0.1', 53533))

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    
    if not all([hostname, ip]):
        return jsonify({'error': 'Missing parameters'}), 400

    register_with_as(hostname, ip)

    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/fibonacci')
def get_fibonacci():
    number = request.args.get('number')
    try:
        number = int(number)
        result = fibonacci(number)
    except ValueError:
        return jsonify({'error': 'Bad format'}), 400
    
    return jsonify({'fibonacci': result}), 200

if __name__ == '__main__':
    app.run(port=9090)

