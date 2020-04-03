# In Nomine Function

Models and code for the paper: 

**In Nomine Function: Naming Functions in Stripped Binaries with Neural Networks**

**TL;DR**: We used a transformer model to predict function name in a stripped binary.

If you are using this code please cite:

```shell script
@article{artuso2019nomine,
  title={In Nomine Function: Naming Functions in Stripped Binaries with Neural Networks},
  author={Artuso, Fiorella and Di Luna, Giuseppe Antonio and Massarelli, Luca and Querzoni, Leonardo},
  journal={arXiv},
  year={2019}
}
```

## Quickstart
Using our model to predict names for a stripped binary is straightforward.
Here we'll show how to predict function names for a given binary.
In this example we will use the same gonnacry sample we used in our paper.

*Requirements*: You need radare2 installed on your machine. To install it look at https://github.com/radareorg/radare2.

---

### Clone this repo and install dependencies

First of all clone this repository:
```shell script
git clone --recursive https://github.com/lucamassarelli/in_nomine_function 
```

After cloning the repo, install all requirements:
```shell script
pip install -r requirements.txt
```
---

### Download trained model

Now you need to download the trained model. To download the transformer_pt model:
```shell script
python downloader.py --transformer_pt
```
This will download the pretrained transformer model described in the paper in the folder *data/model/* .

---

### Disassemble the executable to analise

Then, you need to dump the assembly code for unnamed funtions in your stripped binary:
```shell script
python dump_data_from_binary.py -i gonnacry.o -o data/gonnacry -s
```

This will create two files: *data/gonnacry.asm* where each line correspond to the dumped assembly code for a function and
*data/gonnacry.meta* where each line correspond to the address and the name of each function. The *-s* option tells to 
script to dump all functions in the binary, also the ones that are referenced by a symbol.

---

### Predict!

Finally, launch the predictions:
```shell script
./predict.sh data/gonnacry.asm data/gonnacry.pred data/model/model.transformer_asm_name_step_219400.pt
```
This will predict the names for the functions in your binary and will print them in the prediction file, each line 
in the prediction file represent the predicted name for the corresponding line in *data/gonnacry.asm*
and *data/gonnacry.meta* files.

---

Of course, you can replace gonnacry binary with any unix X86 executable of your choice.

## Reproducing paper results
We are committed to permit an easy reproduction of research result. We hope that the information below will permit to 
anyone to reproduce an easy reproduction of the results in our research paper.

### Downloading ubuntu dataset

If you want to download the whole ubuntu dataset described in the paper, you can use 
(*This operation needs 40 GB of free space*):
```shell script
python downloader.py --all_data
```

You can also download only the test set of the ubuntu dataset:
```shell script
python downloader.py --test_data
```

### Reproducing results on the test set

Once downloaded the ubuntu test set you can run:
```shell script
./predict.sh data/ubuntu_test_data/ubuntu_ds_test.asm \
             ubuntu_ds_test.pred \
             data/model/model.transformer_asm_name_step_219400.pt \
             data/ubuntu_test_data/ubuntu_ds_test.name
```
This will predict names for the functions in the test set and then it will compute precision, recall and f1 score on them.

You can also predict names using our pretrained seq2seq model. To download it:
```shell script
python downloader.py --seq2seq_pt
```
## Acknowledgements

In our code we use godown to download data from Google drive. We thank circulosmeos, the creator of godown.


