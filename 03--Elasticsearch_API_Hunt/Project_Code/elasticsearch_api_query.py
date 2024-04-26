###############################################################################
# Copyright 2021 Crane Co GIS

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentationfiles (the "Software"),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

###############################################################################


import os
import json
import requests



class CreateElasticsearchAPIQuery:

	def __init__(self, time_range_parameters, target_selector_inputs, config, working_directory):
		self.time_range_parameters = time_range_parameters
		self.target_selector_inputs = target_selector_inputs
		self.query_config = config
		self.name = self.query_config["api_query_meta_data"]["query_name"]
		self.id = self.query_config["api_query_meta_data"]["query_id"]
		self.working_directory = working_directory
		self.api_auth_config = self.api_auth_config_load()
		self.skeleton - self.build_query_skeleton()
		self.results = None
		self.total_number_of_results = None

	def api_auth_config_load(self):
		codebase_root_directory = os.getcwd()
		with open(codebase_root_directory + "/" + "secret-elastic-auth-config.json", "r") as f:
			api_auth_config_data = json.load(f)
		return api_auth_config_data


	def api_retrieve_pit(self):
		print("TELEMETRY: Querying Elasticsearch API to retrieve point-in-time ID configurations for query \"" + self.id + "-" + self.name + "\".")
		url = self.api_auth_config["base_api_url"] + "/" + self.query_config["api_query_required_parameters"]["index"] + "/" + "_pit?keep_alive=" + self.query_config["api_query_required_parameters"]["point-in-time_keep_alive"]
		username = self.api_auth_config["username"]
		password = self.api_auth_config["password"]
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		api_response = requests.post(url, verify=False, auth=(username, password)).content
		pit_dict = json.loads(api_response)
		try:
			point_in_time = pit_dict["id"]
		except:
			error_log_file_name = self.search_directory + "/" + "error.log"
			print("ERROR: We did not receive a valid PIT response from the Elasticsearch API.  Please refer to the error log file \"{}\".  Exiting.".format(error_log_file_name))
			with open(error_log_file_name, "a") as f:
				json.dump(pit_dict, f, indent=4)
			exit()
		return point_in_time


	def build_query_skeleton(self):

		skeleton = self.query_config['api_query_syntax_skeleton']

		# Set the results batching size for the API's returned results.
		skeleton['size'] = self.query_config['api_query_required_parameters']['results_batching_size']

		# Query the Elasticsearch API to retrieve a Point in Time identifier.
		# Insert that identifier value into the skeleton.
		point_in_time = self.api_retrieve_pit()
		skeleton['pit']['id'] = point_in_time
		# Specify the keep alive setting for that Point in Time Identifier.
		skeleton['pit']['keep_alive'] = self.query_config['api_query_required_parameters']['point-in-time_keep_alive']

		# Determine which type of time_range_parameters we are dealing with.
		# Properly insert the time_range_parameters into the query's skeleton.
		if self.time_range_parameters['type'] == 'absolute':
			start_range = self.time_range_parameters['after']
			end_range = self.time_range_parameters['before']
			time_range_filter = {"range": {"@timestamp": {"gte": start_range, "lte": end_range}}}
		elif self.time_range_parameters['type'] == "relative":
			relative_range = self.time_range_parameters['relative_range']
			time_range_filter = {"range": {"@timestamp": {"gte": relative_range}}}
		else:
			print("ERROR: The time_range_parameters \"type\" value is not valid.  Please review your current hunt's configuration JSON file and make sure that it's correctly formatted.  Exiting.")
			exit()
		skeleton['query']['bool']['filter'].append(time_range_filter)

		# If this query has the type "targeted_search", then no further
		# values need to be inserted into the skeleton.
		if self.query_config['api_query_meta_data']['search_type'] == "targeted_search":
			return skeleton
		# If it's a bulk_ioc_search then run the load_target_selector_inputs_function.
		elif self.query_config['api_query_meta_data']['search_type'] == "bulk_ioc_search":
			skeleton = self.load_target_selector_inputs(skeleton, self.target_selector_inputs)
			return skeleton
		else:
			print("ERROR: The program has encountered an unknown \"search_type\" value in the query template file \"{}\".  Please review that query template file and the \"search_type\" value to troubleshoot.  Exiting.".format(self.id + "-" + self.name))
			exit()


	def load_target_selector_inputs(self, input_skeleton, target_selector_inputs):
		output_skeleton = input_skeleton
		target_selector = self.query_config['api_query_required_parameters']['target_selector']
		target_selector_query_type = self.query_config['api_query_required_parameters']['target_selector_query_type']
		if target_selector_query_type == "match":
			for i in target_selector_inputs:
				target_selector_input_field_value = i
				target_selector_input_dict_entry = {target_selector_query_type: {target_selector: target_selector_input_field_value}}
				output_skeleton['query']['bool']['should'].append(target_selector_input_dict_entry)
		elif target_selector_query_type == "wildcard":
			for i in target_selector_inputs:
				target_selector_input_field_value = "*" + str(i) + "*"
				target_selector_input_dict_entry = {target_selector_query_type: {target_selector: target_selector_input_field_value}}
				output_skeleton['query']['bool']['should'].append(target_selector_input_dict_entry)
		else:
			print("ERROR: The program has encountered an unknown \"target_selector_query_type\" value in the query template file \"{}\".  Please review that query template file and the \"target_selector_query_type\" value to troubleshoot.  Exiting.".format(self.id + "-" + self.name))
			exit()
		return output_skeleton


	def execute_single_query(self, query_skeleton):
		url = self.api_auth_config['base_api_url'] + "/" + "_search"
		username = self.api_auth_config['username']
		password = self.api_auth_config['password']
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		single_query_results = requests.get(url, verify=False, auth=(username, password), json=query_skeleton).content
		single_query_results = json.loads(single_query_results)
		try:
			hit_list = single_query_results['hits']['hits']
		except:
			error_log_file_name = self.search_directory + "/" + "error.log"
			print("ERROR: We did not receive any query hits from the Elasticsearch API's response.  Please refer to the error log file \"{}\".  Exiting.".format(error_log_file_name))
			with open(error_log_file_name, "a") as f:
				json.dump(single_query_results, f, indent=4)
				exit()
		return single_query_results


	def execute_paginated_query(self):

		current_query_skeleton = self.output_skeleton

		print("TELEMETRY: Executing query \"" + self.id + "-" + "\".  Pagination is enabled.")

		query_search_after_configs = []
		hit_list = []
		total_hits_processed = 0
		total_number_of_results = 0
		# Results returned from the API will be formatted into dicts.
		# Each result will be its own dict, so we will store these results
		# dicts in a large list.
		results_list = []

		# Begin the pagination loop.
		while True:
			# The pagination loop's logic will begin by testing whether
			# we have already gone through this loop at least once.  In other
			# words, whether we have already executed a search against the
			# API that had to be paginated.  If this was the case, then the
			# previous loop's execution will have collected "search_after"
			# configurations from the very last hit record returned in the
			# Elasticsearch API's response.  These "search_after"
			# configurations will have been stored in the
			# "query_search_after_configs" variable.  These configurations
			# have to be inserted in the next paginated query to ensure that
			# our next query starts off where the previous query left off.
			# First, let's test if the "query_search_after_configs" variable
			# even has a value or not.  If it does, then this is NOT the
			# first iteration of the loop, and we are in the middle of a
			# paginated query.  If the "query_search_after_configs" variable
			# IS empty then we don't have to worry about setting this
			# configuration, and can simply go on to make the very first
			# query of the loop.
			if query_search_after_configs != []:
				current_query_skeleton['search_after'] = query_search_after_configs
			# With the "search_after" configs properly set (or NOT), run
			# the query against the Elasticsearch API, and load those results
			# into a dictionary.
			api_response_dict = self.execute_single_query(current_query_skeleton)
			# If we have NOT already executed a query against the API - in
			# other words this is the very first query we've sent - then we
			# need to store the total number of results that the API recorded,
			# and also properly configure the `current_query_skeleton` for
			# the next query in the pagination loop.
			if query_search_after_configs == []:
				total_number_of_results = api_response_dict['hits']['total']['value']
			hit_list = api_response_dict['hits']['hits']
			hit_list_length = len(hit_list)
			# If 0 results have just been returned for the latest query to the
			# API, then break the pagination loop.  No further API queries
			# should be necessary.
			if hit_list_length == 0:
				break
			# Assuming that you did get results back from the latest query,
			# store the last hit that you received from this latest API response.
			last_hit = hit_list[hit_list_length - 1]
			# Store the "sort" value of this last hit into the
			# "query_search_after_configs" variable, so that it can then be
			# inserted into the "search_after" section of the next query
			# in our pagination loop.
			query_search_after_configs = last_hit['sort']
			# For each hit returned from the query that was just run, append
			# that to the results_list.  Count each hit added to the
			# results_list.  This count will help identify any issues
			# with the pagination code.
			results_list.extend(hit_list)
			total_hits_processed = total_hits_processed + hit_list_length
			# Take the number of results that have been processed so far, and
			# compare that to the total number of results that the API said
			# could be returned for the query.
			if total_hits_processed == total_number_of_results:
				# The results processed so far are equal to the total number
				# of results.  Therefore no further paginated queries are
				# necessary.  We can exit the pagination loop.
				break
			elif total_hits_processed > total_number_of_results:
				# Something has gone wrong with our pagination logic.
				print("ERROR: The number of results processed by the query code for query \"" + self.name + "-" + self.id + "\" exceeds the total number of results that the API originally reported for the same query.  This means that the code is not properly executing its pagination logic.  Please refer to the module `elasticsearch_api_query.py` for further troubleshooting.  Exiting.")
				exit()
			else:
				# The number of results processed so far is less than the
				# total number of results.  Therefore the pagination loop
				# needs to continue with the next paginated query.
				print("TELEMETRY: Executing next pagination loop for query \"" + self.id + "-" + self.name + "\".")
				continue
		# Set self.total_number_of_results to total_number_of_results.
		# This is important since this number will be referenced in
		# other parts of the codebase.
		self.total_number_of_results = total_number_of_results
		# We have constructed our object model such that a query object
		# will always have an attribute called `results` which has to be
		# a dictionary.  Therefore we're going to insert our
		# `results_list` into a `query_results_dict` and return that dict.
		query_results_dict = {}
		query_results_dict['results_returned_from_api'] = []
		for i in results_list:
			query_results_dict['results_returned_from_api'].append(i)
		return query_results_dict


	def run(self):
		self.results = self.execute_paginated_query()
		return self