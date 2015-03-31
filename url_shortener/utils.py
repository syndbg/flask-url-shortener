from hashlib import sha256


def hash(salt, string):
    salt = salt.encode('utf-8')
    string = string.encode('utf-8')
    return sha256(salt + string).hexdigest()


# being clever
def apify(db_url):
    return {field: field for field in db_url}


class EncoderError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UrlEncoder(object):
    alphabet = 'mn6j2c4rv8bpygw95z7hsdaetxuk3fq'
    block_size = 24
    min_length = 5
    mask = (1 << block_size) - 1
    mapping = list(reversed(range(block_size)))

    def encode_id(self, id):
        return self.enbase(self.encode(id))

    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)

    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def enbase(self, x):
        result = self._enbase(x)
        padding = self.alphabet[0] * (self.min_length - len(result))
        return '%s%s' % (padding, result)

    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(x / n) + self.alphabet[x % n]

    def decode_id(self, encoded):
        return self.decode(self.debase(encoded))

    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)

    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result

    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            try:
                result += self.alphabet.index(c) * (n ** i)
            except ValueError:
                raise EncoderError("Encoded value characters don't match the "
                                   "defined alphabet.")
        return result
