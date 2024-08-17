Daily Realized Volatility Prediction of SP500 Index (SPX)
====================

This project focuses on predicting the daily realized volatility of the S&P 500 Index using various econometric and machine learning models. The research explores the effectiveness of traditional models, such as GARCH and VAR, compared to more advanced machine learning techniques, including LSTM and RNN.

### Key Components

- **Data Collection and Preprocessing**: The dataset combines daily data and macrofinancial indicators, alongside sentiment analysis of financial news headlines related to S&P 500 companies.
  
- **Model Development**: Univariate and multivariate models were developed, including GARCH, VAR, Linear Regression, Ridge, Lasso, Random Forest, XGBoost, Simple RNN, and LSTM. The models were trained and tested using robust evaluation metrics like **R²**, **RMSE**, **MAE**, and **MAPE**.

- **Sentiment Analysis**: The project incorporates sentiment scores derived from the VADER model applied to news headlines, enhancing the predictive power of the models.

- **Results and Comparison**: The project systematically compares the out-of-sample forecasting performance of the models, highlighting the superior performance of LSTM in capturing complex temporal patterns in financial time series data.

This research provides valuable insights into the application of machine learning in finance, particularly in volatility forecasting, and demonstrates the potential of integrating sentiment analysis with traditional financial modeling techniques.

#### Requirements:
```
The requirements are inside the requirements.txt file.
```

This project can be sub-divided into these main parts:
1. Download Market Capitalization data from CRSP, sourced from Wharton 
2. Download indicators
3. Sentimental Analysis
4. Models

## Download Data
Data was downloaded from these websites:
* __CRSP__ was used for Market Capitalization of SP500 and the first 50 firms of the index
* __Yahoo Finance__ was used for Indicators
* __Economic Policy Uncertainty__ was used for indicators

## Sentimental Analysis
The sentimental analysis can be divided into these main passages:
1. Scrap all information regarding SP500 from Wikipedia. Subsequently, scrap all news from [Business Market Insider](https://markets.businessinsider.com/). Everything is done in [scraper.py](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Sentiment%20Analysis/scraper.py)
2. Run the sentiment on all scraped headlines using [sentimental.py](https://github.com/hosseinabadi/Realized-Volatility-Prediction/tree/master/Sentiment%20Analysis)
3. Plots and analysis of of data scraped in the parts above in [plots_SP500.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Sentiment%20Analysis/plots_SP500.ipynb)
4. Analysis sentimental scores in [sentimental_and_plots.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Sentiment%20Analysis/sentimental_and_plots.ipynb)
5. Computation of extra weight which will be given to the first 50 firms of the SP500. Code is visible in [market_capitalization_weights.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Sentiment%20Analysis/market_capitalization_weights.ipynb)
6. Adjust sentiment scores taking into account the weights computed previously. Run [compute_weighted_sentiments.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Sentiment%20Analysis/compute_weighted_sentiments.ipynb)

Due to GitHub's storage limitations, some CSV files which were used cannot be uploaded. However, they can still be visualized [here](https://drive.google.com/drive/folders/1W8QDA1jgOxivhFTOHspg3MQxtIqEm2Ha?usp=drive_link).

In order to not encounter any problems with the codes, they have to be saved in a Directory called ```Data```. For instance, the CSV file ```sp500_news_and_sentimental.csv``` must be present in ```Data\sp500_news_and_sentimental.csv```, as well as all the other CSV files.

## Model Implementation
Before running financial econometrics and ML's models, we need to scrap financial data from online and to subsequently merge it with the data from Oxford-Man Institute’s and TwelveData. All steps can be visualized in [RV dataset.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/RV%20dataset.ipynb). Then, data analysis is computed in [Data Analysis and Visualization.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Data%20Analysis%20and%20Visualization.ipynb)

Now, after data analysis was done, we ran the models:
1. Regression models: Linear, Lasso, Ridge. Code can be visualized in [Regression.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Regression.ipynb).
2. Financial econometrics models (GARCH and VAR), with the testing of all their assumptions. The code can be found in [GARCH_VAR.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/GARCH_VAR.ipynb)
3. Lastly, ML models (Random Forest, XGBoost, RNN, LSTM) were executed in [ML models.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/ML%20models.ipynb).

All model results can be observed in [Results.ipynb](https://github.com/hosseinabadi/Realized-Volatility-Prediction/blob/master/Results.ipynb).

## Questions
For any question and/or curiosity, feel free to reach
* [Valentin Aolaritei](mailto:valentin.aolaritei@epfl.ch)
* [Alberto De Laurentis](mailto:alberto.delaurentis@epfl.ch)
* [Amirmahdi Hosseinabadi](mailto:amirmahdi.hosseinabadi@epfl.ch)
