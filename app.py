from flask import Flask, request, jsonify

app = Flask(__name__)
codes = {}

@app.route('/submit', methods=['POST'])
def submit_code():
    data = request.json
    codes[data['userId']] = data['code']
    return jsonify({'success': True})

@app.route('/verify', methods=['POST'])
def verify_code():
    data = request.json
    code = data['code']

    if code in codes.values():
        return jsonify({'success': True})
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
