import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

def load_books_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="YOUR_DATABASE"
    )

    query = """
    SELECT book_id, title, rating, availability, category, price_category
    FROM books
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df
def create_features(df):
    df = df.copy()

    df["title_length"] = df["title"].apply(len)

    le = LabelEncoder()
    df["category_encoded"] = le.fit_transform(df["category"])

    df["availability_encoded"] = df["availability"].apply(
        lambda x: 1 if "in stock" in x else 0
    )

    X = df[["rating", "title_length", "category_encoded", "availability_encoded"]]
    y = df["price_category"]

    return X, y, df["book_id"]
def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred, average="weighted"))

    return model, X_test.index, y_test, y_pred
def save_predictions(book_ids, y_true, y_pred):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="YOUR_DATABASE"
    )
    cursor = conn.cursor()

    for bid, actual, pred in zip(book_ids, y_true, y_pred):
        cursor.execute("""
            INSERT INTO model_predictions
            (book_id, actual_category, predicted_category, model_name)
            VALUES (%s, %s, %s, %s)
        """, (int(bid), actual, pred, "RandomForest"))

    conn.commit()
    conn.close()
    if __name__ == "__main__":
       df = load_books_from_db()
       X, y, book_ids = create_features(df)

       model, test_idx, y_test, y_pred = train_and_evaluate(X, y)

       save_predictions(book_ids.loc[test_idx], y_test, y_pred)



