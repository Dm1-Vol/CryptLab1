import hashlib
from PIL import Image

class Xorshift32:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 1

    def next(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def generate_keystream(self, length: int) -> bytes:
        stream = bytearray()
        while len(stream) < length:
            val = self.next()
            stream.extend(val.to_bytes(4, "little"))
        return bytes(stream[:length])

def key_to_seed(key: str) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "little")

def xor_crypt(data: bytes, key: str) -> bytes:
    seed = key_to_seed(key)
    prng = Xorshift32(seed)
    keystream = prng.generate_keystream(len(data))
    return bytes(a ^ b for a, b in zip(data, keystream))

def process_image(input_path: str, output_path: str, key: str):
    img = Image.open(input_path)
    data = img.tobytes()
    result = xor_crypt(data, key)
    out_img = Image.frombytes(img.mode, img.size, result)
    out_img.save(output_path)