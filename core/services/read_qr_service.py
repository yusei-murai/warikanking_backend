from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import base64
import cv2
import numpy as np

class ReadQrService:
    #QRのbase64->原文
    def read_qr(binary_data: str):
        img_binary = base64.b64decode(binary_data)
        jpg = np.frombuffer(img_binary,dtype = np.uint8)
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        
        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

        if retval == False or decoded_info == "":
            return None
        
        return decoded_info[0]