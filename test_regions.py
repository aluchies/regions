#!/usr/bin/env python

import unittest
import regions
import numpy as np

class TestCode(unittest.TestCase):

    def test_Annulus(self):
        """Test Annulus object"""

        # test that object attributes are stored correctly
        radius_in = 0
        radius_out = 0.5
        xc = 1
        zc = 1
        units = 'mm'
        a_annulus = regions.Annulus(xc, zc, radius_in, radius_out, units)
        self.assertEqual(a_annulus.radius_in, radius_in)
        self.assertEqual(a_annulus.radius_out, radius_out)
        self.assertEqual(a_annulus.xc, xc)
        self.assertEqual(a_annulus.zc, zc)
        self.assertEqual(a_annulus.units, units)

        # create a small grid
        x_grid, z_grid = np.meshgrid(
            np.linspace(0, 2, 5),
            np.linspace(0, 2, 5)
        )

        # test if the correct mask is produced
        mask = a_annulus.create_mask(x_grid, z_grid)
        mask_actual = np.asarray([[False, False, False, False, False],
                            [False, False,  True, False, False],
                            [False,  True,  False,  True, False],
                            [False, False,  True, False, False],
                            [False, False, False, False, False]]
        )
        self.assertTrue( np.allclose(mask, mask_actual))

        # extra values from an image
        img = np.sqrt((x_grid - xc) ** 2 + (z_grid - zc) ** 2)
        region_values = a_annulus.get_values_in_region(img, x_grid, z_grid)
        region_values_actual = np.asarray([0.5, 0.5, 0.5, 0.5])
        self.assertTrue(np.allclose(region_values, region_values_actual))



    def test_Circle(self):
        """Test Circle object"""

        # test that object attributes are stored correctly
        radius = 0.5
        xc = 1
        zc = 1
        units = 'mm'
        a_circle = regions.Circle(xc, zc, radius, units)
        self.assertEqual(a_circle.radius, radius)
        self.assertEqual(a_circle.xc, xc)
        self.assertEqual(a_circle.zc, zc)
        self.assertEqual(a_circle.units, units)

        # create a small grid
        x_grid, z_grid = np.meshgrid(
            np.linspace(0, 2, 5),
            np.linspace(0, 2, 5)
        )

        # test if the correct mask is produced
        mask = a_circle.create_mask(x_grid, z_grid)
        mask_actual = np.asarray([[False, False, False, False, False],
                            [False, False,  True, False, False],
                            [False,  True,  True,  True, False],
                            [False, False,  True, False, False],
                            [False, False, False, False, False]]
        )
        self.assertTrue( np.allclose(mask, mask_actual))

        # extra values from an image
        img = np.sqrt((x_grid - xc) ** 2 + (z_grid - zc) ** 2)
        region_values = a_circle.get_values_in_region(img, x_grid, z_grid)
        region_values_actual = np.asarray([0.5, 0.5, 0, 0.5, 0.5])
        self.assertTrue(np.allclose(region_values, region_values_actual))


if __name__ == '__main__':
    print("Running unit tests for stft.py")
    unittest.main()