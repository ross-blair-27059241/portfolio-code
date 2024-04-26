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
from preprocessor import *
from postprocessor import *
from query import *



class CreateSearch:

	def __init__(self, search_name = None, search_order_number_in_hunt = None, search_config_data = None, hunt_working_directory = None):
		self.name = search_name
		self.order_number_in_hunt = search_order_number_in_hunt
		self.config = search_config_data
		self.hunt_directory = hunt_working_directory
		self.working_directory = self.setup_search_directory(hunt_working_directory)
		self.type = self.config['search_type']
		self.selector_type = self.config['selector_type']
		self.time_range = self.load_time_range(self.config['time_range_parameters'])
		self.selector_preprocessors_configs = self.load_preprocessors_configs(self.config)
		self.target_selector_inputs = None
		self.results_postprocessors_configs = self.load_results_postprocessors_configs(self.config)


	def setup_search_directory(self, hunt_working_directory):
		search_working_directory = hunt_working_directory + "/" + "SEARCH" + "-" + str(self.order_number_in_hunt) + "---" + self.name + "---" + "RESULTS"
		print("TELEMETRY: Creating the directory " + "\"" + search_working_directory + "\"" " and its various files and sub-directories.  All reference and results files for Search \"{}\" will be stored here.".format(self.name))
		os.mkdir("search_working_directory")
		with open(search_working_directory + "/" + "Search Results Summary.txt", "w") as f:
			f.write("===========================================================\n")
			f.write(self.name + " RESULTS\n")
			f.write("===========================================================\n")
			f.write("\n")
			f.write("\n")
			f.write("Search Purpose:\n")
			f.write(self.config['search_description'] + "\n")
			f.write("\n")
			f.write("\n")
			f.write("\n")
			f.write("\n")
			f.write("Queries Run As Part of This Search\n")
			f.write("---------------------------------------\n")
		os.mkdir(search_working_directory + "/" + "DEV-REFERENCE---Queries_Run")
		return search_working_directory


	def load_preprocessors_configs(self, search_config):
		if("selector_pre-processors" in search_config) == True:
			if search_config['selector_pre-processors'] == []:
				return None
			else:
				return search_config['selector_pre-processors']
		else:
			return None


	def run_preprocessors(self, preprocessors_configs):
		# Based on the inputs from self.selector_preprocessors, instantiate a processor object, run it, and get back its results.
		# Note that this function should ONLY and ALWAYS return a list for the selector inputs.
		if preprocessors_configs is None:
			return None
		else:
			target_selector_inputs_master_list = []
			for i in preprocessors_configs:
				preprocessor = CreatePreProcessor(i, self.hunt_directory, self.working_directory)
				print("TELEMETRY: Executing pre-processor " + "\"" + i['name'] + "\"" + " for Search " + "\"" + self.name + "\"" + ".")
				preprocessor = preprocessor.run()
				target_selector_inputs = preprocessor.results
				if type(target_selector_inputs) is list:
					for e in target_selector_inputs:
						target_selector_inputs_master_list.append(e)
				else:
					print("ERROR: The selector_pre-processors for the search \"{}\" have returned results that are not the `list` data type.  Input values for the selector of a given query are always expected to be in the form of a list.  Please review your current hunt's configuration JSON file and make sure that the `selector_pre-processor` section is correctly formatted and that you are calling the appropriate module and function to generate your pre-processor inputs for the queries' selector.  Exiting.".format(self.name))
					exit()
			return target_selector_inputs_master_list


	def load_time_range(self, time_range_section):
		time_range_parameters = {}
		# Determine the kind of time range filter you're working with.
		# If it's improperly configured raise a critical error to
		# the user and exit().
		if time_range_section['relative_range'] != "" and time_range_section['after'] == "" and time_range_section['before'] == "":
			time_range_parameters['type'] = "relative"
			time_range_parameters['relative_range'] = time_range_section['relative_range']
		elif time_range_section['after'] != "" and time_range_section['before'] != "" and time_range_section['relative_range'] == "":
			time_range_parameters['type'] = "absolute"
			time_range_parameters['after'] = time_range_section['after']
			time_range_parameters['before'] = time_range_section['before']
		else:
			print("ERROR: The time_range_filter section for the search {} has not been configured properly.  Please review your current hunt's JSON configuration file and make sure that it is correctly formatted.  Exiting.".format(self.name))
			exit()
		return time_range_parameters


	# Here we compare the query_id of the query that was just run, we iterate
	# through all the post_processors loaded for our search.  If the query_id
	# matches that found in the post-processor configs, then that
	# post-processor will be run against that query's results.
	# If the post-processor configs specify "*" instead of a list of id values,
	# then that post-processor will be run against every single query
	# run as part of that search.
	def run_postprocessors(self, query_ran):
		if self.results_postprocessors_configs is None:
			return None
		else:
			postprocessors_ran = []
			for i in self.results_postprocessors_configs:
				# Here's where we're going to start the comparison.
				processor_config_data = i
				if query_ran.id in processor_config_data['target_queries_ids'] or processor_config_data['target_queries_ids'] == "*":
					postprocessor = CreatePostProcessor(processor_config_data, self.hunt_directory, self.working_directory, query_ran)
					print("TELEMETRY: Executing post-processor " + "\"" + processor_config_data['name'] + "\"" + " for Search " + "\"" + self.name + "\"" + ", query " + "\"" + query_ran.id + "-" + query_ran.name + "\"" ".")
					postprocessor_ran = postprocessor.run()
				if postprocessor_ran.outcome != None:
					with open(self.working_directory + "/" + "Search Results Summary.txt", "a") as f:
						f.write(postprocessor_ran.outcome + "\n")
					postprocessors_ran.append(postprocessors)
				else:
					continue
		return postprocessors_ran


	def run(self):
		target_selector_inputs = self.run_preprocessors(self.selector_preprocessors_configs)
		search_working_directory = self.working_directory
		time_range_parameters = self.time_range
		if self.type == "targeted_search":
			query_template_directory = "./Elasticsearch_API_Query_Templates/Targeted_Selector_Searches"
			for i in self.config['custom_api_query_template_files']:
				target_query_template_file_name = i.split('/')[-1]
				for file in os.listdir(query_template_directory):
					if target_query_template_file_name == file:
						query_template_file = query_template_directory + "/" + file
						query = CreateQuery(query_template_file, time_range_parameters, target_selector_inputs, search_working_directory)
						# Write the exact contents of the API queries that
						# we'll be making to a file.  This is to be kept
						# as a useful reference for high-stakes searches.
						with open(search_working_directory + "/" + "DEV-REFERENCE---Queries_Run" + "/" + query.id + "-" + query.name, "w", encoding="utf-16") as f:
							query_run = {}
							query_run['api_query_meta_data'] = query.config['api_query_meta_data']
							query_run['api_query_entered_parameters'] = query.skeleton
							json.dump(query_run, f, indent=4)
						query_ran = query.run()
						postprocessors_ran = self.run_postprocessors(query_ran)
					else:
						continue
		elif self.type == "bulk_ioc_search":
			query_template_directory = "./Elasticsearch_API_Query_Templates/Bulk_Selector_Searches"
			for file in os.listdir(query_template_directory):
				f = open(query_template_directory + "/" + file, "r")
				api_query_template = json.load(f)
				if api_query_template['api_query_meta_data']['search_type'] == self.type and api_query_template['api_query_meta_data']['selector_type'] == self.selector_type:
					query_template_file = query_template_directory + "/" + file
					query = CreateQuery(query_template_file, time_range_parameters, target_selector_inputs, search_working_directory)
					# Write the exact contents of the API queries that
					# we'll be making to a file.  This is to be kept
					# as a useful reference for high-stakes searches.
					with open(search_working_directory + "/" + "DEV-REFERENCE---Queries_Run" + "/" + query.id + "-" + query.name, "w", encoding="utf-16") as f:
							query_run = {}
							query_run['api_query_meta_data'] = query.config['api_query_meta_data']
							query_run['api_query_entered_parameters'] = query.skeleton
							json.dump(query_run, f, indent=4)
					query_ran = query.run()
					postprocessors_ran = self.run_postprocessors(query_ran)
				else:
					continue
		else:
			print("ERROR: Encountered a search_type for search \"{}\" that this program cannot process.  The search_type entered was {}.  Please refer to your current hunt's configuration JSON file and make sure that it is correctly formatted.  Exiting.".format(self.name, self.type))
			exit()
		return self
