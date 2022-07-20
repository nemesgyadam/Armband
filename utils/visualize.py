from matplotlib import pyplot as plt
from IPython.display import clear_output


def showMe(data, range=[-10000, 10000], clear=False):
    if clear:
        clear_output(wait=True)
    plt.rcParams["figure.figsize"] = [17, 2]
    fig, (c1, c2, c3, c4, c5, c6) = plt.subplots(1, 6)
    c1.set_ylim(range[0], range[1])
    c2.set_ylim(range[0], range[1])
    c3.set_ylim(range[0], range[1])
    c4.set_ylim(range[0], range[1])
    c5.set_ylim(range[0], range[1])
    c6.set_ylim(range[0], range[1])
    c1.plot(data[0])
    c2.plot(data[1])
    c3.plot(data[2])
    c4.plot(data[3])
    c5.plot(data[4])
    c6.plot(data[5])
    plt.show()
