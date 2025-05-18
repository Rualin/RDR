from os.path import isfile

import torch
from doctr.models import ocr_predictor, recognition, detection
from doctr.datasets import VOCABS


vocab = "".join(dict.fromkeys(VOCABS["russian"] + VOCABS["latin"] + "№"))


def init_doctr_predictor(det_arch: str, reco_arch: str):
    if isfile("weights/det.pt"):
        det_model = detection.__dict__[det_arch](pretrained=False, pretrained_backbone=False)
        det_params = torch.load("weights/det.pt", map_location="cpu")
        det_model.load_state_dict(det_params)
    else:
        det_model = det_arch

    if isfile("weights/reco.pt"):
        reco_model = recognition.__dict__[reco_arch](pretrained=False, pretrained_backbone=False, vocab=vocab)
        reco_param = torch.load("weights/reco.pt", map_location="cpu")
        reco_model.load_state_dict(reco_param)
    else:
        reco_model = reco_arch

    return ocr_predictor(det_arch=det_model,
                         reco_arch=reco_model,
                         pretrained=True,
                         assume_straight_pages=False)
