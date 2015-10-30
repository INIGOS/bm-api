from flask import Flask, request
import flask
import json
import collections
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
app = Flask(__name__)
connection = MongoClient('188.40.79.87', 27017)
db = connection['brightminds']
def toJson(data):
    return json.dumps(data, default=json_util.default,sort_keys=True,
                  indent=4, separators=(',', ': '))

def getResults(job_title):
	if (job_title=="job_title"):
		result_format = {
				"search":{
				"timed_out":"false",
				"response":{
								"status":"ok",
								"data":{								
											"keyword":"job_title"											
								}
				}
				}
			}


		json_results = []
		
		results = db['jobposts_rawdata_job'].distinct("keyword_fetched")
		
		for result in results:
			print result
			result = result.replace("+"," ")
			json_results.append(result)
			
			
		
		result_format['search']['response']['data']['jobs'] = json_results
		print result_format
		
		return result_format
		
	else:
		error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"found":"0"
								
				}
				}
			}



		return error_format
def geturl(url_name):
	print "url"
	temp=[]
	out=[]

	if request.args.get('source'):
		loc=request.args.get('source')
		print loc
		temp.append(loc)
		print temp[0]
		results=db['videoposts_rawdata'].find({'source':temp[0]})
		count=results.count()
		print count
	else:
		results=db['videoposts_rawdata'].find({})
	count=results.count()
	print count

	for result in results:
		check=collections.OrderedDict()
		check["VIDEO-TITLE"]=result["video_title"]
		check["URL:"] = result["video_url"]
		
		out.append(check)

	result_format = {
				"search":{
				"timed_out":"false",
				"response":{
								"status":"ok",

								"data":{								
											"keyword":"job_title"

								}
								
				}
				}
			}
	result_format['search']['response']['data']['jobs'] = out
	result_format['search']['count']=count
	return result_format

def getKeywords(keyss):
	print "starts here"
	print keyss
	l=[]
	out=[]
	l.append(keyss)
	results=db['temp_skills_extracted'].find({"job":l[0]})
	for result in results:
		check=collections.OrderedDict()
		check["KEYWORDS"]=result["skills"]
		out.append(check)
	result_format = {
				"search":{
				"timed_out":"false",
				"response":{
								"status":"ok",

								"data":{								
											
								}
								
				}
				}
			}
	result_format['search']['response']['data']['jobs'] = out
	return result_format
def getJobs(job_name):
	print "in get jobs"
	print job_name
	i=job_name.split(" AND ")
	#job_name=job_name.split(" AND ")
	#print job_name[0]
	#job_name=job_name.replace("AND","&")
	j1=[dict([x.split('=')]) for x in job_name.split(' AND ')[1:]]
	print j1
	off = int(request.args.get('offset',0))
	src=str(request.args.get('source',0))
	loc=str(request.args.get('location',0))
	comp=str(request.args.get('company',0))
	temp=[{"keyword_fetched":i[0]}]
	temp.extend(j1)
	print temp

	"""if request.args.get('job_name'):
		job=request.args.get('job_name')
		temp_j={"keyword_fetched":job_name}
		temp.append(temp_j)"""
	if request.args.get('location'):
		loc=request.args.get('location')
		temp_l={"job_location":loc}
		temp.append(temp_l)
	if request.args.get('source'):
		src=request.args.get('source')
		temp_s={"source":src}
		temp.append(temp_s)
	if request.args.get('company'):
		comp=request.args.get('company')
		temp_c={"company_name":comp}
		temp.append(temp_c)
	if request.args.get('date'):
		date=request.args.get('date')
		temp_d={"published_date":date}
		temp.append(temp_d)

	#results = db['jobposts_rawdata_job'].find({"$and":[{"keyword_fetched":job_name},{"source":"indeed.com"},{"job_location":"Boston, MA"}]}).limit(10).skip(off)
	#temp=[{"keyword_fetched":job_name},{"source":"indeed.com"},{"job_location":"Boston, MA"}]
	results = db['jobposts_rawdata_job'].find({"$and":temp}).limit(10).skip(off)
	count=db['jobposts_rawdata_job'].find({"keyword_fetched":job_name}).count()
	print count
	new_results = []
	
	out=[]
	
	for result in results:
		#check={}
		check=collections.OrderedDict()
		check["JOB-TITLE : "] = result["job_title"]
		check ["COMPANY : "] = result["company_name"]
		check ["LOCATION : "] = result["job_location"]
		check ["JOB-DESCRIPTION : "] = result["job_description"]
		check["POSTED-DATE : "]=result["published_date"]
		check["URL : "]=result["job_url"]
		check["SOURCE : "]=result["source"]

		#print check
		#print "BEFORE*****************"
		print out
		out.append(check)
		#print "AFTER******************"
		#print out

	result_format = {
				"search":{
				"timed_out":"false",
				"response":{
								"status":"ok",

								"data":{								
											"keyword":"job_title"

								}
								
				}
				}
			}



			
		
	#result_format['search']['response']['data']['jobs'] = new_results
	result_format['search']['response']['data']['jobs'] = out
	result_format['search']['count']=count
	#print result_format
	return result_format
	#return out


@app.route('/v1/keywords/search', methods=['GET'])
def name():
    name = request.args.get("q")
    print name
    
    res = getResults(name)

    return flask.jsonify(**res)

@app.route('/v1/keywords/search/job', methods=['GET'])
def names():
    names = request.args.get("q")
    print names    
    ress = getJobs(names)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**ress)

@app.route('/v1/keywords/search/url', methods=['GET'])
def namess():
    namess = request.args.get("q")
    print namess    
    resss = geturl(namess)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**resss)

@app.route('/v1/keywords/search/key', methods=['GET'])
def namesss():
    namesss = request.args.get("q")
    print namesss    
    ressss = getKeywords(namesss)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**ressss)
    
    


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

#http://localhost:5000/v1/keywords/search?q=job_title

