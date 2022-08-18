# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # signal generation
# N = 10001
# stop = 100
# time = np.linspace(0, stop, N)
# A = 1/4*np.cos(2*np.pi*(np.abs(time - stop/2)/stop)) + 1
# f = np.concatenate((1*np.ones(int(N/4)), 2*np.ones(int(N/2) + 1), 1*np.ones(int(N/4))))
# signal = A * np.sin(2*np.pi*f*time) + 0.05*np.random.randn(N)

# # figure preparation
# fig, ax = plt.subplots(1, 1, figsize = (8*0.9, 6*0.9))
# displayed_period = int(2*f.min())
# span = int(N/stop/f.min())

# def animation(i):
#     # delete previous frame
#     ax.cla()

#     # plot and set axes limits
#     ax.plot(time[span*i: 1 + span*(i + displayed_period)],
#             signal[span*i: 1 + span*(i + displayed_period)])
#     ax.set_xlim([time[span*i], time[span*(i + displayed_period)]])
#     ax.set_ylim([1.1*signal.min(), 1.1*signal.max()])

# # run animation
# anim = FuncAnimation(fig, animation, frames = int(len(time)/span - 1), interval = 10)
# plt.show()








# from matplotlib.animation import FuncAnimation
# import matplotlib.pyplot as plt
# import numpy as np

# # fig, ax = plt.subplots(figsize=(5, 8))
# # ax.set(xlim=(0, 1000), ylim=(-10000, 10000))
# fig, ax = plt.subplots(figsize=(5, 5))
# ax.set_ylim(-10000, 10000)
# # fig, ax = plt.subplots(figsize=(10, 13))
# # plt.rcParams["figure.figsize"] = [17, 2]
# # fig, (c1, c2, c3, c4, c5, c6, c7, c8) = plt.subplots(1, 8)
# data = np.load('C:\Code\Armband\data\Sample\session_1\Fist.npy')


# def update(i):
#     # im_normed = data[0][i]
#     # im_normed = data[:8,:1000]
#     # ax.imshow(im_normed)
#     ax.plot(data[0][i])
#     ax.set_title("Angle: {}".format(i), fontsize=20)
#     ax.set_axis_off()

#     plt.show()


# anim = FuncAnimation(fig, update, frames=np.arange(0, 30), interval=50)
# plt.show()
# # anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
# # plt.close()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# signal generation
N = 10001
stop = 100
time = np.linspace(0, stop, N)
A = 1/4*np.cos(2*np.pi*(np.abs(time - stop/2)/stop)) + 1
f = np.concatenate((1*np.ones(int(N/4)), 2*np.ones(int(N/2) + 1), 1*np.ones(int(N/4))))
signal = A * np.sin(2*np.pi*f*time) + 0.05*np.random.randn(N)

# figure preparation
fig, ax = plt.subplots(1, 1, figsize = (8*0.9, 6*0.9))
displayed_period = int(2*f.min())
span = int(N/stop/f.min())

def animation(i):
    # delete previous frame
    ax.cla()

    # plot and set axes limits
    ax.plot(time[span*i: 1 + span*(i + displayed_period)],
            signal[span*i: 1 + span*(i + displayed_period)])
    ax.set_xlim([time[span*i], time[span*(i + displayed_period)]])
    ax.set_ylim([1.1*signal.min(), 1.1*signal.max()])

# run animation
anim = FuncAnimation(fig, animation, frames = int(len(time)/span - 1), interval = 10)
plt.show()