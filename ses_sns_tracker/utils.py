import base64
import logging

import requests
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from django_ses.utils import BounceMessageVerifier


logger = logging.getLogger(__name__)


class CryptographyBounceMessageVerifier(BounceMessageVerifier):
    """Custom BounceMessageVerifier using cryptography instead of M2Crypto"""

    def is_verified(self):
        """Verifies an SES bounce message."""
        if self._verified is None:
            signature = self._data.get('Signature')
            if not signature:
                self._verified = False
                return self._verified

            # Decode the signature from base64
            signature = bytes(base64.b64decode(signature))

            # Get the message to sign
            sign_bytes = self._get_bytes_to_sign()
            if not sign_bytes:
                self._verified = False
                return self._verified

            if not self.certificate:
                self._verified = False
                return self._verified

            # Extract the public key
            pkey = self.certificate.public_key()

            # Use the public key to verify the signature.
            try:
                pkey.verify(signature, sign_bytes, padding.PKCS1v15(), hashes.SHA1())
                self._verified = True
            except InvalidSignature:
                logger.debug(u'Failed to validate signature')
                self._verified = False

        return self._verified

    @property
    def certificate(self):
        """Retrieves the certificate used to sign the bounce message."""

        if not hasattr(self, '_certificate'):
            cert_url = self._get_cert_url()

            if not cert_url:
                self._certificate = None
                return self._certificate

            response = requests.get(cert_url)
            if response.status_code != 200:
                logger.warning(u'Could not download certificate from %s: "%s"', cert_url, response.status_code)
                self._certificate = None
                return self._certificate

            try:
                self._certificate = x509.load_pem_x509_certificate(response.content, default_backend())
            except ValueError:
                logger.warning(u'Failed to load certificate from %s', cert_url)
                self._certificate = None

        return self._certificate


def verify_bounce_message(msg):
    """Verify an SES/SNS bounce notification message."""
    verifier = CryptographyBounceMessageVerifier(msg)
    return verifier.is_verified()
