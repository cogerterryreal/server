from flask import Flask, request, jsonify

app = Flask(__name__)

# Store valid licenses
VALID_LICENSES = {
    "USER-1234-5678-ABCD": None,
    "USER-9876-5432-WXYZ": None
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "License Server is Running! Use /activate to activate a license."})

@app.route("/activate", methods=["POST"])  # ✅ Allow only POST requests
def activate_license():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be in JSON format"}), 400

    data = request.get_json()
    license_key = data.get("license_key")
    mac_address = data.get("mac_address")

    if not license_key or not mac_address:
        return jsonify({"status": "error", "message": "Missing required parameters."}), 400

    if license_key not in VALID_LICENSES:
        return jsonify({"status": "error", "message": "Invalid License Key"}), 400

    if VALID_LICENSES[license_key] and VALID_LICENSES[license_key] != mac_address:
        return jsonify({"status": "error", "message": "License already activated on another machine"}), 403

    VALID_LICENSES[license_key] = mac_address
    return jsonify({"status": "success", "message": "License Activated"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
