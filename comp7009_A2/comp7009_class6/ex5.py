import hashlib
import itertools

TARGET = "91077079768edba10ac0c93b7108bc639d778d67"
POINTS = "abcdefghi"

for length in range(1, 10):
    for perm in itertools.permutations(POINTS, length):
        pattern = "".join(perm)
        if hashlib.sha1(pattern.encode("utf-8")).hexdigest() == TARGET:
            print("FOUND pattern:", pattern)
            raise SystemExit

print("Pattern not found.")