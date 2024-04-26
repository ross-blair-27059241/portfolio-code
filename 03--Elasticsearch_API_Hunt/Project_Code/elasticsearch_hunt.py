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

import argparse
import json
from os import mkdir
from shutil import copytree
from search import *



class CreateHunt:

	def __init__(self, hunt_folder = None, results_directory = None):
		"""
		Initialize the hunt based on the command line parameters entered
		by the user.
		"""
		self.hunt_folder = hunt_folder
		self.config_data = self.load_hunt_config(hunt_folder)
		self.name = self.config_data['hunt_metadata']['hunt_name']
		self.working_directory = self.setup_hunt_results_directory(results_directory, self.config_data)
		self.searches = self.load_searches_configs(self.config_data)


	def load_hunt_config(self, hunt_folder):
		hunt_config_file = "./Hunts/" + hunt_folder + "/hunt-config.json"
		try:
			f = open(hunt_config_file, "r")
			hunt_config_data = json.load(f)
			f.close()
		except:
			print("ERROR: A hunt config file was not located in the specified hunt folder.  A valid hunt folder should contain a single config file bearing the name `hunt-config.json`.  Please review the name and contents of the specified hunt folder {} to troubleshoot.  Exiting.".format(hunt_folder))
			exit()
		return hunt_config_data


	def setup_hunt_results_directory(self, results_directory, config_data):
		run_number = 1
		hunt_results_directory = results_directory + "/" + config_data['hunt_metadata']['hunt_id'] + "-" + "HUNT" + "---" + config_data['hunt_metadata']['hunt_name'] + "---" + "Run" + str(run_number)
		try:
			mkdir(hunt_results_directory)
		except:
			run_number = 2
			while True:
				hunt_results_directory = results_directory + "/" + config_data['hunt_metadata']['hunt_id'] + "-" + "HUNT" + "---" + config_data['hunt_metadata']['hunt_name'] + "---" + "Run" + str(run_number)
				try:
					mkdir(hunt_results_directory)
					break
				except:
					run_number = run_number + 1
		print("TELEMETRY: Creating the directory " + "\"" + hunt_results_directory + "\"" " that will store all reference and results files for Run {} of the {}".format(run_number, self.name))
		if os.path.isdir("./Hunts/" + self.hunt_folder + "/" + "Hunt_Reference_Files") == True:
			copytree("./Hunts/" + self.hunt_folder + "/" + "Hunt_Reference_Files", hunt_results_directory + "/" + "Hunt_Reference_Files")
		return hunt_results_directory


	def load_searches_configs(self, config):
		"""
		Instantiate a list of search objects that will comprise the hunt.
		Note that NO pre-processor functions NOR API queries are executed
		at this point in time.  Pre-processors and API queries execute
		ONLY when the search.run() function is called on the search object.
		Returns a list of search objects.
		"""
		searches = []
		for key in config:
			if key == "searches":
				search_order_number_in_hunt = 1
				for search_config_section in config[key]:
					search_name = search_config_section
					search_config_data = config[key][search_config_section]
					hunt_working_directory = self.working_directory
					search = CreateSearch(search_name, search_order_number_in_hunt, search_config_data, hunt_working_directory)
					search_order_number_in_hunt = search_order_number_in_hunt + 1
					searches.append(search)
			else:
				continue
		return searches


	def run(self):
		"""
		Run each search in the list of searches configured for the hunt.
		Each search will be executed in the order in which they appear in the
		`hunt-config.json` file.
		"""
		for search in self.searches:
			search_ran = search.run()
		print("TELEMETRY: The hunt program has successfully completed execution.  All reference, input, output, and results files are organized, labeled, and stored in the \"{}\" directory.".format(self.working_directory))


def parse_args():
	"""
	Parse command line arguments.
	Returns result from parser.parse_args.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--hunt_folder",
		help = "REQUIRED: The name (NOT the path) of the hunt folder containing the hunt config file and any other reference input files needed.  Your hunt folder needs to be stored within the \"Hunts\" directory.  Note that this \"Hunts\" directory needs to be located in the same directory as this program's code files."
		)
	parser.add_argument(
		"--results_directory",
		help = "OPTIONAL:  The full path of the directory where you would like to store the results folder for this hunt.  Note that if this is not specified the program will default to storing the results folder in the same directory as this program's code files.",
		default = "."
		)
	return parser.parse_args()


def main():
	args = parse_args()
	try:
		args.hunt_folder
	except:
		print("ERROR: A hunt folder was not entered into this program's command line arguments.  The `hunt_folder` parameter is required.  Please run `--help` for further details.  Exiting.")
		exit()
	hunt = CreateHunt(args.hunt_folder, args.results_directory)
	hunt.run()




if __name__ == '__main__':
	main()