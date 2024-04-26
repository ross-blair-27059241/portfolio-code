# The Detection & Response Strategic Framework \(DRSF\) Core Codebase

<!-- TODO: Insert a description of the DRSF application code here. -->
<!-- TODO: Content is a work in progress. -->


## Features

<!-- TODO: Insert content here. -->
<!-- TODO: Content is a work in progress. -->


## Installation

<!-- TODO: Insert content here. -->
<!-- TODO: Content is a work in progress. -->

It is recommended to install this codebase within a Python virtual environment dedicated specifically to the execution of this application alone.  This keeps your work with this codebase separate from the instance\(s\) of Python \(and its various installed libraries\) that are installed "system-wide" on your local machine.  The following steps should not be taken as an exhaustive summary, but will provide a helpful basic summary for you.
1. Create the virtual environment with a name that indicates its use for the DRSF codebase: `python -m venv venv--app_drsf`, where `venv--app_drsf` is an example name for the virtual environment.  You may call it whatever you like.
2. Open a CLI terminal and activate this virtual environment: `source ./venv--app_drsf/bin/activate`.  You should see `(venv--app_drsf)` displayed at the beginning of your CLI command prompt.
3. Once activated, update the PIP program itself with `pip install --upgrade pip`.
3. Manually invoke `pip` within your activated virtual environment to install some important programs that ensure that your use of the DRSF core codebase and DRSF Workbench tools goes smoothly.
   * `pip install ipykernel`
   * Ensure that your IDE is aware of your virtual environment's Jupyter kernel.  This is essential to properly running the DRSF Workbench Jupyter notebook file.  This is done with the command: `python -m ipykernel install --user --name venv--drsf --display-name "Python X.Y.Z (venv--drsf)"`.  Where `venv--drsf` is the name of your activated virtual environment, and `"Python X.Y.Z (venv--drsf)"` is the display name for this kernel that you'd like to see within your Jupyter UI when you're running Jupyter Notebook files.[^Jupyter_UIs]
4. Use `pip` to install `drsf` within the activated virtual environment.  The exact execution method of this command will depend on how the DRSF codebase has been distributed, and how you intend to use the codebase.  **Make sure to read all the following points before making your decision on how you want to execute the installation with `pip`.**
   * GETTING THE DRSF CODE PACKAGE.  Note that at this early stage in the project's development \(late 2023\), you've almost certainly received the drsf code package through one of two relatively rudimentary methods:
     1. A simple download of its source contents, rather than through downloading it from PyPI \(since it's currently not available there\).  In this scenario you'd simply have a `drsf-x.y.z.tag.gz` in your machine's Downloads directory.
     2. Manually building the package yourself from Project Iona's main repository, using `./05--app_deployment_pipelines/app_code_packaging/python_code_packaging.ipynb`.  Instructions for how to do this are included in that Jupyter Notebook file, but in this scenario you'd end up with the drsf package placed at the file path `./03--app_source_code/drsf/dist/drsf-x.y.z.tag.gz`.
   * INSTALLING THE DRSF CODE PACKAGE.  Once the drsf python package has been retrieved \(or created\), you now need to decide how you're going to install it within your virtual environment.  This depends on how you're going to use the drsf package.  There are two different use cases.
     * Use Case 1: if you're simply using the codebase as an "end user".  In other words, you're not concerned with modifying or improving the drsf codebase itself, you're just using it to build your DRSF.  In this case the command should be: `pip install drsf-x.y.z.tag.gz`.
     * Use Case 2: if you believe that you'll be contributing to the DRSF codebase, or just making changes to it in-between your executions.  It's recommended to perform what's called an "editable installation".  A PIP editable installation is where PIP installs a package such that any code changes you make to the package's source code are immediately reflected after every import of the package.  This saves you the trouble of having to re-build and re-install your package after every source code change.[^fn_001].
       * First, extract the `drsf-x.y.z.tag.gz` file, and place the extracted contents in some logical sub-directory of your project-directory \(e.g. `app_source_code`\).
       * Then execute an editable install of a package within your activated virtual environment: `pip install -e <path to source code directory which contains the setuptools config files>`.  The setuptools config files are `pyproject.toml`, `setup.cfg`, and `setup.py`.


## Usage

<!-- TODO: Insert content here. -->
<!-- TODO: Content is a work in progress. -->

The main DRSF codebase in `./src/drsf` is meant to be used along with a set of configuration files, templates, and a Jupyter Notebook file.  Collectively these are referred to as the "DRSF Workbench", and have been included along with this package when it was last built.  You can find the DRSF Workbench in the `./tools/drsf_workbench` subdirectory.

Finding the location of this `./tools/drsf_workbench` subdirectory depends on how you've used installed the DRSF package \(see above section\).

If you've done a "standard non-editable" installation of drsf, then you will find the workbench at `./<virtual_environment_name>/lib/pythonX.Y/site-packages/drsf-x.y.z/tools/drsf_workbench`.  You can copy this entire directory and place it somewhere within your project's directory that makes sense to you.

If you've done an "editable" installation, then simply navigate to the directory where you extracted the package's contents \(probably you should extract this to the main directory of your project\), and look for the `./tools/drsf_workbench` directory.  Copy this entire directory and place it somewhere within your project's directory that makes sense to you.


## Contributing

<!-- TODO: Insert content here. -->
<!-- TODO: Content is a work in progress. -->


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