import argparse
import os
import json
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description="This script merges two crops directories that was created by \"doctr_converter.py\"")
    parser.add_argument("--path1", "-p1", type=str, help="Path to first directory (to directory with file \"labels.json\")", default="crops")
    parser.add_argument("--path2", "-p2", type=str, help="Path to second directory (to directory with file \"labels.json\")", default="crops2")
    parser.add_argument("--save_dir", "-sd", type=str, help="Path to directory in which result will be stored", default="merged")
    parser.add_argument("--is_detection", "-is_d", type=bool, help="Is exist labels file for detection training", default=False)
    return parser.parse_args()

args = parse_args()
path1 = args.path1
path2 = args.path2
save_dir = args.save_dir
is_detection = args.is_detection

if not(os.path.exists(save_dir)):
    os.mkdir(save_dir)
if not(os.path.exists(os.path.join(save_dir, "images"))):
    os.mkdir(os.path.join(save_dir, "images"))

f1 = open(os.path.join(path1, "labels.json"), encoding="utf-8")
f2 = open(os.path.join(path2, "labels.json"), encoding="utf-8")
data1 = json.load(f1)
data2 = json.load(f2)
keys1 = data1.keys()
keys2 = data2.keys()

resdict = dict()
for key in keys1:
    past_path = os.path.join(path1, "images", key)
    new_name = "from1_" + key
    new_path = os.path.join(save_dir, "images", new_name)
    resdict[new_name] = data1[key]
    shutil.copy(past_path, new_path)
for key in keys2:
    past_path = os.path.join(path2, "images", key)
    new_name = "from2_" + key
    new_path = os.path.join(save_dir, "images", new_name)
    resdict[new_name] = data2[key]
    shutil.copy(past_path, new_path)

fout = open(os.path.join(save_dir, "labels.json"), mode="wt", encoding="utf-8")
json.dump(resdict, fout)
