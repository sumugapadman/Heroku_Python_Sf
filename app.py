import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from simple_salesforce import Salesforce

app = Flask(__name__)
api = Api(app)

#Initialize a connection with Salesforce
sf = Salesforce(username=os.environ.get('SALESFORCE_USERNAME'), password=os.environ.get('SALESFORCE_PASSWORD'), security_token=os.environ.get('SALESFORCE_TOKEN'))

class Account(Resource):
    # Tell the api what are required fields to get a meaniful error while insert
    parser = reqparse.RequestParser()
    parser.add_argument('Ownerid',required=True, help="Ownerid is a required Field")

    def get(self, name):
        results = sf.query("SELECT Id, Name FROM Account WHERE Name LIKE '%"+name+"%'")
        return results, 201

    def post(self, name):
        data = Account.parser.parse_args()
        response = sf.Account.create({'Ownerid':data['Ownerid'],'Name':name})
        return response, 201

#http://herokuapp.cmm/account/Burlington_texttilles
api.add_resource(Account, '/account/<string:name>')

if __name__ == '__main__':
    app.run(debug = True, port=5000)
