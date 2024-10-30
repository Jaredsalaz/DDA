import unittest
from algoritmo import algoritmo_punto_medio_elipse

class TestAlgoritmoPuntoMedioElipse(unittest.TestCase):
    def test_algoritmo_punto_medio_elipse(self):
        Xc, Yc, Rx, Ry = 0, 0, 8, 6
        puntos, region1, region2 = algoritmo_punto_medio_elipse(Xc, Yc, Rx, Ry)
        
        # Expected points for region 1
        expected_region1 = [
            (1, 6, -332),
            (2, 6, -224),
            (3, 6, -44),
            (4, 5, 208),
            (5, 5, -108),
            (6, 4, 288),
            (7, 3, 244)
        ]
        
        # Expected points for region 2
        expected_region2 = [
            (8, 2, -23),
            (8, 1, 361),
            (8, 0, 297),
        ]
        
        # Check if the points in region 1 match the expected values
        for i, (x, y, p) in enumerate(region1):
            self.assertEqual((x, y, p), expected_region1[i])
        
        # Check if the points in region 2 match the expected values
        for i, (x, y, p) in enumerate(region2):
            self.assertEqual((x, y, p), expected_region2[i])

if __name__ == '__main__':
    unittest.main()