import sqlite3

def setup_database():
    conn = sqlite3.connect('rental_app.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS favorites;")
    cursor.execute("DROP TABLE IF EXISTS property_photos;")
    cursor.execute("DROP TABLE IF EXISTS reviews;")
    cursor.execute("DROP TABLE IF EXISTS payments;")
    cursor.execute("DROP TABLE IF EXISTS bookings;")
    cursor.execute("DROP TABLE IF EXISTS properties;")
    cursor.execute("DROP TABLE IF EXISTS users;")

    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR,
            email VARCHAR UNIQUE,
            phone VARCHAR,
            role TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE properties (
            property_id INTEGER PRIMARY KEY,
            landlord_id INTEGER,
            title VARCHAR,
            description TEXT,
            property_type TEXT,
            address VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR,
            bedrooms INTEGER,
            bathrooms INTEGER,
            rent_price DECIMAL(12,2),
            status TEXT,
            listed_at TIMESTAMP,
            FOREIGN KEY (landlord_id) REFERENCES users(user_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE bookings (
            booking_id INTEGER PRIMARY KEY,
            property_id INTEGER,
            tenant_id INTEGER,
            start_date DATE,
            end_date DATE,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(property_id),
            FOREIGN KEY (tenant_id) REFERENCES users(user_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE payments (
            payment_id INTEGER PRIMARY KEY,
            booking_id INTEGER,
            tenant_id INTEGER,
            amount DECIMAL(12,2),
            payment_date DATE,
            status TEXT,
            method TEXT,
            FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
            FOREIGN KEY (tenant_id) REFERENCES users(user_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE reviews (
            review_id INTEGER PRIMARY KEY,
            property_id INTEGER,
            tenant_id INTEGER,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(property_id),
            FOREIGN KEY (tenant_id) REFERENCES users(user_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE property_photos (
            photo_id INTEGER PRIMARY KEY,
            property_id INTEGER,
            photo_url VARCHAR,
            uploaded_at TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(property_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE favorites (
            tenant_id INTEGER,
            property_id INTEGER,
            added_at TIMESTAMP,
            PRIMARY KEY (tenant_id, property_id),
            FOREIGN KEY (tenant_id) REFERENCES users(user_id),
            FOREIGN KEY (property_id) REFERENCES properties(property_id)
        );
    """)

    # --- Sample data to support all queries ---
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, role) VALUES (1, 'Alice', 'Smith', 'landlord');")
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, role) VALUES (2, 'Bob', 'Johnson', 'tenant');")
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, role) VALUES (3, 'Charlie', 'Williams', 'landlord');")
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, role) VALUES (4, 'David', 'Brown', 'tenant');")

    cursor.execute("INSERT INTO properties (property_id, landlord_id, title, city, property_type, rent_price, status, bedrooms) VALUES (101, 1, 'Cozy Apartment', 'London', 'apartment', 1500.00, 'booked', 1);")
    cursor.execute("INSERT INTO properties (property_id, landlord_id, title, city, property_type, rent_price, status, bedrooms) VALUES (102, 1, 'Spacious House', 'Bradford', 'house', 2200.00, 'booked', 3);")
    cursor.execute("INSERT INTO properties (property_id, landlord_id, title, city, property_type, rent_price, status, bedrooms) VALUES (103, 3, 'Riverside Studio', 'London', 'studio', 1100.00, 'available', 1);")
    cursor.execute("INSERT INTO properties (property_id, landlord_id, title, city, property_type, rent_price, status, bedrooms) VALUES (104, 3, 'Modern Apartment', 'London', 'apartment', 2400.00, 'available', 2);")
    cursor.execute("INSERT INTO properties (property_id, landlord_id, title, city, property_type, rent_price, status, bedrooms) VALUES (105, 1, 'Luxury Apartment', 'London', 'apartment', 2200.00, 'available', 2);")

    # Bookings that will generate revenue for landlords
    cursor.execute("INSERT INTO bookings (booking_id, property_id, tenant_id, status, start_date, end_date) VALUES (1001, 101, 2, 'completed', '2024-05-01', '2024-06-01');")
    cursor.execute("INSERT INTO bookings (booking_id, property_id, tenant_id, status, start_date, end_date) VALUES (1002, 102, 2, 'completed', '2024-08-01', '2024-08-15');")
    cursor.execute("INSERT INTO bookings (booking_id, property_id, tenant_id, status, start_date, end_date) VALUES (1003, 104, 4, 'completed', '2024-07-01', '2024-07-31');")

    # Payments for the above bookings
    cursor.execute("INSERT INTO payments (payment_id, booking_id, tenant_id, amount, payment_date, status) VALUES (2001, 1001, 2, 1500.00, '2024-05-01', 'successful');")
    cursor.execute("INSERT INTO payments (payment_id, booking_id, tenant_id, amount, payment_date, status) VALUES (2002, 1002, 2, 2200.00, '2024-08-01', 'successful');")
    cursor.execute("INSERT INTO payments (payment_id, booking_id, tenant_id, amount, payment_date, status) VALUES (2003, 1003, 4, 2400.00, '2024-07-01', 'successful');")

    # Reviews
    cursor.execute("INSERT INTO reviews (review_id, property_id, tenant_id, rating, comment) VALUES (3001, 102, 2, 5, 'Great house, very clean.');")
    cursor.execute("INSERT INTO reviews (review_id, property_id, tenant_id, rating, comment) VALUES (3002, 101, 2, 4, 'Nice location, good service.');")
    cursor.execute("INSERT INTO reviews (review_id, property_id, tenant_id, rating, comment) VALUES (3003, 103, 2, 4, 'Awesome.');")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
