
def gen_cube(faces):
    cubies = set()
    for b in [
        "LDB", "LDF", "LUB", "LUF", "RDB", "RDF", "RUB", "RUF",
        "LCB", "LCF", "LUC", "LDC", "CDB", "CDF", "CUB", "CUF", "RCB", "RCF", "RUC", "RDC",
        "LCC", "RCC", "CUC", "CDC", "CCF", "CCB"
    ]:

        d = {}

        i = b[::-1]

        for j in range(3):
            if i[j] != "C":
                a = faces[i[j]]
                for k in range(3):
                    if j != k:
                        print(a)
                        a = a[i[k]]
                d[i[j]] = pc.Square(a)

        x = pc.Cubie(**d)
        cubies.add(x)

    return pc.Cube(cubies)


def gen_face(pos, data):
    pairs = {"L": "R", "R": "L", "U": "D", "D": "U", "F": "B", "B": "F"}

    a = [find_seq(pos)[1], "C", pairs[find_seq(pos)[1]]]
    b = [find_seq(pos)[0], "C", pairs[find_seq(pos)[0]]]

    d = {}

    for i in range(3):
        for j in range(3):
            if not (a[i] in d.keys()):
                d[a[i]] = {}
            d[a[i]][b[j]] = data[i][j]

    return d


def find_seq(pos):
    return {
        'F': ['L', 'U'],
        'L': ['U', 'F'],
        'R': ['U', 'B'],
        'U': ['L', 'B'],
        'D': ['L', 'F'],
        'B': ['R', 'U']
    }[pos]


print(scan())

x = gen_cube({'B': {'C': {'C': 'orange', 'R': 'orange', 'L': 'red'}, 'U': {'C': 'orange', 'R': 'orange', 'L': 'red'},
                    'D': {'C': 'red', 'R': 'orange', 'L': 'red'}},
              'D': {'C': {'C': 'yellow', 'R': 'yellow', 'L': 'white'},
                    'B': {'C': 'yellow', 'R': 'yellow', 'L': 'white'},
                    'F': {'C': 'white', 'R': 'white', 'L': 'yellow'}},
              'F': {'C': {'C': 'red', 'R': 'orange', 'L': 'red'}, 'U': {'C': 'orange', 'R': 'orange', 'L': 'red'},
                    'D': {'C': 'red', 'R': 'orange', 'L': 'red'}},
              'L': {'C': {'C': 'green', 'U': 'green', 'D': 'blue'}, 'B': {'C': 'green', 'U': 'blue', 'D': 'green'},
                    'F': {'C': 'blue', 'U': 'blue', 'D': 'green'}},
              'R': {'C': {'C': 'blue', 'U': 'green', 'D': 'blue'}, 'B': {'C': 'blue', 'U': 'green', 'D': 'blue'},
                    'F': {'C': 'green', 'U': 'green', 'D': 'blue'}},
              'U': {'C': {'C': 'green', 'R': 'white', 'L': 'yellow'}, 'B': {'C': 'white', 'R': 'yellow', 'L': 'white'},
                    'F': {'C': 'yellow', 'R': 'white', 'L': 'yellow'}}})

list(x["U"].facings.values())[0].colour = "white"

print(x)

kociemba.solve(x)

COORDS = {
    "U1": (3, 198, 52),
    "U2": None,  # TODO: Rotate cube!
    "U3": (3, 387, 51),
    "U4": (3, 178, 87),
    "U5": None,
    "U6": (3, 401, 91),
    "U7": (3, 165, 148),
    "U8": (3, 295, 143),
    "U9": (3, 421, 142),

    "F1": (3, 117, 269),
    "F2": (3, 277, 260),
    "F3": (3, 428, 266),
    "F4": (3, 134, 378),
    "F5": None,
    "F6": (3, 425, 371),
    "F7": (3, 153, 469),
    "F8": None,  # TODO: Rotate cube!
    "F9": (3, 405, 462),

    "B1": (1, 362, 98),
    "B2": (1, 457, 92),
    "B3": (1, 533, 95),
    "B4": (1, 364, 240),
    "B5": None,
    "B6": None,  # TODO: Rotate cube!
    "B7": (1, 357, 385),
    "B8": (1, 458, 366),
    "B9": (1, 528, 343),

    "R1": (1, 101, 100),
    "R2": (1, 175, 94),
    "R3": (1, 253, 93),
    "R4": None,  # TODO: Rotate cube!
    "R5": None,
    "R6": (1, 255, 246),
    "R7": (1, 98, 333),
    "R8": (1, 162, 338),
    "R9": (1, 249, 374),

    "L1": (2, 178, 18),
    "L2": None,  # TODO: Rotate cube!
    "L3": (2, 456, 20),
    "L4": (2, 164, 83),
    "L5": None,
    "L6": (2, 461, 84),
    "L7": (2, 144, 181),
    "L8": (2, 315, 184),
    "L9": (2, 471, 179),

    "D1": (2, 474, 288),
    "D2": (2, 465, 397),
    "D3": (2, 462, 468),
    "D4": (2, 301, 295),
    "D5": None,
    "D6": None,  # TODO: Rotate cube!
    "D7": (2, 147, 304),
    "D8": (2, 167, 409),
    "D9": (2, 186, 470),
}