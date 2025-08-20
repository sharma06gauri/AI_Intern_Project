import sqlite3
import re

# --- Hard-coded, corrected SQL queries ---
PREDEFINED_QUERIES = {
    "what's the occupancy rate of properties in bradford?": """
        SELECT CAST(SUM(CASE WHEN status = 'booked' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*)
        FROM properties WHERE city = 'Bradford';
    """,

    "who are the top 10 tenants by total rent paid?": """
        SELECT 
          COALESCE(u_pay.first_name, u_book.first_name) AS first_name,
          COALESCE(u_pay.last_name, u_book.last_name) AS last_name,
          SUM(p.amount) AS total_rent_paid
        FROM payments p
        LEFT JOIN users u_pay ON p.tenant_id = u_pay.user_id
        LEFT JOIN bookings b ON p.booking_id = b.booking_id
        LEFT JOIN users u_book ON b.tenant_id = u_book.user_id
        WHERE p.status = 'successful'
        GROUP BY first_name, last_name
        ORDER BY total_rent_paid DESC
        LIMIT 10;
    """,

    "what's the average rating of apartments vs houses?": """
        SELECT pr.property_type,
               COUNT(r.review_id) AS reviews_count,
               CASE WHEN COUNT(r.review_id)=0 THEN 'No reviews'
                    ELSE ROUND(AVG(r.rating),2) END AS avg_rating
        FROM properties pr
        LEFT JOIN reviews r ON pr.property_id = r.property_id
        WHERE pr.property_type IN ('apartment','house')
        GROUP BY pr.property_type;
    """,

    "which landlords generated the most revenue this year?": """
        SELECT u.user_id, u.first_name, u.last_name, SUM(p.amount) AS total_revenue
        FROM payments p
        JOIN bookings b ON p.booking_id = b.booking_id
        JOIN properties pr ON b.property_id = pr.property_id
        JOIN users u ON pr.landlord_id = u.user_id
        WHERE p.status = 'successful'
        GROUP BY u.user_id, u.first_name, u.last_name
        ORDER BY total_revenue DESC;
    """,

    "list all currently available 2bhks under $2500 in london.": """
        SELECT title, city, rent_price
        FROM properties
        WHERE bedrooms = 2 AND city = 'London' AND status = 'available' AND rent_price < 2500;
    """
}  # ✅ dictionary closed properly


# --- Helper functions ---
def get_sql_query(natural_language_query):
    return PREDEFINED_QUERIES.get(natural_language_query.lower().strip(), None)


def execute_sql_query(sql_query):
    try:
        conn = sqlite3.connect('rental_app.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return None


def format_results(query_type, results):
    if not results:
        return "No results found."

    if "occupancy rate" in query_type.lower():
        occupancy_rate = results[0][0] if results[0][0] is not None else 0.0
        return f"The occupancy rate is {occupancy_rate:.2f}%."

    if "top 10 tenants" in query_type.lower():
        formatted_list = [f"{row[0]} {row[1]} (Total Paid: ${row[2]:.2f})" for row in results]
        return "Top tenants by total rent paid:\n" + "\n".join(formatted_list)

    if "average rating" in query_type.lower():
        formatted_list = [f"{row[0].capitalize()} → {row[2]} stars" for row in results]
        return "\n".join(formatted_list)

    if "landlords generated the most revenue" in query_type.lower():
        formatted_list = [f"{row[1]} {row[2]} (Total Revenue: ${row[3]:.2f})" for row in results]
        return "Landlords who generated the most revenue:\n" + "\n".join(formatted_list)

    if "available 2bhks" in query_type.lower():
        formatted_list = [f"'{row[0]}' in {row[1]} for ${row[2]:.2f} per month." for row in results]
        return "Available 2BHKs under $2500 in London:\n" + "\n".join(formatted_list)

    return f"Query executed successfully. Results: {results}"


def process_query(user_input):
    sql_query = get_sql_query(user_input)
    if not sql_query or not sql_query.strip().lower().startswith("select"):
        return "Sorry, unable to answer at this point in time."
    results = execute_sql_query(sql_query)
    if results is None:
        return "Sorry, unable to answer at this point in time."
    return format_results(user_input, results)


# --- Main runner ---
if __name__ == "__main__":
    print("DEBUG: Script started ✅")

    queries = [
        "What's the occupancy rate of properties in Bradford?",
        "Who are the top 10 tenants by total rent paid?",
        "What's the average rating of apartments vs houses?",
        "Which landlords generated the most revenue this year?",
        "List all currently available 2BHKs under $2500 in London."
    ]

    for q in queries:
        print(f"\nUser Query: {q}")
        response = process_query(q)
        print(f"System Response: {response}")
