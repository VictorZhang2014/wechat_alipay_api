#! encoding: utf-8

import os

class CertificateManager:

    @staticmethod
    def readAliPayPublicKey() -> str:
        return CertificateManager.readFileContent("alipay_public_key.txt")

    @staticmethod
    def readAliPayPrivateKey() -> str:
        return CertificateManager.readFileContent("alipay_private_key.txt")

    @staticmethod
    def readFileContent(filename: str) -> str:
        try:
            current_folder_path = os.path.dirname(__file__)
            file_path = os.path.join(current_folder_path, "certs/{0}".format(filename))
            with open(file_path, "rb") as f:
                r = f.read()
                return str(r, encoding="utf-8")
        except Exception as e:
            return str(e)

