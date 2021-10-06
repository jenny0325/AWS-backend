import boto3
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import os

application = Flask(__name__)

# cors
cors = CORS(application, resources={r"/*": {"origins": "*"}})


@application.route('/')
def main():
    return "핵심 쏙쏙 AWS"


@application.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
                      )
    s3.put_object(
        ACL="public-read",
        Bucket=os.environ["BUCKET_NAME"],
        Body=file,
        Key=file.filename,
        ContentType=file.content_type
    )

    return jsonify({'result': 'success'})


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    application.debug = True
    application.run()
