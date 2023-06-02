from flask import Flask, render_template, request
# import mysql.connector
import csv
import matplotlib.pyplot as plt
import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('sell.html')
# @app.route('/show')
# def show():
#     # Connect to the database
#     cnx = mysql.connector.connect(user='root', password='root',
#                               host='localhost',
#                               database='mydatabase')
#     cursor = cnx.cursor()

#     # Fetch data from the database
#     cursor.execute("SELECT * FROM customers")
#     data = cursor.fetchall()

#     # Render the HTML template with the data
#     return render_template('home.html', data=data)


@app.route('/Submit', methods=['POST'])
def save_data():
    data1 = request.form['name']
    data2 = request.form['email']
    data3 = request.form['phone']
    data4 = request.form['Manufacturer']
    data5 = request.form['model']
    data6 = request.form['year']
    data7 = request.form['price']
    data8 = request.form['fuel']
    data9 = request.form['Mileage']
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data1, data2, data3, data4, data5, data6, data7, data8, data9])
    return 'Your data saved successfully! We will inform when there is a customer interested in your Car!'



@app.route('/chart')
def index():
    # Read the data from the CSV file
    data = []
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    # Extract the Fuel Type column from the data
    fuel_data = [row[7] for row in data[1:]]

    # Calculate the frequency of each Fuel Type value
    fuel_freq = {}
    for fuel_type in fuel_data:
        if fuel_type in fuel_freq:
            fuel_freq[fuel_type] += 1
        else:
            fuel_freq[fuel_type] = 1

    # Plot a pie chart for Fuel Type
    fuel_labels = list(fuel_freq.keys())
    fuel_sizes = list(fuel_freq.values())
    plt.pie(fuel_sizes, labels=fuel_labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Fuel Type Distribution')
    plt.savefig('static/fuel_pie_chart.png')

    # Extract the Manufacturer column from the data
    manufacturer_data = [row[3] for row in data[1:]]

    # Calculate the frequency of each Manufacturer value
    manufacturer_freq = {}
    for manufacturer in manufacturer_data:
        if manufacturer in manufacturer_freq:
            manufacturer_freq[manufacturer] += 1
        else:
            manufacturer_freq[manufacturer] = 1

    # Plot a pie chart for Manufacturer
    manufacturer_labels = list(manufacturer_freq.keys())
    manufacturer_sizes = list(manufacturer_freq.values())
    plt.pie(manufacturer_sizes, labels=manufacturer_labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Manufacturer Distribution')
    plt.savefig('static/manufacturer_pie_chart.png')
    
    year_data = [row[5] for row in data[1:]]

# Calculate the frequency of each Year value
    year_freq = {}
    for year in year_data:
        if year in year_freq:
            year_freq[year] += 1
        else:
            year_freq[year] = 1

    # Plot a pie chart for Year
    year_labels = list(year_freq.keys())
    year_sizes = list(year_freq.values())
    plt.pie(year_sizes, labels=year_labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Year Distribution')
    plt.savefig('static/year_pie_chart.png')


        # Render the template with the pie chart image file paths
    return render_template('chart.html', fuel_image_file='static/fuel_pie_chart.png',
                            manufacturer_image_file='static/manufacturer_pie_chart.png', year_image_file='static/year_pie_chart.png')

    
    


@app.route('/faq')
def faq():
    return render_template('faq.html')
def chatbot_response(message):
    var_time = time.ctime()
    qna = {
        "What is the business model of carpoint?":"We at CarPoint believe in changing the way people sell their cars in India by simplifying and standardizing the entire process.",
        "How do I book an appointment?":"It’s simple! Log on to our website www.CarPoint.com, fill the form and we will inform you when there is any customer interested in your car.",
        "what is your name?" : "My name is ChatBot",
        "What is your name?" : "My name is ChatBot",
        "how are you?" : "I'am Fine, what about you",
        "what is the time now?" : var_time,
        "Is there an accident history?":"Sorry! We can't provide you any accident history.",
        
        
    }

    return qna.get(message, "I'm sorry, I didn't understand that.")
@app.route('/faq', methods=['POST'])
def get_bot_response():
    user_message = request.form['message']
    bot_response = chatbot_response(user_message)
    return render_template('faq.html', message=user_message, response=bot_response)

@app.route('/car_data')
def display_table():
    data = []
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return render_template('car_data.html', data=data)

       
        

 

if __name__ == '__main__':
    app.run(debug=False)
    