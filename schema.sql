CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(6,2),
    rating INT,
    availability VARCHAR(50),
    category VARCHAR(100),
    price_category ENUM('low', 'medium', 'high'),
    book_url VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category)
);
CREATE TABLE biomarkers (
    geo_id VARCHAR(50) PRIMARY KEY,
    experiment_type VARCHAR(255),
    citations TEXT,
    platforms TEXT,
    samples TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE model_predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    predicted_category ENUM('low', 'medium', 'high'),
    actual_category ENUM('low', 'medium', 'high'),
    model_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    INDEX idx_book_id (book_id)
);

