"""Module providing functions for working with Advanced Encryption Standard"""

# Substitution boxes

sub_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_sub_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

mix_matrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2],
]

inv_mix_matrix = [
    [14, 11, 13, 9],
    [9, 14, 11, 13],
    [13, 9, 14, 11],
    [11, 13, 9, 14],
]


def sub_bytes(s):
    """Substitutes bytes by using substitution box"""
    for i in range(4):
        for j in range(4):
            s[i][j] = sub_box[s[i][j]]

def inv_sub_bytes(s):
    """Substitutes bytes by using inversed substitution box"""
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_sub_box[s[i][j]]

def shift_rows(s):
    """
    Shifts rows in a matrix

    First row does not get shifted
    Second row gets shifted by 1 byte to the left
    Third row gets shifted by 2 byte to the left
    Fourth row gets shifted by 3 byte to the left
    """
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def inv_shift_rows(s):
    """
    Invertively shifts rows in a matrix

    First row does not get shifted
    Second row gets shifted by 1 byte to the right
    Third row gets shifted by 2 byte to the right
    Fourth row gets shifted by 3 byte to the right
    """
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

def add_round_key(s, k):
    """Adds round key to the state by appliying XOR"""
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def gmul(a, b):
    """Galois field multiplication of a and b in GF(2^8)"""
    p = 0

    for _ in range(8):
        if b & 1:
            p ^= a

        hi_bit = a & 0x80
        a = (a << 1) & 0xFF

        if hi_bit:
            a ^= 0x1B

        b >>= 1

    return p


def mix_single_column(col):
    """Mix one column using matrix multiplication"""
    result = [0, 0, 0, 0]

    for i in range(4):
        result[i] = (
            gmul(mix_matrix[i][0], col[0]) ^
            gmul(mix_matrix[i][1], col[1]) ^
            gmul(mix_matrix[i][2], col[2]) ^
            gmul(mix_matrix[i][3], col[3])
        )

    return result

def inv_mix_single_column(col):
    """Mix one column to original state using inversed matrix multiplication"""
    result = [0, 0, 0, 0]

    for i in range(4):
        result[i] = (
            gmul(inv_mix_matrix[i][0], col[0]) ^
            gmul(inv_mix_matrix[i][1], col[1]) ^
            gmul(inv_mix_matrix[i][2], col[2]) ^
            gmul(inv_mix_matrix[i][3], col[3])
        )

    return result

def mix_columns(s):
    """Mixes all columns of a matrix"""
    for i in range(4):
        s[i] = mix_single_column(s[i])


def inv_mix_columns(s):
    """Mixes all columns of a matrix back to original state"""
    for i in range(4):
        s[i] = inv_mix_single_column(s[i])


r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)


def bytes_to_matrix(text):
    """Converts a 16-byte array into a 4x4 matrix"""
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix_to_bytes(matrix):
    """Converts a 4x4 matrix into a 16-byte array"""
    return bytes(sum(matrix, []))

def xor_bytes(a, b):
    """Returns a new byte array with the elements xor'ed"""
    return bytes(i^j for i, j in zip(a, b))

def incriment_bytes(a):
    """Returns a new byte array with the value increment by 1"""
    out = list(a)

    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break

    return bytes(out)

def pad(plaintext):
    """
    Pads the given plaintext padding to a multiple of 16 bytes

    Note that if the plaintext size is a multiple of 16,
    a whole block will be added
    """
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)

    plaintext = bytes(plaintext, encoding="utf-8")

    return plaintext + padding

def unpad(plaintext):
    """
    Removes padding, returning the unpadded text and
    ensuring the padding was correct
    """
    padding_len = plaintext[-1]
    if not padding_len > 0:
        raise ValueError("Padding lenght should be bigger than 0")

    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    if not all(p == padding_len for p in padding):
        raise ValueError("Invalid padding, wrong padding lenght")

    return message

def split_blocks(message, block_size=16, require_padding=True):
    """Splits message into blocks of 16 bytes"""
    if require_padding and len(message) % block_size != 0:
        raise ValueError("Invalid padding, wrong message lenght")

    return [message[i:i+16] for i in range(0, len(message), block_size)]



