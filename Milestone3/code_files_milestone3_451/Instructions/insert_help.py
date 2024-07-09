#This file is supposed to be ran w=after the parser.py
def retrieveTableSizes():
    # Connect to yelpdb database on PostgreSQL server using psycopg2
    # TODO: update the database name, username, and password
    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='none'")
    except:
        print('Unable to connect to the database!')
        return

    cur = conn.cursor()
    table_names = ['businessTable', 'userTable', 'reviewTable']  # Add more table names if needed

    with open('yelpdb_TableSizes.txt', 'w') as outfile:  # Replace <your-name> with your actual name
        for table_name in table_names:
            sql_str = "SELECT COUNT(*) FROM " + table_name + ";"
            cur.execute(sql_str)
            count = cur.fetchone()[0]
            outfile.write(table_name + ": " + str(count) + "\n")

    cur.close()
    conn.close()


# Main program
insert2BusinessTable()
retrieveTableSizes()
