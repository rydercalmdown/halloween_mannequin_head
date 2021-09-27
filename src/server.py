"""Components for running the raspberry pi in server mode"""

import os
from flask import Flask, jsonify, request
from servo_controller import ServoController


app = Flask(__name__)
sc = ServoController()


@app.route('/')
def index():
    """API index route"""
    return jsonify({'status': 'ok'})


@app.route('/servo/')
def alarm():
    """Turn on the relay"""
    percentage = request.args.get('p')
    if not percentage:
        return jsonify({'status': 'no p'})
    sc.set_servo_percent(float(percentage))
    return jsonify({'status': 'p={}'.format(percentage)})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
