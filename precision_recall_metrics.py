# In Nomine Functions Team
# distributed under license: GPL 3 License http://www.gnu.org/licenses/

import argparse
import numpy as np

"""
Precision = #correctly_predicted_tokens / #predicted_tokens

Recall =  #correctly_predicted_tokens / #original_tokens
"""


def calculate_precision_recall(original_names, predicted_names):
    precision_list = list()
    recall_list = list()
    line_number = 0

    if len(original_names) == 0 or len(predicted_names) == 0:
        print("Fiorella Metrics Error Length 0")
        return np.float32(0.0), np.float32(0.0)

    for original_name, predicted_name in zip(original_names, predicted_names):
        if isinstance(original_name, list):
            original_name_tokens = list(set(original_name))
            predicted_name_tokens = list(set(predicted_name))
        else:
            original_name_tokens = list(set([x for x in original_name.strip("\n").split(" ") if len(x)>0]))
            predicted_name_tokens = list(set([x for x in predicted_name.strip("\n").split(" ") if len(x)>0]))


        # DUPLICATES IN ORIGINAL NAMES
        # it's not possible to have duplicated tokens in the original names because normalizations remove them -->
        # set(original_name_tokens) = list(original_name_tokens)

        # DUPLICATES IN PREDICTED NAMES
        # in the case in which there are duplicates in the predicted name, in the #correctly_predicted_tokens computation
        # we should not  consider them.
        # example:
        #	original_name = "open file"
        #	predicted_name = "open open file"
        #	#correctly_predicted_tokens = 2

        # num1 = len(set(original_name_tokens).intersection(set(predicted_name_tokens)))

        num = len(set(original_name_tokens) & set(predicted_name_tokens))

        if len(predicted_name_tokens) and len(original_name_tokens) > 0:
            per_func_precision = num / len(predicted_name_tokens)
            per_func_recall = num / len(original_name_tokens)
        else:
            per_func_precision = 0
            per_func_recall = 0

        precision_list.append(per_func_precision)
        recall_list.append(per_func_recall)
        line_number += 1

    precision = np.float32(sum(precision_list) / len(precision_list))
    recall = np.float32(sum(recall_list) / len(recall_list))
    return precision, recall


def compute_f1(precision, recall):
    if precision + recall > 0:
        f1 = (2 * precision * recall) / (precision + recall)
    else:
        f1 = 0
    return f1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-prediction", type=str, help="Prediction File", default=None)
    parser.add_argument("-reference", type=str,  default=None)
    parser.add_argument("-candidate", type=str,  default=None)
    parser.add_argument("-epoch", type=int, default=0)

    args = parser.parse_args()

    if args.prediction is not None:
        f = open(args.prediction)
        lines = f.readlines()
        lines = [l.split(",") for l in lines]
        original_names = [l[0] for l in lines]
        predicted_names = [l[1] for l in lines]
    if args.reference is not None and args.candidate is not None:
        f = open(args.reference)
        original_names = [l.strip() for l in f.readlines()]
        f.close()
        f = open(args.candidate)
        predicted_names = [l.strip().split(",")[0] for l in f.readlines()]
        f.close()

    #print("P-R of test set")
    precision,recall=calculate_precision_recall(original_names, predicted_names)
    f1 = (2 * precision * recall) / (precision + recall)
    print("{},{},{},{}".format(args.epoch,f1,precision,recall))
