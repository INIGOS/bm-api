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
db1 = connection['bmprod']
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
		out=[]
		
		#results = db['jobposts_rawdata_job'].distinct("keyword_fetched")
		#results = db['jobposts_rawdata_job'].find({})
		results = db1['jobposts_rawdata'].find({})


		for result in results:
			check=collections.OrderedDict()
			check["JOB-ID"] = result["job_id"]
			check["JOB-TITLE"] = result["keyword"]
			lo_count=db1['extracted_videos_new'].find({"job_id":result["job_id"]}).count()
			check["LO-COUNT"]=lo_count
			#print check
			if check not in out:
				out.append(check)
				print out
			else:
				json_results.append(check)
			#print result
			#result = result.replace("+"," ")
			#json_results.append(result)
			#out.append(check)
			
		
		result_format['search']['response']['data']['jobs'] = out
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

def getskills(loids):
	out=[]
	results=db1['extracted_videos_new'].find({"learning_object_id":loids})
	print "gud"
	for result in results:
		check=collections.OrderedDict()
		check["LEARNING OBJECT "]=result["learning_object"]
		check["SKILL "]=result["skill"]
		check["JOB"]=result["job"]
		print "half done"
		check["JOB-ID"]=result["job_id"]
		print "error 1"
		check["LO-ID"]=result["learning_object_id"]
		print "error 2"
		check["SKILL-ID"]=result["skill_id"]
		print "error 3"
		out.append(check)
		print out
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"MESSAGE":"NO RESULTS FOR THIS LEARNING OBJECT - " + loids
								
				}
				}
			}
	
	if not out:
		return error_format
	else:
		result_format['search']['response']['data'] = out
		return result_format

def getsyllabcount(skillid):
	out=[]
	results=db1['extracted_syllabus_new'].find({"skill_id":skillid})
	for result in results:
		check={}
		check["syllabus "]=result["syllabus"]
		out.append(check)
		#print check
		ans=len(check['syllabus '])
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"found":"0"
								
				}
				}
			}	
	if not out:
		return error_format
	else:
		result_format['search']['response']['count'] = ans
		return result_format


def geturl(url_name):
	print "url"
	temp=[]
	out=[]

	if request.args.get('source'):
		loc=request.args.get('source')
		print loc
		temp.append(loc)
		print temp[0]
		#results=db['videoposts_rawdata'].find({'source':temp[0]})
		results=db1['videoposts_rawdata_local'].find({'source':temp[0]})
		count=results.count()
		print count
	else:
		#results=db['videoposts_rawdata'].find({})
		results=db1['videoposts_rawdata_local'].find({})
	count=results.count()
	print count

	for result in results:
		check=collections.OrderedDict()
		#check["VIDEO-TITLE"]=result["video_title"]
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
	l=[]
	out=[]
	out1=[]
	l.append(keyss)
	#results=db['temp_skills_extracted'].find({"job_id":int(keyss)})
	results=db1['extracted_skills_local'].find({"job_id":int(keyss)})
	print keyss
	print results
	for result in results:
		print "Inside "
		check=collections.OrderedDict()
		check1=collections.OrderedDict()
		check["SKILL SET "]=result["skills"]
		lo_count=db1['extracted_videos_new'].find({"job_id":int(keyss)}).count()
		#check["LO-COUNT"]=lo_count
		check1['JOB']=result["job"]
		list_of_skills=result["skills"]
		skills_with_count=[]
		for skill in list_of_skills:
			lo_count=db1['extracted_videos_new'].find({"skill_id":skill["id"]}).count()
			skill['LO-COUNT']=lo_count
			skills_with_count.append(skill)
		check['SKILL SET']=skills_with_count	
		out1.append(check1)
		out.append(check)
		comp="hi"
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"found":"0"
								
				}
				}
			}
	
	if not out1:
		return error_format
	else:
		result_format['search']['response'] = out1[0]
		result_format['search']['response']['data'] = out
		return result_format

def getvideos(ids):
	out=[]
	#results=db['extracted_videos'].find({"learning_object":learning_object})
	results=db1['extracted_videos_new'].find({"learning_object_id":ids})
	print results
	for result in results:
		print "poda"
		check=collections.OrderedDict()
		check["VIDEOS"]=result["videos"]
		out.append(check)
		print "check"
		print out
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"MESSAGE":"NO VIDEOS FOR THIS LEARNING OBJECT - " + ids
								
				}
				}
			}
	if not out:
		return error_format
	else:
		result_format['search']['response']['data'] = out
		return result_format

