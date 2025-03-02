from flask import Flask, request, jsonify

app = Flask(__name__)

# Store valid licenses (Should be stored in a database in production)
VALID_LICENSES = {
    "USER-1234-5678-ABCD": None,
    "USER-9876-5432-WXYZ": None
}

@app.route("/")
def home():
    return "License Server is Running! Use /activate to activate a license."

@app.route("/activate", methods=["POST"])
def activate_license():
    data = request.json
    license_key = data.get("license_key")
    mac_address = data.get("mac_address")

    if license_key not in VALID_LICENSES:
        return jsonify({"status": "error", "message": "Invalid License Key"}), 400

    if VALID_LICENSES[license_key] and VALID_LICENSES[license_key] != mac_address:
        return jsonify({"status": "error", "message": "License already activated on another machine"}), 403

    VALID_LICENSES[license_key] = mac_address
    return jsonify({"status": "success", "message": "License Activated"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
