from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

def get_model_accuracy(combined_data):
    """
    @Args:- combined_data: Dataframe object that contains stock and sentiment grouped data
    @Description:-
                This method trains the model using combined_data and returns the accuracy score
    @Returns:- accuracy_score:- float score rating the model
    """

    # Create target variable: Up (1) or Down (0)
    combined_data['target'] = (combined_data['Close'].shift(-1) > combined_data['Close']).astype(int)

    # Prepare features and target variable
    X = combined_data[['neg', 'neu', 'pos']] # Use sentiment scores as features
    y = combined_data['target']

    # Drop the last row to avoid NaN in target variable due to shifting
    X = X[:-1]
    y = y[:-1]

    # Ensure y is a one-dimensional array
    y = y.values.flatten()  # or use y = y.values.ravel()

    # Check shapes before proceeding
    print("Shape of X:", X.shape)
    print("Shape of y:", y.shape)

    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=42)

    # Train Random Forest Classifier
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    accuracy = model.score(y_test, y_pred)
    print(f"{accuracy:.2f}")
    return accuracy