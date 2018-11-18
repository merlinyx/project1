class Actor:
    def __init__(self, row):
        self.film_name = row[1]
        self.film_imdblink = row[3]
        self.actor_imdblink = row[6]
        self.actor_name = row[8]
        self.actor_gender = row[8]
        self.actor_img = row[10]
        self.character_name = row[12]
        