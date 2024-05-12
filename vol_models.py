import statsmodels
from arch import arch_model
import matplotlib.pyplot as plt


class GARCHModel:
    def __init__(self, p, q, dist='normal'):
        self.p = p
        self.q = q
        self.dist = dist
        self.model = None
        self.result = None
        self.resid = None
        self.conditional_volatility = None

    def fit_garch_model(self, data, disp='final'):
        self.model = arch_model(data, vol='GARCH', p=self.p, q=self.q, dist=self.dist)
        self.result = self.model.fit(disp = disp)
        self.resid = self.result.resid
        self.conditional_volatility = self.result.conditional_volatility

    def plot_results(self):
        print(self.result.summary())
        self.result.plot()
        plt.show()

    def LjungBoxTest_(self):
        return self.result.test('LBQ')

    def EngleArchTest_(self):
        test_result = statsmodels.stats.diagnostic.het_arch(self.resid, nlags=10, store=False, ddof=0)
        print(f"Test results: {test_result}")


def print_hello():
    print("Hello, world!")
