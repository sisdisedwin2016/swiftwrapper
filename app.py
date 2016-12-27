#!flask/bin/python
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

#Bucket Operation

@app.route('/swift/bucket/list', methods=['GET'])
def swift_bucket_list():
	output = subprocess.Popen(["python", "swiftapp.py", "bucket", "list"], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/bucket/create/<string:bucketname>')
def swift_bucket_create(bucketname):
	output = subprocess.Popen(["python", "swiftapp.py", "bucket", "create", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/bucket/delete/<string:bucketname>')
def swift_bucket_delete(bucketname):
	output = subprocess.Popen(["python", "swiftapp.py", "bucket", "delete", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/bucket/content/<string:bucketname>')
def swift_bucket_content(bucketname):
	output = subprocess.Popen(["python", "swiftapp.py", "bucket", "content", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output	


#Object Operation

@app.route('/swift/object/create/<string:bucketname>/<string:objectname>/<string:objectcontent>')
def swift_object_create(bucketname, objectname, objectcontent):
	output = subprocess.Popen(["python", "swiftapp.py", "object", "create", bucketname, objectname, objectcontent], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/object/acl/<string:bucketname>/<string:objectname>/<string:permission>')
def swift_object_acl(bucketname, objectname, permission):
	output = subprocess.Popen(["python", "swiftapp.py", "object", "acl", bucketname, objectname, permission], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/object/delete/<string:bucketname>/<string:objectname>')
def swift_object_delete(bucketname, objectname):
	output = subprocess.Popen(["python", "swiftapp.py", "object", "delete", bucketname, objectname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/swift/object/download/<string:bucketname>/<string:objectname>')
def swift_object_download(bucketname, objectname):
	output = subprocess.Popen(["python", "swiftapp.py", "object", "download", bucketname, objectname], stdout=subprocess.PIPE).communicate()[0]
	return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
