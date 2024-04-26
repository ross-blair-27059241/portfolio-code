import os
import json
import requests



def api_auth_base_config_load():
	with open('secret-cbr-auth-config.json') as config_file:
		api_auth_base_config_data = json.load(config_file)
	return api_auth_base_config_data


def process_query_by_name(api_auth_base_config_data, process_name_to_search):

	response_data = []
	max_batched_results = 3000
	current_offset = 0

	#While loop to paginate our queries and avoid timeouts.
	looping = True
	while looping == True:
		api_endpoint = "/api/v1/process"
		cbr_query_syntax = "?rows=" + str(max_batched_results) + "&cb.comprehensive_search=true" + "&start=" + str(current_offset) + "&q=process_name:" + process_name_to_search + " AND " + "start:[2023-02-01T00:00:00 TO 2023-02-03T00:00:00]"
		query_url = api_auth_base_config_data['base_api_url'] + api_endpoint + cbr_query_syntax
		response = requests.get(query_url, headers=api_auth_base_config_data['headers'], verify=True)
		response = json.loads(response.text)
		total_results = response['total_results']
		response_data.extend(response['results'])
		if current_offset + max_batched_results >= total_results:
			looping = False
		else:
			current_offset = current_offset + max_batched_results
			continue
	with open("response_data.json", "w") as f:
		for i in response_data:
			print(i, file = f)
	exit()

def main():
	api_auth_base_config_data = api_auth_base_config_load()
	process_name = "example_cmd.exe"
	process_query_by_name(api_auth_base_config_data, process_name)
