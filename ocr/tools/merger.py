import argparse
import os
import json
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description="This script merges two crops directories that was created by \"doctr_converter.py\"")
    parser.add_argument("--main_path", "-mp", type=str, help="Path to main directory (to directory with file \"labels.json\" in which will be copied files from subpath)", default="crops")
    parser.add_argument("--sub_path", "-sp", type=str, help="Path to sub directory (to directory with file \"labels.json\")", default="crops2")
    parser.add_argument("--save_dir", "-sd", type=str, help="Path to directory in which result will be stored", default="")
    parser.add_argument("--is_detection", "-is_d", type=bool, help="Is exist labels file for detection training", default=False)
    return parser.parse_args()

args = parse_args()
main_path = args.main_path
sub_path = args.sub_path
save_dir = args.save_dir
is_detection = args.is_detection


if save_dir == "":
    save_dir = main_path
if not(os.path.exists(save_dir)):
    os.mkdir(save_dir)
if not(os.path.exists(os.path.join(save_dir, "images"))):
    os.mkdir(os.path.join(save_dir, "images"))

f1 = open(os.path.join(main_path, "labels.json"), encoding="utf-8")
f2 = open(os.path.join(sub_path, "labels.json"), encoding="utf-8")
data1 = json.load(f1)
data2 = json.load(f2)
keys1 = data1.keys()
keys2 = data2.keys()

resdict = dict()
for key in keys1:
    resdict[key] = data1[key]
    if save_dir != main_path:
        past_path = os.path.join(main_path, "images", key)
        new_path = os.path.join(save_dir, "images", key)
        shutil.copy(past_path, new_path)
for key in keys2:
    past_path = os.path.join(sub_path, "images", key)
    new_path = os.path.join(save_dir, "images", key)
    resdict[key] = data2[key]
    shutil.copy(past_path, new_path)

fout = open(os.path.join(save_dir, "labels.json"), mode="wt", encoding="utf-8")
json.dump(resdict, fout)
