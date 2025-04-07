from mmocr.apis import MMOCRInferencer


class Ocr_Model:
    def __init__(self):
        self.model = MMOCRInferencer(det='DBNet', rec='svtr-small', device='cpu')

    def pred(self, path):
        return self.model(path)['predictions']['rec_texts']
