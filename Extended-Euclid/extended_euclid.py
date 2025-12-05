# Extended Euclid's Algorithm in Python
# Computes gcd(a, b) and finds x, y such that: a*x + b*y = gcd(a, b)

def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0     # gcd, x, y

    gcd, x1, y1 = extended_euclid(b, a % b)

    # Update x and y using the results of recursion
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":
    print("Extended Euclid’s Algorithm")
    a = int(input("Enter value of a: "))
    b = int(input("Enter value of b: "))

    gcd, x, y = extended_euclid(a, b)

    print("\nRESULT")
    print("gcd(", a, ",", b, ") =", gcd)
    print("Coefficients: x =", x, ", y =", y)
    print("Verification: a*x + b*y =", a*x + b*y)
