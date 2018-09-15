#!/usr/bin/python3
# ------------------------------------------------------------------------------
# EMBL-EBI (SW Dev. 01279) coding exame
# ------------------------------------------------------------------------------
# Douglas Bezerra Beniz, douglasbeniz@gmail.com
# ------------------------------------------------------------------------------
# Problem A - query a REST API
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from json import dumps as json_dumps
from numpy import max as np_max, min as np_min, average as np_avg, std as np_std
from requests import get as url_get
from sys import argv as sys_argv
from unittest.mock import patch as mock_patch

import pytest

"""
Class to take care of all available resources of OpenTargets API
-------------------
    For more info, see: http://api.opentargets.io/v3/platform/docs
"""
class OpenTargets:
    def __init__(self):
        self.BASE_URL = 'https://api.opentargets.io/v3/platform/public'

    # Return URL for public association of a specified method
    def _association_url(self, method):
        return self.BASE_URL + '/association' + ('/' + method) if method else ''

    # Return URL for public evidence of a specified method
    def _evidence_url(self, method):
        return self.BASE_URL + '/evidence' + ('/' + method) if method else ''

    # Return URL for public search of a specified method
    def _search_url(self, method):
        return self.BASE_URL + '/search' + ('/' + method) if method else ''

    # Return URL for public utils of a specified method
    def _utils_url(self, method):
        return self.BASE_URL + '/utils' + ('/' + method) if method else ''


    # Fetch association info from filter method, with or without ID parameters
    def get_association_filter(self, target=None, disease=None):
        payload = {}
        if target:
            payload['target'] = target
        if disease:
            payload['disease'] = disease

        response = url_get(self._association_url('filter'), params=payload)

        if response.status_code != 200:
            raise Exception('Error fetching URL: %s' % response.status_code)
        else:
            return response.json()

    # Return some statistics for filtered association scores
    def stats_association_score(self, target=None, disease=None):
        try:
            response = self.get_association_filter(target=target, disease=disease)
        except Exception as e:
            raise e

        return self.calc_stats_association_score(response)

    # Based on fetched association info gather scores and return some statistics
    def calc_stats_association_score(self, json_data):
        overallValues = []
        try:
            for data_item in json_data['data']:
                overallValues.append(data_item['association_score']['overall'])
        except Exception as e:
            raise e

        maxVal = 0.0
        minVal = 0.0
        avgVal = 0.0
        dstVal = 0.0

        if len(overallValues) > 0:
            maxVal = np_max(overallValues)
            minVal = np_min(overallValues)
            avgVal = np_avg(overallValues)
            stdVal = np_std(overallValues)

        return maxVal, minVal, avgVal, dstVal

"""
Class to perform a suite of specific tests
"""
class TestOpenTargets:
    # ------------------------------------------------------------------------------
    # Check the output for: ​
    #   "my_code_test -t ENSG00000157764"
    # ------------------------------------------------------------------------------
    def test_main_ensg00000157764(self, capfd):
        # Mocking system input arguments
        with mock_patch('sys.argv', ['', '--target=ENSG00000157764']):
            # Calling main program
            main()

            # Capturing standard output
            output = capfd.readouterr()[0]

            # Verifying expected results
            expected = self._generate_expected('TARGET-ID=ENSG00000157764',
                '1.00000000', '1.00000000', '1.00000000', '0.00000000')

            # Asserting...
            assert output == expected

    # ------------------------------------------------------------------------------
    # Check the output for: ​
    #   "my_code_test -d EFO_0002422"
    # ------------------------------------------------------------------------------
    def test_main_efo_0002422(self, capfd):
        # Mocking system input arguments
        with mock_patch('sys.argv', ['', '--disease=EFO_0002422']):
            # Calling main program
            main()

            # Capturing standard output
            output = capfd.readouterr()[0]

            # Verifying expected results
            expected = self._generate_expected('DISEASE-ID=EFO_0002422',
                '1.00000000', '1.00000000', '1.00000000', '0.00000000')

            # Asserting...
            assert output == expected

    # ------------------------------------------------------------------------------
    # Check the output for: ​
    #   "my_code_test -d EFO_0000616"
    # ------------------------------------------------------------------------------
    def test_main_efo_0000616(self, capfd):
        # Mocking system input arguments
        with mock_patch('sys.argv', ['', '--disease=EFO_0000616']):
            # Calling main program
            main()

            # Capturing standard output
            output = capfd.readouterr()[0]

            # Verifying expected results
            expected = self._generate_expected('DISEASE-ID=EFO_0000616',
                '1.00000000', '1.00000000', '1.00000000', '0.00000000')

            # Asserting...
            assert output == expected

    def _generate_expected(self, filter_param, max_val, min_val, avg_val, std_val):
        # Verifying expected results
        expected = '---------------------\n'
        expected += 'Statistics of \'association_score.overall\' filtering by %s:\n' % filter_param
        expected += '---------------------\n'
        expected += '  * maximum= %s,\n' % max_val
        expected += '  * minimum= %s,\n' % min_val
        expected += '  * average= %s,\n' % avg_val
        expected += '  * standard deviation= %s\n' % std_val
        expected += '---------------------\n'

        return expected


"""
Principal method
"""
def main():
    # Instance of OpenTargets class to handle such API
    openTargets = OpenTargets()

    # Parsing input paramenters
    parser = ArgumentParser()

    parser.add_argument("-a", "--all", action="store_true",
        help="Get all filtered associations.")
    parser.add_argument("-d", "--disease", type=str,
        help="Query for disease-related information (eg. use the string EFO_0002422​ as a disease id).")
    parser.add_argument("-t", "--target", type=str,
        help="Query for target-related information (eg. use the string ENSG00000157764 as a target id).")
    parser.add_argument("--test", action="store_true",
        help="Runs a suit of tests")

    args = parser.parse_args()

    if args.all:
        try:
            # Calling methods on instantiated object to handle with OpenTargets API
            response = openTargets.get_association_filter()

            # Showing JSON result, if any
            print(json_dumps(response, indent=2, sort_keys=True))
        except Exception as e:
            print('Something wrong when trying to get information or during the results processing!\n\n%s' % e)
    elif args.target or args.disease:
        # Filter parameters
        target = (args.target if args.target else None)
        disease  = (args.disease if args.disease else None)

        try:
            # Calling methods on instantiated object to handle with OpenTargets API
            response = openTargets.stats_association_score(target = target, disease = disease)

            # Showing statistic results
            print('-' * 21)
            print('Statistics of \'association_score.overall\' filtering by %s%s%s:' % 
                    ('TARGET-ID=' + target if target else '', 
                     ', ' if (target and disease) else '', 
                     'DISEASE-ID=' + disease if disease else ''))
            print('-' * 21)
            print('  * maximum= %.8f,\n  * minimum= %.8f,\n  * average= %.8f,\n  * standard deviation= %.8f' % response)
            print('-' * 21)
        except Exception as e:
            print('Something wrong when trying to get information or during the results processing!\n\n%s' % e)
    elif args.test:
        # Call PyTest
        pytest.main(["-vv"], plugins=[TestOpenTargets()])
    else:
        # Missing arguments
        print ('Unknown command, missing arguments.')

if __name__ == "__main__":
    main()
