# Import statements for the code.
import os
import requests
import json
import datetime


# Authenticate to the API and receive the auth token.
# Uses a JSON config file which contains the client ID
# and client secret.
def api_auth():

	with open('secret-auth-config.json') as config_file:
		config_data = json.load(config_file)

	response = requests.post(config_data['url'], data=config_data['data'], headers=config_data['headers'])

	response = json.loads(response.text)

	return response



# Based on an FQL filter, query the API.  Returns a list of detection IDs.
def api_detections(access_token, filter):

	with open('config.json') as config_file:
		config_data = json.load(config_file)

	config_data['headers']['Authorization'] = access_token

	detections_url = config_data['detections_url'] + "?filter=" + filter

	api_response_data = []
	current_offset = 0

	# While loop to handle pagination.
	while True:

		response = requests.get(detections_url, headers=config_data['headers'])
		response = json.loads(response.text)

		api_response_data.extend(response["resources"])

		try:
			if response["meta"]["pagination"]["offset"] + response["meta"]["pagination"]["limit"] > response["meta"]["pagination"]["total"]:
				break
			else:
				current_offset += response["meta"]["pagination"]["limit"]
		except KeyError:
			break

	return api_response_data



# Feeds a list of detection IDs to the API.
# Returns all metadata for any given detection.
def api_detections_summaries(access_token, detection_ids):

	with open('config.json') as config_file:
		config_data = json.load(config_file)

	config_data['headers']['Authorization'] = access_token
	config_data['detections_summaries_data']['ids'] = detection_ids

	api_response_data = []
	current_offset = 0

	# While loop to handle pagination.
	while True:

		response = requests.post(config_data['detections_summaries_url'], data=json.dumps(config_data['detections_summaries_data']), headers=config_data['headers'])
		response = json.loads(response.text)

		api_response_data.extend(response["resources"])

		try:
			if response["meta"]["pagination"]["offset"] + response["meta"]["pagination"]["limit"] > response["meta"]["pagination"]["total"]:
				break
			else:
				current_offset += response["meta"]["pagination"]["limit"]
		except KeyError:
			break

	return api_response_data



# Take the RFC3339 standard timestamp strings
# and transform them into a datetime object.
# This allows us to perform comparisons on timestamp
# data.
def timestamp_parser(timestamp):
	format = '%Y-%m-%dT%H:%M:%S%z'
	obj = datetime.datetime.strptime(timestamp, format)
	return obj.isoformat()





