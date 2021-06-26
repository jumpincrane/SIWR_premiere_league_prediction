import pgmpy
import csv


class ProbApp:

    def __init__(self):
        # variables
        self.dates = []
        self.home_teams = []
        self.away_teams = []
        self.ft_home_goals = []
        self.ft_away_goals = []
        self.ft_results_match = []
        self.ht_home_goals = []
        self.ht_away_goals = []
        self.ht_results_match = []
        self.home_shots = []
        self.away_shots = []
        self.home_target_shots = []
        self.away_target_shots = []

    def load_data(self):
        with open('data.csv', newline='') as csv_file:
            spam_reader = csv.reader(csv_file, quotechar='|')
            next(spam_reader)  # skip first element
            for row in spam_reader:
                self.dates.append(row[0])
                self.home_teams.append(row[1])
                self.away_teams.append(row[2])
                self.ft_home_goals.append(row[3])
                self.ft_away_goals.append(row[4])
                self.ft_results_match.append(row[5])
                self.ht_home_goals.append(row[6])
                self.ht_away_goals.append(row[7])
                self.ht_results_match.append(row[8])
                self.home_shots.append(row[9])
                self.away_shots.append(row[10])
                self.home_target_shots.append(row[11])
                self.away_target_shots.append(row[12])

    def prediction(self):
        pass


def main():
    predict_app = ProbApp()
    predict_app.load_data()


if __name__ == "__main__":
    main()
