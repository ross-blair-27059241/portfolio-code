# README


## What is This Directory?

This directory contains all the source content comprising Project Visindi's documentation: from explaining what the DRSF is and how it works to detailing technical deployment pipelines.


## How to Use This Directory?

The directory is structured such that a Jupyter Book can be built from it.  This said, there is one subdirectory that you should take a special note of to avoid confusion and problems.

The directory `./00--content_files` contains any content that is referenced by the Myst-markdown source documentation that comprise the Jupyter Book.  If you've just cloned this project's repository, you may find that this directory is essentially empty!  This is by design, so don't worry and read on.


## Content File Management Issues for Version Controlled Jupyter Books

Content files for a Jupyter Book directory in some cases can be large \(i.e. above 50MB\).  In such cases of large files, you may begin to encounter errors when attempting to commit your changes to this Jupyter book and pushing those changes to a remote repository.

Project Visindi currently has not implemented a solution to this issue, but we are actively considering solutions like a Git LFS infrastructure in the near future.

In the meantime, please just be aware that while the directories in this `00--content_files` directory imply that large files can be stored within it, this is currently not the case, and you should not include such files in any changes you make to this Jupyter Book.