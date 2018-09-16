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

    - pandas
        to install it, e.g.: sudo pip3 install pandas

# -------------------
* RUNNING
# -------------------
It is not necessary to use 'python3 <script.py>' syntaxe, just './<script.py>' (make sure it has execution permission).

    douglasbeniz>: ./evidence_stats.py -h
    usage: evidence_stats.py [-h] [-s] [-f FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -s, --stats           Parse JSON file gathering important info and saving
                            them into a CSV file.
      -f FILE, --file FILE  Inform a JSON file name to analyze, otherwise will
                            look for the use default, '17.12_evidence_data.json'.

# -------------------
END