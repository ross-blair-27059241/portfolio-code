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


import json
import re
import os
import random
import yaml
import frontmatter
import math
import networkx as nx
import plotly.graph_objects as go


def gen_drsf_entry_file_path_list_from_source_doc_dir(source_doc_dir, drsf_config_mappings):
    drsf_entry_file_paths = []
    drsf_entry_dirs = []
    for entry_type in drsf_config_mappings.keys():
        rel_dir_path = drsf_config_mappings[entry_type]['drsf_documentation_config']['drsf_source_docs_section_rel_dir']
        full_dir_path = source_doc_dir + "/" + rel_dir_path
        drsf_entry_dirs.append(full_dir_path)
    for dir in drsf_entry_dirs:
        for fname in os.listdir(dir):
            reg_pattern = re.compile(r"[A-Z]{2,3}--[0-9]{6}.md")
            if re.match(reg_pattern, fname):
                entry_file_path = os.path.join(dir, fname)
                drsf_entry_file_paths.append(entry_file_path)
            else:
                continue
    return drsf_entry_file_paths


def parse_all_command_function_sections_orig_content(entry_source_doc_file_path):
    # First, open the file and read in the lines.
    with open (entry_source_doc_file_path, "r") as file:
        jb_myst_source_content_lines = file.readlines()
    file.close()

    command_function_captures_list = []

    extract_on = False

    command_function_capture = {}


    for line_number, line_contents in enumerate(jb_myst_source_content_lines):
        if extract_on == False and line_contents.lstrip() == "```\n" and jb_myst_source_content_lines[line_number + 1].lstrip() == "#!\n":
            extract_on = True
            command_function_capture['start_line_ennum_counter'] = line_number
            command_function_capture['orig_content'] = []
            command_function_capture['orig_indent'] = re.match(r'\s*', line_contents).group()
            command_function_capture['orig_content'].append(jb_myst_source_content_lines[line_number])
        elif extract_on == True and line_contents.lstrip() in ["```\n", "```"] and jb_myst_source_content_lines[line_number - 1].lstrip() == "#!\n":
            command_function_capture['end_line_ennum_counter'] = line_number
            command_function_capture['orig_content'].append(jb_myst_source_content_lines[line_number])
            command_function_captures_list.append(command_function_capture)
        elif extract_on == True:
            command_function_capture['orig_content'].append(jb_myst_source_content_lines[line_number])
        else:
            continue

    return command_function_captures_list


def determine_command_function_type_for_all_sections(command_function_captures_list):
    # Now that we have the original contents of every command function section,
    # we'll need to iterate through each item and determine its
    # command function type.  This is essential to understand for ensuring
    # proper parsing of parameters, and the execution order of different
    # command function sections.
    for command_function_section in command_function_captures_list:
        command_function_section['command_function_parameters'] = {}
        parameters_dict = {}
        for i in command_function_section['orig_content']:
            if i.strip() == "#!" or i.strip() == "```":
                continue
            else:
                i = i.lstrip()
                i = i.rstrip()
                command_function_parameter = i.split(': ')
                if command_function_parameter[0] == "command_function_type":
                    parameters_dict['type'] = command_function_parameter[1]
                else:
                    continue
        command_function_section['command_function_parameters'] = parameters_dict
    return command_function_captures_list


def parse_foundational_syntax_params(command_function_capture):
    syntax_dict = {}
    json_string = ""
    capture = False
    capture_start_string = "drsf_entry_foundational_build_config: \"\"\"\n"
    capture_end_string = "\"\"\"\n"
    for i in command_function_capture['orig_content']:
        if capture == False and i == capture_start_string:
            capture = True
        elif capture == True and i == capture_end_string:
            capture = False
        elif capture == True:
            string = i.strip()
            json_string = json_string + string
        else:
            continue
    syntax_dict = json.loads(json_string)
    return syntax_dict


def set_foundational_build_fields_from_file(entry_source_doc_file_path):
    command_function_captures_list = parse_all_command_function_sections_orig_content(entry_source_doc_file_path)
    command_function_captures_list = determine_command_function_type_for_all_sections(command_function_captures_list)
    build_dict = {}
    for command_function_capture in command_function_captures_list:
        command_function_type = command_function_capture['command_function_parameters']['type']
        if command_function_type == "drsf_entry_foundational_build":
            build_dict = parse_foundational_syntax_params(command_function_capture)
        else:
            continue
    return build_dict

