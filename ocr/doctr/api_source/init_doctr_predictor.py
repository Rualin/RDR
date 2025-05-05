from os.path import isfile

import torch
from doctr.models import ocr_predictor, crnn_vgg16_bn, fast_base
from doctr.datasets import VOCABS


vocab = "".join(dict.fromkeys(VOCABS['russian'] + VOCABS['latin'] + '№'))


def init_doctr_predictor():
    det_weights = 'weights/det.pt'
    if isfile(det_weights):
        det_model = fast_base(pretrained=False, pretrained_backbone=False)
        det_params = torch.load(det_weights, map_location="cpu")
        det_model.load_state_dict(det_params)
    else:
        det_model = 'fast_base'

    reco_weights = 'weights/reco.pt'
    if isfile(reco_weights):
        reco_model = crnn_vgg16_bn(pretrained=False, pretrained_backbone=False, vocab=vocab)
        reco_param = torch.load(reco_weights, map_location="cpu")
        reco_model.load_state_dict(reco_param)
    else:
        reco_model = 'crnn_vgg16_bn'

    return ocr_predictor(det_arch=det_model,
                         reco_arch=reco_model,
                         pretrained=True,
                         assume_straight_pages=False)
