def perm_to_octal(perm: str) -> int:
    perm = (perm or "").strip()

    # Allow ls-style strings like "-rwxr-xr--" by dropping the file-type char.
    if len(perm) == 10 and perm[0] in "-d":
        perm = perm[1:]

    if len(perm) != 9:
        raise ValueError("Permission string must be exactly 9 characters.")

    for i, ch in enumerate(perm):
        if i % 3 == 0 and ch not in "r-":
            raise ValueError("Invalid permission format at read position.")
        if i % 3 == 1 and ch not in "w-":
            raise ValueError("Invalid permission format at write position.")
        if i % 3 == 2 and ch not in "x-":
            raise ValueError("Invalid permission format at execute position.")

    vals = {"r": 4, "w": 2, "x": 1, "-": 0}
    out_digits = []
    for i in range(0, 9, 3):
        triplet = perm[i:i + 3]
        digit = vals[triplet[0]] + vals[triplet[1]] + vals[triplet[2]]
        out_digits.append(str(digit))

    return int("".join(out_digits))


if __name__ == "__main__":
    permission = input("Enter Linux permissions: ")
    try:
        print(f"Octal permission: {perm_to_octal(permission)}")
    except ValueError as err:
        print(f"Error: {err}")