# TODO The function logic looks way off here.  You need to review.
def create_entry_build_dict_from_existing_entry_file(entry_source_doc_file_path, drsf_config_mappings):
    entry_build_dict = {}
    foundational_build_fields = set_foundational_build_fields_from_file(entry_source_doc_file_path)
    entry_build_dict['entry_type'] = foundational_build_fields['drsf_entry_type']
    entry_build_dict['title'] = foundational_build_fields['drsf_title']
    entry_build_dict['id'] = foundational_build_fields['drsf_id']
    entry_build_dict['foundational_build_fields'] = foundational_build_fields
    entry_build_dict['auto_generated_fields'] = drsf_config_mappings[foundational_build_fields['drsf_entry_type']]
    entry_file_name = entry_build_dict['id'] + ".md"
    entry_build_dict['source_doc_dir_rel_file_path'] = drsf_config_mappings[foundational_build_fields['drsf_entry_type']]['drsf_documentation_config']['drsf_source_docs_section_rel_dir'] + "/" + entry_file_name
    return entry_build_dict


def gen_rand_id(digit_length, floor=1):
    top = 10**digit_length
    if floor > top:
        raise ValueError(f"Floor '{floor}' must be less than requested top '{top}'")
    return f'{random.randrange(floor, top):0{digit_length}}'


def generate_unique_entry_id(new_entry_type, existing_entry_ids, drsf_config_mappings):
    id_prefix = ""
    unique_id_generated = False
    while unique_id_generated == False:
        id_prefix = drsf_config_mappings[new_entry_type]['id_prefix'] + "--"
        id_number = gen_rand_id(6)
        drsf_id = id_prefix + id_number
        if drsf_id not in existing_entry_ids:
            unique_id_generated = True
            continue
        else:
            continue
    return drsf_id


def create_entry_build_dict_from_template_file(new_entry_type, new_entry_title, new_entry_id, source_doc_dir, source_doc_templates_dir, drsf_config_mappings):
    entry_build_dict = {}
    entry_build_dict['entry_type'] = new_entry_type
    entry_build_dict['title'] = new_entry_title
    entry_build_dict['id'] = new_entry_id
    entry_build_dict['foundational_build_fields'] = drsf_config_mappings[new_entry_type]['drsf_entry_config']['foundational_build_fields']
    entry_build_dict['foundational_build_fields']['drsf_id'] = entry_build_dict['id']
    entry_build_dict['foundational_build_fields']['drsf_title'] = entry_build_dict['title']
    entry_build_dict['auto_generated_fields'] = drsf_config_mappings[new_entry_type]['drsf_entry_config']['auto_generated_fields']
    entry_file_name = entry_build_dict['id'] + ".md"
    entry_build_dict['source_doc_dir_rel_file_path'] = drsf_config_mappings[new_entry_type]['drsf_documentation_config']['drsf_source_docs_section_rel_dir'] + "/" + entry_file_name
    return entry_build_dict


def insert_new_entry_source_doc_into_toc(drsf_config_mappings, drsf_entry_obj, source_doc_dir):
    insert_result = False
    toc_file_path = source_doc_dir + "/" + "_toc.yml"
    with open(toc_file_path, "rt", encoding="utf-8") as file:
        yaml_dict = yaml.safe_load(file)
    file.close()
    target_part_caption = drsf_config_mappings[drsf_entry_obj.entry_type]['drsf_documentation_config']['drsf_toc_config']['target_caption']
    target_chapter = drsf_config_mappings[drsf_entry_obj.entry_type]['drsf_documentation_config']['drsf_toc_config']['target_chapter']
    section_dir_prefix = drsf_config_mappings[drsf_entry_obj.entry_type]['drsf_documentation_config']['drsf_toc_config']['section_dir_prefix']
    parts_index_counter = 0
    for part in yaml_dict['parts']:
        if part['caption'] == target_part_caption:
            break
        else:
            parts_index_counter = parts_index_counter + 1
            continue
    for chapter in yaml_dict['parts'][parts_index_counter]['chapters']:
        if chapter['file'] == target_chapter:
            if "sections" in chapter:
                chapter['sections'].append({"file": section_dir_prefix + "/" + drsf_entry_obj.id})
            else:
                chapter['sections'] = []
                chapter['sections'].append({"file": section_dir_prefix + "/" + drsf_entry_obj.id})
            with open(toc_file_path, "wt", encoding="utf-8") as file:
                yaml.dump(yaml_dict, file, sort_keys=False)
            file.close
            insert_result = True
        else:
            continue
    return insert_result


