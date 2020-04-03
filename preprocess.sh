#!/bin/bash

DATA_FOLDER=data/ubuntu_all_data/

TRAIN_SRC=$DATA_FOLDER/ubuntu_ds_train.asm
TRAIN_TGT=$DATA_FOLDER/ubuntu_ds_train.name
VALID_SRC=$DATA_FOLDER/ubuntu_ds_validation.asm
VALID_TGT=$DATA_FOLDER/ubuntu_ds_validation.name

VOCAB_SOURCE=$DATA_FOLDER/asm_vocabulary.txt
VOCAB_TARGET=$DATA_FOLDER/name_vocabulary.txt

PREPROCESSED_FOLDER=data/preprocessed_ubuntu_dataset/

python OpenNMT-py/preprocess.py -train_src $TRAIN_SRC -train_tgt $TRAIN_TGT \
		-valid_src $VALID_SRC -valid_tgt $VALID_TGT \
		-save_data $PREPROCESSED_FOLDER/ubuntu_dataset_preprocessed \
                -src_vocab_size 200000 \
                -tgt_vocab_size 2000 \
		            -num_threads 10 \
                -min_src_length 5 -min_tgt_length 1 \
                -src_seq_length_trunc 500 --tgt_seq_length_trunc 10 \
                -shard_size 50000 \
                -report_every 10000



