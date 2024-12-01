from flask import Flask, request, send_file, render_template_string, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Configure the static folder to serve the logo
app.config['STATIC_FOLDER'] = 'static'

# HTML template for the file upload form
UPLOAD_FORM_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>CSV to Excel Converter</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      
        background-image: url('/static/background1.webp');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
      .container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        text-align: center;
      }
      h1 {
        margin-bottom: 20px;
      }
      input[type="file"] {
        margin-bottom: 10px;
      }
      input[type="submit"] {
        background-color: #007bff;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
      }
      input[type="submit"]:hover {
        background-color: #0056b3;
      }
      img {
        max-width: 150px;
        margin-bottom: 20px;
      }
    </style>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
      <link rel="icon" href="/static/logo-avocarbon-carre.ico" type="image/x-icon">
  </head>
  <body>
    <div class="container">
      <img src="/static/logo-avocarbon (1).png" alt="Logo">
      <h1 style="color: green;"><i class="fas fa-file-csv" style="color: green; vertical-align: middle;"></i> Upload CSV to Convert to Excel<i class="fas fa-file-excel" style="color: green; vertical-align: middle;"></i></h1>
      <form action="/convert" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required><br>
        <input type="submit" value="Convert">
      </form>
    </div>
  </body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(UPLOAD_FORM_HTML)


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        # Read CSV file into a DataFrame
        df = pd.read_csv(file)

        # Save DataFrame to an Excel file
        output_excel_path = "converted_output.xlsx"
        df.to_excel(output_excel_path, index=False)

        # Send the generated Excel file to the user
        return send_file(output_excel_path, as_attachment=True)
    else:
        return "Invalid file type. Please upload a CSV file."


if __name__ == '__main__':
    app.run(debug=True, port=5000)
