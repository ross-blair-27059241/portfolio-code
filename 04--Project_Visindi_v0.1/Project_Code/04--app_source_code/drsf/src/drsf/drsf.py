#                 COPYRIGHT & LICENSE TERMS NOTICE
# =============================================================================
# All following code and content is © 2024 Ross Blair,
# and falls under the licensing terms of Ross Blair's
# derivative of the Business Source License \(BSL\).
# The precise license and warranty terms of the BSL can be found in the file 
# `LICENSE.BSL.md`, which should have been distributed
# along with this code file.  All other use of original-work code and content
# falling outside of this BSL license is prohibited.
# =============================================================================


""" A module for defining the DRSF object and its functions.

<!-- TODO: Content within this section remains a work in progress. -->

"""

# Python standard library codebase imports.
import json

# Non-standard codebase imports.
import networkx as nx


class DRSF():
    """A class encapsulating all component data structures and functions of a DRSF.

    Attributes
    ----------
    DRSF_CONFIG_MAPPINGS: dict
        A dictionary of foundational configuration settings for instantiating the DRSF object.
    entries: array_like
        A list of `drsf.drsf_entry.DRSF_Entry()` objects for instantiating the DRSF object.
    database: dict
        A dictionary that serves as the DRSF database.  Generated from the entries attribute by the instantiate_drsf_database_from_entries() method.
    master_graph: networkx.MultiGraph()
        A multi-edged, bidirectional graph instantiated using the `networkx.MultiGraph()` class.


    Methods
    -------
    instantiate_drsf_database_from_entries()
        Builds the DRSF's database dictionary from the list of DRSF entry objects.

    create_drsf_master_graph(self)
        Builds the DRSF's multi-edged bidirectional "master graph" from the DRSF database dictionary, using multiple helper functions.

    process_auto_gen_entry_assoc_fields(database_dict)
        A helper function to `instantiate_drsf_database_from_entries()`.  Iterate over all DRSF entries, ensuring that all associations between any two given DRSF entries are documented in each entry's section in the DRSF database.  For example, if Adverse Event "A" has Attack "B" listed in its `preceeding_attacks` field, then this function will automatically add a "A" to the `proceeding_adverse_events` fields of Attack "B".

    build_master_graph_nodes_and_edges()
        A helper function to `build_drsf_master_graph()`.  Reads in the DRSF database dictionary, and assembles various data structures used to easily instantiate a multi-edged, bidirectional graph of the `networkx.MultiGraph()` class.

    build_drsf_master_graph(self)
        A helper function to `create_drsf_master_graph()`.  Instantiates a multi-edged bidirectional "master graph" and adds all nodes and edges to that graph.
    """


    def __init__(self, drsf_entries_list, drsf_config_mappings):
        """Constructor
        
        Parameters
        ----------
        drsf_entries_list: array_like
            A list of DRSF_Entry() objects for instantiating the DRSF object.
        drsf_config_mappings: dict
            A dictionary of foundational configuration settings for instantiating the DRSF object.
        """

        self.DRSF_CONFIG_MAPPINGS = drsf_config_mappings
        # Entries are already assumed to be validated.
        self.entries = drsf_entries_list
        # The database is then instantiated from the entries list.
        self.database = self.instantiate_drsf_database_from_entries()
        # And the graph is instantiated from the database.
        self.master_graph = self.create_drsf_master_graph()


    def process_auto_gen_entry_assoc_fields(self, database_dict):
        # TODO FURTHER RESEARCH AND IMPROVEMENT
        # To be completely honest you have no idea why 
        # json.dumps and json.loads was necessary here.
        # But it was the only way that you got around
        # a terrible bug where the following function was
        # actually updating two key-value pairs with 
        # proceeding_adverse_events when they should have been only
        # updating one...  You spent two days trying to wrestle it down,
        # but never arrived at a clear explanation.
        # Putting the dict through this pipeline was how you got it working,
        # but you still don't understand why this workaround was
        # necessary in the first place.
        json_string = json.dumps(database_dict)
        database_dict = json.loads(json_string)
        for k in database_dict['adverse_events'].keys():
            for i in database_dict['adverse_events'][k]['preceeding_attacks']:
                database_dict['attacks'][i]['proceeding_adverse_events'].append(k)
        for k in database_dict['threats'].keys():
            for i in database_dict['threats'][k]['preceeding_attacks']:
                database_dict['attacks'][i]['proceeding_threats'].append(k)
        for k in database_dict['attacks'].keys():
            for i in database_dict['attacks'][k]['preceeding_threats']:
                database_dict['threats'][i]['proceeding_attacks'].append(k)
        for k in database_dict['attacks'].keys():
            for i in database_dict['attacks'][k]['associated_detection_signatures']:
                database_dict['detection_signatures'][i]['associated_attacks'].append(k)
        for k in database_dict['attacks'].keys():
            for i in database_dict['attacks'][k]['associated_mitigating_control_implementations']:
                database_dict['mitigating_control_implementations'][i]['associated_attacks'].append(k)
        for k in database_dict['mitigating_control_implementations'].keys():
            mit_ctrl = database_dict['mitigating_control_implementations'][k]['associated_mitigating_control']
            database_dict['mitigating_controls'][mit_ctrl]['associated_mitigating_control_implementations'].append(database_dict['mitigating_control_implementations'][k]['drsf_id'])
        return database_dict


    def instantiate_drsf_database_from_entries(self):
        # First build the basic sections of the database.
        database = {}
        for key in self.DRSF_CONFIG_MAPPINGS.keys():
            section_title = self.DRSF_CONFIG_MAPPINGS[key]['drsf_database_config']['json_database_section']
            database[section_title] = {}
        # Then load the entries into the database
        for entry in self.entries:
            target_database_section = self.DRSF_CONFIG_MAPPINGS[entry.entry_type]['drsf_database_config']['json_database_section']
            database[target_database_section][entry.id] = {}
            database[target_database_section][entry.id].update(entry.foundational_build_fields)
            for key in self.DRSF_CONFIG_MAPPINGS[entry.entry_type]['drsf_entry_config']['auto_generated_fields'].keys():
                database[target_database_section][entry.id].update(self.DRSF_CONFIG_MAPPINGS[entry.entry_type]['drsf_entry_config']['auto_generated_fields'][key])
            database[target_database_section][entry.id]['source_doc_dir_rel_file_path'] = entry.source_doc_dir_rel_file_path
        # DEBUG
        # print(json.dumps(database, indent=4))
        database = self.process_auto_gen_entry_assoc_fields(database)
        return database


    def build_master_graph_nodes_and_edges(self):
        nodes = {
        "adverse_events": [],
        "threats": [],
        "attacks": [],
        "detection_signatures": [],
        "mitigating_control_implementations": [],
        "mitigating_controls": []
        }
        edges = {
            "metric-impact": [],
            "metric-probability": [],
            "concept-attack_path": [],
            "concept-defense_application_to": []
        }
        for section_label in self.database.keys():
            if section_label in ["adverse_events", "threats", "attacks", "detection_signatures", "mitigating_control_implementations", "mitigating_controls"]:
                for drsf_entry in self.database[section_label].keys():
                    # Insertion of the node into the nodes dict.
                    # Add DRSF entry data as node attributes.
                    node_label = self.database[section_label][drsf_entry]['drsf_id']
                    node_attributes = {}
                    for key in self.database[section_label][drsf_entry].keys():
                        node_attributes[key] = self.database[section_label][drsf_entry][key]
                    node = (node_label, node_attributes)
                    nodes[section_label].append(node)
                    # Insertion of all edges by category into our edges dict.
                    if self.database[section_label][drsf_entry]['drsf_entry_type'] == "adverse_event":
                        for prec_atk_entry in self.database[section_label][drsf_entry]['preceeding_attacks']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = prec_atk_entry
                            edge_type = "metric-impact"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                            edge_from_node = prec_atk_entry
                            edge_to_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_type = "concept-attack_path"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                    elif self.database[section_label][drsf_entry]['drsf_entry_type'] == "threat":
                        for prec_atk_entry in self.database[section_label][drsf_entry]['preceeding_attacks']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = prec_atk_entry
                            edge_type = "metric-impact"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                        for proc_atk_entry in self.database[section_label][drsf_entry]['proceeding_attacks']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = proc_atk_entry
                            edge_type = "metric-probability"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                            edge_type = "concept-attack_path"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                    elif self.database[section_label][drsf_entry]['drsf_entry_type'] == "attack":
                        for prec_threat_entry in self.database[section_label][drsf_entry]['preceeding_threats']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = prec_threat_entry
                            edge_type = "metric-impact"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                        for proc_threat_entry in self.database[section_label][drsf_entry]['proceeding_threats']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = proc_threat_entry
                            edge_type = "metric-probability"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                            edge_type = "concept-attack_path"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                    elif self.database[section_label][drsf_entry]['drsf_entry_type'] == "detection_signature":
                        for assoc_atk in self.database[section_label][drsf_entry]['associated_attacks']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = assoc_atk
                            edge_type = "concept-defense_application_to"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)   
                    elif self.database[section_label][drsf_entry]['drsf_entry_type'] == "mitigating_control_implementation":
                        for assoc_atk in self.database[section_label][drsf_entry]['associated_attacks']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = assoc_atk
                            edge_type = "metric-probability"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                            edge_type = "concept-defense_application_to"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
                    elif self.database[section_label][drsf_entry]['drsf_entry_type'] == "mitigating_control":
                        for assoc_mit_ctrl_imp in self.database[section_label][drsf_entry]['associated_mitigating_control_implementations']:
                            edge_from_node = self.database[section_label][drsf_entry]['drsf_id']
                            edge_to_node = assoc_mit_ctrl_imp
                            edge_type = "concept-defense_application_to"
                            edge = (edge_from_node, edge_to_node, {"edge_type": edge_type})
                            edges[edge_type].append(edge)
        return (nodes, edges)


    def build_drsf_master_graph(self):
        nodes_and_edges = self.build_master_graph_nodes_and_edges()
        nodes_dict = nodes_and_edges[0]
        edges_dict = nodes_and_edges[1]
        G = nx.MultiDiGraph()
        for key in nodes_dict.keys():
            G.add_nodes_from(nodes_dict[key])
        for key in edges_dict.keys():
            G.add_edges_from(edges_dict[key])
        return G


    def create_drsf_master_graph(self):
        self.master_graph = self.build_drsf_master_graph()
        return self.master_graph