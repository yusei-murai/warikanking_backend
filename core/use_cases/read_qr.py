from core.entities.qr import Qr

class ReadQr:
    def read_qr(self,qr: Qr):
        result = qr.read_qr()
        return result