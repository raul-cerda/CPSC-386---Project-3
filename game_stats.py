# Raul Cerda
# raul.cerda@csu.fullerton.edu
# Project 3: Space Invaders


# keeps track of level, score, ships, and high scores
class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

        score_file = open('high_scores.txt', 'r')
        self.high_scores = score_file.readlines()
        self.high_score = int(self.high_scores[0])
        score_file.close()

        self.last_ufo_points = 0

        self.ships_left = 0
        self.score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    # replaces old leaderboard scores with current higher scores
    def new_high_score(self, new_score):
        if new_score > int(self.high_scores[0]):
            self.high_scores[0] = str(new_score)+'\n'
        elif new_score > int(self.high_scores[1]):
            self.high_scores[1] = str(new_score)+'\n'
        elif new_score > int(self.high_scores[2]):
            self.high_scores[2] = str(new_score)+'\n'
        self.save_high_scores()

    # saves the 3 top scores to text file for next game session
    def save_high_scores(self):
        score_file = open('high_scores.txt', 'w')
        for i in self.high_scores:
            score_file.write(i)
        score_file.close()
