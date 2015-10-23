from flask import Flask, request
import flask
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
app = Flask(__name__)
connection = MongoClient('188.40.79.87', 27017)
db = connection['brightminds']

#results = db['jobposts_rawdata_job'].distinct("keyword_fetched")
results = db['jobposts_rawdata_job'].find({"keyword_fetched":"Data+Scientist"})
for result in results:
    print result["job_title"]
#print results.count
#for i in range(len(results)):
    #print results[i]["job_title"]
#for result in results:
    #ans = db['jobposts_rawdata_job'].distinct("job_title")
    #json_results = []
    #print result
    #break
    #json_results.append(result)
#print results[2]
