#!/bin/bash

SOURCE_FILE=$1 # File with preprocesed assembly code of functions
OUT=$2         # File where to write name predictions
MODEL=$3       # Path to the trained model
REFERENCE=$3   # Reference file to compute precision and recall score

# For further argumnets for translation please look at: https://opennmt.net/OpenNMT-py/options/translate.html
python translate.py --model $MODEL \
                    --src $SOURCE_FILE \
                    --beam_size 1 \
                    --gpu 0 \
                    --max_length 10 \
                    --output $OUT \
                    --batch_size 256 \

if [ $REFERENCE != "" ]
then
  python precision_recall_metrics.py -candidate $OUT -reference $REFERENCE
fi