from core.services.read_qr_service import ReadQrService

class ReadQr:
    def read_qr(self,binary_data: str):
        result = ReadQrService.read_qr(binary_data)
        
        return result