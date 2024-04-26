---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: python3
  language: python
  name: python3
---

# Introduction

The following book serves as the official project documentation for Project Visindi.  Here you can find everything from hardcore technical documentation of the codebases to background context on various efforts of the project.

```{note} 
If you have already been reading the contents of Project Visindi's various README files in the project's code repository, then you may find some of the following sections of this introduction repetitive.  Certain instructions have been intentionally duplicated between the README files and this book.  This ensures that no matter which documentation source you start from, you can guide yourself through what Project Visindi is and how to use it.
```

```{warning}
**Project Visindi is very much a work in progress. While the project aims to always provide a "minimum viable codebase" on the main Git branch, you will definitely find places lacking adequate documentation as well as undocumented code.  To help avoid confusion, where functionality is mentioned that has yet to be fully implemented, or where there's incomplete documentation or content, you should see either a footnote,  `TODO:` tag, or some other explicit marker.  These tags may be present in "source document content" \(i.e. a standard markdown file\) or in rendered content \(i.e. the page of a published Jupyter book\).  Despite the project's efforts to explicitly identify gaps in documentation, for the near future some surely remain unidentified.**
```


## The Project's Goal & Components

Project Visindi's end goal is to provide operational documentation and strategic perspective to all members of a security program: from an entry-level Analyst to the Chief Information Security Officer \(CISO\).  The tool that helps achieve this goal is a collection of documents and code called the Detection & Response Strategic Framework \(DRSF\).

On a technical level, the DRSF consists of three main components:
1. A core DRSF codebase that can programatically create, read, process, and analyze formalized documentation files, which are referred to as "DRSF source documents".
2. A Jupyter Notebook file called "DRSF Workbench" which uses config and input files to harness the core DRSF codebase to create, modify, and analyze DRSF source documents.
3. The output DRSF source documents, which are built into a Jupyter Book for processing into multiple desired formats \(e.g. static web-page, pdf, etc.\).

The other components of Project Visindi all support creating, deploying, building, and continuing to update this DRSF.


## Getting Familiar with Project Visindi's Composite Technologies

Here are the key technologies and codebases that any user or contributor of Project Visindi should have at least a introductory level of experience with.
* The Git file version control system, within the context of using GitHub's Git platform.  Essential for cloning the Project Visindi code repo, and contributing to the content and code of the project.
* Python.  For the core DRSF codebase, Python package distribution, and virtual environment instantiations.
* Jupyter Lab.  For executing Jupyter Notebook files key to the DRSF codebase.  Also used for executing packaging and distribution code for the DRSF codebase.
* GitHub Markdown Syntax.  For reading and writing content of the code repository's various README files as well as the content blocks of various Jupyter Notebook files.
* Myst Markdown Syntax.  For writing narrative content for DRSF source documents.
* Jupyter Book.  For processing DRSF source documents into a final draft of DRSF documentation. Also used for building Project Visindi's own project documentation into various output formats.

The following paragraphs will provide more context and detail on how these technologies tie into the project.

Project Visindi's core content and codebases are all tracked using the Git file version control system.  The Git platform which hosts and operates Project Visindi's remote repository is GitHub.

The DRSF core codebase is written in Python.  Key functionality relies upon several important codebases:
* networkx
* plotly
Packaging this core codebase into an `pip` installable Python package relies on `setuptools` as the "build backend", and `build` as the "build frontend".

