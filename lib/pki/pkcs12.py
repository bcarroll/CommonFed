import logging
from OpenSSL import crypto
logging.basicConfig(level=logging.DEBUG)
class PKCS12():
    logging.debug('PKCS12 object instantiated')
    def __init__(self, p12_file, password=None):
        logging.debug('Initializing p12 file: %s' % p12_file)
        p12 = None
        self.password = password
        try:
            if self.password is None:
                logging.debug('Password not specified for p12 file')
                p12 = crypto.load_pkcs12(open(p12_file, 'rb').read(), self.password)
            else:
                p12 = crypto.load_pkcs12(open(p12_file, 'rb').read(), bytes(self.password, 'utf8'))
            self.cert  = p12.get_certificate()     # (signed) certificate object
            self.key   = p12.get_privatekey()      # private key.
            self.chain = p12.get_ca_certificates() # ca chain.
        except crypto.Error as e:
            tip = ""
            if password is None:
                tip = '  Incorrect password specified?'
            message = 'Unable to open keystore.%s' % tip
            logging.exception(message)
            raise AttributeError (message)

    def get_cert(self, type=None):
        if type == None or type.lower() == 'pem':
            return crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert)
        elif type.lower() == 'der':
            return crypto.dump_certificate(crypto.FILETYPE_ASN1, self.cert)
        else:
            return crypto.dump_certificate(crypto.FILETYPE_TEXT, self.cert)

    def get_key(self, type=None, cipher=None, passphrase=None):
        if type == None or type.lower() == 'pem':
            return crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key, cipher=cipher, passphrase=passphrase)
        elif type.lower() == 'der':
            return crypto.dump_privatekey(crypto.FILETYPE_ASN1, self.key, cipher=cipher, passphrase=passphrase)
        else:
            return crypto.dump_privatekey(crypto.FILETYPE_TEXT, self.key, cipher=cipher, passphrase=passphrase)

if __name__ == '__main__':
    ks = PKCS12('selfsigned1.p12', password='changeit')
    print(ks.get_cert())
    print(ks.get_key())
