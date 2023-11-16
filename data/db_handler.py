import http.server as server
import socketserver
import sqlite3

class DBHandler(server.BaseHTTPRequestHandler):

    def do_POST(self):
        '''connects to a database and inserts data from a form'''

        data = self.parseHTTP()
        connection = self.connectToDB()
        db_cursor = connection.cursor()

        # Insert data into the database
        query = """INSERT INTO form_data (category, business_stage, years, revenue, email,
          company_name, contact, team, description, funding) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        business_stage = self.formatDataString(data['business_stage'])
        category = self.formatDataString(data['category'])
        company_name = self.formatDataString(data['company_name'])
        description = self.formatDataString(data['description'])
        email = self.formatDataString(data['email'])
        values = (category, business_stage, int(data['years']), int(data['revenue']), email, company_name, int(data['contact']), data['team'], description, int(data['funding']))

        try:
            db_cursor.execute(query, values)
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Form data successfully submitted', 'utf-8'))

        except Exception as e:
            self.send_error(500, 'Internal Server Error', str(e))

        finally:
            db_cursor.close()
            connection.close()


    def connectToDB(self) -> sqlite3.Connection:
        return sqlite3.connect('form_data.db')


    def parseHTTP(self):
        '''parses HTTP request body and returns a dictionary of form data'''

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = {}

        for item in body.split('&'):
            key, value = item.split('=')
            data[key] = value

        return data
    

    def formatDataString(self, string: str) -> str:
        if "+" not in string:
            return string
        words = string.split("+")
        return " ".join(words)
    

    def createTable(self, cursor: sqlite3.Cursor):
        '''creates a table in the database if it doesn't exist'''

        query = """CREATE TABLE IF NOT EXISTS form_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            business_stage TEXT NOT NULL,
            years INTEGER NOT NULL,
            revenue INTEGER NOT NULL,
            email TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact INTEGER NOT NULL,
            team TEXT NOT NULL,
            description TEXT NOT NULL,
            funding INTEGER NOT NULL
        );"""

        cursor.execute(query)

    def start_server():
        '''starts the server'''

        PORT = 8000
        with socketserver.TCPServer(('127.0.0.1', PORT), DBHandler) as httpd:
            print('Serving at port', PORT)
            httpd.serve_forever()

if __name__ == '__main__':
    DBHandler.start_server()