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
import calc


class PointHolderProxy:

    def __init__(self, playerno):
        self.playerno = playerno
        self.fine = tk.IntVar()
        self.points = tk.IntVar()
        self.whists = [tk.IntVar() for i in range(3)]

        self.results = tk.StringVar()

    def as_point_holder(self, ph_limit):
        return calc.PointHolder(
            self.playerno,
            fine=self.fine.get(),
            points=self.points.get(),
            whists=[w.get() for w in self.whists[:ph_limit-1]])


class Preferences:
    """
    Singleton
    """

    def __init__(self):
        self.players_count = tk.IntVar(value=4)
        self.fine_points_ratio = tk.IntVar()
        self.total_ratio = tk.IntVar(value=4)


class Application:

    def __init__(self):

        self.top = tk.Tk()
        self.preferences_dialog = None
        self.preferences = Preferences()
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
        self.last_whist_entries = []

        container = ttk.Frame(self.top)
        container.pack(fill="both", expand=1)
        container.lower()
        for i in range(1, 5):
            lf = ttk.LabelFrame(container, text="Player %s" % i)
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
            self.last_whist_entries.append(whists[-1])
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

        for col, lf in enumerate(self.player_frames):
            lf.grid(column=col, row=0,
                    sticky="nwe", pady=2, padx=3)

        for i in range(2):
            container.grid_columnconfigure(i, weight=1, uniform=True)

    def button_group(self):
        btns = ttk.Frame(self.top)
        sep = ttk.Separator(btns)
        sep.pack(side="top", fill="x",  pady=2)

        self.QUIT = ttk.Button(btns, text="Close", command=self.top.destroy)
        self.CALCULATE = ttk.Button(btns, text="Calculate",
                                    command=self.on_calculate)
        self.PREFERENCES = ttk.Button(btns, text="Preferences...",
                                      command=self.on_preferences)
        for num, b in enumerate([self.QUIT, self.PREFERENCES, self.CALCULATE]):
            b.pack(side="right", padx=8, pady=8)
        btns.pack(side="bottom", fill="x")

    def on_calculate(self):
        calc.FINE_RATIO, calc.POINTS_RATIO = calc.fine_points_ratio_list[
            self.preferences.fine_points_ratio.get()]
        calc.TOTAL_RATIO = self.preferences.total_ratio.get()

        ph_limit = self.preferences.players_count.get()
        score = calc.Total([ph.as_point_holder(ph_limit)
                            for ph in self.ph_proxies[:ph_limit]])
        results = score.calculate()
        for i, ph in enumerate(self.ph_proxies[:ph_limit]):
            ph.results.set("Результат: %s" % results[i])
        if not self.results_visible:
            self.results_visible = True
            for rf in self.results_frames:
                rf.pack(fill="x")

    def on_preferences(self):
        if not self.preferences_dialog:
            self.preferences_dialog = PreferencesDialog(self.top, self)
        else:
            self.preferences_dialog.deiconify()
        self.preferences_dialog.focus_set()
        self.preferences_dialog.lift()

    def recount_fp_ratio(self):
        print(self.preferences.fine_points_ratio.get())

    def recount_total_ratio(self):
        print(self.preferences.total_ratio.get())

    def recount_players(self):
        players_count = self.preferences.players_count.get()
        last_frame = self.player_frames[-1]
        if players_count < 4:
            for widget in self.last_whist_entries:
                widget.state(("disabled",))
            last_frame.grid_remove()
        else:
            for widget in self.last_whist_entries:
                widget.state(("!disabled",))
            last_frame.grid()


class PreferencesDialog(tk.Toplevel):

    def __init__(self, parentwindow, app):
        tk.Toplevel.__init__(self, parentwindow)
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.app = app
        self.title("Pref calc preferences")
        self.CreateWidgets()

    def on_players_recount(self):
        players_count = self.app.preferences.players_count
        total_ratio = self.app.preferences.total_ratio
        if players_count.get() < 4:
            if total_ratio.get() > 3:
                total_ratio.set(3)

            self.radioTotalRatio4.state((tk.DISABLED,))
        else:
            self.radioTotalRatio4.state(("!disabled",))

        self.app.recount_players()

    def CreateWidgets(self):
        self.frameMain = frameMain = ttk.Frame(self, pad="3 3 12 12")
        frameMain.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        frameMain.columnconfigure(0, weight=1)
        frameMain.rowconfigure(0, weight=1)

        toplabel = ttk.Label(frameMain, text="Preferences", anchor=tk.CENTER)
        toplabel.grid(row=0, column=0, pady=20)

        # Players amount (3 or 4)
        playersCountFrame = ttk.LabelFrame(frameMain,
                                           text="Количество игроков")
        players_count_var = self.app.preferences.players_count
        radioPC1 = ttk.Radiobutton(playersCountFrame,
                                   text="Трое",
                                   variable=players_count_var,
                                   command=self.on_players_recount,
                                   value=3
                                   )
        radioPC2 = ttk.Radiobutton(playersCountFrame,
                                   text="Четверо",
                                   variable=players_count_var,
                                   value=4,
                                   command=self.on_players_recount,
                                   )
        radioPC1.grid(row=0, column=0, sticky=(tk.W,))
        radioPC2.grid(row=1, column=0, sticky=(tk.W,))
        playersCountFrame.grid(row=1, column=0, sticky=(tk.W,))

        fine_poins_ratio_var = self.app.preferences.fine_points_ratio
        frameFPRatio = ttk.LabelFrame(frameMain, text="Стоимость пули/горы")
        ttk.Radiobutton(frameFPRatio,
                        text="Пуля = 10, гора = 10",
                        variable=fine_poins_ratio_var,
                        value=0,
                        command=self.app.recount_fp_ratio
                        )
        ttk.Radiobutton(frameFPRatio,
                        text="Пуля = 20, гора = 10",
                        variable=fine_poins_ratio_var,
                        value=1,
                        command=self.app.recount_fp_ratio
                        )
        for row, widget in enumerate(frameFPRatio.winfo_children()):
            widget.grid(row=row, column=0, sticky=(tk.W,))
        frameFPRatio.grid(row=1, column=1, sticky=(tk.W,))

        total_ratio_var = self.app.preferences.total_ratio
        frameTotalRatio = ttk.LabelFrame(frameMain, text="Делимость горы")
        ttk.Radiobutton(frameTotalRatio,
                        text="на 1",
                        variable=total_ratio_var,
                        value=1,
                        command=self.app.recount_total_ratio
                        )
        ttk.Radiobutton(frameTotalRatio,
                        text="на 2",
                        variable=total_ratio_var,
                        value=2,
                        command=self.app.recount_total_ratio
                        )
        ttk.Radiobutton(frameTotalRatio,
                        text="на 3",
                        variable=total_ratio_var,
                        value=3,
                        command=self.app.recount_total_ratio
                        )
        self.radioTotalRatio4 = ttk.Radiobutton(
            frameTotalRatio,
            text="на 4",
            variable=total_ratio_var,
            value=4,
            command=self.app.recount_total_ratio
        )
        for row, widget in enumerate(frameTotalRatio.winfo_children()):
            widget.grid(row=row, column=0, sticky=(tk.W,))

        frameTotalRatio.grid(row=1, column=2, sticky=(tk.W,))

        for child in frameMain.winfo_children():
            child.grid_configure(padx=5, pady=5)
