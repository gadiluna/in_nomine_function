# In Nomine Function

Models and code for the paper: 

**In Nomine Function: Naming Functions in Stripped Binaries with Neural Networks**

**TL;DR**: We used a transformer model to predict function name in a stripped binary.

If you are using this code please cite:

```json
@article{artuso2019nomine,
  title={In Nomine Function: Naming Functions in Stripped Binaries with Neural Networks},
  author={Artuso, Fiorella and Di Luna, Giuseppe Antonio and Massarelli, Luca and Querzoni, Leonardo},
  journal={arXiv},
  year={2019}
}
```

## Quickstart

Using our model to predict names for a stripped binary is straightforward.

After cloning this repo, install all requirements:

```shell script
pip install -r requirements.txt
```

Download the transformer models:
```shell script
python downloader.py --transformer_pt
```
This will download the pretrained transformer model described in the paper in the folder *data/model/* .

Then you need to dump the assembly code for unnamed funtions in your stripped binary:
```shell script
python dump_data_from_binary.py -i [YOUR_BINARY] -o [SUFFIX]
```
This will create two files: [SUFFIX].asm where each line correspond to the dumped assembly code for a function and
[SUFFIX].meta where each line correspond to the address and the name of each function.

Finally, launch the predictions:
```shell script
./predict.sh [SUFFIX].name [PREDICTION_FILE] data/model/model.transformer_asm_name_step_219400.pt
```
This will predict the names for the functions in your binary and will print them in the prediction file, each line 
in the prediction file represent the predicted name for the corresponding line in [SUFFIX].asm and [SUFFIX].name files.

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


