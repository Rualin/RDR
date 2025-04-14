import os
import json
from argparse import ArgumentParser
import math
from hashlib import sha256

import cv2


det_labels = dict()
crops_labels = dict()
repeats = set()


def parse_args():
    parser = ArgumentParser(description="This script converts label-studio dataset format in docTR dataset format")
    parser.add_argument('ls_label_file', type=str, help='Path to label studio label file (.json)')
    parser.add_argument('local_img_dir', type=str, help="Path to directory with images")
    parser.add_argument('save_dir', type=str, help="Path to directory where to save crops")
    parser.add_argument('--en_det', type=bool, help="Also create label file for detection training", default=False)
    return parser.parse_args()


def read_image(local_img_dir: str, remote_img: str):
    # .replace is used here because label-studio read '!' as '%21'
    # so we have to delete these symbols
    img_name = remote_img[remote_img.rfind("/") + 1:].replace("%21", "")
    local_img = os.path.join(local_img_dir, img_name)
    image_bgr = cv2.imread(local_img)
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), img_name


def get_bbox_cords(value: dict, image_shape: list) -> dict:
    return {
        'x': int(math.floor(value['x'] / 100 * image_shape[1])),
        'y': int(math.floor(value['y'] / 100 * image_shape[0])),
        'width': int(math.ceil(value['width'] / 100 * image_shape[1])),
        'height': int(math.ceil(value['height'] / 100 * image_shape[0]))
    }


def make_det_label(image, img_name: str):
    det_labels[img_name] = {
        'img_dimensions': image.shape[0:2],
        'img_hash': sha256(str.encode(img_name)).hexdigest(),
        'polygons': []
    }


def add_polygon(bbox_cords: dict, img_name: str):
    polygon = [
        [bbox_cords['x'], bbox_cords['y']],
        [bbox_cords['x'] + bbox_cords['width'], bbox_cords['y']],
        [bbox_cords['x'], bbox_cords['y'] + bbox_cords['height']],
        [bbox_cords['x'] + bbox_cords['width'], bbox_cords['y'] + bbox_cords['height']]
    ]

    det_labels[img_name]['polygons'].append(polygon)


def make_crop(bbox_cords: dict, image, crop_id: int) -> tuple[list, str]:
    crop = image[
        bbox_cords['y']:bbox_cords['y'] + bbox_cords['height'],
        bbox_cords['x']:bbox_cords['x'] + bbox_cords['width']
    ]
    crop_name = str(crop_id) + '.png'

    return crop, crop_name


def main():
    args = parse_args()

    crops_dir = os.path.join(args.save_dir, 'images')
    if not os.path.isdir(crops_dir):
        os.mkdir(crops_dir)

    crop_id = 0
    label_file = open(args.ls_label_file, "r")
    with label_file:
        annotations = json.load(label_file)
        for label_obj in annotations:
            image, img_name = read_image(args.local_img_dir, label_obj['data']['ocr'])
            if args.en_det:
                make_det_label(image, img_name)
            for label_info in label_obj['annotations'][0]['result']:
                if label_info['type'] == 'textarea':
                    bbox_cords = get_bbox_cords(label_info['value'], image.shape)
                    if args.en_det:
                        add_polygon(bbox_cords, img_name)
                    if label_info['value']['text'][0] not in repeats:
                        crop, crop_name = make_crop(bbox_cords, image, crop_id)
                        crops_labels[crop_name] = label_info['value']['text'][0]
                        cv2.imwrite(os.path.join(crops_dir, crop_name), crop)
                        repeats.add(label_info['value']['text'][0])
                        crop_id += 1

    crops_labels_file = open(os.path.join(args.save_dir, "labels.json"), "wt")
    with crops_labels_file:
        json.dump(crops_labels, crops_labels_file)

    if args.en_det:
        det_labels_file = open(os.path.join(args.save_dir, "det_labels.json"), "wt")
        with det_labels_file:
            json.dump(det_labels, det_labels_file)


if __name__ == "__main__":
    main()
