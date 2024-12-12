from flask import Flask, request, jsonify, send_file
from rembg import remove
from io import BytesIO
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Route to handle background removal
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Check if a file is included in the request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided."}), 400

        # Get the uploaded file
        image_file = request.files['image']

        # Read the image and process it
        input_image = image_file.read()
        output_image = remove(input_image)

        # Save the output image to a BytesIO object
        output_buffer = BytesIO()
        output_buffer.write(output_image)
        output_buffer.seek(0)

        # Send the processed image back to the client
        return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='output.png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app on localhost, port 5000
    app.run(debug=True)
