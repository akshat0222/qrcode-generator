from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
# Enable CORS for the frontend running on a different port/domain (e.g., serving index.html directly)
CORS(app) 

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    try:
        # 1. Get the data (link) from the POST request
        data = request.json.get('data')
        if not data:
            return jsonify({"error": "No 'data' field provided"}), 400

        # 2. Generate the QR Code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image instance
        img = qr.make_image(fill_color="black", back_color="white")

        # 3. Save the image to an in-memory byte buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        # 4. Encode the byte buffer to a Base64 string
        # This allows the image to be easily embedded directly into the HTML <img> tag
        base64_encoded_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 5. Return the Base64 string in a JSON response
        return jsonify({
            "qr_code": base64_encoded_img,
            "data_encoded": data
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Run the Flask app on port 8000
    app.run(port=8000, debug=True)
