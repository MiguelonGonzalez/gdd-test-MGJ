import geopandas as gpd
import os
import warnings


class Read_Dataset:

    def __init__(self, path, polygon=True, **kwargs):
        """
        This class allows reading spatial dataset in which of the following formats:
        GeoParquet, ESRI Shapefile, GeoJSON and KML (Other formats might be read, although 
        the class is not prepared to), check if the dataset is (or contains) any polygon
        object, and if the Area of Interest (AOI, from now on) is within the province of 
        Corrientes.

        path: str. Path to the dataset. Check slashes direction if fails.

        polygon: bool (default=True)
            Change to False when reading non-polygon objects. In this case, both checkings 
            are stopped.

        """

        import geopandas as gpd
        import os

        # Checking path format.
        msg = "Excepting path as string, not {}.".format(type(path))
        assert isinstance(path, str), msg
        
        file_format = path.split('.')[-1].lower()

        if file_format == 'parquet':
            _gdf = self._geoparquet(path, **kwargs)
            
        elif file_format == 'geojson':
            _gdf = self._geojson(path, **kwargs)
            
        elif file_format == 'kml':
            _gdf = self._kml(path, **kwargs)

        elif file_format == 'shp':
            _gdf = gpd.read_file(path, **kwargs)
            
        else:
            try:
                _gdf = gpd.read_file(path, **kwargs)

            except:
                raise TypeError("""The format is wrong of the class is not prepared for reading this file format.
                You can check 'geopandas.read_file' function to see the possible file formats. You might have to add
                some keyword arguments or use other geopandas function""")

        self._gdf = _gdf

        # Checking if the dataset is a (or contains any) polygon
        self._is_polygon() if polygon else None
        
        # Checking if the AOI is inside Corrientes Province:
        self._is_inside() if polygon else None

    @property
    def gdf(self):
        return self._gdf

    def _geoparquet(self, path, **kwargs):
        return gpd.read_parquet(path, **kwargs)

    def _geojson(self, path, **kwargs):
        return gpd.read_file(path, driver='GeoJSON', **kwargs)

    def _kml(self, path, **kwargs):
        
        try:
            return gpd.read_file(path, driver='kml', **kwargs)
    
        except:
            # If there is problems reading a KML file, it is possible that the reason is
            # that the Fiona library does not have the KML driver enabled by default.

            import fiona
             
            fiona.drvsupport.supported_drivers['libkml'] = 'rw'
            fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
            fiona.supported_drivers['kml'] = 'rw'
            fiona.supported_drivers['KML'] = 'rw'
        
            return gpd.read_file(path, driver='kml', **kwargs)

    def _area(self, polygon):
        """ Calculate the extension of the polygon (or polygons if multi-polygon feature), in ha. 
        A re-projection is needed for metric calculus to EPGS 22195 ("Campo Inchaupse / Argentina 5"),
        the approximate UTM zone for Corriente province"""
        
        return sum(polygon.to_crs(epsg=22195).area/10000)

    def _is_polygon(self):
        """Check if the dataset corresponds to an polygonal geometry object (Polygon or Multi-Polygon) and
        deletes other geometry objects (such as Lines or Points) if exist.
        If there is not any polygonal object, raise a TypeError."""

        # Checking polygonal geometries
        is_any_polygon = any([i in ['Polygon', 'MultiPolygon'] for i in self._gdf.geom_type.to_list()])

        if not is_any_polygon:
            raise TypeError("The input dataset does not contain any polygonal geometry for representing "
                           "the area of interest within Corrientes province.")
        else:
            pol_mask = self._gdf['geometry'].map(lambda x: (x.geom_type == 'Polygon') or (x.geom_type =='MultiPolygon'))
            self._gdf = self._gdf[pol_mask]

    def _is_inside(self):
        """" Check if the AOI is within the argentinian province of Corrientes. In case that the AOI lies
        in the province limits, with a part outside an other inside, Warning messages are risen, reporting
        about the size of the inner part and how it fits to the general size of the AOI (between 100 and 5000 ha)"""
        
        # The province of Corrientes has been obtained from the Argentinian - IGN service. 
        prov_corrientes = load_corrientes()

        inside = prov_corrientes.contains(self._gdf)

        if inside.all():
            # inside var is only True when the whole AOI lies within the province.
            print('The area of interest lies completeley inside Corrientes province')
            area = self._area(self._gdf)

            if not 100 < area < 5000:
                warnings.warn('\nThe AOI has an extension out of the general terms (100-5.000 ha): '
                              '{}'.format(round(area,2)),
                              stacklevel=2)
            
        else:
            # A part, or the whole AOI does not lie within Corrientes province')
            intersection_polygon = prov_corrientes.intersection(self._gdf)

            if intersection_polygon.is_empty.all():
                # No intersection is possible --> empty intersection polygon
                warnings.warn('The AOI lies completely outside of Corrientes Province', stacklevel=2)
                
            else:
                # A portion of the AOI lies within Corrientes Province!
                inner_area = self._area(intersection_polygon)
                msg_warning = "\nAlthough part of the AOI is out of Corrientes Province"
                                
                if inner_area<100:
                    warnings.warn("{}, there is a small part inside with a size of {} ha (general range: 100-5000 ha)".format(
                        msg_warning, round(inner_area,2)), stacklevel=2)

                elif 100<inner_area<5000:
                    warnings.warn("{}, there is a significant portion (within the general ranging size between 100 and 5000 ha) "
                    "inside, with a size  of {} ha".format(msg_warning, round(inner_area,2)), stacklevel=2)
                    
                elif inner_area>5000:
                    warnings.warn("{}, there is a part inside that exceeds the general ranging terms (100-5000 hs), "
                    "with a size  of {} ha (general range: 100-5000 ha)".format(msg_warning, round(inner_area,2)),
                    stacklevel=2)


def load_corrientes():
    """Return Corrientes shapefile as geopandas DataFrame."""
    return gpd.read_file('data\Layers\Raw\corrientes\corrientes.shp')


def import_tiles():
    """Defining some base layers (tiles) to include in the final
    folium map, created with explore method, of geopandas.gdf object."""
    
    some_tiles = {   
        'ESRI-Imagen':dict(
            tile='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imager\
    y/MapServer/tile/{z}/{y}/{x}',
            attr="""Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AE\
    X, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"""
                          ),
        'ESRI-Callejero':dict(
            tile='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street\
    _Map/MapServer/tile/{z}/{y}/{x}',
            attr="""Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, \
    Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand)\
    , TomTom, 2012"""
                             ),
        'Stamen Terrain':dict(
            tile='Stamen Terrain',
            attr="""Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a \
    href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map dat\
    a &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> co\
    ntributors""",
                             ),
        'Blank':dict(
            tile='',
            attr="""blank""",
                             )
                  }

    return some_tiles