class AES:
    """Class with implementation of Asymmetric encryption standard (AES)"""

    rounds_by_key_size = {16: 10, 24: 12, 32: 14}

    def __init__(self, master_key):
        """Initializes the object with a given key"""
        if len(master_key) not in AES.rounds_by_key_size:
            raise ValueError("AES only supports keys with lenghts of 16, 24 and 32 bytes")

        self.n_rounds = AES.rounds_by_key_size[len(master_key)]
        self.__master_key = master_key
        self.__key_matrices = self.__expand_key(master_key)

    def __expand_key(self, master_key):
        """Expands and returns a list of key matrices for the given master_key"""
        # Initialize round keys with raw key material
        key_columns = bytes_to_matrix(master_key)
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            # Copy previous word
            word = list(key_columns[-1])

            # Perform schedule_core once every "row"
            if len(key_columns) % iteration_size == 0:
                # Circular shift.
                word.append(word.pop(0))
                # Map to sub-box
                word = [sub_box[b] for b in word]
                # XOR with first byte of R-CON, since the others bytes of R-CON are 0
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                # Run word through S-box in the fourth iteration when using a
                # 256-bit key
                word = [sub_box[b] for b in word]

            # XOR with equivalent word from previous iteration
            word = xor_bytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        # Group key words in 4x4 byte matrices
        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]


    def encrypt_block(self, plaintext):
        """Encrypts a single block of 16 byte long plaintext"""
        if len(plaintext) != 16:
            raise ValueError("Can only work with blocks of 16 bytes")

        plain_state = bytes_to_matrix(plaintext)

        add_round_key(plain_state, self.__key_matrices[0])

        for i in range(1, self.n_rounds):
            sub_bytes(plain_state)
            shift_rows(plain_state)
            mix_columns(plain_state)
            add_round_key(plain_state, self.__key_matrices[i])

        sub_bytes(plain_state)
        shift_rows(plain_state)
        add_round_key(plain_state, self.__key_matrices[-1])

        return matrix_to_bytes(plain_state)

    def decrypt_block(self, ciphertext):
        """Decrypts a single block of 16 byte long ciphertext"""
        if len(ciphertext) != 16:
            raise ValueError("Can only work with blocks of 16 bytes")

        cipher_state = bytes_to_matrix(ciphertext)

        add_round_key(cipher_state, self.__key_matrices[-1])
        inv_shift_rows(cipher_state)
        inv_sub_bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            add_round_key(cipher_state, self.__key_matrices[i])
            inv_mix_columns(cipher_state)
            inv_shift_rows(cipher_state)
            inv_sub_bytes(cipher_state)

        add_round_key(cipher_state, self.__key_matrices[0])

        return matrix_to_bytes(cipher_state)


    def encrypt(self, plaintext):
        """Encrypts `plaintext` using CBC mode and PKCS#7 padding with master_key"""
        plaintext = pad(plaintext)

        blocks = []
        previous = self.__master_key
        for plaintext_block in split_blocks(plaintext):
            # Encrypt(plaintext_block XOR previous)
            block = self.encrypt_block(xor_bytes(plaintext_block, previous))
            blocks.append(block)

            previous = block

        return b''.join(blocks)

    def decrypt(self, ciphertext):
        """Decrypts `ciphertext` using CBC mode and PKCS#7 padding with master_key"""
        blocks = []
        previous = self.__master_key
        for ciphertext_block in split_blocks(ciphertext):
            # Decrypt: previous XOR decrypt(ciphertext)
            blocks.append(xor_bytes(previous, self.decrypt_block(ciphertext_block)))

            previous = ciphertext_block

        return unpad(b''.join(blocks))

if __name__ == '__main__':
    my_key = b"12312312312312311231231231231231" # 32 byte key
    aes = AES(my_key)
    my_message = "67/11"
    my_cipher = aes.encrypt(my_message)
    print(my_cipher)
    print(aes.decrypt(my_cipher))
