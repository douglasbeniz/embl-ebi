#!/usr/bin/python3
# ------------------------------------------------------------------------------
# EMBL-EBI (SW Dev. 01279) coding exame
# ------------------------------------------------------------------------------
# Douglas Bezerra Beniz
# ------------------------------------------------------------------------------
# Problem A - query a REST API
# ------------------------------------------------------------------------------
import argparse
import pytest
import requests
import json
import numpy

"""
Class to take care of all available resources of OpenTargets API
For more info, see: http://api.opentargets.io/v3/platform/docs
"""
class OpenTargets:
    BASE_URL = 'https://api.opentargets.io/v3/platform/public'

    def __init__(self):
        pass

    def _association_url(self, method):
        return self.BASE_URL + '/association' + ('/' + method) if method else ''

    def _evidence_url(self, method):
        return self.BASE_URL + '/evidence' + ('/' + method) if method else ''

    def _search_url(self, method):
        return self.BASE_URL + '/search' + ('/' + method) if method else ''

    def _utils_url(self, method):
        return self.BASE_URL + '/utils' + ('/' + method) if method else ''


    def get_association_filter(self, target=None, disease=None):
        payload = {}
        if target:
            payload['target'] = target
        if disease:
            payload['disease'] = disease

        response = requests.get(self._association_url('filter'), params=payload)

        if response.status_code != 200:
            raise Exception('Error fetching URL: %s' % response.status_code)
        else:
            return response.json()

    def stats_association_score(self, target=None, disease=None):
        try:
            response = self.get_association_filter(target=target, disease=disease)
        except Exception as e:
            raise e

        return self.calc_stats_association_score(response)


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
            maxVal = numpy.max(overallValues)
            minVal = numpy.min(overallValues)
            avgVal = numpy.average(overallValues)
            stdVal = numpy.std(overallValues)

        return maxVal, minVal, avgVal, dstVal

"""
Class to perform a suit of specific tests
"""
class TestOpenTargets:
    # basic method
    def calculateOne(self):
        return 1

    # assertion of calculate_one method return
    def test_calculateOne(self):
        assert self.calculateOne() == 1

"""
main()
"""
def main():
    # Instance of an OpenTargets
    openTargets = OpenTargets()

    # Parsing input paramenters
    parser = argparse.ArgumentParser()
    #parser.add_argument("-h", "--help", action="store_true", help="Display all available input parameters.")
    parser.add_argument("-t", "--target", type=str, 
        help="Query for target-related information (eg. use the string ENSG00000157764 as a target id).")
    parser.add_argument("-d", "--disease", type=str, 
        help="Query for disease-related information (eg. use the string EFO_0002422​ as a disease id).")
    parser.add_argument("-a", "--all", action="store_true", help="Get all filtered associations.")
    parser.add_argument("--test", action="store_true", help="Runs a suit of tests")
    parser.add_argument("-v", "--verbose", help="Increases output verbosity", action="store_true")

    args = parser.parse_args()

    if args.target or args.disease:
        # parameters
        target = (args.target if args.target else None)
        disease  = (args.disease if args.disease else None)
        # calling methods on instantiated object to handle with OpenTargets API
        response = openTargets.stats_association_score(target = target, disease = disease)

        # Showing the results
        print('-' * 21)
        print('Statistics of \'association_score.overall\' filtering by %s%s%s:' % 
                ('target=' + target if target else '', 
                 ', ' if (target and disease) else '', 
                 'disease=' + disease if disease else ''))
        print('-' * 21)
        print('  * maximum= %.8f,\n  * minimum= %.8f,\n  * average= %.8f,\n  * standard deviation= %.8f' % response)
        print('-' * 21)
    elif args.all:
        response = openTargets.get_association_filter()

        print(json.dumps(response, indent=2, sort_keys=True))
    elif args.test:
        pytest.main(["-v"], plugins=[TestOpenTargets()])
    else:
        print ('Unknown command, missing arguments.')

if __name__ == "__main__":
    main()
