import matplotlib.pyplot as plt
import numpy as np

from pcr import PCR

def function(p, x, y):
    # return x+y
    # return p.calculate_pcr_diff_quadratic(x, y)
    return p.calculate_pcr_diff_linear(x, y)

if __name__ == '__main__':
    match = {'match_data': {'level': 3}}
    p = PCR(match)

    #############################################################
    x = list(range(-100, 100+1))
    x = [v / 100 for v in x]
    y = [function(p, v, 1000) for v in x]

    plt.figure()
    plt.plot(x, y)
    plt.title('Percentage difference dependency: Positive PCR diff')
    plt.xlabel('Percentage difference')
    plt.ylabel('PCR adjustmend calculation')
    plt.grid()

    #############################################################
    x = list(range(-100, 100+1))
    x = [v / 100 for v in x]
    y = [function(p, v, -1000) for v in x]

    plt.figure()
    plt.plot(x, y)
    plt.title('Percentage difference dependency: Negative PCR diff')
    plt.xlabel('Percentage difference')
    plt.ylabel('PCR adjustmend calculation')
    plt.grid()

    #############################################################
    x = list(range(-3000, 3000+1))
    y = [function(p, 0.2, v) for v in x]

    plt.figure()
    plt.plot(x, y)
    plt.title('PCR difference dependency: Positive percentage diff')
    plt.xlabel('PCR difference')
    plt.ylabel('PCR adjustmend calculation')
    plt.grid()

    #############################################################
    x = list(range(-3000, 3000+1))
    y = [function(p, -0.2, v) for v in x]

    plt.figure()
    plt.plot(x, y)
    plt.title('PCR difference dependency: Negative percentage diff')
    plt.xlabel('PCR difference')
    plt.ylabel('PCR adjustmend calculation')
    plt.grid()

    #############################################################
    x = np.linspace(-1.0, 1.0, 1000)
    y = np.linspace(-5000, 5000, 1000)
    Z = np.empty((len(x), len(y)))

    for idx1, i in enumerate(x):
        for idx2, j in enumerate(y):
            if any(((i == -1.0 and j == 3000),
                    (i == 1.0 and j == 3000),
                    (i == -1.0 and j == -3000),
                    (i == 1.0 and j == -3000),
                    (i == 0.0 and j == 0.0),
                    )):
                print(f'Point {i}:{j} = {function(p, i, j)}')
                print('\n\n')
            Z[idx1][idx2] = function(p, i, j)

    ax = plt.figure().add_subplot(projection='3d')

    X, Y = np.meshgrid(x, y, indexing='ij')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    plt.xlabel('percentage_difference [/100]')
    plt.ylabel('pcr_difference')

    plt.show()

