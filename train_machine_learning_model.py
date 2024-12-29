import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score

def get_model_accuracy(combined_data):
    """
    @Args:- combined_data:- dataframe object that contains the columns of both stock data and sentiment data
                            (Date, Close, High, Low, Volume, date, neg, neu, pos)
    @Description:-
                This method does the following:-
                i. calculates new features,
                ii. prepares feature and target variables
                iii. Scales and normalizes feature variable values
                iv. Uses RidgeCV model to train the model with training data
                v. Calculates metrics(Cross Validation-R2, R2, MAE)
    @Returns:- cv_scores, mae, r2 - float model metrics
    """

    # Calculate daily returns
    combined_data['daily_return'] = combined_data['Close'].pct_change()

    # Calculate moving averages
    combined_data['SMA_5'] = combined_data['Close'].rolling(window=5).mean()
    combined_data['SMA_20'] = combined_data['Close'].rolling(window=20).mean()

    # Calculate RSI (14-day)
    delta = combined_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    combined_data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD
    ema_12 = combined_data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = combined_data['Close'].ewm(span=26, adjust=False).mean()
    combined_data['MACD'] = ema_12 - ema_26

    # Calculate ATR (14-day)
    high_low = combined_data['High'] - combined_data['Low']
    high_close = abs(combined_data['High'] - combined_data['Close'].shift())
    low_close = abs(combined_data['Low'] - combined_data['Close'].shift())
    tr = high_low.combine(high_close, max).combine(low_close, max)
    combined_data['ATR'] = tr.rolling(window=14).mean()

    # Calculate average volume over a specified period
    combined_data['avg_volume_5'] = combined_data['Volume'].rolling(window=5).mean()

    # Lagged features
    combined_data['prev_close'] = combined_data['Close'].shift(1)

    # Prepare target variable
    combined_data['target'] = combined_data['Close'].shift(-1)

    # Drop NaN values created by rolling calculations
    combined_data.dropna(inplace=True)
    print(combined_data)

    # Prepare features and target variable
    X = combined_data[['neg', 'neu', 'pos', 'daily_return', 'SMA_5', 'SMA_20', 'RSI', 'MACD', 'ATR', 'avg_volume_5', 'prev_close']]
    y = combined_data['target']

    # Impute missing values using mean strategy (if any remain)
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Split the dataset into training and testing sest
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Use Linear Regression - method that studies the relationship between two variables and is used to predict the value of one variable wrt another.
    # Train Ridge Regression model with cross-validation for hyperparameter tuning
    model = RidgeCV(alphas=np.logspace(-6, 6, 13), store_cv_values=True)
    model.fit(X_train, y_train)

    # Evaluate the model using cross-validation on the entire dataset for R-squared
    # Cross validated R-square:- is a statistical measure that rates the model against new or unseen data
    cv_scores = cross_val_score(model, X_imputed, y, cv=5)
    print(f"Cross-validated R-squared: {cv_scores.mean():.2f}")

    # Evaluate the model on the test set
    y_pred = model.predict(X_test)

    # Calculate performance metrics
    # Mean absolute error:- is a statistical measure used to compute the differences between actual and predicted values
    mae = mean_absolute_error(y_test, y_pred)

    # R-squared value:- R-squared, also known as the coefficient of determination, measures the proportion of variance in the dependent variable that can be explained by the independent variables in a regression model. It ranges from 0 to 1, where:
    # 0 indicates that the model does not explain any variability in the target variable.
    # 1 indicates that the model perfectly explains all variability.
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R-squared: {r2:.2f}")

    return cv_scores, mae, r2