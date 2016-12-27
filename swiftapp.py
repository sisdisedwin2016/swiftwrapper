import sys
import swiftclient
import subprocess

user = 'your-username:swift'
key = 'your-secret-key'

conn = swiftclient.Connection(
        user=user,
        key=key,
        #authurl='https://objects.dreamhost.com/auth',
        authurl='your-gateway-host:7480/auth/1.0',
)


if(len(sys.argv) <3):
	print "error, see the documentation"

elif(len(sys.argv) >= 3 and sys.argv[1] == "bucket"):
	
	operation = sys.argv[2]
	
	#List all bucket
	#Usage: python s3app.py bucket list
	if(operation == "list"):

		container = conn.get_account()[1]
		json = '{"data": ['
		for index in range(0,len(container)):
			if(index == len(container)-1):
				json += '{"name": "' + container[index]['name'] + '"}]}'
			else:
				json += '{"name": "' + container[index]['name'] + '"},'
		print json


	#List a bucket contents
	#Auto create bucket if it's not created
	#Usage: python s3app.py bucket content <bucketname>
	elif (operation == "content"):
		bucketname = sys.argv[3]
		bucket = conn.put_container(bucketname)

		counter = 0
		for key in conn.get_container(bucketname)[1]:
			counter+=1

		json = '{"data": ['
		index  = 0
		for key in conn.get_container(bucketname)[1]:
			index+= 1
			if(index==counter):
				json += '{"name": "' + key['name'] + '", "size": "' + str(key['bytes']) + '", "last_modified": "' + key['last_modified'] + '"}]}'
			else:
				json += '{"name": "' + key['name'] + '", "size": "' + str(key['bytes']) + '", "last_modified": "' + key['last_modified'] + '"},'
		if counter < 1:
			json = '{"data":""}'
		print json

	#Create new bucket
	#Usage: python s3app.py bucket create <bucketname>
	elif (operation == "create"):
		bucketname = sys.argv[3]
		conn.put_container(bucketname)
		json = '{ "data": "success creating bucket: ' + bucketname + '"}' 
		print json

	#Delete a bucket
	#Usage: python s3app.py bucket delete <bucketname>
	elif (operation == "delete"):
		bucketname = sys.argv[3]
		conn.delete_container(bucketname)
		json = '{ "data": "success deleting bucket: ' + bucketname + '"}' 
		print json

elif(len(sys.argv) >= 3 and sys.argv[1] == "object"):
	
	operation = sys.argv[2]

	#Create a new object
	#The content of the object is optional, available in 4th argument if exists
	#Usage: python s3app.py object create <bucketname> <objectname> <objectcontent>
	if(operation == "create"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]
		objectcontent = sys.argv[5]

		bucket = conn.put_container(bucketname)

		subprocess.Popen(["touch", objectname], stdout=subprocess.PIPE).communicate()[0]
		with open(objectname, 'r') as hello_file:
			conn.put_object(bucketname, objectname,
											contents= objectcontent,
											content_type='text/plain')
		subprocess.Popen(["rm", objectname], stdout=subprocess.PIPE).communicate()[0]		
		json = '{ "data": "success creating bucket: ' + objectname + '"}' 
		print json

	#Change an object's ACL
	#Public or Private are set on the 3th argument, default is public
	#Usage: python s3app.py object acl <bucketname> <objectname> <permission>
	elif(operation == "acl"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]
		permission = sys.argv[5]

		bucket = conn.create_bucket(bucketname)
		if(permission == "private"):
			plans_key = bucket.get_key(objectname)
			plans_key.set_canned_acl('private')
			json = '{ "data": "' + objectname + '" permission is set to private}' 
			print json
		else:
			plans_key = bucket.get_key(objectname)
			plans_key.set_canned_acl('public-read')
			json = '{ "data": "' + objectname + '" permission is set to public}' 
			print json

	#Delete an object
	#Usage: python s3app.py object delete <bucketname> <objectname>
	elif(operation == "delete"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]

		# bucket = conn.create_bucket(bucketname)
		# bucket.delete_key(objectname)
		conn.delete_object(bucketname, objectname)
		json = '{ "data": "success deleting object: ' + objectname + '"}' 
		print json

	#Create a downloadable link
	#Usage: python s3app.py object download <bucketname> <objectname>
	elif(operation == "download"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]

		# bucket = conn.create_bucket(bucketname)
		# hello_key = bucket.get_key(objectname)
		# hello_url = hello_key.generate_url(3600, query_auth=False, force_http=False)

		obj_tuple = conn.get_object(bucketname, objectname)
		with open(objectname, 'w') as my_hello:
			my_hello.write(obj_tuple[1])

		#Move file to accessible path
		path = "/var/www/html/file/" + objectname
		download_path = "http://rahman.sisdis.ui.ac.id/file/" + objectname
		subprocess.Popen(["mv", objectname, path], stdout=subprocess.PIPE).communicate()[0]

		json = '{ "data": "' + download_path + '"}' 
		print json

else:
	print "Bad request"



			




			
