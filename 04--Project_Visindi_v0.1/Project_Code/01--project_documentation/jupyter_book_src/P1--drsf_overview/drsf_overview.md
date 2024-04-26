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

# What the DRSF Is

In short, the DRSF is a framework of formalized documentation that can be read, processed, and analyzed by an accompanying DRSF codebase.  The end goal is to provide operational documentation and strategic perspective to all members of a security program: from an entry-level Analyst to the Chief Information Security Officer \(CISO\).


# Origins

In December 2017, the Incident Response Team at the artificial intelligence company Palantir published a blog post titled "Alerting and Detection Strategy Frameworks". <!--TODO: citation and link here. -->  The blog post presented a strong case that formalized documentation could significantly improve a security department's Detection Engineering \(SecDetEng\), Security Operations \(SecOps\), and Incident Response \(IR\) capabilities. Several months later, in the summer of 2018, I was just starting out in my first Security Engineering position and at the beginning of my IT Security career.  My Team Lead sent the post's link to us during a morning meeting, and mentioned that he was considering whether to implement something like it for our own team.  We never did because of competing priorities, but that article sparked my intense interest in how to effectively document, prioritize, and coordinate work using such a framework of formalized documentation.

My experiences in threat detection and response work in the years since have only fueled this interest, and in October 2022 I started building my own framework, called the Detection and Response Strategic Framework \(DRSF\).  While inspired by this original work of Palantir's IR Team, the DRSF is substantially different.  DRSF documents are designed to be parsed and edited by an accompanying DRSF program codebase.  The DRSF code can programmatically edit those same documents.

This ability to write documentation that can then be programatically read, processed, and edited by code can provide powerful capabilities that I'll elaborate on below.

-- Ross Blair


# Basic Anatomy of the DRSF

If I arrived at the office one morning as CISO, and my CEO said "hey, are we secure, tell me everything?", my response would start with the bad outcomes that our company has been defending itself against and avoiding.  In the DRSF these "bad things that can happen" are known as adverse events.

I'd then describe the various threats and attacks that could lead to that given adverse event "x".  Threats are footholds that a malicious actor has gained: execution privilege on the system, API key, etc.  Attacks are actions that they are taking: running malware on the system, using that stolen API token, etc.  Multiple threats and attacks can be chained together to lead to an adverse event.  In days gone by \(I'm old\) this had the militaristic term of "kill chain", but the DRSF calls them "paths of compromise" \(PACs\).

So I'd described threats and attacks, chained together in paths-of-compromise \(PACs\), eventually leading to one or more adverse events.  But I haven't answered the CEO's question yet.  They want to know whether we are secure.  So now I start to describe the detection signatures that we've written for these various threats and attacks, and our various implementations of mitigating controls to either prevent or significantly reduce the success rate of given attacks.

This narrative above explains the origin of the six conceptual "entry types" of the DRSF:
* Adverse Events
* Attacks
* Threats
* Detection Signatures
* Mitigating Control Implementations
* Mitigating Controls
Every DRSF entry has its own document file, formally structured and fully documented.  As entries are added to the DRSF, complex chains and webs of entries can form, illustrating paths-of-compromise \(PACs\), their potentially resulting adverse events, and the detection signatures and mitigating controls hopefully preventing those adverse events.

The DRSF ultimately is represented by two outputs:
* formal DRSF entries documents that are logically organized and human readable, 
* and code objects and data structures generated from those entry documents and made accessible through code.


# What the DRSF Aims to Achieve

A framework of formalized documentation can foster and maintain three essential - yet unfortunately rare - capabilities for a security organization's work across Detection Engineering \(SecDetEng\), Security Operations \(SecOps\), Governance Risk and Compliance \(GRC\), and Incident Response \(IR\):
1. comprehensive documentation
2. rigor
3. strategic perspective

Comprehensive documentation.  This is a bit self-evident, honestly, but should be explicitly stated and elaborated on.  Such documentation can provide a single source of information, available for reference by multiple individuals and teams.  When built with open-source formatting-syntax and publication-software, it can be updated and improved within a version-controlled content system \(e.g. GitLab, GitHub\).  The documentation's accuracy can be maintained through enforceable review/approval procedures \(e.g. commit reviews\).  Finalized documentation can be automatically deployed to multiple formats and locations through a "continuous integration, continous deployment" \(CI/CD\) publication pipeline \(e.g. GitHub Actions\).[^tech_complexity_concern_ref]

