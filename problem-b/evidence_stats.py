#!/usr/bin/python3
# ------------------------------------------------------------------------------
# EMBL-EBI (SW Dev. 01279) coding exame
# ------------------------------------------------------------------------------
# Douglas Bezerra Beniz, douglasbeniz@gmail.com
# ------------------------------------------------------------------------------
# Problem B - parse a (huge) JSON dump
# ------------------------------------------------------------------------------
import io
import os
import json
import multiprocessing as mp
import pandas as pd

from argparse import ArgumentParser
from time import localtime, sleep, strftime

FILE_NAME = '17.12_evidence_data.json'
KEYS_PATH = ['target.id', 'disease.id', 'scores.association_score']
KEYS_STATS = [('scores.association_score','median'), ('scores.association_score','_top_three')]
#PARSER_FILE_OUT = 'parsing_results%s.csv' % strftime('_%Y%m%d_%H%M%S', localtime())
PARSER_FILE_OUT = 'results_20180916_041646.csv'
STATS_FILE_OUT = 'stats_results%s.csv' % strftime('_%Y%m%d_%H%M%S', localtime())
STOP_TOKEN = '5t@p_T0k3n'

"""
Listen for messages on the q, writes to file.
"""
def listener(queue):
    try:
        output = open(PARSER_FILE_OUT, 'a')
        stopReceived = False
        while 1:
            task = queue.get()
            if task == STOP_TOKEN:
                stopReceived = True
            if queue.qsize() == 0 and stopReceived:
                break
            else:
                output.write(','.join(task) + '\n')
        output.close()
    except Exception as e:
        raise Exception('Error on thread to write final CSV file!\n\n%s' % str(e.args[0]))

"""
Process a chunk of the JSON file
"""
def process_wrapper(jsonFileName, chunkStart, chunkSize, queue):
    try:
        with open(PARSER_FILE_OUT, 'a') as output:
            with open(jsonFileName, 'r') as json_file:
                # Look for desired chunk
                json_file.seek(chunkStart)
                # Load all records of this chunk
                lines = json_file.read(chunkSize).splitlines()

                for line in lines:
                    record = ['', '', '']

                    json_object = json.loads(line)

                    for index in range(3):
                        key  = KEYS_PATH[index].split('.')[0]
                        item = KEYS_PATH[index].split('.')[1]
                        record[index] = str(json_object[key][item])

                    queue.put(record)
            json_file.close()
        output.close()
    except Exception as e:
        raise Exception('Error while parsing and getting desired info!\n\n%s' % str(e.args[0]))


"""
Split the JSON file in chunks that should be process in parallel.
"""
def chunkify(fname, size=1024*1024):
    try:
        fileEnd = os.path.getsize(fname)
        if size > fileEnd:
            size = fileEnd

        with open(fname,'rb') as json_file:
            chunkEnd = json_file.tell()

            while True:
                chunkStart = chunkEnd
                json_file.seek(size,1)
                json_file.readline()
                chunkEnd = json_file.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break
        json_file.close()
    except Exception as e:
        raise Exception('Error while trying to chunkify full JSON file!\n\n%s' % str(e.args[0]))

"""
Parse the JSON file.
"""
def parse_json(jsonFile):
    try:
        # -----------------------------
        # Maximum of cores (CPUs) available
        cores = mp.cpu_count()

        # Initialize objects
        jobs = []

        manager = mp.Manager()
        queue   = manager.Queue()
        pool    = mp.Pool(cores)

        #put listener to work first
        watcher = pool.apply_async(listener, (queue,))

        # Prepare output, at first simply erase, if any, then open to append data
        erase = open(PARSER_FILE_OUT, 'w')
        erase.write(','.join(KEYS_PATH) + '\n')
        erase.close()

        # Create jobs
        for chunk_start, chunk_size in chunkify(jsonFile):
            jobs.append(pool.apply_async(process_wrapper, (jsonFile, chunk_start, chunk_size, queue)))

        # Wait for all jobs to finish
        for job in jobs:
            job.get()

        # Now we are done, kill the listener
        queue.put(STOP_TOKEN)

        # Clean up
        pool.close()

        while queue.qsize() > 0:
            sleep(10)
    except Exception as e:
        raise Exception('Error while trying to parse the JSON file!\n\n%s' % str(e.args[0]))


def process_stats(csvFile):
    try:
        # Load parsed CSV file from previous JSON processment
        csv_data = pd.read_csv(csvFile)

        def _top_three(dataFrame):
             top_list = []
             for item in dataFrame.nlargest(3):
                 top_list.append(item)
             return top_list
        # ------------------------------------
        # Desired:
        #   > for each ​ 'target.id​', ​'disease.id' pair, calculates the median and
        # the top 3 association_score​;
        #   > outputs the resulting table in ​CSV format, sorted in ascending
        # order by the 'median' value of the '​association_score';
        # ------------------------------------
        # Calculate, this could take a while...
        aggFrame = csv_data.groupby([KEYS_PATH[0], KEYS_PATH[1]]).agg({
            KEYS_PATH[2]: ['median', _top_three]})
        # Sorting and storing the result in a CSV file...
        aggFrame.sort_values(by=[KEYS_STATS[0], KEYS_PATH[0], KEYS_PATH[1]]).to_csv(STATS_FILE_OUT, sep=';')
    except Exception as e:
        raise Exception('Error while trying to process statistics!\n\n%s' % str(e.args[0]))

"""
Principal method
"""
def main():
    # Initialization
    json_file = FILE_NAME

    # Parsing input paramenters
    parser = ArgumentParser()

    parser.add_argument("-s", "--stats", action="store_true",
        help="Parse JSON file gathering important info and saving them into a CSV file.")

    parser.add_argument("-f", "--file", type=str,
        help="Inform a JSON file name to analyze, otherwise will look for the use default, \'17.12_evidence_data.json\'.")

    args = parser.parse_args()

    if args.file:
        try:
            json_file = args.file
        except Exception as e:
            print('Error when setting file name!')
            exit()

    if args.stats:
        try:
            print('-' * 21)
            print('Parsing JSON file: \'%s\', this could take a while...\n\n' % json_file)

            # At first, parse the JSON file...
            #parse_json(json_file)

            print('-' * 21)
            print('JSON file was successfully parsed as \'%s\'!\n\n' % PARSER_FILE_OUT)

            print('-' * 21)
            print('Starting the creation of summarized statistics, this could also take a while...\n\n')

            # Then, process statistics...
            process_stats(PARSER_FILE_OUT)
            print('Statistics CSV file was successfully created as \'%s\'!\n' % STATS_FILE_OUT)

        except Exception as e:
            print('Fatal error!\n\n')
            print(e.args[0])
            exit()
    else:
        print('Please, inform one action!\n\nUse <-h> parameter for help.\n')


if __name__ == "__main__":
    main()
