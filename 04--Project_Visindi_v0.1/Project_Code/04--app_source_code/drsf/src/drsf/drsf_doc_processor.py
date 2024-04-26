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
import drsf.drsf_doc_processor_helpers
import drsf.drsf_entry
import drsf.drsf
import os
import re
import shutil


class DRSFDocProcessor():

    def __init__(self, drsf_base_config_mappings_file_path, drsf_source_docs_template_dir_path, drsf_entry_templates_dir_path, drsf_source_docs_dev_dir_path, drsf_source_docs_staging_dir_path, drsf_source_docs_build_dir_path):
        self.BASE_CONFIG_MAPPINGS = self.load_drsf_config_mappings(drsf_base_config_mappings_file_path)
        self.ID_PREFIX_TO_ENTRY_TYPE_MAPPING = self.gen_id_prefix_to_entry_type_mapping()
        self.DRSF_SOURCE_DOCS_TEMPLATE_DIR = drsf_source_docs_template_dir_path
        self.DRSF_ENTRY_TEMPLATES_DIR = drsf_entry_templates_dir_path
        self.SOURCE_DOCS_DEV_DIR = drsf_source_docs_dev_dir_path
        self.SOURCE_DOCS_STAGING_DIR = drsf_source_docs_staging_dir_path
        self.SOURCE_DOCS_BUILD_DIR = drsf_source_docs_build_dir_path
        self.current_instantiation_directory = ""


    # The following three functions are merely establishing all the "mappings"
    # that the code uses throughout its document processing operations.

    def load_drsf_config_mappings(self, drsf_base_config_mappings_file_path):
        f = open(drsf_base_config_mappings_file_path)
        json_data = json.load(f)
        f.close()
        return json_data
    
    def gen_id_prefix_to_entry_type_mapping(self):
        mapping = {}
        for key in self.BASE_CONFIG_MAPPINGS.keys():
            entry_type = key
            id_prefix = self.BASE_CONFIG_MAPPINGS[key]['id_prefix']
            mapping[id_prefix] = entry_type
        return mapping


    def wipe_source_doc_dirs_and_build_from_scratch(self):
        if os.path.exists(os.path.join(os.getcwd(), self.SOURCE_DOCS_BUILD_DIR)) == True:
            shutil.rmtree(os.path.join(os.getcwd(), self.SOURCE_DOCS_BUILD_DIR))
        if os.path.exists(os.path.join(os.getcwd(), self.SOURCE_DOCS_STAGING_DIR)) == True:
            shutil.rmtree(os.path.join(os.getcwd(), self.SOURCE_DOCS_STAGING_DIR))
        if os.path.exists(os.path.join(os.getcwd(), self.SOURCE_DOCS_DEV_DIR)) == True:
            shutil.rmtree(os.path.join(os.getcwd(), self.SOURCE_DOCS_DEV_DIR))
        shutil.copytree(self.DRSF_SOURCE_DOCS_TEMPLATE_DIR, self.SOURCE_DOCS_DEV_DIR)
        return None


    # The most fundamental function.  Creating a new DRSF entry from a template file.
    def create_new_drsf_entry(self, new_entry_type, new_entry_title):
        if (new_entry_type in self.BASE_CONFIG_MAPPINGS.keys()) == False:
            print("CRITICAL ERROR: The entry_type parameter \"{}\" does not exist.  Please refer to the following list for all valid entry_type parameters.".format(new_entry_type))
            for possible_entry_type in self.BASE_CONFIG_MAPPINGS.keys().keys():
                print(possible_entry_type)
            return None
        # We're creating a simple listing of all existing entry source documents.
        # This allows us to engage in some simple validation checks to ensure
        # unique DRSF IDs and entry titles.
        existing_entry_ids = []
        existing_entry_titles = []
        entry_source_doc_file_paths = drsf.drsf_doc_processor_helpers.gen_drsf_entry_file_path_list_from_source_doc_dir(self.SOURCE_DOCS_DEV_DIR, self.BASE_CONFIG_MAPPINGS)
        for entry_source_doc_file_path in entry_source_doc_file_paths:
            entry_build_dict = drsf.drsf_doc_processor_helpers.create_entry_build_dict_from_existing_entry_file(entry_source_doc_file_path, self.BASE_CONFIG_MAPPINGS)
            entry = drsf.drsf_entry.DRSF_Entry(entry_build_dict)
            existing_entry_ids.append(entry.id)
            existing_entry_titles.append(entry.title)
        if new_entry_title in existing_entry_titles:
            print("CRITICAL ERROR: The DRSF entry title parameter \"{}\" you submitted already exists.  All DRSF entry titles must be unique.".format(new_entry_title))
            return None
        else:
            # Provided we've passed the validations, proceed to create the new DRSF entry.
            new_entry_id = drsf.drsf_doc_processor_helpers.generate_unique_entry_id(new_entry_type, existing_entry_ids, self.BASE_CONFIG_MAPPINGS)
            new_entry_build_dict = drsf.drsf_doc_processor_helpers.create_entry_build_dict_from_template_file(new_entry_type, new_entry_title, new_entry_id, self.SOURCE_DOCS_DEV_DIR, self.DRSF_ENTRY_TEMPLATES_DIR, self.BASE_CONFIG_MAPPINGS)
            new_entry = drsf.drsf_entry.DRSF_Entry(new_entry_build_dict)
            # Ensure that this new DRSF entry is properly inserted in the Table of Contents file
            # `_toc.yml` in the source doc DEV directory.  This can be a hard thing for a
            # Analyst to remember when creating each entry, and it doesn't lend the operation
            # to automation, so the code does it for them.
            if drsf.drsf_doc_processor_helpers.insert_new_entry_source_doc_into_toc(self.BASE_CONFIG_MAPPINGS, new_entry, self.SOURCE_DOCS_DEV_DIR) == True:
                new_entry_template_file_path = self.DRSF_ENTRY_TEMPLATES_DIR + "/" + self.BASE_CONFIG_MAPPINGS[new_entry.entry_type]['source_doc_template_file']
                new_entry_source_doc_file_path = self.SOURCE_DOCS_DEV_DIR + "/" + new_entry.source_doc_dir_rel_file_path
                shutil.copyfile(new_entry_template_file_path, new_entry_source_doc_file_path)
                drsf.drsf_doc_processor_helpers.write_foundational_build_section(new_entry_source_doc_file_path, new_entry.foundational_build_fields)
                drsf.drsf_doc_processor_helpers.insert_to_existing_yml_frontmatter(new_entry.foundational_build_fields, new_entry_source_doc_file_path)
                return new_entry
            else:
                print("ERROR: The program was unable to update the Table of Contents with this DRSF entry.  This could be due to an error in the formatting of the _toc.yml file, or inherent in the program's logic.  Please review the formatting of the TOC file, and/or the program's code.")
                return None


    # Editing an existing entry's foundational build field.
    def edit_existing_entry_foundational_build_field(self, existing_entry_id, found_build_field_name, found_build_field_new_value: str|list):
        # First we want to load the entry from the proper file in the DEV directory.
        id_prefix = re.search(r"[A-Z]{2,3}", existing_entry_id).group()
        entry_type = self.ID_PREFIX_TO_ENTRY_TYPE_MAPPING[id_prefix]
        entry_file_name = existing_entry_id + ".md"
        entry_file_path = self.SOURCE_DOCS_DEV_DIR + "/" + self.BASE_CONFIG_MAPPINGS[entry_type]['drsf_documentation_config']['drsf_source_docs_section_rel_dir'] + "/" + entry_file_name
        # Then we need to instantiate the entry object and modify the target field.
        entry_build_dict = drsf.drsf_doc_processor_helpers.create_entry_build_dict_from_existing_entry_file(entry_file_path, self.BASE_CONFIG_MAPPINGS)
        existing_entry = drsf.drsf_entry.DRSF_Entry(entry_build_dict)
        existing_entry = existing_entry.set_foundational_build_field(found_build_field_name, found_build_field_new_value)
        # Finally, edit this entry's source doc file to account for the changed field.
        entry_file_path = drsf.drsf_doc_processor_helpers.remove_foundational_build_syntax_section(entry_file_path)
        drsf.drsf_doc_processor_helpers.write_foundational_build_section(entry_file_path, entry_build_dict['foundational_build_fields'])
        return existing_entry


    def instantiate_drsf_obj_from_source_doc_dir(self, source_doc_dir):
        entry_source_doc_file_paths = drsf.drsf_doc_processor_helpers.gen_drsf_entry_file_path_list_from_source_doc_dir(source_doc_dir, self.BASE_CONFIG_MAPPINGS)
        are_entries_validated = True
        drsf_entries = []
        output_entry_ids = []
        output_entry_titles = []
        for entry_source_doc_file_path in entry_source_doc_file_paths:
            entry_build_dict = drsf.drsf_doc_processor_helpers.create_entry_build_dict_from_existing_entry_file(entry_source_doc_file_path, self.BASE_CONFIG_MAPPINGS)
            entry = drsf.drsf_entry.DRSF_Entry(entry_build_dict)
            # Run first entry validation check.
            # Checking that the id from the Foundational Build Syntax section matches
            # the entry's file name.
            if (entry.id + ".md") != os.path.basename(entry_source_doc_file_path):
                print("CRITICAL ERROR: The entry's id \"{}\" (derived from the entry file's Foundational Build Syntax) does not match the id in the entry's file name \"{}\".  These must match, or the DRSF Jupyter book will not build correctly.".format(entry.id, os.path.basename(entry_source_doc_file_path)))
                are_entries_validated = False
            output_entry_ids.append(entry.id)
            output_entry_titles.append(entry.title)
            drsf_entries.append(entry)
        # Now run the rest of the validation checks on the entries.
        assoc_entry_field_names = ["preceeding_attacks", "preceeding_threats", "associated_detection_signatures", "associated_mitigating_control_implementations", "associated_mitigating_control" ]
        for entry in drsf_entries:
            # Checking for unique IDs for all entries.
            if output_entry_ids.count(entry.id) > 1:
                print("CRITICAL ERROR: There are two DRSF entries with the id \"{}\".  The DRSF code object will not be instantiated.  Please review your source documents and remove this duplication.".format(entry.id))
                are_entries_validated = False
            # Checking for unique titles for all entries.
            if output_entry_titles.count(entry.title) > 1:
                print("CRITICAL ERROR: There are two DRSF entries with the title \"{}\".  The DRSF code object will not be instantiated.  Please review your source documents and remove this duplication.".format(entry.title))
                are_entries_validated = False
            # Checking that all referenced associated entry ids in the Foundational Build Syntax section correspond
            # to existing entries.
            for field in entry.foundational_build_fields.keys():
                if field in assoc_entry_field_names:
                    for e_id in entry.foundational_build_fields[field]:
                        if e_id not in output_entry_ids:
                                print("CRITICAL ERROR: The DRSF entry \"{}\" refers to an associated entry id \"{}\" in its \"{}\" field.  This associated entry could not be found in the source docs.  All associated entries must exist in order to build a valid DRSF code object.".format(entry.id, e_id, field))
                                are_entries_validated = False
                        else:
                            continue
                else:
                    continue
        if are_entries_validated == False:
            drsf_obj = None
        else:
            drsf_obj = drsf.drsf.DRSF(drsf_entries, self.BASE_CONFIG_MAPPINGS)
        return drsf_obj


    def write_auto_doc_assoc_fields_into_entry_source_docs(self, drsf_obj, source_doc_dir):
        # Building a reference list and mappings dict that will be useful
        # as we iterate through the drsf_obj's database and write those values
        # back into the source docs.
        drsf_entry_type_sections = []
        for k in self.BASE_CONFIG_MAPPINGS.keys():
            drsf_entry_type_sections.append(self.BASE_CONFIG_MAPPINGS[k]['drsf_database_config']['json_database_section'])
        auto_documented_assoc_entry_fields_mapping_dict = {}
        for k in self.BASE_CONFIG_MAPPINGS.keys():
            for field in self.BASE_CONFIG_MAPPINGS[k]['drsf_documentation_config']['auto_documented_fields_mappings']['auto_documented_associated_entry_fields'].keys():
                if field in auto_documented_assoc_entry_fields_mapping_dict.keys():
                    continue
                else:
                    auto_documented_assoc_entry_fields_mapping_dict[field] = self.BASE_CONFIG_MAPPINGS[k]['drsf_documentation_config']['auto_documented_fields_mappings']['auto_documented_associated_entry_fields'][field]
        # Iterate through the drsf_obj's database.  Take the fields that it has automatically processed,
        # and ensure that those fields are written back in to the DRSF entry source document.
        for k in drsf_obj.database.keys():
            if k in drsf_entry_type_sections:
                for nk in drsf_obj.database[k].keys():
                    entry_to_edit_file_path = source_doc_dir + "/" + drsf_obj.database[k][nk]['source_doc_dir_rel_file_path']
                    for ek in drsf_obj.database[k][nk].keys():
                        if ek in auto_documented_assoc_entry_fields_mapping_dict.keys():
                            edited_file_path = drsf.drsf_doc_processor_helpers.edit_target_auto_doc_assoc_field_section(entry_to_edit_file_path, ek, drsf_obj.database[k][nk][ek], auto_documented_assoc_entry_fields_mapping_dict, drsf_obj.database)
                        else:
                            continue
            else:
                continue
        return None


    def deploy_dev_source_docs_to_staging_dir(self):
        # Copy all source doc files from the dev dir into the staging
        # dir.
        shutil.copytree(self.SOURCE_DOCS_DEV_DIR, self.SOURCE_DOCS_STAGING_DIR)
        # Now instantiate the DRSF object from the entries in this new STAGING dir.
        # Note that this instantiation will automatically kick off all associated entry
        # calculations and other metrics that the DRSF database and graph are designed
        # to process.
        drsf_obj = self.instantiate_drsf_obj_from_source_doc_dir(self.SOURCE_DOCS_STAGING_DIR)
        self.write_auto_doc_assoc_fields_into_entry_source_docs(drsf_obj, self.SOURCE_DOCS_STAGING_DIR)
        html_output_file = self.SOURCE_DOCS_STAGING_DIR + "/" + "01-content_files/html_files/drsf_illustrated_graph.html"
        drsf.drsf_doc_processor_helpers.create_drsf_illustrated_graph(drsf_obj.master_graph, html_output_file)
        entry_source_doc_file_paths = drsf.drsf_doc_processor_helpers.gen_drsf_entry_file_path_list_from_source_doc_dir(self.SOURCE_DOCS_STAGING_DIR, self.BASE_CONFIG_MAPPINGS)
        for entry_source_doc_file_path in entry_source_doc_file_paths:
            drsf.drsf_doc_processor_helpers.remove_foundational_build_syntax_section(entry_source_doc_file_path)
        return None


    def deploy_staging_source_docs_to_build_dir(self):
        shutil.copytree(self.SOURCE_DOCS_STAGING_DIR, self.SOURCE_DOCS_BUILD_DIR)
        return None