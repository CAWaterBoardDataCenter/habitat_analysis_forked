from fun import *


class Raster:
    def __init__(self, file_name, band=1, raster_array=None, epsg=3857, geo_info=False):
        """
        A GeoTiff Raster dataset (wrapped osgeo.gdal. Dataset)
        :param file_name: STR of a GeoTiff file name including directory (must end on ".tif")
        :param band: INT of the band number to use
        :param raster_array: numpy.ndarray of values to use (if new raster has to be created)
        :param epsg: INT of EPSG:XXXX projection to use - default=4326
        :param geo_info: TUPLE defining a gdal.DataSet.GetGeoTransform object (supersedes origin, pixel_width, pixel_height)
                            default=False
        """
        # extract raster name and retrieve geospatial information
        self.name = file_name.split("/")[-1].split("\\")[-1].split(".")[0] # EXTRACT FROM FILE NAME

        if not os.path.exists(file_name):
            # this creates a new Raster if the provided file name does not exist)
            if raster_array is None:
                geo.create_raster(file_name, raster_array=np.zeros((100, 100)), epsg=epsg, geo_info=geo_info)
            else:
                geo.create_raster(file_name, raster_array=raster_array, epsg=epsg, geo_info=geo_info)

        self.dataset, self.array, self.geo_transformation = geo.raster2array(file_name, band_number=band)# USE GEO.RASTER2ARRAY FUNCTION TO LOAD RASTER DATA AND GEOTRANFORMATION

        self.srs = geo.get_srs(self.dataset)# USE GEO.GET_SRS FUNCTION TO OPEN THE SPATIAL REFERENCE SYSTEM
        self.epsg = int(epsg)
        #self.epsg = int(self.srs.GetAuthorityCode(None))# READ THE EPSG AUTHORITY CODE FROM SELF.SRS

        
    def __truediv__(self, constant_or_raster):
        """
        Division of the input Raster by a constant or another Raster
        :param constant_or_raster: Constant (numeric) or Raster with the same number of rows and columns as the input Raster
        :return: Raster
        """
        
        # THIS IS AN EXAMPLE TO IMPLEMENT THE USAGE OF THE / OPERATOR BETWEEN TWO RASTER OBJECTS
        
        try:
            self.array = np.divide(self.array, constant_or_raster.array)
        except AttributeError:
            self.array /= constant_or_raster
        return self._make_raster("div")

    def __add__(self, constant_or_raster):
        """
        Addition of a constant or a Raster to the input Raster (of same dimensions as input raster)
        :param constant_or_raster: Constant (numeric) or Raster with the same number of rows and columns as the input Raster
        :return: Raster
        """
        # WRITE MAGIC METHOD TO USE + OPERATOR
        try:
            self.array += constant_or_raster.array
        except AttributeError:
            self.array += constant_or_raster
        return self._make_raster("add")
        
        #pass

    def __mul__(self, constant_or_raster):
        """
        Multiplication of the input Raster with a contant or another Raster
        :param constant_or_raster: Constant (numeric) or Raster with the same number of rows and columns as the input Raster
        :return: Raster
        """
        # WRITE MAGIC METHOD TO USE * OPERATOR
        try:
            self.array = np.multiply(self.array, constant_or_raster.array)
        except AttributeError:
            self.array *= constant_or_raster
        return self._make_raster("mul")

        
        #pass


    def __pow__(self, constant_or_raster):
        """
        Put every value of the raster to the power of a constant or another Raster's pixel values
        :param constant_or_raster:
        :return: Raster
        """
        
        # WRITE MAGIC METHOD TO USE ** (POWER) OPERATOR
        try:
            self.array = np.power(self.array, constant_or_raster.array)
        except AttributeError:
            self.array **= constant_or_raster
        return self._make_raster("pow")
        
        #pass


    def __sub__(self, constant_or_raster):
        """
        Subtraction of a constant or a Raster from the input Raster (of same dimensions as input raster)
        :param constant_or_raster: Constant (numeric) or Raster with the same number of rows and columns as the input Raster
        :return: Raster
        """
        # WRITE MAGIC METHOD TO USE - OPERATOR
        try:
            self.array -= constant_or_raster.array
        except AttributeError:
            self.array -= constant_or_raster
        return self._make_raster("sub")

        #pass


    def _make_raster(self, file_marker):
        """
        file_markers are string variables used in the magic methods
        """
        
        f_ending = "__{0}{1}__.tif".format(file_marker, create_random_string(4))
        geo.create_raster(cache_folder + self.name + f_ending, self.array, epsg=self.epsg,
                          nan_val=nan_value,
                          geo_info=self.geo_transformation) # MAKE A VALID FILE NAME ENDING ON  ".TIF"
        
        # USE GEO.CREATE_RASTER(...) TO STORE THE TEMPORARY CALCULATION DATASET IN THE CACHE FOLDER
        
        return Raster(cache_folder + self.name + f_ending) # RASTER OBJECT OF THE TEMPORARY CALCULATION

    def save(self, file_name=str(os.path.abspath("") + "\\00_%s.tif" % create_random_string(7))):
        """
        Save raster to file (GeoTIFF format)
        :param file_name: string of file name including directory and must end on ".tif"
        :return: 0 = success; -1 = failed
        """
        print("Saving Raster as %s ..." % file_name)
        
        # USE THE GEO.CREATE_RASTER FUNCTION AND RETURN THE SAVE STATUS (0=SUCCESS)       
        save_status = geo.create_raster(file_name, self.array, epsg=self.epsg,
                                        nan_val=0.0, geo_info=self.geo_transformation)

        return save_status # SAVE_STATUS
