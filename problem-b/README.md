# EMBL-EBI (SW Dev. 01279) coding exame, Problem-B

Douglas Bezerra Beniz, douglasbeniz@gmail.com

## Getting Started

It was written using Python 3.6 version.

### Prerequisites

What things you need to install the software and how to install them

```
- argparse
    to install it, e.g.: sudo pip3 install argparse

- json
    to install it, e.g.: sudo pip3 install json

- pandas
    to install it, e.g.: sudo pip3 install pandas
```

### Running

It is not necessary to use \'python3 <script.py>\' syntaxe, just \'./<script.py>\' (make sure it has execution permission).


```
    douglasbeniz>: ./evidence_stats.py -h
    usage: evidence_stats.py [-h] [-s] [-f FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -s, --stats           Parse JSON file gathering important info and saving
                            them into a CSV file.
      -f FILE, --file FILE  Inform a JSON file name to analyze, otherwise will
                            look for the use default, '17.12_evidence_data.json'.
    douglasbeniz>: 
    douglasbeniz>: 
    douglasbeniz>: time ./evidence_stats.py -s
    ---------------------
    Parsing JSON file: '17.12_evidence_data.json', this could take a while...


    ---------------------
    JSON file was successfully parsed as 'parsing_results_20180916_130038.csv'


    ---------------------
    Starting the creation of summarized statistics, this could also take a while...


    Statistics CSV file was successfully created as 'stats_results_20180916_130038.csv'


    real  51m46,081s
    user  68m12,289s
    sys   13m36,925s

```

Main two parts of this processing take about *50 minutes* for provided JSON file, '17.12_evidence_data.json', with approximately 28.0 Gbytes. The first step, while parsing JSON file, during the tests it took about *35 minutes*, and the second step, of calculating statistics and generating a sorted CSV file, took *15 minutes* in average.