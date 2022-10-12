from matplotlib import pyplot as plt
from IPython.display import clear_output


def showMe(data, range=[-10000, 10000], clear=False):
    if clear:
        clear_output(wait=True)
    plt.close()
    plt.rcParams["figure.figsize"] = [17, 2]
    fig, (c1, c2, c3, c4, c5, c6, c7, c8) = plt.subplots(1, 8)

  

    c1.set_ylim(range[0], range[1])
    c2.set_ylim(range[0], range[1])
    c3.set_ylim(range[0], range[1])
    c4.set_ylim(range[0], range[1])
    c5.set_ylim(range[0], range[1])
    c6.set_ylim(range[0], range[1])
    c7.set_ylim(range[0], range[1])
    c8.set_ylim(range[0], range[1])
    c1.plot(data[0])
    c2.plot(data[1])
    c3.plot(data[2])
    c4.plot(data[3])
    c5.plot(data[4])
    c6.plot(data[5])
    c7.plot(data[6])
    c8.plot(data[7])
    
    plt.show(block = False)
    plt.draw()
    plt.pause(0.001)
    #plt.draw()

def showHistory(history):
    plt.rcParams["figure.figsize"] = [5, 5]
    with plt.rc_context({'figure.facecolor':'white'}):
   
        for key in history.history.keys():

            if "val_" not in key and "lr" != key:
                try:
                    plt.clf()
                    

                    plt.plot(history.history[key])
                    plt.plot(history.history["val_" + key])
                    plt.ylabel(key)
                    plt.xlabel("epoch")
                    plt.legend(["train", "validation"], loc="upper left")
                    plt.show()
                except:
                    ...



def showAvg(dataset,c, range = [-10000, 10000]):
    print(f'---{c}---')
    avg = dataset[c].mean(axis=0)
    print(f'{avg.min()} - {avg.max()}')
    print(avg.mean())
    showMe(avg, range =range)