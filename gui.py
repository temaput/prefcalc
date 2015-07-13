"""
Simple tkinter gui for preferance calculator
Copyright © 2015 Artem Putilov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk
from calc import PointHolder, Total


class PointHolderProxy:

    def __init__(self, playerno):
        self.playerno=playerno
        self.fine = tk.IntVar(0)
        self.points = tk.IntVar()
        self.whists = [tk.IntVar(0) for i in range(3)]

        self.results = tk.StringVar()

    def as_point_holder(self):
        return PointHolder(self.playerno,
                           fine=self.fine.get(),
                           points=self.points.get(),
                           whists=[w.get() for w in self.whists])


class Application:

    def __init__(self):
        self.top = tk.Tk()
        self.top.title("Preferance calculator")
        self.top.iconname("PrefCalc")
        self.top.geometry("+300+300")

        self.toplabel = ttk.Label(
            self.top, text="Simple preferance calculator", anchor="center")
        self.toplabel.pack(side="top", fill="x")

        self.button_group()
        self.score_body()
        self.results_visible = False

    def score_body(self):
        self.player_frames = []
        self.ph_proxies = []
        self.results_frames = []

        for i in range(1,5):
            lf = ttk.LabelFrame(self.top, text="Player %s" % i)
            ph = PointHolderProxy(i)

            fineframe = ttk.Frame(lf)
            finelabel = ttk.Label(fineframe, text="Гора")
            fine = ttk.Entry(fineframe, textvariable=ph.fine, width=4)
            finelabel.pack(side="left")
            fine.pack(side="right")

            sep1 = ttk.Separator(lf)

            pointsframe = ttk.Frame(lf)
            pointslabel = ttk.Label(pointsframe, text="Пуля")
            points = ttk.Entry(pointsframe, textvariable=ph.points, width=4)
            pointslabel.pack(side="left")
            points.pack(side="right")

            sep2 = ttk.Separator(lf)

            whistsframe = ttk.Frame(lf)
            whistslabel = ttk.Label(whistsframe, text="Висты")
            whists = [ttk.Entry(whistsframe,
                                textvariable=ph.whists[ii], width=4)
                      for ii in range(3)]
            whistslabel.pack(side="top")
            for w in whists:
                w.pack(side="left")

            for el in (fineframe, sep1, pointsframe, sep2, whistsframe,
                       ):
                el.pack(fill="x", pady=2, padx=3)

            # prepare results
            resultsframe = ttk.Frame(lf)
            resultslabel = ttk.Label(resultsframe, anchor="center",
                                     textvariable=ph.results)
            resultslabel.pack(fill="x", pady=20, padx=3)
            self.results_frames.append(resultsframe)

            self.player_frames.append(lf)
            self.ph_proxies.append(ph)

        container = ttk.Frame(self.top)
        container.pack(fill="both", expand=1)
        container.lower()

        for col, lf in enumerate(self.player_frames):
            lf.grid(column=col, row=0,
                    in_=container, sticky="nwe", pady=2, padx=3)

        for i in range(2):
            container.grid_columnconfigure(i, weight=1, uniform=True)


    def button_group(self):
        btns = ttk.Frame(self.top)
        sep = ttk.Separator(btns)
        sep.pack(side="top", fill="x",  pady=2)

        self.QUIT = ttk.Button(btns, text="Close", command=self.top.destroy)
        self.CALCULATE = ttk.Button(btns, text="Calculate",
                                    command=self.on_calculate)
        for num, b in enumerate([self.QUIT, self.CALCULATE]):
            b.pack(side="right", padx=8, pady=8)
        btns.pack(side="bottom", fill="x")

    def on_calculate(self):
        score = Total([ph.as_point_holder() for ph in self.ph_proxies])
        results = score.calculate()
        for i, ph in enumerate(self.ph_proxies):
            ph.results.set("Результат: %s" % results[i])
        if not self.results_visible:
            self.results_visible = True
            for rf in self.results_frames:
                rf.pack(fill="x")




if __name__ == '__main__':
    app = Application()
    tk.mainloop()
