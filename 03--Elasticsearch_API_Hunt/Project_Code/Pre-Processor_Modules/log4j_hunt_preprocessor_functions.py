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



def process_input_log4j_ioc_ip_csv(parameters):
	target_selector_ips = []
	hunt_directory = parameters['hunt_directory']
	search_directory = parameters['search_directory']
	ip_input_file = hunt_directory + "/" + "Hunt_Reference_Files" + "/" + parameters['custom_parameters']['input_file']
	df = pandas.read_csv(ip_input_file)
	for row_element in df['IOC']:
		ip = str(row_element)
		target_selector_ips.append(ip)
	return target_selector_ips


def process_input_log4j_ioc_domain_csv(parameters):
	target_selector_domains = []
	hunt_directory = parameters['hunt_directory']
	search_directory = parameters['search_directory']
	domains_input_file = hunt_directory + "/" + "Hunt_Reference_Files" + "/" + parameters['custom_parameters']['input_file']
	df = pandas.read_csv(domains_input_file)
	for row_element in df['IOC']:
		domain = str(row_element)
		target_selector_domains.append(domain)
	return target_selector_domains
