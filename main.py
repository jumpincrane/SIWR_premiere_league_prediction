from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
import os
import pandas as pd


class ProbApp:

    def __init__(self):
        # temp input
        self.input = ["25/06/2021", "Liverpool", "Tottenham"]
        self.result = None
        # variables
        self.data = pd.read_csv('data.csv')
        self.teams = {}

    def prediction(self):
        self.calculate_team_strength()
        model = BayesianModel()

    def calculate_team_strength(self):
        # get list of teams
        teams = []
        for row in self.data.values:
            home_team = row[1]
            away_team = row[2]
            teams.append(home_team)
            teams.append(away_team)
        # removing duplicates
        teams = set(teams)
        # group scores to a team
        for team in teams:
            # FTHG, FTAG, FTHWINS, FTAWINS, FTDRAWS, MATCHES, HR, AR, HST, AST, TEAMSTR
            team_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            matches = 0
            team_str = 0
            for row in self.data.values:
                if team == row[1]:
                    matches += 1
                    team_stat[0] += row[3]
                    team_stat[6] += row[19]
                    team_stat[8] += row[11]
                    if 'H' == row[5]:
                        team_stat[2] += 1
                        team_str += 3
                    elif 'D' == row[5]:
                        team_stat[4] += 1
                        team_str += 1
                elif team == row[2]:
                    matches += 1
                    team_stat[1] += row[4]
                    team_stat[7] += row[20]
                    team_stat[9] += row[12]
                    if 'A' == row[5]:
                        team_stat[3] += 1
                        team_str += 5
                    elif 'D' == row[5]:
                        team_stat[4] += 1
                        team_str += 2
            team_stat[5] = matches
            team_stat[10] = team_str
            self.teams[team] = team_stat

def main():
    predict_app = ProbApp()
    predict_app.prediction()
    print(predict_app.teams)

if __name__ == "__main__":
    main()
