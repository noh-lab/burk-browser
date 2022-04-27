Genome Browser for various Burkholderia studied in the Noh Lab, forked from Jbrowse version 1.16.11. 

# About

This project uses a modified version of [Jbrowse](https://github.com/GMOD/jbrowse) to display information about the Burkholderia genome. This instance of Jbrowse 
is using Node.js (v10.23.1) and the Express framework (v4.15.4) compiled with yarn (v1.22.20) for the front-end. The back-end of 
the application is based in static JSON files used to represent various genomic features and rendered in real time by the
browsers' front-end. These files are generated using either prebuild Jbrowse Perl (v5.26.3) scripts or custom built Python (v3.6.8) 
scripts. The front-end is served by a Centos 8 server running Nginx (v1.14.1) and available at [burk.colby.edu](burk.colby.edu).

## Source Code Changes from Base Jbrowse 

1. Genomic Feature Protein Sequences

The feature details page of the original Jbrowse only displays the nucleotide sequence of the feature and not the protein sequence. This change
added a view to the feature description page of genomic features that renders the protein sequence for the expanded feature. For more information, see PR [#1](https://github.com/noh-lab/burk-browser/pull/1).

2. Descriptive Feature Labels

Jbrowse by default shows the identifier for genes, but these are not descriptive identifiers. This change altered the display logic for feature names
so that it would by default show the protein product for genes and only show the identifier if a protein product was unavailable. This facillitated 
easier scanning of the gene track in the browser. For more information, see PR [#2](https://github.com/noh-lab/burk-browser/pull/2).

3. Zoom to Genomic Feature

This change allows a user to right click on a feature and zoom to it so they are more easily able to see surrounding features and other genomic context.
For more information, see PR [#3](https://github.com/noh-lab/burk-browser/pull/3).

4. Modern Bed File Support

Jbrowse offers support for BED files, but the BED files that stored data about our Burkholderia genomic islands were in a format unrecognizable to the
default Jbrowse Perl script. This change added a Python script that parses these genomic island bed files and puts data into the JSON format expected
by Jbrowse. For more information, see PR [#5](https://github.com/noh-lab/burk-browser/pull/5).

5. Feature Name Searching

Jbrowse offers support for feature searching, but these search indexes must be generated for the front-end. This change added functionality to the BED
scripts and added other name index generation scripts so that Jbrowse would recognize and find search results for custom tracks. For more information,
see PR [#6](https://github.com/noh-lab/burk-browser/pull/6) and [#8](https://github.com/noh-lab/burk-browser/pull/8). (currently not working? Will investigate.)

6. Secretion System Coloration

By default, features in Jbrowse render as the same color if they are in the same track. This change allowed for secretion system features to render in 
different colors so they could be more easily identified and grouped into distinct systems. For more information, see PR [#7](https://github.com/noh-lab/burk-browser/pull/7).
