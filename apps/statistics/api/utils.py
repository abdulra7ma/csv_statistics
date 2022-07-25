import hashlib


def generate_file_hash(file_path):
    """This function returns the SHA-256 hash of the file passed into it"""

    # make a hash object
    h = hashlib.sha256()

    # open file for reading in binary mode
    with open(file_path, "rb") as file:

        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            h.update(byte_block)

    # return the hex representation of digest
    return h.hexdigest()
