

class Property:
    def __init__(
            self,
            general: dict = {},
            location: dict = {},
            amenities: dict = {},
    ):
        self.general = general
        self.location = location
        self.amenities = amenities

    def clear_nulls(self):
        def _clear_nulls(d):
            if isinstance(d, dict):
                d_copy = d.copy()

                for key, value in d_copy.items():
                    if isinstance(value, dict):
                        _clear_nulls(value)

                    if value is None or value in ["Don't say", 0, []]:
                        del d[key]

            return d

        self.general = _clear_nulls(self.general)
        self.location = _clear_nulls(self.location)
        self.amenities = _clear_nulls(self.amenities)

        return self

    #def get_factsheet(self):

