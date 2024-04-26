# About This Project

The Elasticsearch API Hunt project was undertaken during my time at Crane Co in 2021.  The project was a collaborative effort between myself and one other team member who participated during a summer internship.  The core code that executes queries against the Elasticsearch API and properly paginates and saves their results was a collaborative effort \(see `elasticsearch_api_query.py`\).  The vast majority of the remaining code is my work.


# The Goal

The overarching goal of the project was to automate complex routines of successive searches against the Elasticsearch API.  The results from the first search against certain indices would be retrieved, processed, and then fed into a second search against another set of indices.  Such a process could be repeated multiple times.  In this way complex routines of successive searches - which the project referred to as "hunts" - could be written once in code and then run as many times as we needed.


# Old Way vs. New Way: An Example

Let's say that an Analyst wants to query log sources for inbound network traffic to the organization's web application servers.  They're looking for strings in the web traffic and application input logs that could be indicative of malicious attempts to exploit a given vulnerability.  Results of attempted exploits from different IPs and/or domains are returned from the API and number in the dozens or hundreds.  Now the Analyst needs to find a way to submit these IPs and domain names back into the API as search parameters across multiple Elasticsearch indices \(e.g. EDR domain resolution logs, certain web app outbound traffic logs, etc.\).  The Analyst wants to know whether any of these attempted exploits was followed shortly thereafter by outbound traffic to the suspect IP or domain.  This might indicate a successful exploit of the vulnerability.  These two successive searches would have involved a laborious process of manually manipulating several lists of IP addresses and domain names, and then manually pasting those lists into the search UI of Kibana.

The Elasticsearch API Hunt project automated such a process.  See the included `code_explainer_diagram.png` for an illustration of the program's conceptual execution flow.  What took a focused Analyst 1-2 hours in the past could now be done in 30 minutes from start to finish.  Any future re-runs of the hunt could of course be run in a matter of minutes, since the hunt and its searches were already configured in code.  The project created a "detection-as-code" approach that formally specified, documented, and executed complex search routines against our Elasticsearch API.


# The Project In Action

In November and December of 2021, the Elasticsearch API Hunt project was used to effectively monitor Crane Co's web application infrastructures for attempted and potentially successful exploits of the Log4j vulnerability.  Many hours of time were saved as the code repeatedly ran complex routines of searches against Crane Co's various log sources as application teams worked to patch any instances of the Log4j vulnerability.