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
import importlib



class CreateQuery:

	def __init__(self, query_template_file = None, time_range_parameters = None, target_selector_inputs = None, search_directory = None):
		self.template_file = query_template_file
		self.config = self.load_config_from_template_file(query_template_file)
		self.name = self.config['api_query_meta_data']['query_name']
		self.id = self.config['api_query_meta_data']['query_id']
		self.time_range_parameters = time_range_parameters
		self.target_selector_inputs = target_selector_inputs
		self.search_directory = self.setup_search_directory(search_directory)
		self.api_query_module = self.load_api_query_module(self.config)
		self.api_query_create_function = self.load_api_query_create_function(self.config)
		self.api_query_instance = self.load_api_query_instance()
		self.skeleton = self.api_query_instance.skeleton
		self.results = None
		self.total_number_of_results = None


	def load_config_from_template_file(self, query_template_file):
		f = open(query_template_file, "r")
		query_config = json.load(f)
		f.close()
		return query_config


	def setup_search_directory(self, search_directory):
		with open(search_directory + "/" "Search Results Summary.txt", "a") as f:
			f.write("\n")
			f.write("Query Name: " + self.name + "\n")
			f.write("Query ID: " + self.id + "\n")
			f.write("Purpose: " + self.config['api_query_meta_data']['api_query_description'] + "\n")
		return search_directory


	def load_api_query_module(self, config):
		if config['api_query_meta_data']['api_platform'] == "elasticsearch":
			module = importlib.import_module("elasticsearch_api_query")
		else:
			print("ERROR: The program has encountered an unknown value for the field 'api_platform' in the api query template file \"{}\".  What this means in practice is that there are no known api query modules which support the api platform specified in this api query template file.  Please review the api-query-template-file's JSON.  Exiting.".format(self.template_file))
			exit()
		return module


	def load_api_query_create_function(self, config):
		if config['api_query_meta_data']['api_platform'] == "elasticsearch":
			function = "CreateElasticsearchAPIQuery"
		else:
			print("ERROR: The program has encountered an unknown value for the field 'api_platform' in the api query template file \"{}\".  What this means in practice is that there are no known api query modules which support the api platform specified in this api query template file.  Please review the api-query-template-file's JSON.  Exiting.".format(self.template_file))
			exit()
		return function


	def load_api_query_instance(self):
		api_query_init_function = getattr(self.api_query_module, self.api_query_create_function)
		api_query = api_query_init_function(self.time_range_parameters, self.target_selector_inputs, self.config, self.search_directory)
		return api_query


	def write_api_query_results(self):
		query_results_file_name = self.id + "-" + "QUERY" + "---" + self.name + "---" + "RESULTS.json"
		with open(self.search_directory + "/" + "Search Results Summary.txt", "a") as f:
			f.write("Results: This API query returned {} results.  The results are stored in the file {}.\n".format(self.total_number_of_results, query_results_file_name))
		with open(self.search_directory + "/" + query_results_file_name, "w") as f:
			json.dump(self.results, f, indent=4)
		return "Success"


	def run(self):
		api_query_instance_ran = self.api_query_instance.run()
		self.results = api_query_instance_ran.results
		self.total_number_of_results = api_query_instance_ran.total_number_of_results
		api_query_results_written = self.write_api_query_results()
		return self


