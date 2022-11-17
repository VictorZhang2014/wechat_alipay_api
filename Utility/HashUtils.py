#! encoding: utf-8

import base64
import hashlib
import uuid
import hmac

class HashUtils:

    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    @staticmethod
    def md5(unencrypted_str):
        '''
        参考文档：https://docs.python.org/2/library/hashlib.html#module-hashlib
        :param unencrypted_str: 未加密字符串
        :return: 加密后的字符串
        '''
        m = hashlib.md5()
        m.update(unencrypted_str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def hmac_sha256(unencrypted_str):
        message = bytes(unencrypted_str, 'utf-8')
        secret = bytes('the shared secret key here', 'utf-8')

        hash = hmac.new(secret, message, hashlib.sha256)
        # to lowercase hexits
        hash.hexdigest()
        # to base64
        return base64.b64encode(hash.digest())


    @staticmethod
    def sha256(unencrypted_str):
        return hashlib.sha256(unencrypted_str.encode("utf-8")).hexdigest()


    @staticmethod
    def sha1(unencrypted_str):
        return hashlib.sha1(unencrypted_str.encode("utf-8")).hexdigest()


    @staticmethod
    def base64_encode(unencrypted_str):
        return base64.b64encode(unencrypted_str) 
 

