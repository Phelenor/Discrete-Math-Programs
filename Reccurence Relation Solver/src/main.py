import numpy as np

# Tn = a * Tn-1 + b * Tn-2 + c * Tn-3
RELATION_COEFFICIENTS = np.zeros(3)  # a, b, c

# Tn = a * r1^n + b * r2^n + c * r3^n
POLYNOMIAL_COEFFICIENTS = np.zeros(3)  # alfa, beta, gama

INDEX_WANTED = 0

ELEMENTS = []

ROOTS = []


def read_roots():
    for i in range(3):
        successful = False
        while not successful:
            try:
                user_in = float(input(f"Unesite prvo rjesenje x_{i} karakteristicne jednadzbe: "))
                if user_in in ROOTS:
                    raise Exception("Rjesenja moraju biti razliciti realni brojevi.")

            except ValueError:
                print("Rjesenja jednadzbe moraju biti realni brojevi.")
                continue

            except Exception as error:
                print(error)
                continue

            successful = True
        ROOTS.append(user_in)


def read_elements():
    str_helper = ["nultog", "prvog", "drugog"]
    for i in range(4):
        # In the extra pass take the wanted member position
        if i == 3:
            global INDEX_WANTED
            successful = False
            while not successful:
                try:
                    user_in = int(input(f"Unesite redni broj n trazenog clana niza: "))
                except ValueError:
                    print("Redni broj mora biti ne-negativni cijeli broj.")
                    continue
                successful = True
                INDEX_WANTED = user_in
                return

        successful = False
        while not successful:
            try:
                user_in = float(input(f"Unesite vrijednost {str_helper[i]} clana niza a_{i}: "))
            except ValueError:
                print("Elementi rekurzivne relacije moraju biti realni brojevi.")
                continue

            successful = True
        ELEMENTS.append(user_in)


def compute_relation_coeffs(r):
    global RELATION_COEFFICIENTS
    a = np.array([
        [r[0] ** 2, r[0], 1],
        [r[1] ** 2, r[1], 1],
        [r[2] ** 2, r[2], 1]
    ])

    b = np.array([r[0] ** 3, r[1] ** 3, r[2] ** 3])

    RELATION_COEFFICIENTS = np.linalg.solve(a, b)


def compute_polynomial_coeffs(r):
    global POLYNOMIAL_COEFFICIENTS
    a = np.array([
        [r[0] ** 0, r[1] ** 0, r[2] ** 0],
        [r[0] ** 1, r[1] ** 1, r[2] ** 1],
        [r[0] ** 2, r[1] ** 2, r[2] ** 2]
    ])

    b = np.array([ELEMENTS[0], ELEMENTS[1], ELEMENTS[2]])

    POLYNOMIAL_COEFFICIENTS = np.linalg.solve(a, b)


def search_by_formula(r):
    p = POLYNOMIAL_COEFFICIENTS
    return p[0] * r[0] ** INDEX_WANTED + p[1] * r[1] ** INDEX_WANTED + p[2] * r[2] ** INDEX_WANTED


def search_recursively(index):
    if index == 0:
        return ELEMENTS[0]
    elif index == 1:
        return ELEMENTS[1]
    elif index == 2:
        return ELEMENTS[2]
    else:
        try:
            return ELEMENTS[index]
        except Exception:
            pass

        ELEMENTS.insert(index, RELATION_COEFFICIENTS[0] * search_recursively(index - 1) +
                        RELATION_COEFFICIENTS[1] * search_recursively(index - 2) +
                        RELATION_COEFFICIENTS[2] * search_recursively(index - 3))

        return ELEMENTS[index]


def main():
    read_roots()
    read_elements()

    compute_relation_coeffs(ROOTS)
    compute_polynomial_coeffs(ROOTS)

    term1 = search_by_formula(ROOTS)
    term2 = search_recursively(INDEX_WANTED)

    print("Vrijednost n-tog clana niza pomocu formule: {:.2f}".format(term1))
    print("Vrijednost n-tog clana niza iz rekurzije: {:.2f}".format(term2))


if __name__ == '__main__':
    main()