def build_foundational_syntax_section_skeleton():
    foundational_syntax_skeleton = [
        "\n",
        "# DSRF Foundational Build Syntax\n",
        "\n",
        "The following syntax section contains the \"foundational build\" configuration values for this DRSF Entry.  Every field within the `build_config` dictionary must contain a value that satisfies DRSF graph build criteria.\n",
        "\n",
        "```\n",
        "#!\n",
        "command_function_type: drsf_entry_foundational_build\n",
        "drsf_entry_foundational_build_config: \"\"\"\n",
        "\"\"\"\n"
        "#!\n",
        "```"
    ]
    return foundational_syntax_skeleton

def write_foundational_build_section(entry_source_doc_file_path, foundational_build_fields_dict):
    file = open(entry_source_doc_file_path, "a")
    syntax_skeleton = build_foundational_syntax_section_skeleton()
    for line in syntax_skeleton:
        if line == "drsf_entry_foundational_build_config: \"\"\"\n":
            file.write(line)
            json.dump(foundational_build_fields_dict, file, indent=4)
            file.write("\n")
        else:
            file.write(line)
    return None


def insert_to_existing_yml_frontmatter(input_values_dict, source_file):
    post = frontmatter.load(source_file)
    for key in input_values_dict.keys():
        if key in post['myst']['substitutions'].keys():
            post['myst']['substitutions'][key] = input_values_dict[key]
        else:
            continue
    with open(source_file, 'wb') as f:
        frontmatter.dump(post, f)
    f.close()
    return None


def remove_foundational_build_syntax_section(entry_file_path):
    with open(entry_file_path, "r") as file:
        content_lines = file.readlines()
    file.close()
    match_start_string = "# DSRF Foundational Build Syntax(\r\n|\r|\n)"
    insert_area_match_start_pattern = re.compile(match_start_string)
    pre_insert = []
    pre_insert_copy = True
    for index, line in enumerate(content_lines):
        if pre_insert_copy == True:
            if not re.match(insert_area_match_start_pattern, line):
                pre_insert.append(line)
            # If the line does match our start pattern.
            else:
                pre_insert_copy = False
    # Ensure to remove trailing lines that contain nothing but the newline character,
    # since Foundation Build section is always at the
    # end of an entry file.
    while pre_insert[-1] == "\n":
        pre_insert.pop()
    edited_content_string = ''.join(pre_insert)
    with open(entry_file_path, "w") as file:
        file.write(edited_content_string)
    file.close()
    return entry_file_path


def edit_target_auto_doc_assoc_field_section(entry_file_path, auto_doc_assoc_field, auto_doc_assoc_field_list, auto_documented_field_mapping_dict, drsf_obj_database):
    with open(entry_file_path, "r") as file:
        content_lines = file.readlines()
    file.close()
    match_start_string = auto_documented_field_mapping_dict[auto_doc_assoc_field]['entry_doc_section']
    match_stop_string = "^# (.*)(\r\n|\r|\n)"
    match_start_pattern = re.compile(match_start_string)
    match_stop_pattern = re.compile(match_stop_string)
    pre_auto_doc_section = []
    auto_doc_section = []
    post_auto_doc_section = []
    pre_section_copy = True
    post_section_copy = False
    section_match = False
    for line in content_lines:
        if pre_section_copy == True:
            if re.match(match_start_pattern, line):
                pre_section_copy = False
                auto_doc_section.append(line)
                section_match = True
            else:
                pre_auto_doc_section.append(line)
            continue
        if section_match == True:
            if re.match(match_stop_pattern, line):
                section_match = False
                post_section_copy = True
                post_auto_doc_section.append(line)
            else:
                auto_doc_section.append(line)
            continue
        if post_section_copy == True:
            post_auto_doc_section.append(line)
            continue
    if len(auto_doc_assoc_field_list) == 0:
        edited_content_lines = pre_auto_doc_section + post_auto_doc_section
    else:
        edited_auto_doc_section = []
        edited_auto_doc_section.append(auto_doc_section[0])
        edited_auto_doc_section.append("\n")
        for i in auto_doc_assoc_field_list:
            # Insert Jupyter Book reference syntax.
            db_section = auto_documented_field_mapping_dict[auto_doc_assoc_field]['database_ref_section']
            insert_assoc_entry_id = drsf_obj_database[db_section][i]['drsf_id']
            insert_assoc_entry_title = drsf_obj_database[db_section][i]['drsf_title']
            insert_assoc_entry_rel_path = "../" + drsf_obj_database[db_section][i]['source_doc_dir_rel_file_path'].split("P2--drsf_entries/")[1].split(".md")[0]
            insert_line = "{doc}" + "`" + insert_assoc_entry_id + ": " + insert_assoc_entry_title + " <" + insert_assoc_entry_rel_path + ">`" + "\n"
            edited_auto_doc_section.append(insert_line)
            edited_auto_doc_section.append("\n")
        edited_content_lines = pre_auto_doc_section + edited_auto_doc_section + post_auto_doc_section
    edited_content_string = ''.join(edited_content_lines)
    with open(entry_file_path, "w") as file:
        file.write(edited_content_string)
    file.close()
    return None



