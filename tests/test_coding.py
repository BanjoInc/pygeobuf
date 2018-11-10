import json
import math
import unittest

from geobuf import Decoder, Encoder

from tests import get_data_path


class CodingTests(unittest.TestCase):
    def setUp(self):
        with open(get_data_path("precision.json")) as f:
            self.precision_data = json.load(f)

    def test_high_precision(self):
        pbf = Encoder().encode(self.precision_data)
        geojson2 = Decoder().decode(pbf)
        ring = geojson2['features'][0]['geometry']['coordinates'][0]
        assert ring[0] == ring[4]

    def test_line_accumulating_error(self):
        """
        Generate a line of 40 points. Each point's x coordinate, x[n] is at x[n - 1] + 1 + d, where
        d is a floating point number that just rounds to 0 at 6 decimal places, i.e. 0.00000049.
        Therefore a delta compression method that only computes x[n] - x[n - 1] and rounds to 6 d.p.
        will get a constant delta of 1.000000. The result will be an accumulated error along the
        line of 0.00000049 * 40 = 0.0000196 over the full length.
        """
        feature = {
            'type':        'MultiPolygon',
            'coordinates': [[[]]],
        }
        points = 40
        # X coordinates[0, 1.00000049, 2.00000098, 3.00000147, 4.00000196, ...,
        #               37.00001813, 38.00001862, 39.00001911, 40.00001960, 0]
        feature['coordinates'][0][0] = [[i * 1.00000049, 0] for i in range(0, points + 1)]
        feature['coordinates'][0][0].append([0, 0])
        pbf = Encoder().encode(feature)
        round_tripped = Decoder().decode(pbf)

        def round_x(coord):
            x, _ = coord
            return round(x * 1000000) / 1000000.0

        xs_orig = [round_x(coord) for coord in feature['coordinates'][0][0]]
        xs_round_tripped = [round_x(coord) for coord in round_tripped['coordinates'][0][0]]
        assert xs_round_tripped == xs_orig

    def test_circle_accumulating_error(self):
        feature = {
            'type':        'MultiPolygon',
            'coordinates': [[[]]],
        }
        points = 16
        feature['coordinates'][0][0] = [
            [math.cos(math.pi * 2.0 * i / points), math.sin(math.pi * 2.0 * i / points)]
            for i in range(0, points + 1)
        ]
        pbf = Encoder().encode(feature)
        round_tripped = Decoder().decode(pbf)

        def round_coord(coord):
            x, y = coord
            return [round(x * 1000000), round(y * 1000000)]

        ring_orig = [round_coord(coord) for coord in feature['coordinates'][0][0]]
        ring_round_tripped = [round_coord(coord) for coord in round_tripped['coordinates'][0][0]]
        assert ring_round_tripped == ring_orig
