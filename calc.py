"""
Preferance total calculator
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

from decimal import Decimal, getcontext

TOTAL_RATIO = None  # may be 1, 2, 3, 4 or None meaning = players_count
POINTS_RATIO = FINE_RATIO = Decimal(10)  # may be 20, 10


getcontext().prec = 2


class DecimalDescriptor:

    def __init__(self):
        self.values = {}

    def __get__(self, obj, objtype):
        if obj is None:
            return max(self.values.values())
        if obj not in self.values:
            return Decimal()
        return self.values[obj]

    def __set__(self, obj, value):
        self.values[obj] = Decimal("%s" % value)


class PointHolder:
    fine = DecimalDescriptor()
    points = DecimalDescriptor()
    applied_fine = DecimalDescriptor()

    def whists():
        doc = "The whists property."

        def fget(self):
            return self._whists

        def fset(self, whists_tuple):
            self._whists = tuple(Decimal("%s" % w) for w in whists_tuple)

        def fdel(self):
            del self._whists
        return locals()
    whists = property(**whists())

    def __init__(self, playerno, **kwargs):

        self.playerno = playerno - 1
        if "whists" in kwargs:
            self.whists = kwargs.pop("whists")
        self.fine = kwargs['fine']
        self.points = kwargs['points']

    def calculate_fine(self):
        if self.applied_fine:
            return self.applied_fine
        fine = self.fine * FINE_RATIO
        max_points = PointHolder.points
        players_count = len(self.whists) + 1
        points_shortage = (max_points - self.points) * POINTS_RATIO
        fine = (fine + points_shortage) / (TOTAL_RATIO or players_count)
        self.applied_fine = fine
        return fine

    def __gt__(self, rhs):
        return self.playerno > rhs.playerno

    def __sub__(self, rhs):
        return self.get_whist_value(rhs) - rhs.get_whist_value(self)

    def get_whist_value(self, rhs):
        if self == rhs:
            return 0
        whists_count = len(self.whists)
        players_count = whists_count + 1
        whist_pos = (
            whists_count - self.playerno + rhs.playerno) % players_count
        return self.whists[whist_pos] - self.calculate_fine()

    def __repr__(self):
        return "Player #%s, %s points, %s fine, %s whists\n" % (
            self.playerno, self.points, self.fine, self.whists)


class Total:

    def __init__(self, point_holders):
        self.point_holders = sorted(point_holders)

    def calculate(self):
        players_count = len(self.point_holders)
        if players_count == 0:
            return 0

        results = []
        for lph in self.point_holders:
            results.append(sum(lph - rph for rph in self.point_holders))
        return results