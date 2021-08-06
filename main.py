import math
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
import pandas as pd


class ProbApp:

    def __init__(self):
        # storing inputs
        # self.input_date = input()
        # self.input_ht = input()
        # self.input_at = input()
        self.data = pd.read_csv('data.csv')
        # dict to store data for a single team
        self.teams_str = {}

    def prediction(self):
        # calculating teams strength and predict results based on strength
        self.calculate_team_strength()

        # ================= MODEL =======================
        model = BayesianModel()
        model.add_edges_from([('HomeTeam', 'HST'), ('HST', 'FTHG'), ('AwayTeam', 'FTHG'), ('FTHG', 'FTR'),
                              ('AwayTeam', 'AST'), ('AST', 'FTAG'), ('HomeTeam', 'FTAG'), ('FTAG', 'FTR'),
                              ('HT_STR', 'STR_RESULT'), ('AT_STR', 'STR_RESULT'), ('STR_RESULT', 'FTR')])
        model.fit(self.data)
        # ===============================================

        # inference
        infer = VariableElimination(model)
        query = infer.map_query(variables=['FTR'],
                            evidence={'HomeTeam': self.input_ht, 'AwayTeam': self.input_at})

        print(query['FTR'])

    def test_results(self, model, test_data, train_number):
        """
        Temporary function for testing results via model.predict()

        model - input your bayesian model
        test_data - input your splitted part of data for testing
        train_number - the specific index where the data is splitted
        """
        predicted = model.predict(test_data)
        predicted_ftr = predicted.pop('FTR').values
        cmp_ftr = self.data[train_number:].pop('FTR').values
        num_correct = 0
        for i in range(len(predicted_ftr)):
            if predicted_ftr[i] == cmp_ftr[i]:
                num_correct += 1

        print(f'{int((num_correct / len(predicted_ftr)) * 100)}%')

    def calculate_team_strength(self):
        # get list of teams and removing duplicates
        teams = list(self.data['HomeTeam'])
        teams = set(teams)

        # calc team strength
        for team in teams:
            matches = 0
            team_str = 0
            for row in self.data.values:
                if team == row[1]:
                    matches += 1
                    if 'H' == row[5]:
                        team_str += 3
                    elif 'D' == row[5]:
                        team_str += 1
                elif team == row[2]:
                    matches += 1
                    if 'A' == row[5]:
                        team_str += 5
                    elif 'D' == row[5]:
                        team_str += 2

            self.teams_str[team] = team_str

        # normalize strength to <0;1> and give them a value from [0, 1, 2] in a specific range
        max_str = max(self.teams_str.values())
        min_str = min(self.teams_str.values())
        for team in self.teams_str:
            temp = self.teams_str[team]
            temp = (temp - min_str) / (max_str - min_str)
            st = 0
            if temp >= 0.8:
                st = 2
            elif 0.8 > temp >= 0.25:
                st = 1
            elif 0.25 > temp:
                st = 0
            self.teams_str[team] = st

        # calculate result based on str
        home_team_str = []
        away_team_str = []
        result_str = []
        for row in self.data.values:
            home_team = row[1]
            away_team = row[2]

            temp_htstr = self.teams_str[home_team]
            temp_atstr = self.teams_str[away_team]
            temp_result = 0
            if temp_atstr == temp_htstr:
                temp_result = 'D'
            elif temp_atstr > temp_htstr:
                temp_result = 'A'
            elif temp_htstr > temp_atstr:
                temp_result = 'H'

            result_str.append(temp_result)
            home_team_str.append(temp_htstr)
            away_team_str.append(temp_atstr)

        # add columns to data
        self.data['HT_STR'] = home_team_str
        self.data['AT_STR'] = away_team_str
        self.data['STR_RESULT'] = result_str

    def split_data(self, ratio):
        """
            Temporary function for splitting data

            ratio - input how you want the data to be splitted f.e (80:20 = 0.8)
        """
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
