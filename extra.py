from flask import Flask, request
import flask
import json
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

def getJobs(job_name):
	print "in get jobs"
	print job_name
	results = db['jobposts_rawdata_job'].find({"keyword_fetched":job_name})
	new_results = []
	for result in results:
		#print "Processing result", result['job_title']
		#print "Processing result", result['company_name']
		temp_str = result.get('job_title','N/A') +' - ' + result.get('company_name','N/A')
		new_results.append(temp_str)
		#new_results.append()
		#final=new_results.append(result['job_title']) + new_results.append(result['company_name'])
		#print result["job_title"]
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


		#json_results = []
		
		#results = db['jobposts_rawdata_job'].distinct("keyword_fetched")
		
		#for result in results:
		#	print result
		#	result = result.replace("+"," ")
		#	json_results.append(result)
			
			
		
	result_format['search']['response']['data']['jobs'] = new_results
	#print result_format
	return result_format
	#return final


@app.route('/v1/keywords/search', methods=['GET'])
def name():
    name = request.args.get("q")
    print name
    
    res = getResults(name)
    return flask.jsonify(**res)

@app.route('/v2/keywords/search', methods=['GET'])
def names():
    names = request.args.get("job_title")
    #print names    
    ress = getJobs(names)
    return flask.jsonify(**ress)
    
    


if __name__ == '__main__':
    app.run(debug=True)

#http://localhost:5000/v1/keywords/search?q=job_title