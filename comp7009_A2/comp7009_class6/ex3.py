import hashlib

TARGET = "3ddcd95d2bff8e97d3ad817f718ae207b98c7f2c84c5519f89cd15d7f8ee1c3b"
WORDLIST = "phpbb.txt"

algorithms = ["sha1", "sha224", "sha256", "sha384", "sha512"]

def apply_hash_rounds(text, algorithm, rounds):
    data = text.encode("utf-8")
    for _ in range(rounds):
        data = hashlib.new(algorithm, data).digest()
    return data.hex()

found = False

with open(WORDLIST, "r", encoding="utf-8", errors="ignore") as f:
    for word in f:
        word = word.strip()
        if not word:
            continue

        for algorithm in algorithms:
            for rounds in range(1, 4):
                if apply_hash_rounds(word, algorithm, rounds) == TARGET:
                    print("FOUND password:", word)
                    print("Algorithm:", algorithm)
                    print("Rounds:", rounds)
                    found = True
                    break
            if found:
                break
        if found:
            break

if not found:
    print("Password not found.")