Understanding [Project Jupyter's suite of notebook tools](https://docs.jupyter.org/en/latest/) is critically important.  A Jupyter Notebook file called `drsf_workbench.ipynb` is how an end-user invokes the DRSF core codebase to programmatically instantiate, modify, and analyze their own DRSF.  Jupyter Notebook files are used in several other areas of Project Visindi as well.  Just one example is the `python_code_packaging.ipynb` file which helps document and execute Python packaging for the DRSF's core codebase.

Writing narrative content in the markdown cells of Jupyter Notebook files, as well as writing Project Visindi's various markdown README files, is done using GitHub's derivative of the Markdown document file syntax.  While an end-user of Project Visindi will probably not need to worry about this, just be aware that the markdown of the DRSF's source documents is quite different than that used in the Project Visindi repo's "basic" \(i.e. not meant to be built into a Jupyter book\) documentation files.

While the core codebase and `drsf_workbench.ipynb` are responsible for instantiating source document templates, processing DRSF entry metrics, and building final publication outputs, actually writing the narrative content of the DRSF will be done manually.  Writing properly formatted DRSF source documents requires a familiarity with the ["Myst" derivative of the Markdown document formatting syntax](https://jupyterbook.org/en/stable/content/myst.html).

The [Jupyter Book program](https://jupyterbook.org/en/stable/intro.html) is responsible for processing the DRSF source documents into their final publication formats.


## Finding Your Way Through Project Visindi's Code Repository

The main directory of Project Visindi's code repository is organized by files and numbered directories which proceed in an order logical to the first-time user of - or contributor to - this project.  Note that as you work through these directories, you'll see multiple `README.md` files.  These files are meant to guide you through their specific directory's content structure.  Always make sure that you read them thoroughly, otherwise you could easily get confused and run into problems.

The best start to understanding Project Visindi is focusing on the following two files in Project Visindi's main directory.
* `./README.md` gives you a very brief overview of Project Visindi and some detailed information about how to find the project's documentation files.  Some sections of this README are very similar to those of the page you're reading here.
* `./LICENSE.md` contains detailed information on this project's licensing terms, though the README document mentioned just above also contains a "plain English" section describing the project's licensing as well.

With those two files read, let's move on to understanding all the various directories of Project Visindi.

`./00--copyright_and_licensing`: This directory contains detailed information on all licenses and copyrights that apply to all code and content within Project Visindi.

`./01--project_documentation`: All documentation related to Project Visindi is contained in this directory.  Its files and subdirectories are organized such that a jupyter book can be generated from them using the Jupyter Book program.  Further details on using this directory's contents can be found in this subdirectory's README file at `./01--project_documentation/README.md`.

`./02--project_infra_deployment_pipelines`: Contains all code necessary to instantiate any infrastructures required to deploy and use the DRSF.  For example, instantiating container infrastructure for the application to run on top of.  Each subdirectory should reflect this specific type of deployment \(e.g. "docker_runtime_local_machine", "aws_ecs", etc.\).

`./03--app_deployment_pipelines`: Contains all code necessary to properly package and distribute the core DRSF codebase.

`./04--app_source_code`: All source code and development notebooks for the project's application\(s\) are contained in this directory.  The structure of this directory follows the "source layout" convention for Python-source-code-project-directories.  The convention is that each "application" has its own separate subdirectory.  Since the DRSF is our only "core codebase" application in the project, you'll see a single subdirectory called `drsf`.

<!-- TODO: Content within this paragraph remains a work in progress. -->
<!-- TODO: Each bullet needs at least a brief explanation of the purpose of the file or dir is. -->
The source code directory of any application is an essential directory to understand, so let's dive into the details of the layout of the DRSF-core-codebase's source code directory.  They are:
* `README.md`
* `src/`
* `tools/`
  * `tools/drsf_development_notebooks`: 
  * `tools/drsf_workbench`: This directory is specific to building a Detection & Response Strategic Framework \(DRSF\) on your local machine.  Here you'll find a number of input files and a Jupyter notebook file.  These input files include DRSF-configuration-JSON files, DRSF template directories, and DRSF entry templates.  When you work with the DRSF codebase, you'll do so through the `drsf_workbench.ipynb` Jupyter notebook located in this directory.
* `setup.py`
* `app_drsf-requirements.txt`: A PIP requirements file. Used to instantiate Project Visindi's `venv--app_drsf` virtual environment \(explained in the following section\).
* `pyproject.toml`
* `setup.cfg`
* `MANIFEST.in`

As you look through the project's files and directories, you'll also note several files with a `.sig` suffix.  These are the GPG-public-key-detached-signature-files corresponding to their respective source files.  They are often simply referred to as a "signature files".  The signature file bears the same name as its source file plus a ".sig" suffix.  The signature file can be located in the same directory as its corresponding source file.  Signature files are used to verify the authenticity of a digital file \(making certain assumptions which we won't get into here\).  Signature files are used throughout Project Visindi to prove authenticity of code, documents, copyrights, and licenses.

Finally, if you return back to the main directory of the project, you'll see the file `proj_visindi-requirements.txt`.  This file is a PIP requirements files.  It is used to instantiate Project Visindi's `venv--proj_visindi` virtual environment \(explained in the following sections\).


## Instantiating Project Visindi's Virtual Environments

As mentioned earlier, Project Visindi is comprised of several important codebases.  These codebases are used for a wide variety of purposes.  To provide just a few possible examples:
* Developing and executing the DRSF's core application codebase,
* packaging the DRSF's core codebase,
* deploying the DRSF application into one or more technical infrastructures.

It's important to ensure that the Python codebases installed and imported to achieve any of these operations do not have dependency clashes with those codebases needed to achieve a different operation in the project.  In the world of Python programming, a common solution for this problem is to create Python virtual environments.

Project Visindi makes use of several different virtual environments:
1. `venv--proj_visindi`: the virtual environment for executing Python app-code-distribution packaging scripts, as well as building the Project Visindi documentation into a Jupyter Book.
2. `venv--app_drsf`: the virtual environment for developing the DRSF core codebase, and for instantiating the kernels for the various Jupyter notebooks.

If you're just starting out with Project Visindi, each of these virtual environments should be instantiated after cloning Project Visindi's repository.  This is done by entering the following commands on the command line interface \(CLI\) of your machine.
* `python -m venv venv--proj_visindi`
* `python -m venv venv--app_drsf`

With each virtual environment built, we now need to activate each virtual environment and install a series of Python packages for each environment.  This will ensure that your virtual environment's codebases are configured to the latest common specifications for the latest stable version of the project's code.

At this point in time it's also a good idea to run any other additional commands that you might need to get your virtual environment properly configured.

Let's first start with ensuring that our `venv--proj_visindi` virtual environment is configured with the proper versions of our "common spec" Python packages, with an additional step to make it play nice with is Jupyter kernel running within the VSCode IDE.
1. `source ./venv--proj_visindi/bin/activate`.  Activating the `venv--proj_visindi` virtual environment.  You should now see a prefix of `(venv--proj_visindi)` on your CLI command prompt.
2. `pip install --upgrade pip`.  Ensuring that your virtual environment is working with the latest version of PIP.
3. Ensure that on your CLI you have navigated to the main directory of the project.
4. `pip install -r proj_visindi-requirements.txt`.  Installing this virtual environment's required Python programs.
5. `python -m ipykernel install --user --name venv--proj_visindi --display-name "Python 3.11.0 (venv--proj_visindi)"`.  Ensuring that your virtual environment's jupyter kernel will be recognized by the VS Code integrated development environment \(IDE\).  This makes the kernel available to be selected within the user interface \(UI\) of VS Code's Jupyter Notebook windows.
6. `deactivate`.  To deactivate the `venv--proj_visindi` virtual environment, and move on to activating and configuring the next one.

With the overall project's virtual environment configured, let's move on to the very important task of configuring the `venv--app_drsf` virtual environment, which will be responsible for running and developing the the core DRSF codebase and DRSF Workbench tool.
1. `source ./venv--app_drsf/bin/activate`.  Activating the `venv--app_drsf` virtual environment.  You should now see a prefix of `(venv--app_drsf)` on your CLI command prompt.
2. `pip install --upgrade pip`.  Ensuring that your virtual environment is working with the latest version of PIP.
3. Ensure that on your CLI you have navigated to the `04--app_source_code/drsf` directory.
4. `pip install -r ./04--app_source_code/drsf/app_drsf-requirements.txt`.  Installing this virtual environment's required Python programs.
5. Here you could take one of several courses of action, depending on how you're going to work with the DRSF codebase.  There are several options which we should not go into detail here.  The current best recommendation for an end user or contributor is to perform an "editable install" of the DRSF application's dependent Python packages with the command `pip install -e <path to source code directory which contains the setuptools config files>`.  In this case that directory path would be `./04--app_source_code/drsf`, relative to the main project directory.  This will make the drsf package available to your virtual environment for imports.  NOTE: despite this operation, you will still need to repeat this `pip install -e` command within every Jupyter notebook you're working with.  The exact reasons for why a `pip install` command executed from the CLI does not get recognized by a Jupyter kernel instantiated from that exact same virtual environment is not currently known.  This said, code cells have been provided in each notebook to remind the user to run this install command and avoid confusion.
6. `python -m ipykernel install --user --name venv--app_drsf --display-name "Python 3.11.0 (venv--app_drsf)"`.  Ensuring that your virtual environment's jupyter kernel will be recognized by the VS Code integrated development environment \(IDE\).  This makes the kernel available to be selected within the user interface \(UI\) of VS Code's Jupyter Notebook windows.
7. `deactivate`.  To deactivate the `venv--app_drsf` virtual environment.


## Using Project's Visindi's Code & Tools

% <!-- TODO: Content within this paragraph remains a work in progress. -->

With your orientation around the project's directories, as well as your instantiation of the requisite virtual environments, you're now ready to use and contribute to Project Visindi's docs and code!


## Acknowledgements

% <!-- TODO: Insert content here.  Make some mention of the original inspiration for all this from the Palantir IR Team's ADSF, as well as your indebtedness to the Jupyter Ecosystem. -->


## Non-Legalese Summary of Copyright and Licensing

The Devil's always in the details with this stuff, and you should read the finer details explained in the file `LICENSE.md`, contained in the same directory as this README file.  But with that said, here's a general, non-legalese, summary.

**A helpful "TLDR".  You are allowed many opportunities to copy, use, modify, and re-distribute all the code and nearly all the content found here in these projects, documentations, and/or codebases \(referred to collectively as "the Licensed Work"\).  While most students and IT Security professionals will find these opportunities sufficient for their own goals or the goals of their organization/employer, there are some important limitations.**

Let's first focus on some examples of what you **CAN** do.
1. Copy, modify, use, and redistribute this Licensed Work internally at your own company, organization, or employer to improve its security program.
2. Copy, modify, use, and redistribute this Licensed Work personally to further your knowledge of security.
3. Copy, modify, use, and redistribute this Licensed Work personally as a portfolio of work to prove your knowledge and skills to potential employers.
All of the above provisions apply to both code AND written content of the Licensed Work.  Please be aware that in cases of quotations or content explicitly signed by a particular person, you're welcome to copy, modify, use, and redistribute that content provided that you attribute that original writing to the original author.

Now for some examples of what you **CANNOT** do.
1. You cannot simply copy or modify this Licensed Work and then claim the work as solely your own.  You must acknowledge and cite Ross Blair's contribution to what you've built upon.
2. You cannot simply copy or modify this Licensed Work and then place a different license on it.  The BSL licensing terms carry through to any copy or "derivative work" of this Licensed Work.
3. You cannot take this Licensed Work and then sell or offer it as a product or service to "third parties" in such a way that it's competitive with the commercial services or products of Ross Blair.  That last sentence is a mouthful, so let's dissect this a bit.  By "third parties" we mean someone apart from you or your employer.   For example, you could NOT use this Licensed Work as a service offering or product to any customers.  But, as we've said earlier, you CAN use the Licensed Work for the benefit of your company's or employer's own internal security program, regardless of Ross Blair's current commercial products or services.
4. You cannot use, copy, modify, or re-distribute the copywritten or trademarked logos within this Licensed Work.  To make this easier, all relevant logos that are off-limits will explicitly bear a copyright or trademark.


## Official Statement of Copyright & Licensing

Unless explicitly indicated otherwise, all code and content within this publication is © 2024 Ross Blair, and falls under the licensing terms of Ross Blair's derivative of the Business Source License \(BSL\).  The precise terms of the BSL can be referenced by reading the `LICENSE.md` file in the same directory as this README.

Code and content whose licensing terms are exceptions to this generally-applied-BSL will be explicitly indicated through either:
* a license-disclaimer-section at the beginning of the file \(e.g. a license disclaimer at the beginning of a `.py` code file\);
* a license-disclaimer-section at the end of the file \(e.g. a `LICENSE DISCLAIMER` section at the end of a markdown file\);
* the de-facto Copyright identified by "signed content" \(e.g. a section of content or a file signed by, or clearly attributed to, a name or pen-name, such as that found at the end of this document\);
* the Copyright identified by a citation of another's work \(e.g. cited text from another person, research paper, etc.\).


## Cryptographic Verification of Project Work

I sign all my commits as well as certain important documents \(including this file\) with my personal OpenPGP standard \(PGP\) key-certificate.  This PGP key-certificate's certifying-primary-key-pair's public-key bares the PGP fingerprint `5089 BF57 0395 FA05 9380  BC80 2C19 753D B797 5FDF`.  It's available via Github API [here](https://api.github.com/users/ross-blair-27059241/gpg_keys) or direct download [here](https://github.com/ross-blair-27059241/ross-blair-27059241).

You can doubly verify the authenticity of this key by verifying that the fingerprint of the downloaded GPG public key \(mentioned above\) is the same as the GPG public key fingerprint specified in my X \(formerly Twitter\) account profile: `@rb_27059241`.

The project intends to have an unbroken pattern of verified commits on code and content contributions from all contributors.


---
> -- Ross Blair
> 
> © 2024 [Ross Blair](https://github.com/ross-blair-27059241).
> 
> To verify the authenticity of this document with this written signature here, please first refer to the following three peices of information:
>
>   1. The document file which you are reading at this very moment, referred to in this context as the "source file".
>   2. The GPG-public-key-detached-signature-file corresponding to the source file, often referred to as the "signature file".  The signature file bares the same name as its source file plus a ".sig" suffix.  The signature file can be located in the same directory as this source file.
>   3. The OpenPGP standard \(PGP\) key-certificate belonging to the source file's author: [Ross Blair](https://github.com/ross-blair-27059241).  The PGP key-certificate's certifying-primary-key-pair's public-key bares the PGP fingerprint `5089 BF57 0395 FA05 9380  BC80 2C19 753D B797 5FDF`.  Available via Github API [here](https://api.github.com/users/ross-blair-27059241/gpg_keys) or direct download [here](https://github.com/ross-blair-27059241/ross-blair-27059241).
>
> To doubly verify the authenticity of this PGP key-certificate you've just retrieved \(mentioned above in step 3\), check that the PGP fingerprint of that key-certificate's certifying-primary-key-pair's public-key is the same as that fingerprint specified in the account profile of Ross Blair's X \(formerly Twitter\) account: `@rb_27059241`.
>
> With these peices of data/information, and the authenticity of the PGP public key-certificate confirmed, you can move on to the final step of truly verifying this signed document. Download and install the application [GnuPG](https://gnupg.org/index.html) - or a derivative program like [GPGTools](https://gpgtools.org). Then use this program to to verify that this file was indeed signed by the holder of the PGP private key corresponding to Ross Blair's PGP public key.  There are two technical steps to this process:
>   1. Import Ross Blair's PGP public key-certificate to your GPG program's keystore.  Run this \(or some very similar\) CLI command: `gpg --import [public-key-file]`.
>   2. Finally, verify Ross Blair's signature on this document. Run this \(or some very similar\) CLI command: `gpg --verify [signature-file-name] [source-file-name]`.
>
> The resulting message from the GPG program on your command line should confirm that the signature is valid, and that this signed document is authentic.
> 