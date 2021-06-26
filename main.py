from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator
import csv
import pandas as pd

class ProbApp:

    def __init__(self):
        # temp input
        self.input = ["25/06/2021", "Liverpool", "Tottenham"]
        self.result = None
        # variables
        self.data = pd.read_csv('data.csv')
        self.nodes = list(self.data.columns)
        print(self.nodes)

    def prediction(self):
        model = BayesianModel([self.nodes])




def main():
    predict_app = ProbApp()
    predict_app.prediction()

if __name__ == "__main__":
    main()