Rigor.  Every finalized "entry" in the documentation must have its sections fully documented, reviewed, and approved.  Let's say a Detection Engineer on the team wants to build and deploy a new detection signature.  They'll have to ensure that their submitted "detection signature" entry is associated to an existing "attack entry".  The submitted entry will also require fully documented sections such as "Assumptions, Blind Spots, Obstacles", "Validation", and "Known False Positives".  The time spent rigorously engineering the detection signature is time gained by avoiding excessive false positives, or lessening an SecOps Analyst's mean-time-to-respond \(MTTR\) with thoroughly documented technical context and response plans.

Strategic Perspective.[^disclaimer_of_future_capability]  Here's where the DRSF becomes powerful, and all the hard work of formal documentation starts to pay off!  As mentioned earlier, every properly formatted and completely documented DRSF entry document can be read, processed, and edited with the DRSF code.  The DRSF codebase builds graph data structures that programatically map the different relationships between every single DRSF entry.  This allows us to change the attributes of one DRSF entry, and then have every related DRSF entry's attributes updated, throughout the entire graph.  Let's explore an example of why this capability is powerful.  Let's say we just updated the "90%-confidence-interval upper-bound impact" \(`90CI_UPPER_IMPACT`\) of an adverse event entry called "Manufacturing System Compromised".  Latest analysis has indicated there's high confidence that potential damages could reach up to \$10M, instead of \$2M.  That adverse event's "expected loss metric" \(ELM\) now changes.  As mentioned earlier, adverse event entries lie at the ends of chains of attack and threat entries which comprise an "attack path" to each adverse event.  Any given attack or threat can be associated with any other given attack path leading to multiple adverse events.  The ELM of every attack and threat entry, therefore, should be derived from the collection of ELMs of all their possible proceeding adverse event entries \(i.e. the adverse events that lie at the end of their attack paths\).  If a company was tracking something like 30 adverse events, with a total of 100 interwoven threat and attack entries in their respective attack paths, manually updating the metrics of each threat and attack entry would not be practical.  Graphs allow us to programmatically update every DRSF entry in the DRSF graph, and write those metrics back into each DRSF entry document.  Step back now from the technical details and look at the big picture.  Imagine the strategic perspective gained from being able to objectively prioritize, in a logical and constantly updated order, every single detection signature in your detections portfolio.  Imagine the clarity gained by your Detection and Response team when they have five different confirmed true positive detections fire at the same time, yet are able to immediately prioritize all five investigations relative to one another.  Imagine the strategic perspective gained when a D&R Team Lead can programmatically query the DRSF graph for every attack or threat entry with an ELM of "x" or above for which there is no associated detection signature.  Or let's consider an "governance, risk, and compliance" \(GRC\) leader whose able to precisely calculate the return on investment from their mitigating controls.  They could query the DRSF graph for the ELMs of each associated attack or threat entry to any given mitigating control.  The ELM multiplied by the percent reduction in probability of successful compromise \(due to the mitigating control's implementation\) would yield a financial number which could then be compared to the costs of implementing the mitigating control.  This is the power of formalized documentation frameworks that can be programatically processed into graph data structures.




[^tech_complexity_concern_ref]: At first review, this whole praxis might seem unnecessarily complicated.  Systems like git and platforms like GitHub are complex, and have steep learning curves for the uninitiated.  There are already wiki platforms like Atlassian's Confluence, which has version control and approval workflows, all with a more intuitive user-interface \(UI\).  These points are valid, yet I feel that, once harnessed, an open-source and flexible tech-stack gives a powerful combination of two capabilities that proprietary wiki platforms rarely do: stability and deployment-flexibility.  For example, contributors are not constantly guided down a path of platform-specific markdown flavors \(e.g. Confluence Wiki Markup\).  Nor is the documentation held hostage by the vagaries of mass-export formatting \(e.g. a mass export of Confluence articles to a different wiki platform\).  By using open-source publication software \(e.g. Jupyter Book\), combined with open-source web-app-server stacks \(e.g. Flask, GUnicorn\) running within containers \(e.g. Docker\), a team can deploy their documentation in a variety of on-premise and/or cloud infrastructures.
[^disclaimer_of_future_capability]: Note that at the time of writing \(April 2024\) the functionality to compute objective risk metrics for DRSF entries has not yet been implemented.