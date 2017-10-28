# geodesic2shape
QGIS Plugin to solve geodetic problems on the reference ellipsoid and export the geodesic's line segment of interest to a shapefile.

Solving Geodetic Problems:
- Foward Geodetic Problem: computes the geographic position of a point, given the initial geodetic azimuth and ellipsoidal distance from a point with known geographic position. 

- Inverse Geodetic Problem: computes the initial geodetic azimuth and ellipsoidal distance between two points, given their geographic positions.

The plugin's solution for both problems are based on Vicenty formulae [1]. Strong evidences that Vicenty formulae provides sub-millimeter accuracy over for them over all geodesics' segments on the ellipsoid of up to 18000 km are shown in [2].  

Creating Shapefiles:
- Foward Problem (SHP Point): at first, the point that corresponds to the First Station is created. Then, the foward problem is solved n times, for every each 1000m (DEFAULT) sequentially, where, by DEFAULT, n=int(ellipsoidal distance/1000). It begins in the First Station with the initial geodetic azimuth and the distance of 1000m (DEFAULT). Then, the distance is increased to 2000, 3000, 4000...n*1000m (DEFAULT) and all solutions are added as new points to the SHP. At last, the foward problem is solved for the whole ellipsoidal distance, in order to provide the last point of the geodesic's line segment of interest. The created points are called SOLUTION POINTS.

- Foward Problem (SHP Line): the SOLUTION POINTS are computed in the same way of the Foward Problem (SHP Point). Besides, at the end, the SHP Line is created using all the SOLUTION POINTS as vertices of the line sequentially.

- Inverse Problem (SHP Point): first of all, the inverse problem is solved, so the initial geodetic azimuth from the First Station is computated. After that, it follows the same procedure as in Foward Problem (SHP Point).

- Inverse Problem (SHP Line): it follows the same procedure as in the Inverse Problem (SHP Point). Besides, at the end, the SHP Line is created using all the SOLUTION POINTS as vertices of the line sequentially.

References
- [1] Direct and inverse solutions of geodesics on the ellipsoid with application of nested equations. Vicenty, T. Survey Review XXII: 1975. 
- [2] Validation of Vincenty’s Formulas for the Geodesic Using a New Fourth-Order Extension of Kivioja’s Formula. Thomas, C. M. and Featherstone, W. E. Journal of Surveying Engineering: Feb 2005.
