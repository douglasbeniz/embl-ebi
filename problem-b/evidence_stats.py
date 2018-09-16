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

from time import localtime, sleep, strftime

#FILE_NAME = '17.12_evidence_data.json'
FILE_NAME   = 'evidence_excerpt.json'
#FILE_NAME = 'evidence_excerpt_short.json'
FILE_OUT    = 'results%s.csv' % strftime('_%Y%m%d_%H%S%m', localtime())
KEYS_PATH   = ['target.id', 'disease.id', 'scores.association_score']
STOP_TOKEN  = '5t@p_T0k3n'

"""
Listen for messages on the q, writes to file.
"""
def listener(queue):
    try:
        output = open(FILE_OUT, 'a')
        stopReceived = False
        while 1:
            task = queue.get()
            if task == STOP_TOKEN:
                stopReceived = True
            if queue.qsize() == 0 and stopReceived:
                break
            else:
                output.write(', '.join(task) + '\n')
        output.close()
    except Exception as e:
        raise('Error on thread to write final CSV file!\n\n%s' % e)

"""
Process a chunk of the JSON file
"""
def process_wrapper(chunkStart, chunkSize, queue):
    try:
        with open(FILE_OUT, 'a') as output:
            with open(FILE_NAME, 'r') as json_file:
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
        raise('Error while parsing and getting desired info!\n\n%s' % e)

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
        raise('Error while trying to chunkify full JSON file!\n\n%s' % e)


"""
Principal method
"""
def main():
    # -----------------------------
    # Maximum of cores available
    cores = mp.cpu_count()

    # Initialize objects
    jobs = []

    manager = mp.Manager()
    queue = manager.Queue()
    pool = mp.Pool(cores)

    #put listener to work first
    watcher = pool.apply_async(listener, (queue,))

    # Prepare output, at first simply erase, if any, then open to append data
    erase = open(FILE_OUT, 'w')
    erase.write(', '.join(KEYS_PATH) + '\n')
    erase.close()

    # Create jobs
    for chunkStart, chunkSize in chunkify(FILE_NAME):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize, queue)))

    # Wait for all jobs to finish
    for job in jobs:
        job.get()

    # Now we are done, kill the listener
    queue.put(STOP_TOKEN)

    # Clean up
    pool.close()

    while queue.qsize() > 0:
        sleep(10)


if __name__ == "__main__":
    main()