from flask import Flask, jsonify, request

app = Flask(__name__)

# Route for adding two numbers
@app.route('/add', methods=['GET'])
def add():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        return jsonify({'result': a + b})
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide integers'}), 400

# Route for subtracting two numbers
@app.route('/subtract', methods=['GET'])
def subtract():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        return jsonify({'result': a - b})
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide integers'}), 400

# Route for multiplying two numbers
@app.route('/multiply', methods=['GET'])
def multiply():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        return jsonify({'result': a * b})
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide integers'}), 400

# Route for dividing two numbers
@app.route('/divide', methods=['GET'])
def divide():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 1))  # Default b to 1 to avoid ZeroDivisionError
        if b == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400
        return jsonify({'result': a / b})
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide integers'}), 400

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == "__main__":
    app.run(debug=True)
