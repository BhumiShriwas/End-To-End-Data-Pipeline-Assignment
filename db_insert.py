from sql.db_utils import get_connection

def insert_books(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO books
            (title, price, rating, availability, category, price_category, book_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['title'],
            row['price'],
            row['rating'],
            row['availability'],
            row['category'],
            row['price_category'],
            row['book_url']
        ))

    conn.commit()
    conn.close()