if __name__ == '__main__':


	# Derive the authentication token.
	auth_response = api_auth()
	auth_access_token = "Bearer " + auth_response['access_token']


	# Set our FQL filter and timestamp ranges to retrieve
	# all detections over a specified range of time.
	# NOTE: For some reason the CrowdStrike API at this point does
	# not seem to allow for complex logic in the FQL filters fed to the
	# detections API.  Therefore it's not possible to write "between"
	# logic in the FQL filter.  We'll have to retrieve a less precise
	# output from the API, then filter the results further to get the exact
	# timestamp ranges we're targeting.
	api_detection_fql_filter_logic = "first_behavior:>='2022-01-01'"
	time_range_recent = timestamp_parser("2022-04-01T00:00:00Z")
	time_range_past = timestamp_parser("2022-03-01T00:00:00Z")

	# Querying the API to retrieve the detections IDs.
	detection_ids = []
	detection_ids = api_detections(auth_access_token, api_detection_fql_filter_logic)

	# Querying the API to retrieve the summary information for each ID.
	detection_summary_data = []
	detection_summary_data = api_detections_summaries(auth_access_token, detection_ids)

	# Here's where we take the larger set of data from the APIs and narrow it
	# down to an exact timestamp range according to the timestamp of the
	# "first behavior" that created a detection.
	detection_ids_narrowed = []
	detection_summary_data_narrowed = []
	for i in range(len(detection_summary_data)):
		detection_element = detection_summary_data[i]
		first_behavior_timestamp = timestamp_parser(detection_element['first_behavior'])
		within_range = time_range_past <= first_behavior_timestamp <= time_range_recent
		if within_range == True:
			detection_summary_data_narrowed.append(detection_element)
			detection_ids_narrowed.append(detection_element['detection_id'])
		else:
			continue



	# Now write the summary information of all detection IDs to
	# an output file for further reference by the user.
	with open('detection_summary_data_output.json','w') as detection_summary_data_file:
		json.dump(detection_summary_data_narrowed, detection_summary_data_file)



	# Summarize the data by detection severity.
	high_sev_detection_ids = []
	med_sev_detection_ids = []
	low_sev_detection_ids = []
	for i in range(len(detection_summary_data_narrowed)):
		detection_element = detection_summary_data_narrowed[i]
		severity = detection_element['max_severity_displayname']
		if severity == "High":
			high_sev_detection_ids.append(detection_element['detection_id'])
		elif severity == "Medium":
			med_sev_detection_ids.append(detection_element['detection_id'])
		elif severity == "Low":
			low_sev_detection_ids.append(detection_element['detection_id'])
		else:
			print("IMPORTANT ERROR: Unknown severity value encountered, exiting!")
			exit()

	# Summarize the data by detection type.
	# For the time being, we have three different designations:
	# 1. The detection events initiated by the work of Falcon Overwatch.
	# 2. The detection events initiated by the work of Falcon machine learning algorithms.
	# 3. The detection events initiated by Falcon's standard signatures.
	# The code also generates a comment noting how many detection events were in any
	# assisted by Falcon Overwatch analysis.
	detection_type_dict = {}
	overwatch_assisted_detections = set()
	for i in range(len(detection_summary_data_narrowed)):
		detection_element = detection_summary_data_narrowed[i]
		first_behavior_timestamp = detection_element['first_behavior']
		behaviors = detection_element['behaviors']
		for i in behaviors:
			behavior_timestamp = i['timestamp']
			behavior_objective = i['objective']
			behavior_tactic = i['tactic']
			behavior_technique = i['technique']
			if behavior_objective == "Falcon Detection Method" and behavior_tactic == "Falcon Overwatch":
				overwatch_assisted_detections.add(detection_element['detection_id'])
			elif behavior_timestamp == first_behavior_timestamp:
				if behavior_objective == "Falcon Detection Method" and behavior_tactic == "Falcon Overwatch":
					if "Falcon Overwatch Analysis" in detection_type_dict.keys():
						detection_type_dict['Falcon Overwatch Analysis'].add(detection_element['detection_id'])
					else:
						detection_type_dict['Falcon Overwatch Analysis'] = set()
						detection_type_dict['Falcon Overwatch Analysis'].add(detection_element['detection_id'])
				elif behavior_objective == "Falcon Detection Method" and behavior_tactic == "Machine Learning":
					if "Falcon Machine-Learning" in detection_type_dict.keys():
						detection_type_dict['Falcon Machine-Learning'].add(detection_element['detection_id'])
					else:
						detection_type_dict['Falcon Machine-Learning'] = set()
						detection_type_dict['Falcon Machine-Learning'].add(detection_element['detection_id'])
				else:
					detection_type_string = "Falcon Standard Signatures --- " + i['objective'] + " / " + i['tactic'] + " / " + i['technique']
					if detection_type_string in detection_type_dict.keys():
						detection_type_dict[detection_type_string].add(detection_element['detection_id'])
					else:
						detection_type_dict[detection_type_string] = set()
						detection_type_dict[detection_type_string].add(detection_element['detection_id'])
			else:
				continue
	overwatch_associated_events_note = "--- NOTE: Of the %s detections generated, %s were either initiated or assisted by Overwatch analysis." %(len(detection_ids_narrowed), len(overwatch_assisted_detections))



	# Finally, print all of the results out to the terminal for the user.

	print("\n")

	print("NOTES:\n========================================")
	print("\n- The program has generated the following output file: detection_summary_data_output.json")
	print("  It contains all raw data on each detection event retrieved and filtered from the CrowdStrike API based on the timestamp filters.")
	print("- All other sections of text output below summarize the returned data based on the fully filtered data.")
	print("\n")


	print("DETECTION TOTALS BY SEVERITY\n========================================")
	print("\nTotal number of all detections: %s\n----------------------------------------" %(len(detection_ids_narrowed)))
	print("Total high severity detections: %s" %(len(high_sev_detection_ids)))
	print("Total med severity detections: %s" %(len(med_sev_detection_ids)))
	print("Total low severity detections: %s" %(len(low_sev_detection_ids)))


	print("\n")


	print("DETECTIONS BY TYPE\n========================================")
	print("\nType by raw numbers:\n----------------------------------------")
	for i in detection_type_dict.keys():
		detection_type = i
		associated_detections = len(detection_type_dict[detection_type])
		print("%s: %s" %(detection_type, associated_detections))
	print(overwatch_associated_events_note)
	print("\nType by percentage:\n----------------------------------------")
	total_detections = len(detection_ids_narrowed)
	for i in detection_type_dict.keys():
		detection_type = i
		associated_detections = len(detection_type_dict[detection_type])
		type_percentage = '{0:.2f}'.format((associated_detections / total_detections) * 100)
		print("%s: %s %%" %(detection_type, type_percentage))


	print("\n")