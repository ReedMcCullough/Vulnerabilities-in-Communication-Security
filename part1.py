from Crypto.Random import *
from Crypto.Util import *
from Crypto.Util.Padding import *
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import random

def main():
    # prime number
    p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
    # primitive root estimate
    g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5


    # Alice
    a = random.randint(0, p - 1)
    a_final = pow(g, a, p)
    # Bob
    b = random.randint(0, p - 1)
    b_final = pow(g, b, p)

    # ALICE SENDS BOB a, BOB SENDS ALICE b

    sA = pow(b_final, a, p)
    sB = pow(a_final, b, p)

    # truncating SHA digest to 16 bytes for CBC encryption
    kA = SHA256.new()
    kA.update(sA.to_bytes(256, 'big'))
    kaVal = kA.hexdigest()[:16]
    kB = SHA256.new()
    kB.update(sB.to_bytes(256, 'big'))
    kbVal = kB.hexdigest()[:16]

    print("\nAlice Key: " + kaVal)
    print("Bob Key: " + kbVal)
    print()

    # messages being sent
    mA = pad(b'Hi Bob!', 16, style='pkcs7')
    mB = pad(b'Hi Alice!', 16, style='pkcs7')

    # message is encrypted by both parties
    # each party has a way to encrypt and decrypt
    iv = get_random_bytes(16)
    boxA = AES.new(bytes(kaVal, 'utf-8'), AES.MODE_CBC, iv)
    decA = AES.new(bytes(kaVal, 'utf-8'), AES.MODE_CBC, iv)

    boxB = AES.new(bytes(kbVal, 'utf-8'), AES.MODE_CBC, iv)
    decB = AES.new(bytes(kbVal, 'utf-8'), AES.MODE_CBC, iv)

    c0 = boxA.encrypt(mA)
    c1 = boxB.encrypt(mB)

    # message is sent, and decrypted by both parties for viewing
    print("\nAlice's Original Message: " + str(b'Hi Bob!'))
    print("Alice's Encrypted Message: " + str(c0))
    print("Alice's Message after Decryption")
    print("(Using only Bob's Info to Decrypt): " + str(unpad(decB.decrypt(c0), 16)))

    print("\nBob's Original Message: " + str(b'Hi Alice!'))
    print("Bob's Encrypted Message: " + str(c1))
    print("Bob's Message after Decryption")
    print("(Using only Alice's Info to Decrypt): " + str(unpad(decA.decrypt(c1), 16)))
    print()







if __name__ == "__main__":
    main()