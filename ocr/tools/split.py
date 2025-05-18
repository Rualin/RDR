import os
import json
from argparse import ArgumentParser

import numpy as np


class Bernulli:
    def __init__(self, p: float):
        self.random_gen = np.random.default_rng()
        self.p = p

    def __call__(self) -> bool:
        return self.random_gen.uniform() <= self.p


def make_paths(output: str, split_name: str) -> tuple[str, str]:
    split_dir = os.path.join(output, split_name)
    os.makedirs(split_dir, exist_ok=True)
    split_dir_images = os.path.join(split_dir, "images")
    os.makedirs(split_dir_images, exist_ok=True)
    return split_dir, split_dir_images


def dump_labels(labels: dict, dst_folder: str):
    with open(os.path.join(dst_folder, "labels.json"), "wt") as labels_file:
        json.dump(labels, labels_file)


def parse_args():
    parser = ArgumentParser(description="This script splits data")
    parser.add_argument("-p", "--part", type=float, required=True,
                        help="How many percents of data are taken for val")
    parser.add_argument("-l", "--labels", type=str, required=True,
                        help="Path to json file with labels")
    parser.add_argument("-d", "--data", type=str, required=True,
                        help="Path to dir which stores source images")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Path to dir where to save split data and labels")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.labels, "rt") as labels_file:
        labels = json.load(labels_file)

    train_folder, train_folder_images = make_paths(args.output, "train")
    val_folder, val_folder_images = make_paths(args.output, "valid")

    train_labels = {}
    val_labels = {}
    bernulli = Bernulli(args.part)
    for file_name in os.listdir(args.data):
        if bernulli():
            dst_folder_images = val_folder_images
            dst_labels = val_labels
        else:
            dst_folder_images = train_folder_images
            dst_labels = train_labels
        os.system(f"cp -u {os.path.join(args.data, file_name)} {os.path.join(dst_folder_images, file_name)}")
        dst_labels[file_name] = labels[file_name]

    dump_labels(val_labels, val_folder)
    dump_labels(train_labels, train_folder)


if __name__ == "__main__":
    main()
