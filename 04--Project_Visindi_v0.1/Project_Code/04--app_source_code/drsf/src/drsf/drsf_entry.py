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


class DRSF_Entry():

    def __init__(self, entry_build_dict):
        self.entry_type = entry_build_dict['entry_type']
        self.title = entry_build_dict['title']
        self.id = entry_build_dict['id']
        self.foundational_build_fields = entry_build_dict['foundational_build_fields']
        self.auto_generated_fields = entry_build_dict['auto_generated_fields']
        self.source_doc_dir_rel_file_path = entry_build_dict['source_doc_dir_rel_file_path']
    

    def set_foundational_build_field(self, target_field, new_value):
        # Make the changes to the object's fields.
        self.foundational_build_fields[target_field] = new_value
        return self

