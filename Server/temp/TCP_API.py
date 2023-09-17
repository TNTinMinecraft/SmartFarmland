from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "There is API!!!!!!!!!!!"

@app.route('/api')
def api_endpoint():
    api_id_out = request.args.get('id_out')
    api_set = request.args.get('set')
    return f'id_out: {api_id_out}, set: {api_set}'

if __name__ == '__main__':
    app.run(debug=True)
