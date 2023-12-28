from flask import Flask, render_template, request, send_file
import pandas as pd 
from datetime import date
import openpyxl
from io import BytesIO


app = Flask(__name__)

@app.route("/")
def salary_app():
    return render_template("index.html", status = "", salary="", year = date.today().year)

@app.route('/process_amount', methods=['POST'])
def process_amount():
    # Access the submitted data from the HTML form
    
    amount = request.form['amount']
    bincome = 'bincome' in request.form
    bexpense = 'bexpense' in request.form
    bmakeup = 'bmakeup' in request.form
    best = 'best' in request.form
    bbar = 'bbar' in request.form
    
    status = enter_amount(amount, bincome, bmakeup, best, bbar)
    
    # Redirect or render another template as needed
    return render_template("index.html", status = status, salary="", year = date.today().year)

@app.route('/process_salary', methods=['POST'])
def process_salary():
    # Access the submitted data from the HTML form
    bnet = 'bnet' in request.form
    bgross = 'bgross' in request.form
    year = request.form['year']
    
    salary = calc_salary(bnet, bgross, year)
    
    # Redirect or render another template as needed
    return render_template("index.html", status = "", salary=salary, year = date.today().year)

@app.route('/display_data')
def display_data():
    # Read data from the Excel file
    workbook = openpyxl.load_workbook('salary_data.xlsx')
    try:
        sheet = workbook['Sheet1']
    except:
        sheet = workbook['Sheet']

    # Get header and data
    header = [cell.value for cell in sheet[1]]
    header = header[1:]
    data = [[cell.value for cell in row][1:] for row in sheet.iter_rows(min_row=2)]

    return render_template('table.html', header=header, data=data)

@app.route('/remove_rows', methods=['POST'])
def remove_rows():
    # Get the list of row indices to remove from the request
    rows_to_remove = request.json.get('rowsToRemove', [])

    # Read data from the Excel file
    workbook = openpyxl.load_workbook('salary_data.xlsx')
    try:
        sheet = workbook['Sheet1']
    except:
        sheet = workbook['Sheet']

    # Remove selected rows
    for i in reversed(rows_to_remove):
        sheet.delete_rows(i + 2)  # Adding 2 to account for 1-based index and header row

    # Save the updated workbook
    updated_data = BytesIO()
    workbook.save(updated_data)
    updated_data.seek(0)

    return send_file(updated_data, download_name='salary_data.xlsx', as_attachment=True,  mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download_excel', methods=['POST'])
def download_excel():
    # Get the data from the request
    data = request.json.get('data', [])
    print(request.json.get('data', []))
    # Create a new workbook and write the data to it
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write header
    header = data[0]
    sheet.append(header)

    # Write data
    for row_data in data[1:]:
        sheet.append(row_data)

    # Save the workbook to a BytesIO object
    updated_data = BytesIO()
    workbook.save(updated_data)
    updated_data.seek(0)

    # Send the file in the response
    return send_file(updated_data, download_name='salary_data.xlsx', as_attachment=True,  mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

def enter_amount(amount, bincome, bmakeup, best, bbar):
        
    if not amount:
        return ""

    amount = float(amount)
    salary_df = pd.read_excel('salary_data.xlsx')

    try:
        salary_df.drop(columns={'Unnamed: 0'}, inplace=True)
    except:
        pass

    if not bincome:
        amount = amount*-1

    salary_dict = {'entries': [0], 'makeup': [0], 'bartending': [0], 'esthetician': [0], 'year': [0]}
    if bmakeup:
        salary_dict['makeup'] = [amount]
    elif bbar:
        salary_dict['bartending'] = [amount]
    elif best:
        salary_dict['esthetician'] = [amount]

    salary_dict['year'] = date.today().year
    salary_dict['entries'] = len(salary_df)

    new_df = pd.DataFrame(salary_dict)
    salary_df = pd.concat([salary_df, new_df])
    salary_df.reset_index(drop=True, inplace=True)
    salary_df.to_excel('salary_data.xlsx')

    return "Entry Added"

def calc_salary(bnet, bgross, year):
        
    if not year:
        return ""
    
    year = int(year)
    salary_df = pd.read_excel('salary_data.xlsx')

    try:
        salary_df.drop(columns={'Unnamed: 0'}, inplace=True)
    except:
        pass

    if bnet:
        salary_df = salary_df[salary_df['year'] == year]
        salary = salary_df['makeup'].sum() + salary_df['bartending'].sum() + salary_df['esthetician'].sum()
    elif bgross:
        salary_df = salary_df[salary_df['year'] == year]
        salary_df = salary_df[salary_df['makeup'] >= 0]
        salary_df = salary_df[salary_df['bartending'] >= 0]
        salary_df = salary_df[salary_df['esthetician'] >= 0]

        salary = salary_df['makeup'].sum() + salary_df['bartending'].sum() + salary_df['esthetician'].sum()

    return str(salary)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')