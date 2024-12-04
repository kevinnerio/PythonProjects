import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse

def connect_to_db(host, database, user, password):
    """Connect to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return connection
    except Error as e:
        print(f"Failed to connect to database: {e}")
        return None

def query_db(connection, query):
    """Execute a query on the database."""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Error as e:
        print(f"Failed to execute query: {e}")
        return None

def get_wordpress_multisite_posts(connection, search_string):
    """Query WordPress multisite database for posts containing a specific string."""
    query = """
        SELECT 
            wp_blogs.blog_id, 
            wp_blogs.domain AS sitename, 
            wp_posts.ID AS post_id, 
            wp_posts.post_content, 
            CONCAT('https://', wp_blogs.domain, wp_posts.post_name) AS page_url
        FROM 
            wp_blogs
        JOIN 
            wp_posts ON wp_blogs.blog_id = wp_posts.blog_id
        WHERE 
            wp_posts.post_content LIKE %s
    """
    search_string = f"%{search_string}%"
    results = query_db(connection, query, (search_string,))
    return results

def main():
    # Database connection details
    host = input("Enter RDS endpoint host: ")
    database = input("Enter database name: ")
    user = input("Enter username: ")
    password = input("Enter password: ")

    connection = connect_to_db(host, database, user, password)
    if connection:
        search_string = input("Enter the string to search for: ")
        results = get_wordpress_multisite_posts(connection, search_string)
        if results:
            for result in results:
                print("Blog ID:", result['blog_id'])
                print("Site Name:", result['sitename'])
                print("Post ID:", result['post_id'])
                print("Post Content:", result['post_content'])
                print("Page URL:", result['page_url'])
                print("------------------------")
        else:
            print("No results found.")
        connection.close()
    else:
        print("Failed to connect to database.")

if __name__ == "__main__":
    main()