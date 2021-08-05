import math
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
import pandas as pd


class ProbApp:

    def __init__(self):
        # self.input_date = input()
        # self.input_ht = input()
        # self.input_at = input()
        self.input_date = '02/01/2021'
        self.input_ht = 'Southampton'
        self.input_at = 'Fulham'
        self.data = pd.read_csv('data.csv')
        # dict to store data for a single team
        self.teams = {}

    def prediction(self):
        self.calculate_team_strength()
        # for team in self.teams:
        #     print(team)
        #     print(self.teams[team])
        # train_number, train_data, test_data = self.split_data(ratio=0.1)

        model = BayesianModel()
        model.add_edges_from([('HomeTeam', 'HST'), ('HST', 'FTHG'), ('AwayTeam', 'FTHG'), ('FTHG', 'FTR'),
                              ('AwayTeam', 'AST'), ('AST', 'FTAG'), ('HomeTeam', 'FTAG'),
                              ('FTAG', 'FTR')])
        model.fit(self.data)
        print(f'Home Team str:{self.teams[self.input_ht]} vs Away Team str:{self.teams[self.input_at]}')
        infer = VariableElimination(model)
        query = infer.query(variables=['FTR'],
                                evidence={'HomeTeam': self.input_ht, 'AwayTeam': self.input_at})
        print(query)

    def test_results(self, model, test_data, train_number):
        predicted = model.predict(test_data)
        predicted_ftr = predicted.pop('FTR').values
        cmp_ftr = self.data[train_number:].pop('FTR').values
        num_correct = 0
        for i in range(len(predicted_ftr)):
            if predicted_ftr[i] == cmp_ftr[i]:
                num_correct += 1

        print(f'{int((num_correct / len(predicted_ftr)) * 100)}%')

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
            for row in self.data.values:
                print(row)
            self.teams[team] = team_stat

    def split_data(self, ratio):
        train_number = int(math.ceil(len(self.data) * ratio) - 1)

        train_data = self.data[:train_number]
        test_data = self.data[train_number:]
        data2pop = ['FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST', 'AST', 'HF',
                    'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'Date']

        for element in data2pop:
            test_data.pop(element)

        return train_number, train_data, test_data


def main():
    predict_app = ProbApp()
    predict_app.prediction()


if __name__ == "__main__":
    main()
