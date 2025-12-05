# Discrete Logarithm Implementation in Python (Brute Force Method)
# Solves g^x ≡ h (mod p) for x

def discrete_log(g, h, p):
    """
    Brute force discrete log solver.
    Returns x such that g^x ≡ h (mod p)
    """
    g %= p
    h %= p

    for x in range(p):    # search in range 0 to p-1
        if pow(g, x, p) == h:
            return x
    return None


# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":
    print("Discrete Logarithm: Solve g^x ≡ h (mod p)")
    g = int(input("Enter value of g: "))
    h = int(input("Enter value of h: "))
    p = int(input("Enter prime modulus p: "))

    result = discrete_log(g, h, p)

    if result is None:
        print("\nNo solution found for the given values.")
    else:
        print("\nSolution found!")
        print(f"x = {result}")
        print(f"Verification: {g}^{result} mod {p} = {pow(g, result, p)}")
