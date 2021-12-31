from flask_restful import Resource

class PingPong(Resource):
    def get(self):
        return {'ping' : 'pong'}, 200
