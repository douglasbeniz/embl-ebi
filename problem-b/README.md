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

- numpy
    to install it, e.g.: sudo pip3 install numpy

- pytest
    to install it, e.g.: sudo pip3 install pytest

- requests
    to install it, e.g.: sudo pip3 install requests

- unittest
    to install it, e.g.: sudo pip3 install unittest
```

### Running

It is not necessary to use \'python3 <script.py>\' syntaxe, just \'./<script.py>\' (make sure it has execution permission).


```
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
```

## Running the tests

* [PyTest](https://docs.pytest.org/en/latest) - The test framework used

```
douglasbeniz>: pytest my_code_test.py -vv
```

### or

```
douglasbeniz>: ./my_code_test.py --test
```

```
============================================================ test session starts =============================================================
platform linux -- Python 3.6.5, pytest-3.8.0, py-1.6.0, pluggy-0.7.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/douglasbeniz/Documents/EMBL-EBI/Coding_Exame-13Sep2018/ProposedResolution/embl-ebi, inifile:
collected 3 items                                                                                                                            

my_code_test.py::TestOpenTargets::test_main_ensg00000157764 PASSED                                                                     [ 33%]
my_code_test.py::TestOpenTargets::test_main_efo_0002422 PASSED                                                                         [ 66%]
my_code_test.py::TestOpenTargets::test_main_efo_0000616 PASSED                                                                         [100%]

========================================================== 3 passed in 0.93 seconds ==========================================================
```
