from flask import Flask, jsonify


# instantiate the app
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# set config
app.config.from_object('project.config.DevelopmentConfig')


@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
    })
