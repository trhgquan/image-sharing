from flask import request

class Utils:
    @staticmethod
    def get_input(input_name):
        input_val = request.args.get(input_name)

        if input_val == None or len(input_val) == 0:
            raise Exception('Missing ' + input_name)
        else:
            return input_val
