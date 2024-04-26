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

# IMPORTANT NOTE: This setup.py file is intentionally an empty stub that ensures
# non-erroring execution of some older development workflows: ones where this
# `setup.py` script file was invoked directly.  One example of such an older
# workflow is that of now old versions of `pip` running "in development mode",
# and requiring the presence of a `setup.py` to execute "editable installs"
# properly.
# In most modern workflows, invoking this file directly with setuptools
# via the CLI is NOT recommended, and in more recent versions of setuptools
# you will likely run into errors.
# The Setuptools project is actively deprecating its CLI interfaces, and
# moving forward its development is focused on serving exclusively as a
# "build backend" tool.  See this URL for more information:
# https://setuptools.pypa.io/en/latest/userguide/quickstart.html
# While this file should remain in your source directory to provide
# some backwards compatibility in certain niche cases that users or contributors
# might have, you should more or less ignore it.

from setuptools import setup
if __name__ == '__main__':
    setup()