import os
from argparse import ArgumentParser

import cv2
import numpy as np


def update(shape_info: np.ndarray, value: int):
    if value < shape_info[0]:
        shape_info[0] = value
    elif value > shape_info[1]:
        shape_info[1] = value
    shape_info[2] += value


def print_info(shape_info: np.ndarray, prefix: str, num_of_crops: int):
    print(f"({prefix}_min: {shape_info[0]} | {prefix}_max: {shape_info[1]} | {prefix}_avg: {shape_info[2] / num_of_crops})")


def parse_args():
    parser = ArgumentParser(description="This script analyzes shapes of crops and print MAX, MIN, AVG values")
    parser.add_argument("--data", "-d", type=str, required=True,
                        help="Path to folder with crops")
    return parser.parse_args()


def main():
    args = parse_args()

    h_info = np.array([np.inf, -1, 0])
    w_info = np.array([np.inf, -1, 0])
    num_of_crops = 0
    for file_name in os.listdir(args.data):
        crop = cv2.imread(os.path.join(args.data, file_name))
        update(h_info, crop.shape[0])
        update(w_info, crop.shape[1])
        num_of_crops += 1

    print_info(h_info, "h", num_of_crops)
    print_info(w_info, 'w', num_of_crops)


if __name__ == "__main__":
    main()
