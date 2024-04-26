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
import importlib



class CreatePostProcessor:

	def __init__(self, processor_config_data = None, hunt_directory = None, search_directory = None, query_to_process = None):
		self.name = processor_config_data['name']
		self.config = processor_config_data
		self.hunt_directory = hunt_directory
		self.search_directory = self.setup_working_directory(search_directory)
		self.query_to_process = query_to_process
		self.module = importlib.import_module("Post-Processor_Modules" + "." + processor_config_data['processor_module'])
		self.function = processor_config_data['processor_function']
		self.function_parameters = self.load_function_parameters()
		self.outcome = None


	def setup_working_directory(self, search_directory):
		postprocessor_results_directory = search_directory + "/" + "DEV-REFERENCE---Post-Processor Outputs"
		if os.path.isdir(postprocessor_results_directory):
			return search_directory
		else:
			os.mkdir(postprocessor_results_directory)
			return search_directory


	def load_function_parameters(self):
		function_parameters = self.config
		function_parameters['hunt_directory'] = self.hunt_directory
		function_parameters['search_directory'] = self.search_directory
		function_parameters['query_to_process'] = self.query_to_process
		return function_parameters


	def run(self):
		function_to_call = getattr(self.module, self.function)
		self.outcome = function_to_call(self.function_parameters)
		return self