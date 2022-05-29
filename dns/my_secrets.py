from cryptography.fernet import Fernet

'''
Decrypts the encrypted password
'''
def my_decrypt(key, encryptedPassword):
    f = Fernet(key)
    return f.decrypt(encryptedPassword)
'''
Encrypts the password
'''
def my_encrypt(key, password):
    encodedPassword = password.encode()
    f = Fernet(key)
    return f.encrypt(encodedPassword)