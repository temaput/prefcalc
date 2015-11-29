import unittest
import calc

POINTS_FOUR = (
    dict(points=20, fine=8, whists=(10, 10, 10)),
    dict(points=20, fine=9, whists=(20, 20, 20)),
    dict(points=20, fine=10, whists=(30, 30, 30)),
    dict(points=20, fine=11, whists=(40, 40, 40)),
)

RESULTS_FOUR = (-45, -15, 15, 45)

POINTS_THREE = (
    dict(points=20, fine=7, whists=(10, 10)),
    dict(points=20, fine=9, whists=(30, 30)),
    dict(points=20, fine=8, whists=(20, 20)),
)

RESULTS_THREE = (-20, 20, 0)

POINTS_INCOMPLETE = (
    dict(points=10, fine=8, whists=(10, 10, 10)),
    dict(points=2, fine=9, whists=(20, 20, 20)),
    dict(points=20, fine=10, whists=(30, 30, 30)),
    dict(points=15, fine=11, whists=(40, 40, 40)),
)

RESULTS_INCOMPLETE = (-62, -112, 98, 78)


class TestCalculation(unittest.TestCase):

    def test_three(self):
        results = calc.Total(
            (calc.PointHolder(i, **d) for i, d in enumerate(POINTS_THREE, 1))
        ).calculate()
        for i, r in enumerate(results):
            self.assertEqual(r, RESULTS_THREE[i])

    def test_four(self):
        results = calc.Total(
            (calc.PointHolder(i, **d) for i, d in enumerate(POINTS_FOUR, 1))
        ).calculate()
        for i, r in enumerate(results):
            self.assertEqual(r, RESULTS_FOUR[i])

    def test_incomplete(self):
        results = calc.Total(
            (calc.PointHolder(i, **d)
             for i, d in enumerate(POINTS_INCOMPLETE, 1))).calculate()
        for i, r in enumerate(results):
            self.assertEqual(r, RESULTS_INCOMPLETE[i])

if __name__ == '__main__':
    unittest.main()
