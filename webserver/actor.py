class Actor:
    def __init__(self, row):
        self.film_name = row[1]
        self.film_imdblink = row[3]
        self.filmmaker = row[5]
        self.filmmaker_imdblink = row[4]
        self.actor_imdblink = row[8]
        self.actor_name = row[10]
        self.actor_gender = row[11]
        self.actor_img = row[12]
        self.character_name = row[14]


        
