# SAFE TEAM
# distributed under license: CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)

import argparse
import os
import sys
from subprocess import call

class Downloader:

    def __init__(self):
        parser = argparse.ArgumentParser(description='In Nomine Function downloader')

        parser.add_argument("--transformer_pt", dest="transformer_pt",
                            help="Download the trained transformer model for x86",
                            action="store_true",
                            required=False)

        parser.add_argument("--seq2seq_pt", dest="seq2seq_pt",
                            help="Download the trained seq2seq model for x86",
                            action="store_true",
                            required=False)

        parser.add_argument("--test_data", dest="test_data",
                            help="Download the test data for ubuntu dataset",
                            action="store_true",
                            required=False)

        parser.add_argument("--all_data", dest="all_data",
                            help="Download whole ubuntu dataset (! It require 30 GB of free space !)",
                            action="store_true",
                            required=False)

        args = parser.parse_args()

        self.download_transfomer = args.transformer_pt
        self.download_seqseq = args.seq2seq_pt
        self.download_test_data = args.test_data
        self.download_all_data = args.all_data

        if not (self.download_transfomer or self.download_seqseq or self.download_test_data or self.download_all_data):
            parser.print_help(sys.__stdout__)

        self.url_transfomer_pt_model = "https://drive.google.com/file/d/19-CD2wGk9hqaowJ8bEQ97t2linaPHUAx/view?usp=sharing"
        self.url_s2s_pt_model = "https://drive.google.com/file/d/1sV7zMPlJdBEHPUwZQWapRZNxCv7MofLS/view?usp=sharing"
        self.url_ubuntu_test_data = "https://drive.google.com/file/d/1QrP80FmkGgQ8eSjlb3n_2JWSEpR_3JfZ/view?usp=sharing"
        self.url_ubuntu_all_data = "https://drive.google.com/file/d/1LeDA8Naw5SxKWyjX33lNQOpzIhjH2WDz/view?usp=sharing"

        self.base_path = "data"
        self.path_transformer_pt = os.path.join(self.base_path, "models")
        self.path_s2s_pt = os.path.join(self.base_path, "models")
        self.path_ubuntu_test_data = os.path.join(self.base_path, "")
        self.path_ubuntu_all_data = os.path.join(self.base_path, "")

        self.path_transformer_pt_compress_name = "pretrained_transformer.tar.bz2"
        self.path_s2s_pt_compress_name = "pretrained_seq2seq.tar.bz2"
        self.path_ubuntu_test_data_compress_name = "ubuntu_test_data.tar.bz2"
        self.path_ubuntu_all_data_compress_name = "ubuntu_all_data.tar.bz2"

    @staticmethod
    def download_file(id, path):
        try:
            print("Downloading from "+ str(id) +" into "+str(path))
            call(['./godown.pl',id,path])
        except Exception as e:
            print("Error downloading file at url:" + str(id))
            print(e)

    @staticmethod
    def decompress_file(file_src,file_path):
        try:
            call(['tar','-xvf',file_src,'-C',file_path])
        except Exception as e:
            print("Error decompressing file:" + str(file_src))
            print('you need tar command e b2zip support')
            print(e)

    def download(self):
        print('Making the godown.pl script executable, thanks:'+str('https://github.com/circulosmeos/gdown.pl'))
        call(['chmod', '+x','godown.pl'])
        print("SAFE --- downloading models")

        if self.download_transfomer:
            print("Downloading transformer_pt model.... in the folder data/models/")
            if not os.path.exists(self.path_transformer_pt):
                os.makedirs(self.path_transformer_pt)
            Downloader.download_file(self.url_transfomer_pt_model, os.path.join(self.path_transformer_pt, \
                                                                                self.path_transformer_pt_compress_name))

            print("Decompressing transformer_pt model and placing in" + str(self.path_transformer_pt))
            Downloader.decompress_file(os.path.join(self.path_transformer_pt, self.path_transformer_pt_compress_name), \
                                       self.path_transformer_pt)

        if self.download_transfomer:
            print("Downloading transformer_pt model.... in the folder data/models/")
            if not os.path.exists(self.path_transformer_pt):
                os.makedirs(self.path_transformer_pt)
            Downloader.download_file(self.url_transfomer_pt_model, os.path.join(self.path_transformer_pt, \
                                                                                self.path_transformer_pt_compress_name))

            print("Decompressing transformer_pt model and placing in" + str(self.path_transformer_pt))
            Downloader.decompress_file(os.path.join(self.path_transformer_pt, self.path_transformer_pt_compress_name), \
                                       self.path_transformer_pt)

        if self.download_seqseq:
            print("Downloading seq2seq_pt model.... in the folder data/models/")
            if not os.path.exists(self.path_s2s_pt):
                os.makedirs(self.path_s2s_pt)
            Downloader.download_file(self.url_transfomer_pt_model, os.path.join(self.path_s2s_pt, \
                                                                                self.path_transformer_pt_compress_name))

            print("Decompressing seq2seq_pt model and placing in" + str(self.path_s2s_pt))
            Downloader.decompress_file(os.path.join(self.path_s2s_pt, self.path_s2s_pt_compress_name), \
                                       self.path_s2s_pt)

        if self.download_test_data:
            print("Downloading test data.... in the folder data/")
            if not os.path.exists(self.path_ubuntu_test_data):
                os.makedirs(self.path_ubuntu_test_data)
            Downloader.download_file(self.path_ubuntu_test_data, os.path.join(self.path_ubuntu_test_data, \
                                                                                self.path_ubuntu_test_data_compress_name))

            print("Decompressing ubuntu test dataset and placing in" + str(self.path_ubuntu_test_data))
            Downloader.decompress_file(os.path.join(self.path_ubuntu_test_data, self.path_ubuntu_test_data_compress_name), \
                                       self.path_ubuntu_test_data)

        if self.download_all_data:
            print("Downloading all data.... in the folder data/")
            if not os.path.exists(self.path_ubuntu_all_data):
                os.makedirs(self.path_ubuntu_all_data)
            Downloader.download_file(self.path_ubuntu_all_data, os.path.join(self.path_ubuntu_all_data, \
                                                                                self.path_ubuntu_all_data_compress_name))

            print("Decompressing all ubuntu dataset and placing in" + str(self.path_ubuntu_all_data))
            Downloader.decompress_file(os.path.join(self.path_ubuntu_all_data, self.path_ubuntu_all_data_compress_name), \
                                       self.path_ubuntu_all_data)


if __name__=='__main__':
    a=Downloader()
    a.download()