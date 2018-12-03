import random
import requests
import json 
import numpy as np
from datetime import datetime

LOGS_URL = "http://18.222.204.247:3000/logs"


def get_logs(user_id):
	r= requests.get("{}/{}".format(LOGS_URL, user_id))
	resp = json.loads(r.text)
	return resp

def ep_to_day(ep):
	return datetime.fromtimestamp(ep/1000).strftime("%A")

def ep_to_hour(ep):
	return datetime.fromtimestamp(ep/1000).strftime("%H")

def aggregate_logs(resp):

	i=0
	data = dict()

	while i < len(resp)-1:
		i += 1
		day =  ep_to_day(int(resp[-i]["time"]))
		hour = ep_to_hour(int(resp[-i]["time"]))
		if not day in data:
			data[day] = {}
			data[day]["total"] = 0
		else:
			if not hour in data:
				data[day][hour] = 1
				data[day]["total"] += 1
			else:
				data[day][hour] += 1
				data[day]["total"] += 1

#   print(data)
	return data

def get_min_max(data):
	habits = {"max_day": None, "max_day_value": None, "min_day": None, 
				"min_day_value":None, "max_hour": None, "min_hour": None,
				"max_hour_value": None, "min_hour_value": None}

	for day in data.keys():
		if habits["max_day"] is None:
			habits["max_day_value"] = data[day]["total"]
			habits["max_day"] = day
		else:
			if habits["max_day"] > data[day]["total"]:
				habits["max_day_value"] = data[day]["total"]
				habits["max_day"] = day

		if habits["min_day"] is None:
			habits["min_day_value"] = data[day]["total"]
			habits["min_day"] = day
		else:
			if habits["min_day"] < data[day]["total"]:
				habits["min_day_value"] = data[day]["total"]
				habits["min_day"] = day

		for time in data[day].keys():
			if time == "total":
				# print("Continuing in here")
				continue
			if habits["max_hour"] is None:
				habits["max_hour_value"] = data[day][time]
				habits["max_hour"] = time
			else:
				if habits["max_hour"] > data[day][time]:
					habits["max_hour_value"] = data[day][time]
					habits["max_hour"] = time

			if habits["min_hour"] is None:
				habits["min_hour_value"] = data[day][time]
				habits["min_hour"] = time
			else:
				if habits["min_hour"] < data[day][time]:
					habits["min_hour_value"] = data[day][time]
					habits["min_hour"] = time

	# print(habits)
	return habits


def get_habits(user_id):
	resp = get_logs(user_id)
	aggr_logs = aggregate_logs(resp)
	habits = get_min_max(aggr_logs)
	return habits, aggr_logs
	

if __name__ == '__main__':
	print(get_habits('5bf0c3889c7cd00010aa1134'))