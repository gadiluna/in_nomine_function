#!/bin/bash

# In Nomine Functions Team
# distributed under license: GPL 3 License http://www.gnu.org/licenses/

SOURCE_FILE=$1 # File with preprocesed assembly code of functions
OUT=$2         # File where to write name predictions
MODEL=$3       # Path to the trained model
REFERENCE=$3   # Reference file to compute precision and recall score

# For further argumnets for translation please look at: https://opennmt.net/OpenNMT-py/options/translate.html
# use -gpu 0 argument to run on gpu
python OpenNMT-py/translate.py --model $MODEL \
                    --src $SOURCE_FILE \
                    --beam_size 1 \
                    --max_length 10 \
                    --output $OUT \
                    --batch_size 256 \

if [ "$#" -ge 4 ]
then
  python precision_recall_metrics.py -candidate $OUT -reference $REFERENCE
fi