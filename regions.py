import numpy as np
import matplotlib.patches as mpatches


class Circle:
    def __init__(self, xc, zc, radius, units):
        self.radius = radius
        self.xc = xc
        self.zc = zc
        self.area = np.pi * self.radius**2
        self.units = units

    def create_mask(self, x_grid, z_grid):
        """
        Create a mask from a grid. The mask is added to the object.

        Parameters
        ----------
        x_grid : ndarray
            2D grid of x (lateral) coordinates
        z_grid : ndarray
            2D grid of z (axial) coordinates
        
        Returns
        -------
        mask : ndarray

        """

        mask = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask = (mask <= self.radius)

        return mask

    def get_values_in_region(self, img, x_grid, z_grid):
        """
        Create a mask from a grid. The mask is added to the object.

        Parameters
        ----------
        img : ndarray
            Extract values from this 2D image that are inside the region
        x_grid : ndarray
            2D grid of x (lateral) coordinates
        z_grid : ndarray
            2D grid of z (axial) coordinates
        
        Returns
        -------
        values : 1D array of values

        """

        mask = self.create_mask(x_grid, z_grid)

        return img[mask]


    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """
        patch =  mpatches.Circle([ self.xc, self.zc] , self.radius,
            edgecolor='red', facecolor="None" )
        return patch


class Annulus:
    def __init__(self, xc, zc ,radius_in, radius_out, units):
        self.radius_in = radius_in
        self.radius_out = radius_out
        self.xc = xc
        self.zc = zc
        self.area = np.pi * (self.radius_out ** 2 - self.radius_in ** 2)
        self.units = units

    def create_mask(self, x_grid, z_grid):
        """
        Return a mask from a grid

        Parameters
        ----------
        x_grid : ndarray
            Grid of x (lateral) coordinates
        z_grid : ndarray
            Grid of z (axial) coordinates

        Returns
        -------
        mask : array_like
        """

        mask_out = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask_out = (mask_out <= self.radius_out)

        mask_in = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask_in = (mask_in <= self.radius_in)

        mask = mask_out ^ mask_in

        return mask

    def get_values_in_region(self, img, x_grid, z_grid):
        """
        Create a mask from a grid. The mask is added to the object.

        Parameters
        ----------
        img : ndarray
            Extract values from this 2D image that are inside the region
        x_grid : ndarray
            2D grid of x (lateral) coordinates
        z_grid : ndarray
            2D grid of z (axial) coordinates
        
        Returns
        -------
        values : 1D array of values

        """

        mask = self.create_mask(x_grid, z_grid)

        return img[mask]

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch
        
        """

        patch = mpatches.Wedge([ self.xc, self.zc] , self.radius_out,
            0, 360, self.radius_out - self.radius_in,
            edgecolor='red', facecolor="None" )
        return patch


def create_region(**kwargs):
    """Helper function for creating region objects
    
    Based on the type variable, this function creates a region object.
    """

    if kwargs['type'] == 'circle':
        del kwargs['type']
        return Circle(**kwargs)

    elif kwargs['type'] == 'annulus':
        del kwargs['type']
        return Annulus(**kwargs) 
