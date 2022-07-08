from solution import calc_time,length_of_items_func
import os,json
import sys
import re
import requests as req
# import hashlib
 

api_data , length_of_items = length_of_items_func()

@calc_time
def results_file_check(*args):
	if sys.platform =='win32':

      		path = str(os.getcwd())+"\\results.csv"
	else:
		path = str(os.getcwd())+"/results.csv"
	

	list_of_lines = []
	set_of_line = set()
	set_os_ids = set()

	with open(path,'r') as file:

		text = file.readlines()
		
		for line in text:
			
			assert re.match("\d*\s, https:\W{2}i.\w+.com\W\w+.\w+ , \d+ , \d+ , \W\d+, \d+, \d+\W, \W\d+, \d+, \d+\W, \W\d+, \d+, \d+\W, \W\d+, \d+, \d+\W",line),"some of the line has the incorrect pattern"
			list_of_lines.append(line)
		
		print("Every line has the correct pattern ")
		#putting the list in a set to check for duplication
		set_of_line.update(list_of_lines)
		assert len(set_of_line) == length_of_items , "There are duplicate lines"
		print("No duplicate lines")
		
		
		for i in list_of_lines:
			set_os_ids.add(i.split(',')[0])

		try:
			assert len(set_os_ids) == length_of_items
		except:
			print("length of non duplicate items is less or more then 100")
		

@calc_time
def check_api_data(api_data,*args):
	test_api_data = req.get("https://api.imgflip.com/get_memes")
	assert json.loads(test_api_data.content) == api_data,"api data dosent match"
	print("api data is matching !")


results_file_check()

check_api_data(api_data)