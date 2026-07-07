# Capa de seguridad simple para SafeVault.
#Para la demostración se usa cifrado simétrico con Fernet. Esto permite que
#Wireshark ya no muestre el JSON en texto plano.

import json
import os
from typing import Any, Dict

from cryptography.fernet import Fernet


# IMPORTANTE: La clave se deja fija para la demo. En un
# sistema real debería  desde variables de entorno.

# Clave compartida entre sensor, servidor y actuador.
DEFAULT_SECRET_KEY = b"UQu8j9DT7GCENlqXFFYi1fbv3y9CzBgY_8IdvSGA3zE="


def _load_key() -> bytes:
    key = os.getenv("SAFEVAULT_SECRET_KEY") or os.getenv("SafeVault_SECRET_KEY")
    if key:
        return key.encode("utf-8")
    return DEFAULT_SECRET_KEY


fernet = Fernet(_load_key())


def encrypt_message(texto: str) -> bytes:
    # Cifra un texto y devuelve bytes listos para enviar por red.
    return fernet.encrypt(texto.encode("utf-8"))


def decrypt_message(payload: bytes) -> str:
    # Descifra bytes recibidos por red y devuelve el texto original.
    return fernet.decrypt(payload).decode("utf-8")


def encrypt_json(data: Dict[str, Any]) -> bytes:
    # Convierte un diccionario a JSON y lo cifra.
    return encrypt_message(json.dumps(data, ensure_ascii=False))


def decrypt_json(payload: bytes) -> Dict[str, Any]:
    # Descifra un payload y lo interpreta como JSON.
    return json.loads(decrypt_message(payload))
