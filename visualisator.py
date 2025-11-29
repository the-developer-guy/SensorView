import tkinter
import serial

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure



root = tkinter.Tk()
root.wm_title("Sensor View")

fig = Figure(figsize=(5, 4), dpi=100)

measurements = [1, 2, 3]
meas2 = [2, 4, 6]
timestamps = [1, 2, 3]

subplot = fig.add_subplot(111)
subplot.set_xlabel("idő (s)")
subplot.set_ylabel("hőmérséklet (C)")
subplot.set_title("szenzorok")
subplot.plot(timestamps, measurements)
subplot.plot(timestamps, meas2)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()
    root.destroy()


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
