from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    target = data.get("target")

    if not target:
        return jsonify({"error": "No IP or domain entered"}), 400

    try:
        result = subprocess.check_output(
            ["nmap", "-sT", "-Pn", target], stderr=subprocess.STDOUT
        )
        output = result.decode()
        return jsonify({"output": output})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

