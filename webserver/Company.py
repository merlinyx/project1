class Company:
    def __init__(self, row):
        self.film_name = row[1]
        self.film_imdblink = row[3]
        self.company_imdblink = row[6]
        self.company_name = row[7]
