import dataclasses
import base64
import cv2
import numpy as np

@dataclasses.dataclass(frozen=True)
class QrId:
    id: str

@dataclasses.dataclass(frozen=True)
class QrBinaryData:
    binary_data: str

class Qr:
    def __init__(self, id: QrId, binary_data: QrBinaryData):
        self.id = id
        self.binary_data = binary_data
        
    #QRのbase64->原文
    def read_qr(self):
        img_binary = base64.b64decode(self.binary_data)
        jpg = np.frombuffer(img_binary,dtype = np.uint8)
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        
        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

        if retval == False or decoded_info == "":
            return None
        
        return decoded_info[0]
        
    