import os
import json
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="This script deletes repeated words from crops dataset")
    parser.add_argument("-l", "--labels", type=str, required=True,
                        help="Path to labels.json of dataset")
    parser.add_argument("-d", "--data", type=str, required=True,
                        help="Path to folder with crops")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.labels, "rt") as labels_file:
        labels = json.load(labels_file)

    repeats = set()
    cleaned_labels = {}
    for file_name in labels:
        if labels[file_name] not in repeats:
            cleaned_labels[file_name] = labels[file_name]
            repeats.add(labels[file_name])
        else:
            os.system(f"rm {os.path.join(args.data, file_name)}")

    cleaned_labels_path = args.labels[:args.labels.rfind("/") + 1] + "cleaned_labels.json"
    with open(cleaned_labels_path, "wt") as cleaned_labels_file:
        json.dump(cleaned_labels, cleaned_labels_file)


if __name__ == "__main__":
    main()
