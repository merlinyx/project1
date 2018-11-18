GMAP_PREFIX = "http://maps.google.com/maps?q={:.6f},{:.6f}"

class Film:
    def __init__(self, row):
        self.year = row[0]
        self.name = row[1]
        self.url_encoded_name = row[2]
        self.film_imdblink = row[3]
        self.filmmaker = row[5]
        self.filmmaker_imdblink = row[6]
        self.gmap_url = GMAP_PREFIX.format(row[7], row[8])
        self.location = row[12]
        self.borough = row[13]
        self.neighborhood = row[14]
    