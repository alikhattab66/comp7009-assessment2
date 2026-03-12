import random

def encrypt(message, key):
    return f"enc({message})with[{key}]"

def decrypt(ciphertext, key):
    prefix = "enc("
    suffix = f")with[{key}]"
    if ciphertext.startswith(prefix) and ciphertext.endswith(suffix):
        return ciphertext[len(prefix):-len(suffix)]
    return None

Kas = "Key_AS"   # shared key between A and S
Kbs = "Key_BS"   # shared key between B and S

A = "A"
B = "B"

print("Needham-Schroeder Protocol Demonstration\n")

# Step 1: A -> S
Na = random.randint(1000, 9999)
print(f"1) {A} -> S : ({A}, {B}, Na={Na})")

# Step 2: S -> A
Kab = f"SessionKey{random.randint(100,999)}"
ticket_for_B = encrypt(f"{Kab},{A}", Kbs)
message2_plain = f"{Na},{B},{Kab},{ticket_for_B}"
message2 = encrypt(message2_plain, Kas)

print(f"2) S -> {A} : {message2}")

# A authenticates Message 2
decrypted_m2 = decrypt(message2, Kas)
if decrypted_m2 is None:
    print("Authentication failed at Step 2: A could not decrypt message from S.")
    raise SystemExit

parts = decrypted_m2.split(",", 3)
if len(parts) != 4:
    print("Authentication failed at Step 2: malformed message from S.")
    raise SystemExit

recv_Na, recv_B, recv_Kab, recv_ticket = parts

if recv_Na != str(Na):
    print("Authentication failed at Step 2: nonce Na does not match.")
    raise SystemExit

if recv_B != B:
    print("Authentication failed at Step 2: recipient B does not match.")
    raise SystemExit

print(f"A decrypts Message 2 successfully: Na={recv_Na}, B={recv_B}, Kab={recv_Kab}")
print("A authenticates S using matching Na and intended recipient B.")

# Step 3: A -> B
print(f"\n3) {A} -> {B} : {recv_ticket}")

# B authenticates Message 3
decrypted_ticket = decrypt(recv_ticket, Kbs)
if decrypted_ticket is None:
    print("Authentication failed at Step 3: B could not decrypt ticket.")
    raise SystemExit

ticket_parts = decrypted_ticket.split(",")
if len(ticket_parts) != 2:
    print("Authentication failed at Step 3: malformed ticket.")
    raise SystemExit

ticket_Kab, claimed_A = ticket_parts

if claimed_A != A:
    print("Authentication failed at Step 3: ticket does not claim sender A.")
    raise SystemExit

print(f"B decrypts ticket successfully: Kab={ticket_Kab}, claimed sender={claimed_A}")

# Step 4: B -> A
Nb = random.randint(1000, 9999)
message4 = encrypt(str(Nb), ticket_Kab)
print(f"\n4) {B} -> {A} : {message4}")

# A authenticates Message 4
decrypted_m4 = decrypt(message4, recv_Kab)
if decrypted_m4 is None:
    print("Authentication failed at Step 4: A could not decrypt B's challenge.")
    raise SystemExit

print(f"A decrypts challenge successfully: Nb={decrypted_m4}")

# Step 5: A -> B
response = encrypt(str(int(decrypted_m4) - 1), recv_Kab)
print(f"\n5) {A} -> {B} : {response}")

# B authenticates Message 5
decrypted_response = decrypt(response, ticket_Kab)
if decrypted_response is None:
    print("Authentication failed at Step 5: B could not decrypt A's response.")
    raise SystemExit

if decrypted_response != str(Nb - 1):
    print("Authentication failed at Step 5: response is not Nb-1.")
    raise SystemExit

print(f"B decrypts response successfully: {decrypted_response}")
print("\nAuthentication successful.")
print(f"A and B now share the session key Kab = {ticket_Kab}")