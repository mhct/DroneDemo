from Helper import MapParams, MapWidth, CellSize
import os


class Configuration:
    def __init__(self):
        parameters = self._load_configration()
        self._map_param = MapParams(MapWidth(parameters["MapWidthX"], parameters["MapWidthY"]),
                                    CellSize(parameters["ResolutionX"], parameters["ResolutionY"]))

    def _load_configration(self):
        parameters = {}

        script_dir = os.path.dirname(__file__)
        with open(script_dir + "/Configuration.txt") as f:
            for line in f:
                (key, val) = line.split()
                parameters[key] = int(val)

        return parameters

    def get_map_params(self):
        return self._map_param
