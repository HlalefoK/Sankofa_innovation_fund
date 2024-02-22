import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS form_data ( 
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   category TEXT,
                   business_stage TEXT,
                   years INTEGER,
                   revenue INTEGER,
                   email TEXT,
                   company_name TEXT,
                   contact TEXT,
                   team INTEGER,
                   description TEXT,
                   funding INTEGER,
                   file_path TEXT)
                   ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        category = request.form['category']
        business_stage = request.form['business_stage']
        years = int(request.form['years'])
        revenue = int(request.form['revenue'])
        email = request.form['email']
        company_name = request.form['company_name']
        contact = request.form['contact']
        team = int(request.form['team'])
        description = request.form['description']
        funding = int(request.form['funding'])
        
        file = request.files['documents']
        if file:
            file_path = 'uploads/' + file.filename
            file.save(file_path)
        else:
            file_path = None

        connection = sqlite3.connect('form_data.db')
        cursor = connection.cursor()

        query = """INSERT INTO form_data 
        (category, business_stage, years, revenue, email, company_name, contact, team, description, funding, file_path) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?);
        """
        values = (category, business_stage, years, revenue, email, company_name, contact, team, description, funding, file_path)
        cursor.execute(query, values)
        connection.commit()
        connection.close()

        # # Create or load an existing Excel workbook
        # workbook = openpyxl.load_workbook('form_data.xlsx')

        # # Select the worksheet where you want to store the data (create if it doesn't exist)
        # if 'Form Data' in workbook.sheetnames:
        #     sheet = workbook['Form Data']
        # else:
        #     sheet = workbook.create_sheet(title='Form Data')

        #     # Add headers if the sheet is newly created
        #     headers = ['Category', 'Business Stage', 'Years', 'Revenue', 'Email', 'Company Name', 'Contact', 'Team', 'Description', 'Funding']
        #     sheet.append(headers)

        # # Append form data to the Excel sheet
        # data = [category, business_stage, years, revenue, email, company_name, contact, team, description, funding]
        # sheet.append(data)

        # # Save the workbook
        # workbook.save('form_data.xlsx')

        # Redirect to a thank you page
        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
