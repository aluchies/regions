# regions
Module to extract pixel values from an arbitrary shaped region inside an image

## Overview
Some of the shapes included in this module include Ellipse, Circle, Rectangle, Square, Annulus, and Polygon. It is also possible take unions and intersections of regions.

## Example
```python
from regions import Square

# define region
region_dict = {'type': 'square', 'xc':1, 'zc':1, 'length':4, 'units':'mm'}
region = create_region(**region_dict)

print(f"Region area: {region.area}")

# extract values from inside the region
vals = region.get_values_in_region(im, x_mm, z_mm)

# create mpl patch for displaying the region
patch = region.create_mpl_patch()
ax.add_patch(patch)

```
