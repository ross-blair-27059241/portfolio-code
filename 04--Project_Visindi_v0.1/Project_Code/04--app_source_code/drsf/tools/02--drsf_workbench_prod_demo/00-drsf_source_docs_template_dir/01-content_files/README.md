# Content File Management

Content files for a Jupyter Book directory can be large, and therefore are not practical to track in Git file version control.  An alternative way of managing these large files had to be created.

If you have just started working with the repository which contains this Jupyter Book directory, you will see that `01-content_files` only contains this README file and a subdirectory called `00-content_files_mgmt_code`.  If you were to just leave this as is, and try to create the Jupyter Book from the latest versions of the documentation files, you'd almost certainly run into build errors.  This is because those source markdown documents are referring to content files that cannot be found in the `01-content_files` directory.

You will need to retrieve the content files from their storage location: typically a clould file storage/sharing platform.  And if you add to or change these files, you'll also need to "publish" those new or changed files to that storage location.  **WARNING: Because such changes and additions are NOT tracked by any form of file version control protocol by default, if you're working with a team you will need to devise a process - either technical or procedural - for coordinating such changes.**

The following sections provide instructions for how to do this.


# Retrieving Content Files

Current solution is to simply rely on a local copy of the repository to store these files, and occassionally make backups of this local repository to an external hard drive.

This obviously is not a proper long-term solution.  Future work will entail code that utilizes a service like AWS S3 to retrieve and publish files.  This code can be found in the subdirectory `./00-content_files_mgmt_code`.


# Publishing New or Altered Content Files

Current solution is to simply rely on a local copy of the repository to store these files, and occassionally make backups of this local repository to an external hard drive.

This obviously is not a proper long-term solution.  Future work will entail code that utilizes a service like AWS S3 to retrieve and publish files.  This code can be found in the subdirectory `./00-content_files_mgmt_code`.