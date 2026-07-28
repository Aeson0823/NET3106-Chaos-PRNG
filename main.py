

import struct
import numpy as np


def logistic_map_bits(r, x0, n, skip=1000):

    x = x0


    for _ in range(skip):
        x = r * x * (1 - x)

    bits = np.empty(n, dtype=np.uint8)
    for i in range(n):
        x = r * x * (1 - x)
        raw = struct.unpack('>Q', struct.pack('>d', x))[0]
        bits[i] = (raw >> 30) & 1

    return bits


def bits_to_string(bits):
    return ''.join(str(b) for b in bits)


if __name__ == "__main__":
    #The parameters that can be adjust, the iteration would be 100,000,0
    #the seed is the initial number of system
    N = 1000000
    SEED = 0.6013265

    print("Generating STRONG source (r=3.99, chaotic)...")
    #r representing the most chaotic result if r is 3.99, the number will become unpredictable
    strong_bits = logistic_map_bits(r=3.99, x0=SEED, n=N, skip=1000)

    print("Generating WEAK source (r=3.5, period-4 cycle)...")
    #however, r in weak source will be representing the stable number in the formula
    weak_bits = logistic_map_bits(r=3.5, x0=SEED, n=N, skip=1000)

    for name, bits in [("strong", strong_bits), ("weak", weak_bits)]:
        ones_pct = 100 * bits.sum() / len(bits)
        print(f"  {name}: {len(bits)} bits, {ones_pct:.2f}% ones")

    with open(r"strong_source.txt", "w") as f:
        f.write(bits_to_string(strong_bits))

    with open(r"weak_source.txt", "w") as f:
        f.write(bits_to_string(weak_bits))

    print("\nSaved strong_source.txt and weak_source.txt (1,000,000 bits each)")
