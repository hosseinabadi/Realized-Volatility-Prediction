from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

'''
Plot the ACF and PACF of a time series
'''


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

    plt.savefig(f"Outputs/Models/GARCH/{column}_acf_pacf.png")
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


# %%
def calculate_aic_bic(y_true, y_pred, num_predictors, num_samples):
    # Calculate RSS
    rss = np.sum((y_true - y_pred) ** 2)

    # Estimate the variance of the error
    sigma_squared = rss / num_samples

    # Calculate the likelihood
    likelihood = np.prod(1 / np.sqrt(2 * np.pi * sigma_squared) * np.exp(-(y_true - y_pred) ** 2 / (2 * sigma_squared)))

    # Calculate AIC
    aic = 2 * num_predictors - 2 * np.log(likelihood)

    # Calculate BIC
    bic = num_samples * np.log(rss / num_samples) + num_predictors * np.log(num_samples)

    return aic, bic


# %%
def calculate_cp(y_true, y_pred, num_predictors, num_samples):
    # Calculate RSS
    rss = np.sum((y_true - y_pred) ** 2)

    # Estimate the variance of the error
    sigma_squared = rss / (num_samples - num_predictors - 1)

    # Calculate C_p
    cp = (1 / num_samples) * (rss + 2 * num_predictors * sigma_squared)

    return cp


# %%
def calculate_adjusted_r2(y_true, y_pred, num_predictors, num_samples):
    # Calculate R^2
    r2 = r2_score(y_true, y_pred)

    # Calculate adjusted R^2
    adjusted_r2 = 1 - (1 - r2) * ((num_samples - 1) / (num_samples - num_predictors - 1))

    return adjusted_r2


def mean_percentage_error(actual, predicted):
    """
    Calculate Mean Percentage Error (MPE).

    Parameters:
    actual (list): List of actual values.
    predicted (list): List of predicted values.

    Returns:
    float: Mean Percentage Error (MPE).
    """
    # Calculate absolute percentage error for each pair of actual and predicted values
    absolute_percentage_error = [abs((actual_val - pred_val) / actual_val) for actual_val, pred_val in
                                 zip(actual, predicted)]

    # Calculate mean of absolute percentage error
    mpe = sum(absolute_percentage_error) / len(absolute_percentage_error)

    return mpe
