from flask import Flask, request, jsonify
from loguru import logger

app = Flask(__name__)

@app.route('/', methods=['POST'])
def udp_message_handler():
    data = request.get_json()
    source_ip = data.get('source_ip')
    udp_message = data.get('udp_message')

    # Process the UDP message here
    # ...
    logger.debug(data)

    # Send a response (optional)
    response = {
        'status': 'success',
        'message': 'UDP message received and processed successfully'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
