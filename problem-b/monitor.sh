#!/bin/bash

if [ -z "$2" ]; then
    # default total number of recurds of '17.12_evidence_data.json' file
    totLines=5784598
else
    totLines=$2
fi
curLines=`wc -l $1 | awk '{print $1}'`

perConclusion=`bc <<< "scale = 5; (($curLines / $totLines) * 100)"`
echo "=>"   $perConclusion "%"