# Derive a simpler single-edge directed graph derived from the nodes and edges
# of the master multi-edge directed graph.  This graph will represent a simple
# visual representation of the entire drsf graph for illustrating in our
# Jupyter Book documentation.
def create_drsf_illustrated_graph(drsf_master_graph, html_output_file):
    # The first thing that we want to accomplish is to build a single-edge
    # directed graph using "metric-impact" edges and inverted
    # "concept-defense_application_to" edges.  Using these specific edges
    # will build a directional graph that flows from adverse events down to their preceeding
    # attacks and threats, and then out to the detections and controls.
    # This is an essential step in generating some very rudimentary metrics
    # that will be key to properly illustrating our final visualization graph
    # using Plotly.
    G1 = nx.DiGraph()
    G1.add_nodes_from(drsf_master_graph.nodes(data=True))
    impact_path_edges = [(u,v) for u,v,e in drsf_master_graph.edges(data=True) if e['edge_type']=="metric-impact"]
    # Note the inversion here of the defense application edges from the orginal graph.
    # We need this inversion to get the distance calculation correct.
    inverted_defense_application_edges = [(v,u) for u,v,e in drsf_master_graph.edges(data=True) if e['edge_type']=="concept-defense_application_to"]
    G1.add_edges_from(impact_path_edges)
    G1.add_edges_from(inverted_defense_application_edges)
    # Now we'll put this single-edge directed graph to some work.
    # When we think about how we want to view this graph, it makes sense that our
    # nodes for adverse events would be visually at the top of our graph.
    # Furthermore, as any DRSF entry gets "farther away" from any adverse event,
    # it should get placed vertically lower in the graph relative to other entries.
    # Doing all this involves
    # manually editing the graph-layout's z-coordinates.
    # The challenge is to programatically calculate every node's distance from any
    # of its associated adverse event nodes.
    # We'll use a NetworkX function to derive the shortest path
    # between any given node, and all the rest of the nodes in the graph.
    # Remember, we're dealing with a directed graph here, so the output of this
    # spl function will only calculate paths "along the flow" of the directed graph.
    spl = dict(nx.all_pairs_shortest_path_length(G1))
    # We need to get the longest possible distance to any adverse event in our graph.
    # This first requires that we collect all distances from an adverse event to any
    # other connected node in the graph.
    agg_distances_to_ae = set()
    # Create a dict of every entry's respective distance to any AE node in our graph.
    entry_distances_to_ae = {}
    # Build the dict of any entry's distances to an AE node.
    for key in spl.keys():
        # Remember, we're dealing with a directed graph which flows from AE nodes on down the line.
        # Therefore, we're only interested in collecting path distances extending from any adverse
        # event to its linked nodes.
        if key.startswith("AE--") == True:
            for nested_key in spl[key].keys():
                    # Add this distance to the aggregate distance to AE set.
                    agg_distances_to_ae.add(spl[key][nested_key])
                    # Build the dictionary.
                    if nested_key in entry_distances_to_ae.keys():
                        entry_distances_to_ae[nested_key].add(spl[key][nested_key])
                    else:
                        entry_distances_to_ae[nested_key] = set()
                        entry_distances_to_ae[nested_key].add(spl[key][nested_key])
        else:
            continue
    # Now determine each entry's minimum distance to any linked AE node in the graph.
    # Take that and add this as an attribute to the nodes in the graph. 
    for key in entry_distances_to_ae.keys():
        min_dist_to_ae = min(entry_distances_to_ae[key])
        G1.nodes[key]['nearest_dist_to_adverse_event'] = min_dist_to_ae
    # Calculate the maximum distance between any AE, and any of the
    # connected nodes.  This will inform the scale of our three dimensional graph.
    max_agg_distance_to_ae = max(agg_distances_to_ae)
    # Build the initial coordinate layout of our 3D graph.
    # Here we'll experiment with the kamada kawai layout function to create our
    # initial coordinates.
    layout_3d = nx.kamada_kawai_layout(G1, dim = 3, scale = max_agg_distance_to_ae)
    # Then modify the y coordinates of all entries based on its respective distance
    # to an adverse event.
    for key in layout_3d.keys():
        layout_3d[key][0] = (layout_3d[key][0])
        layout_3d[key][1] = (layout_3d[key][1])
        # Here's the exact moment of z-coordinate modification.
        # Note that we're using the square root in order to
        # reduce the scale of the z-coordinate verticality
        # relative to the other nodes.
        layout_3d[key][2] = abs(layout_3d[key][2] * math.sqrt(max_agg_distance_to_ae - G1.nodes[key]['nearest_dist_to_adverse_event']))
    # We already have instantiated a NetworkX graph, and constructed
    # a layout containing the x, y, and z coordinates for all of its nodes.
    # We still need to separate the x, y, and z coordinates of our graph's nodes in order to
    # be properly processed by Plotly.
    x_nodes = [layout_3d[key][0] for key in layout_3d.keys()]
    y_nodes = [layout_3d[key][1] for key in layout_3d.keys()]
    z_nodes = [layout_3d[key][2] for key in layout_3d.keys()]
    # Next, we'll create lists that contain the start and end coordinates
    # for each edge.
    edge_x_coords = []
    edge_y_coords = []
    edge_z_coords = []
    # Populate these coordinate lists with the coordinates of the
    # 3D layout.
    for edge in G1.edges():
            x_coords = [layout_3d[edge[0]][0],layout_3d[edge[1]][0],None]
            edge_x_coords += x_coords
            y_coords = [layout_3d[edge[0]][1],layout_3d[edge[1]][1],None]
            edge_y_coords += y_coords
            z_coords = [layout_3d[edge[0]][2],layout_3d[edge[1]][2],None]
            edge_z_coords += z_coords
    # We also want to capture the DRSF ID and entry type, listed in the same
    # order as our graph's nodes.  This will be used to properly illustrate our
    # graph with hover labels and different node colors.
    node_drsf_ids = []
    node_drsf_titles = []
    node_drsf_entry_types = []
    # These integers refer to certain colors that Plotly's functions
    # can apply to nodes.
    entry_type_to_color_index = {
        "adverse_event": 1,
        "threat": 2,
        "attack": 3,
        "detection_signature": 4,
        "mitigating_control_implementation": 5,
        "mitigating_control": 6
    }
    for node in G1.nodes(data=True):
        node_drsf_ids.append(node[0])
        node_drsf_entry_types.append(entry_type_to_color_index[node[1]['drsf_entry_type']])
        node_drsf_titles.append(node[1]['drsf_title'])
    #create a trace for the edges
    trace_edges = go.Scatter3d(
        x=edge_x_coords,
        y=edge_y_coords,
        z=edge_z_coords,
        mode='lines',
        line=dict(color='rgb(125,125,125)', width=1),
        hoverinfo='none')
    #create a trace for the nodes
    trace_nodes = go.Scatter3d(
        x = x_nodes,
        y = y_nodes,
        z = z_nodes,
        mode = 'markers+text',
        marker = dict(
            symbol = 'circle',
            size = 10,
            color = node_drsf_entry_types,
            colorscale = 'Viridis',
            line = dict(color='rgb(50,50,50)', width = 0.5)),
            text = node_drsf_ids,
            hovertext = node_drsf_titles,
            hoverinfo = "text"
        )
    axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='', showspikes=False)
    layout = go.Layout(
            title="DRSF Attack Graph",
            width=500,
            height=500,
            showlegend=False,
            font=dict(
                family="Courier New, monospace",
                size=12
            ),
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ))
    #Include the traces we want to plot and create a figure
    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)
    html_string = fig.to_html()
    f = open(html_output_file, 'w')
    f.write(html_string)
    f.close()
    return None