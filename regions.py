import numpy as np
import matplotlib.patches as mpatches


class Region:
    """Parent class for regions.
    """
    def __init__(self):
        pass

    def create_mask(self, x_axis, z_axis):
        """
        Create a mask from a grid.

        Parameters
        ----------
        x_axis : ndarray
            x- (lateral) coordinates
        z_axis : ndarray
            z- coordinates
        
        Returns
        -------
        mask : ndarray

        """

        mask = ( np.ones(z_axis.shape[0], x_axis.shape[0]) == 1 )

        return mask


    def get_values_in_region(self, img, x_axis, z_axis):
        """
        Create a mask from a grid. The mask is added to the object.

        Parameters
        ----------
        img : ndarray
            Extract values from this 2D image that are inside the region
        x_axis : ndarray
            x- (lateral) coordinates
        z_axis : ndarray
            z- (axial) coordinates
        
        Returns
        -------
        values : 1D array of values

        """

        mask = self.create_mask(x_axis, z_axis)

        return img[mask]



class Rectangle(Region):
    def __init__(self, xc, zc, width, height, units):
        super().__init__()
        self.width = width
        self.height = height
        self.xc = xc
        self.zc = zc
        self.area = self.width * self.height
        self.units = units

    def create_mask(self, x_axis, z_axis):
        """
        Create a mask from a grid.

        Parameters
        ----------
        x_axis : ndarray
            x- (lateral) coordinates
        z_axis : ndarray
            z- (axial) coordinates
        
        Returns
        -------
        mask : ndarray

        """

        x_grid, z_grid = np.meshgrid( x_axis, z_axis )

        mask_x = np.abs( x_grid - self.xc ) <= (self.width / 2)
        mask_z = np.abs( z_grid - self.zc ) <= (self.height / 2)

        mask = mask_x * mask_z

        return mask

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """
        patch =  mpatches.Rectangle(
            [ self.xc - self.width/2, self.zc - self.height/2],
            self.width,
            self.height,
            edgecolor='red', facecolor="None" )
        return patch


class Circle(Region):
    def __init__(self, xc, zc, radius, units):
        super().__init__()
        self.radius = radius
        self.xc = xc
        self.zc = zc
        self.area = np.pi * self.radius**2
        self.units = units

    def create_mask(self, x_axis, z_axis):
        """
        Create a mask from a grid.

        Parameters
        ----------
        x_axis : ndarray
            x- (lateral) coordinates
        z_axis : ndarray
            z- (axial) coordinates
        
        Returns
        -------
        mask : ndarray

        """

        x_grid, z_grid = np.meshgrid( x_axis, z_axis )

        mask = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask = (mask <= self.radius)

        return mask

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """

        patch =  mpatches.Circle([ self.xc, self.zc] , self.radius,
            edgecolor='red', facecolor="None" )
        return patch


class Annulus(Region):
    def __init__(self, xc, zc ,radius_in, radius_out, units):
        super().__init__()
        self.radius_in = radius_in
        self.radius_out = radius_out
        self.xc = xc
        self.zc = zc
        self.area = np.pi * (self.radius_out ** 2 - self.radius_in ** 2)
        self.units = units

    def create_mask(self, x_axis, z_axis):
        """
        Return a mask from a grid

        Parameters
        ----------
        x_axis : ndarray
            x- (lateral) coordinates
        z_axis : ndarray
            z- (axial) coordinates

        Returns
        -------
        mask : array_like
        """

        x_grid, z_grid = np.meshgrid( x_axis, z_axis )

        mask_out = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask_out = (mask_out <= self.radius_out)

        mask_in = np.sqrt( (x_grid - self.xc) ** 2 + (z_grid - self.zc) ** 2 )
        mask_in = (mask_in <= self.radius_in)

        mask = mask_out ^ mask_in

        return mask

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