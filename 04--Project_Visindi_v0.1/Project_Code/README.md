# README

![Project Visindi Logo](./00--content_files/Project_Visindi_Logo.png)


## Welcome to Project Visindi

Welcome to Project Visindi.  This README document is a very brief initial guide to understanding the highest level details of what this project is, what its main objectives are, what its composite technologies are, and how the project's directories are organized.


### The Project's Goal & Components

Project Visindi's end goal is to provide operational documentation and strategic perspective to all members of a security program: from an entry-level Analyst to the Chief Information Security Officer \(CISO\).  The foundational tool that helps achieve this goal is a collection of documents and code called the Detection & Response Strategic Framework \(DRSF\).

On a technical level, the DRSF consists of three main components:
1. A core DRSF codebase that can programatically create, read, process, and analyze formalized documentation files.  These documentation files are referred to throughout the project as "DRSF source documents".
2. A Jupyter Notebook file called the "DRSF Workbench" which uses config and input files to harness the core DRSF codebase to create, modify, and analyze DRSF source documents.
3. The output DRSF source documents, which are built into a Jupyter Book for processing into multiple desired formats \(e.g. static web-page, pdf, etc.\)


### Getting Started

Everything you need to know about Project Visindi is contained in its official documentation. Please refer to the `./01--project_documentation` directory.

> [!IMPORTANT]
> Currently the default representation of this documentation to you is simply the jupyter-book-source-content-files located at the `./01--project_documentation/jupyter_book_src` directory.  In order to view this documentation in a more polished, intuitive format, you will have to manually build a Jupyter Book from these source files yourself on your local machine.  This is obviously not an ideal way to read introductory documentation, and improvements are coming soon!

> [!TIP]
> If you're new to the Jupyter Book project, please refer [here](https://jupyterbook.org/en/stable/start/overview.html) for how to install the Jupyter Book CLI utility, and [here](https://jupyterbook.org/en/stable/start/build.html) for instructions on how to build a book from source-content-files.  We recommend that you create a Python virtual environment called `venv--proj_visindi` first before installing and running Jupyter Book.  This will ensure that any pip install actions do not affect any "system-wide" Python installations on your machine.  The "Instantiating Project Visindi's Virtual Environments" section of the documentation file at `01--project_documentation/jupyter_book_src/intro.md` has some helpful details on creating virtual environments.


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