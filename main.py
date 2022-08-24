from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    # insert method here
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()  # init

        parser.add_argument('userId', required=True, location='args')
        parser.add_argument('lname', required=True, location='args')
        parser.add_argument('fname', required=True, location='args')
        parser.add_argument('title', required=True, location='args')
        parser.add_argument('location', required=False, location='args')

        args = parser.parse_args()

        new_data = pd.DataFrame({
            'userId': args['userId'],
            'lname': args['lname'],
            'fname': args['fname'],
            'title': args['title'],
            'location': args['location']

        }, index=[0])
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 401
        else:

            new_data = pd.DataFrame({
                'userId': args['userId'],
                'lname': args['lname'],
                'fname': args['fname'],
                'title': args['title'],
                'location': args['location']
            }, index=[0])
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200  # return data with 200 OK
            data = pd.read_csv('users.csv')

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True, location='args')  # add args
        parser.add_argument('title', required=True, location='args')
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['title'] = data['title'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['title'] = user_data['title'].values[0] \
                .append(args['title'])

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True, location='args')  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


api.add_resource(Users, '/users')  # entry point

if __name__ == '__main__':
    app.run()