def getsyllabus(skills):
	out=[]
	#results=db['extracted_syllabus'].find({"skill":skills})
	results=db1['extracted_syllabus_new'].find({"skill":skills})
	for result in results:
		check=collections.OrderedDict()
		check["SYLLABUS"]=result["syllabus"]
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"found":"0"
								
				}
				}
			}
	if not out:
		return error_format
	else:
		result_format['search']['response']['data'] = out
		return result_format


def getJobs(job_name):
	print "in get jobs"
	print job_name
	i=job_name.split(" AND ")
	j1=[dict([x.split('=')]) for x in job_name.split(' AND ')[1:]]
	print j1
	off = int(request.args.get('offset',0))
	src=str(request.args.get('source',0))
	loc=str(request.args.get('location',0))
	comp=str(request.args.get('company',0))
	temp=[{"keyword":i[0]}]
	temp.extend(j1)
	print temp

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

	
	#results = db['jobposts_rawdata_job'].find({"$and":temp}).limit(10).skip(off)
	results = db1['jobposts_rawdata'].find({"$and":temp}).limit(10).skip(off)
	#count=db['jobposts_rawdata_job'].find({"keyword_fetched":job_name}).count()
	count=db1['jobposts_rawdata'].find({"keyword":job_name}).count()
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


		print out
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

def getSkillsetIds(skill_id):
	out=[]
	results=db1['extracted_syllabus_new'].find({"skill_id":skill_id})

	for result in results:
		check=collections.OrderedDict()
		check["SYLLABUS"]=result["syllabus"]
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
	error_format= {
				"search":{
				"timed_out":"false",
				"response":{
								"found":"0"
								
				}
				}
			}
	if not out:
		return error_format
	else:
		result_format['search']['response']['data'] = out
		return result_format

#/v1/keywords/search/job_listing?q=job_title
@app.route('/v1/keywords/search/job_listing', methods=['GET'])
def name():
    name = request.args.get("q")
    print name
    
    res = getResults(name)

    return flask.jsonify(**res)
#/v1/keywords/search/job_position?q=Business Analyst
@app.route('/v1/keywords/search/job_position', methods=['GET'])
def names():
    names = request.args.get("q")
    print names    
    ress = getJobs(names)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**ress)
#/v1/keywords/search/video?q=xyz&source=youtube.com
@app.route('/v1/keywords/search/learningcontent', methods=['GET'])
def namess():
    namess = request.args.get("q")
    print namess    
    resss = geturl(namess)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**resss)


@app.route('/v1/keywords/search/videos', methods=['GET'])
def video():
    video = request.args.get("q")
    print video    
    resssss = getvideos(video)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**resssss)
    
@app.route('/v1/keywords/search/syllabus', methods=['GET'])
def syllabus():
    syllabus = request.args.get("q")
    print syllabus    
    ressssss = getsyllabus(syllabus)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**ressssss)    
#/v1/keywords/search/skillset?q=Digital Marketing
@app.route('/v1/keywords/search/skillset', methods=['GET'])
def namesss():
    namesss = request.args.get("q")
    print namesss    
    ressss = getKeywords(namesss)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"
    
    #return ress
    return flask.jsonify(**ressss)

#/v1/keywords/search/LoTopics?q=SK6_28
@app.route('/v1/keywords/search/LoTopics', methods=['GET'])
def LoTopics():
    LoTopics = request.args.get("q")
    print LoTopics    
    resssssss = getSkillsetIds(LoTopics)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"  
    
    #return ress
    return flask.jsonify(**resssssss)

#/v1/keywords/search/skills?q=LO4_SK1_25
@app.route('/v1/keywords/search/skills', methods=['GET'])
def skill():
    skill = request.args.get("q")
    #print LoTopics    
    ressssssss = getskills(skill)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"  
    
    #return ress
    return flask.jsonify(**ressssssss)  


@app.route('/v1/keywords/search/getsyllabcount', methods=['GET'])
def syl():
    syl = request.args.get("q")
    #print LoTopics    
    resssssssss =getsyllabcount(syl)
    #print "RRESSSSSSSSSSSSSSSSSSSSSSS"  
    
    #return ress
    return flask.jsonify(**resssssssss) 
    


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')