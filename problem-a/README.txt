# ------------------------------------------------------------------------------
# EMBL-EBI (SW Dev. 01279) coding exame, Problem-A
# ------------------------------------------------------------------------------
# Douglas Bezerra Beniz, douglasbeniz@gmail.com
# ------------------------------------------------------------------------------

# -------------------
* REQUIREMENTS
# -------------------
It was written using Python 3.6 version

    - argparse
        to install it, e.g.: sudo pip3 install argparse

    - json
        to install it, e.g.: sudo pip3 install json

    - numpy
        to install it, e.g.: sudo pip3 install numpy

    - pytest
        to install it, e.g.: sudo pip3 install pytest

    - requests
        to install it, e.g.: sudo pip3 install requests

    - unittest
        to install it, e.g.: sudo pip3 install unittest

# -------------------
* RUNNING
# -------------------
It is not necessary to use 'python3 <script.py>' syntaxe, just './<script.py>' (make sure it has execution permission).

    douglasbeniz>: ./my_code_test.py -h
    usage: my_code_test.py [-h] [-a] [-d DISEASE] [-t TARGET] [--test]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Get all filtered associations.
      -d DISEASE, --disease DISEASE
                            Query for disease-related information (eg. use the
                            string EFO_0002422​ as a disease id).
      -t TARGET, --target TARGET
                            Query for target-related information (eg. use the
                            string ENSG00000157764 as a target id).
      --test                Runs a suit of tests

# -------------------
END