from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
from scipy.stats import skew, kurtosis, norm, shapiro
import seaborn as sns
from scipy import stats


def check_t_distribution(std_resid):
    # Fit a t-distribution to the standardized residuals
    t_params = stats.t.fit(std_resid)

    # Perform Kolmogorov-Smirnov test
    ks_stat, p_value = stats.kstest(std_resid, 't', t_params)

    print(f"KS-statistic: {ks_stat}")
    print(f"P-value: {p_value}")

    # If the p-value is greater than 0.05, we cannot reject the null hypothesis that the data follows a t-distribution
    if p_value > 0.05:
        print("The standardized residuals could be from a t-distribution.")
    else:
        print("The standardized residuals are not from a t-distribution.")


def check_normality(data):
    skewness = skew(data)
    kurt = kurtosis(data)

    # 2. Visualize the distribution and plot the PDF of the normal distribution
    plt.figure(figsize=(10, 6))

    # Plot the data's PDF
    sns.histplot(data, kde=True, color='blue', bins=30, stat='probability', label='Data PDF')

    # Generate normal distribution data with the same mean and standard deviation
    mu, sigma = data.mean(), data.std()
    x = np.linspace(data.min(), data.max(), 1000)
    pdf = norm.pdf(x, mu, sigma)  # Calculate the PDF of the normal distribution
    # Normalize the PDF

    # 3. Perform normality tests
    shapiro_test = shapiro(data)
    p_value = shapiro_test[1]

    # Print results
    print(f"Skewness: {skewness}", "Skewness of a normal distribution is 0.")
    print(f"Kurtosis: {kurt}", "Kurtosis of a normal distribution is 3.")
    print(f"Shapiro-Wilk Test p-value: {p_value}")

    # Assess normality based on p-value
    if p_value > 0.05:
        print("The data could be assumed to be approximately normally distributed.")
    else:
        print("The data significantly deviates from a normal distribution.")

    # Plot the normal distribution's PDF
    plt.plot(x, pdf, 'r', label='Normal Distribution')

    plt.title('Distribution of Data with Normal Distribution')
    plt.xlabel('Values')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.show()


def plot_autocorrelations(columns, series_list, lags=30):
    num_cols = len(columns)
    fig, axes = plt.subplots(num_cols, 2, figsize=(15, 5 * num_cols))

    if num_cols == 1:
        axes = np.expand_dims(axes, axis=0)

    for i, column in enumerate(columns):
        # Plot autocorrelation
        plot_acf(series_list[i], lags=lags, ax=axes[i, 0])
        axes[i, 0].set_title(f'Autocorrelation of {column}')

        # Plot partial autocorrelation
        plot_pacf(series_list[i], lags=lags, ax=axes[i, 1])
        axes[i, 1].set_title(f'Partial Autocorrelation of {column}')

    plt.tight_layout()
    plt.show()


# Assuming 'data' is your DataFrame and 'return' is the column you want to test
def stationarity_test(data):
    result = adfuller(data)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))


def transform_to_float(df):
    for column in df.columns:
        df[column] = df[column].astype(float)


def Ljung_Box_Test(data, lags):
    result = sm.stats.acorr_ljungbox(data, lags=lags, return_df=True)
    return result
