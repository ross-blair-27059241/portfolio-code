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


import pandas
import re
import validators



def generate_output_log4j_ioc_csv_files(parameters):
	query = parameters['query_to_process']
	if query.total_number_of_results != 0:
		ioc_attacker_source_ip_list = []
		ioc_callback_ip_list = []
		ioc_callback_domain_list = []
		# We're dealing with a list of dictionary items, each item being
		# an individual record returned as a an individual result from the
		# API.  So first, let's retrieve that list of dictionary items.
		query_results_list = query.results['results_returned_from_api']
		# We now need to do some transformations to make sure that our
		# data can fit nicely into a standard dataframe.
		transformed_query_results_list = []
		for i in query_results_list:
			transformed_query_result = {}
			transformed_query_result['_id'] = i['_id']
			for key, value in i['fields'].items():
				transformed_query_result[key] = value[0]
			transformed_query_results_list.append(transformed_query_result)
		# Write the transformed list of dictionary items to a dataframe.
		df = pandas.DataFrame(transformed_query_results_list)
		# Create the IOC list for source IPs observed generating the
		# Log4J attack traffic.
		for row_element in df['source.ip']:
			ioc_attacker_source_ip_list.append(row_element)
		# Set the regular expression syntax for successful parsing of
		# IP addresses and domain names.
		ipv4_address_match_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3})')
		ipv6_address_match_pattern = re.compile(r'((?=.*::)(?!.*::.+::)(::)?([\dA-Fa-f]{1,4}:(:|\b)|){5}|([\dA-Fa-f]{1,4}:){6})((([\dA-Fa-f]{1,4}((?!\3)::|:\b|(?![\dA-Fa-f])))|(?!\2\3)){2}|(((2[0-4]|1\d|[1-9])?\d|25[0-5])\.?\b){4})')
		domain_name_match_pattern = re.compile(r'(\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b)')
		for column in df [['url.original', 'user_agent.original']]:
			for row_element in df[column]:
				if ipv4_address_match_pattern.search(row_element) is not None:
					ipv4_match = ipv4_address_match_pattern.search(row_element)[0]
					if validators.ipv4(ipv4_match) == True:
						ioc_callback_ip_list.append(ipv4_match)
					else:
						continue
				elif ipv6_address_match_pattern.search(row_element) is not None:
					ipv6_match = ipv6_address_match_pattern.search(row_element)[0]
					if validators.ipv6(ipv6_match) == True:
						ioc_callback_ip_list.append(ipv6_match)
					else:
						continue
				elif domain_name_match_pattern.search(row_element) is not None:
					domain_match = domain_name_match_pattern.search(row_element)[0]
					if validators.domain(domain_match) == True:
						ioc_callback_domain_list.append(domain_match)
					else:
						continue
				else:
					continue
		ioc_attacker_and_callback_ips = ioc_attacker_source_ip_list + ioc_callback_ip_list
	else:
		ioc_attacker_source_ip_list = []
		ioc_callback_domain_list = []
	with open(parameters['hunt_directory'] + "/" + "Hunt_Reference_Files" + "/" + "Log4J-External_Sources_Input_IOC_IPs.txt", "r") as f:
		for line in f:
			line = line.strip("\n")
			line = line.replace("[.]", ".")
			if validators.ipv4(line) == True:
				ioc_attacker_and_callback_ips.append(line)
			elif validators.ipv6(line) == True:
				ioc_attacker_and_callback_ips.append(line)
			else:
				continue
	ioc_attacker_and_callback_ips = list(set(ioc_attacker_and_callback_ips))
	ioc_ips_df = pandas.DataFrame({"IOC": ioc_attacker_and_callback_ips})
	ioc_attacker_domains = list(set(ioc_callback_domain_list))
	valid_tld_list = []
	valid_tld_ioc_attacker_domains = []
	with open("General_Reference_Files" + "/" + "Valid_ICANN_TLDs.txt", "r") as f:
		for line in f:
			tld = line.strip("\n").lower()
			valid_tld_list.append(tld)
	for i in ioc_attacker_domains:
		if i.split('.')[-1] in valid_tld_list:
			valid_tld_ioc_attacker_domains.append(i)
		else:
			continue
	ioc_domains_df = pandas.DataFrame({"IOC": valid_tld_ioc_attacker_domains})
	ioc_ips_df.to_csv(parameters['hunt_directory'] + "/" + "Hunt_Reference_Files" + "/" + "Log4J-Hunt_Search_Results_IOC_IPs.csv", index = False)
	ioc_ips_df.to_csv(parameters['search_directory'] + "/" + "DEV-REFERENCE---Post-Processor Outputs" + "/" + "Log4J-Hunt_Search_Results_IOC_IPs.csv", index = False)
	ioc_domains_df.to_csv(parameters['hunt_directory'] + "/" + "Hunt_Reference_Files" + "/" + "Log4J-Hunt_Search_Results_IOC_Domains.csv", index = False)
	ioc_domains_df.to_csv(parameters['search_directory'] + "/" + "DEV-REFERENCE---Post-Processor Outputs" + "/" + "Log4J-Hunt_Search_Results_IOC_Domains.csv", index = False)
	return "FURTHER PROCESSING: The results of this API query were further processed by the post-processor \"generate_output_log4j_ioc_csv_files\".  This generated two separate output files: \"Log4J-Hunt_Search_Results_IOC_IPs.csv\", and \"Log4J-Hunt_Search_Results_IOC_Domains.csv\".  Both files were stored in this hunt's \"Hunt_Reference_Files\" directory."