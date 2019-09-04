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

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """

        return None


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


class Square(Rectangle):
    def __init__(self, xc, zc, length, units):
        super().__init__(xc, zc, length, length, units)
        self.length = length


class Ellipse(Region):
    def __init__(self, xc, zc, radius_x, radius_z, units):
        super().__init__()
        self.radius_x = radius_x
        self.radius_z = radius_z
        self.xc = xc
        self.zc = zc
        self.area = np.pi * self.radius_x * self.radius_z
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

        mask = np.sqrt( (x_grid - self.xc) ** 2 / self.radius_x ** 2
            + (z_grid - self.zc) ** 2 / self.radius_z ** 2 )
        mask = (mask <= 1)

        return mask

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """

        patch =  mpatches.Ellipse([ self.xc, self.zc] , width=2*self.radius_x,
            height=2*self.radius_z,
            edgecolor='red', facecolor="None" )
        return patch


class Circle(Ellipse):
    def __init__(self, xc, zc, radius, units):
        super().__init__(xc, zc, radius, radius, units)
        self.radius = radius


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

class Polygon(Region):
    def __init__(self, vertices, units):
        super().__init__()
        self.vertices = vertices
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

        # create patch for testing if points inside the region
        # It seems like I should be able to call self.create_mpl_patch() here,
        # but the returned patch did not have correct contains_points()
        # behavior.
        patch =  mpatches.Polygon(xy=self.vertices)

        # create grid data
        x_grid, z_grid = np.meshgrid( x_axis, z_axis )

        # reshape things
        x_grid = np.reshape( x_grid, len(x_axis) * len(z_axis))
        z_grid = np.reshape( z_grid, len(x_axis) * len(z_axis))

        # need an Nx2 array of xz-coordinates for grid points
        xy_grid = np.vstack([x_grid, z_grid]).transpose()

        # test if points inside the patch
        mask = patch.contains_points(xy_grid)

        # reshape outputs
        mask = np.reshape(mask, (len(z_axis), len(x_axis)))
        x_grid = np.reshape(x_grid, (len(z_axis), len(x_axis)))
        z_grid = np.reshape(z_grid, (len(z_axis), len(x_axis)))

        return mask

    def create_mpl_patch(self):
        """Create a matplotlib patch for the region.

        Returns
        -------
        patch : matplotlib patch

        """
        patch =  mpatches.Polygon(xy=self.vertices,
            edgecolor='red', facecolor="None" )
        return patch    


def create_region(**kwargs):
    """Helper function for creating region objects
    
    Based on the type variable, this function creates a region object.
    """

    if kwargs['type'] == 'circle':
        del kwargs['type']
        return Circle(**kwargs)

    elif kwargs['type'] == 'ellipse':
        del kwargs['type']
        return Ellipse(**kwargs)

    elif kwargs['type'] == 'square':
        del kwargs['type']
        return Square(**kwargs)

    elif kwargs['type'] == 'rectangle':
        del kwargs['type']
        return Rectangle(**kwargs)

    elif kwargs['type'] == 'annulus':
        del kwargs['type']
        return Annulus(**kwargs) 