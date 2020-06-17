from flask import Flask, render_template, session, request, redirect, g, url_for, flash
from pymongo import MongoClient
import os
from random import randrange
import smtplib
from unidecode import unidecode
import requests, json


client= MongoClient('localhost',27017)
database = client['Webbanhang']

collection = database['users']
collection_Shop = database['shopdata']
collection_Bill = database['bill']

collection_Cart = database["cart"]
collection_Cart.drop()
collection_Cart = database["cart"]

#Điền thông tin tài khoản admin vào database users
x = 0
admin = { "name" : "admin", "username" : "admin", "password" : "admin", "phone" : "None", "email" : "None"} 
for i in collection.find():
    if i["name"] == admin["name"]:
        x = 1
if x!=1:
    collection.insert_one(admin)
############

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Phần hiển thị chính
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        
        session.pop('search_key', None)
        
        if "search-key" in request.form:
            
            session['search_key'] = request.form['search-key']
            return redirect(url_for("search"))
        
        else:
            if "username" in session and session['username'] != 'admin':
                name = request.form["name"]
                color = request.form["color"]
                price = request.form["price"]
                id = request.form['id']
                
                test_num = 0
                
                for i in collection_Cart.find():
                    if i["name"] == name and i["color"] == color and i["id"] == id:
                        test_num = 1
                
                if test_num == 0:
                    data = {"id":id, "name": name, "color": color, "price": price}
                    collection_Cart.insert_one(data)
            
            else:
                flash("Vui lòng đăng nhập!")
                return redirect(url_for("login"))
    #Lọc
    product = []
    product_id = []
    product_name = []
    product_price = []
    product_color = []
    product_pic = []
    for i in collection_Shop.find():
        if i['pic'] not in product_pic and i['id'] not in product_id:
            product_pic.append(i['pic'])
        if i['id'] not in product_id:
            product_id.append(i['id'])
        if i['name'] not in product_name:
            product_name.append(i['name'])
        if i['price'] not in product_price:
            product_price.append(i['price'])
        if i not in product:
            product.append(i)
    if 'username' in session:
        return render_template('index.html', user = session['username'], products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic, count=0)
    else:
        return render_template('index.html', products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic)
@app.route('/ao', methods=["GET", "POST"])
def ao():
    if request.method == 'POST':
        
        session.pop('search_key', None)
        
        if "search-key" in request.form:
            
            session['search_key'] = request.form['search-key']
            return redirect(url_for("search"))
        
        else:
            if "username" in session and session['username'] != 'admin':
                name = request.form["name"]
                color = request.form["color"]
                price = request.form["price"]
                id = request.form['id']
                
                test = True
                
                for i in collection_Cart.find():
                    if (i["id"] == id and i["name"] != name) or (i["id"] == id and i["name"] == name and i["color"] == color) or (i["name"] == name and i["id"] != id):
                        test = False
                        break
                
                if test == True:
                    data = {"id":id, "name": name, "color": color, "price": price.split(",")[0]}
                    collection_Cart.insert_one(data)
            
            else:
                flash("Vui lòng đăng nhập!")
                return redirect(url_for("login"))
    #Lọc
    product = []
    product_id = []
    product_name = []
    product_price = []
    product_color = []
    product_pic = []
    for i in collection_Shop.find():
        if i['pic'] not in product_pic and i['id'] not in product_id and i["id"][0:1] == "a":
            product_pic.append(i['pic'])
        if i['id'] not in product_id and i["id"][0:1] == "a":
            product_id.append(i['id'])
        if i['name'] not in product_name and i["id"][0:1] == "a":
            product_name.append(i['name'])
        if i['price'] not in product_price and i["id"][0:1] == "a":
            product_price.append(i['price'])
        if i not in product and i["id"][0:1] == "a":
            product.append(i)
    if 'username' in session:
        return render_template('ao.html', user = session['username'], products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic)
    else:
        return render_template('ao.html', products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic)
@app.route('/quan', methods=["GET", "POST"])
def quan():
    if request.method == 'POST':
        
        session.pop('search_key', None)
        
        if "search-key" in request.form:
            
            session['search_key'] = request.form['search-key']
            return redirect(url_for("search"))
        
        else:
            if "username" in session and session['username'] != 'admin':
                name = request.form["name"]
                color = request.form["color"]
                price = request.form["price"]
                id = request.form['id']
                
                test_num = 0
                
                for i in collection_Cart.find():
                    if i["name"] == name and i["color"] == color and i["id"] == id:
                        test_num = 1
                
                if test_num == 0:
                    data = {"id":id, "name": name, "color": color, "price": price}
                    collection_Cart.insert_one(data)
            
            else:
                flash("Vui lòng đăng nhập!")
                return redirect(url_for("login"))
    #Lọc
    product = []
    product_id = []
    product_name = []
    product_price = []
    product_color = []
    product_pic = []
    for i in collection_Shop.find():
        if i['pic'] not in product_pic and i['id'] not in product_id and i["id"][0:1] == "q":
            product_pic.append(i['pic'])
        if i['id'] not in product_id and i["id"][0:1] == "q":
            product_id.append(i['id'])
        if i['name'] not in product_name and i["id"][0:1] == "q":
            product_name.append(i['name'])
        if i['price'] not in product_price and i["id"][0:1] == "q":
            product_price.append(i['price'])
        if i not in product and i["id"][0:1] == "q":
            product.append(i)
    if 'username' in session:
        return render_template('quan.html', user = session['username'], products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic)
    else:
        return render_template('quan.html', products = product, products_id = product_id, products_name = product_name, products_price = product_price, products_pic = product_pic)
################################################################################################################################################

#Phần tài khoản
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('username',None)
        search = collection.find()
        for x in search:
            if request.form['password'] == x['password'] and request.form['username'] == x['username']:
                session['username'] = request.form['username']
                if session['username'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
        flash("Sai mật khẩu hoặc tên đăng nhập!")
        return redirect(request.url)
    if "username" in session:
        return redirect("/")
    else:
        return render_template('login.html')

#-----Phần Đăng Ký
@app.route('/signin', methods=['GET','POST'])
def signin():

    site_key = "6LdHPOEUAAAAANmHAokqVIWOm1WpDEhA7euAcCJH"

    if request.method == 'POST':

        captcha_response = request.form["g-recaptcha-response"]

        if is_human(captcha_response):

            session.pop('username', None)
            session.pop('code', None)
            session.pop('name', None)
            session.pop('password', None)
            session.pop('phone', None)
            session.pop('email', None)
            searchSignIn = collection.find()
            for i in searchSignIn:
                if i['username'] == request.form['username']:
                    return render_template('signin.html', error="Tên tài khoản đã tồn tại", site_key = site_key)
                elif i['email'] == request.form['email']:
                    return render_template('signin.html', error="Email này đã tồn tại", site_key = site_key)
            session['name'] = request.form['name']
            session['username'] = request.form['username'] 
            session['password'] = request.form['password']
            session['phone'] = request.form['phone'] 
            session['email'] = request.form['email']
            verNum = randrange(1000,10000,1)
            session['code'] = str(verNum)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("finalprojectmindx@gmail.com", "mindxc4e59")
            toEmail = request.form['email']
            server.sendmail("finalprojectmindx@gmail.com", toEmail, str(verNum))
            server.quit()

            return redirect(url_for('verifySignin'))
        else:
            flash("You not a human")
            return redirect(url_for("signin"))
    else:
        return render_template('signin.html', site_key = site_key)
def is_human(captcha_response):
    
    secret = "6LdHPOEUAAAAAHc32kv2eA9N1WWEXsRoIB3gU2qm"
    payload = {"response": captcha_response, "secret": secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text["success"]


###------Phần nhập mã xác nhận dành riêng cho đăng ký
@app.route('/verifysignin',methods=['GET','POST'])
def verifySignin():
    if g.username:
        if request.method == 'POST':
            if g.code == request.form['code']:
                data = {'name':g.name, 'username':g.username, 'password':g.password, 'phone':g.phone, 'email':g.email}
                collection.insert_one(data)
                return 'Successful'
            else:
                return render_template('verifysignin.html')
        else:
            return render_template('verifysignin.html')
    return redirect(url_for('signin'))

###-----Quên mật khẩu
@app.route('/forgetpass', methods=['GET','POST'])
def forgetpass():
    if request.method == 'POST':
        
        session.pop('forgetCode',None)
        session.pop('username',None)
        search = collection.find()
        for x in search:
            if request.form['username'] == x['username']:
                xacNhan = randrange(1000,10000,1)
                session['forgetCode'] = str(xacNhan)
                session['username'] = request.form['username']

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("finalprojectmindx@gmail.com", "mindxc4e59")
                toEmail = x['email'] 
                server.sendmail(
                "finalprojectmindx@gmail.com", toEmail, str(xacNhan))
                server.quit()

                return redirect(url_for('verifyForgetPass'))
        return redirect(url_for('forgetpass'))
    else:
        return render_template('forgetpass.html')

@app.route('/verifyforgetpass',methods=['GET','POST'])
def verifyForgetPass():
    if request.method == 'POST':
        if request.form['codeForget'] == g.forgetcode:
            return redirect(url_for('inputPass'))
        else:
            return redirect(url_for('verifyForgetPass'))
    else:
        return render_template('verifyforgetpass.html')

@app.route('/inputnewpass', methods=['GET','POST'])
def inputPass():
    if request.method == 'POST':
        myquery = { "username": g.username }
        newvalue = { "$set": {"password": request.form['newPass']}}
        collection.update_one(myquery,newvalue)
        return 'Successful'
    else:
        return render_template('inputpass.html')

@app.before_request
def before_request():
    g.username = None
    g.name = None
    g.password = None
    g.phone = None
    g.code = None
    g.email = None
    g.forgetcode = None


    if 'username' in session:
        g.username = session['username']

    if 'code' in session:
        g.code = session['code']

    if 'name' in session:
        g.name = session['name']

    if 'phone' in session:
        g.phone = session['phone']

    if 'email' in session:
        g.email = session['email']

    if 'password' in session:
        g.password = session['password']
    
    if 'forgetCode' in session:
        g.forgetcode = session['forgetCode']
    
@app.route('/getsession')
def getsession():
    if 'username' in session:
        return session['username']
    return 'Not logged in'

@app.route('/dropsession')
def dropsession():
    session.pop('username', None)
    flash("Đăng xuất thành công!")
    return redirect("/login")
################################################################################################################################################

#Phần chức năng của admin
@app.route('/admin', methods=['GET','POST'])
def admin():
    if session['username'] == 'admin':
        if request.method == 'POST':
            sdata = collection_Shop.find()
            shopdata = []
            for i in sdata:
                if i["pic"] not in shopdata:
                    shopdata.append(i["pic"])
            
            for i in shopdata:
                if request.form["productpic"] == i or shopdata == []:
                    flash("Trùng dữ liệu!")
                    return redirect(request.url)
            data_product = {'id':request.form['productid'], 'name':request.form['productname'],'pic':request.form['productpic'], 'price':request.form['productprice'],'color':request.form['productcolor']}
            collection_Shop.insert_one(data_product)
            flash("Thành công!")
            return redirect(request.url)
        return render_template('admin.html')
    return redirect("/")
################################################################################################################################################

#Phần chức năng tìm kiếm
@app.route('/search')
def search():
    #Lọc
    product = []
    product_id = []
    product_name = []
    product_price = []
    product_color = []
    product_pic = []
    for i in collection_Shop.find():
        if i['pic'] not in product_pic and i['id'] not in product_id:
            product_pic.append(i['pic'])
        if i['id'] not in product_id:
            product_id.append(i['id'])
        if i['name'] not in product_name:
            product_name.append(i['name'].lower())
        if i['price'] not in product_price:
            product_price.append(i['price'])
        if i not in product:
            product.append(i)
    if 'search_key' in session:
        
        search_key = session["search_key"]
        search_key = unidecode(search_key.lower())
        
        result = []
        for i in product:

            keys_word = []
            for j in search_key.split():
                keys_word.append(j)
                for k in j:
                    keys_word.append(k)
            
            if search_key in keys_word and search_key in unidecode(i["name"]).lower():
                result.append(i)
        
        return render_template('search.html', search_key = session["search_key"], result = result)
    return redirect("/")
################################################################################################################################################

#Phần thông tin hóa đơn khách hàng
@app.route('/bill_info', methods = ["GET", "POST"])
def bill_info():
    if "username" in session and session['username'] != 'admin':
        session.pop('ma_don_hang', None)
        session["ma_don_hang"] = "#" + str(randrange(1000,9999,1))
        
        cart = []
        product = [] 
        for i in collection_Cart.find():
            if i not in cart:
                cart.append(i)
        for i in collection_Shop.find():
            if i not in product:
                product.append(i)
        
        #Check id_bill đã tồn tại chưa và thay đổi
        id_bill = []
        for i in collection_Bill.find():
            if i["id_bill"] not in id_bill:
                id_bill.append(i["id_bill"])
        
        while session["ma_don_hang"] in id_bill:
                session["ma_don_hang"] = "#" + str(randrange(1000,9999,1))
        ###
        
        if request.method == "POST":
            
            if request.form['name'] == "" or request.form['email']== "" or request.form['phone'] == "" or request.form['address'] == "" or request.form['city']== "":
                flash("Vui lòng điền đủ thông tin")
                return redirect(url_for('bill_info'))
            
            numbers = []
            for i in range (len(cart)):
                name_form = "number-{}".format(i)
                numbers.append(request.form[name_form])

            product_info = {}
            total = 0
            for i in cart:
                product_info[str(cart.index(i))] = {"id": i["id"],
                    "name":i["name"],
                    "color":i["color"],
                    "number":str(numbers[cart.index(i)]),
                    "price":i["price"]} 
                total += int(numbers[cart.index(i)])*int(i["price"].split(",")[0])
            
            customer = {'id_bill' : session["ma_don_hang"],
                'username':session['username'],
                'name':request.form['name'] ,
                'email': request.form['email'],
                'phone': request.form['phone'],
                'address': request.form['address'],
                'city' : request.form['city'],
                "product_info": product_info,
                "total": str(total)+"000" }
                
            collection_Bill.insert_one(customer)

            total_product = ""
            for i in product_info:
                total_product += "{} - {} : {} item\n\t".format(product_info[i]["name"], product_info[i]["color"], product_info[i]["number"])

            message = """
From: MindX 59 Web Shop
To: %s 
ID BILL: %s
You have just bought the following products:
        %s
Total expenditure: %s₫
            """%(request.form['name'], session["ma_don_hang"], total_product, str(total)+"000")

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("finalprojectmindx@gmail.com", "mindxc4e59")
            toEmail = request.form['email']
            server.sendmail("finalprojectmindx@gmail.com", toEmail, message)
            server.quit()

            product_info.clear()
            collection_Cart.drop()
            
            flash("Thành công gửi đơn hàng! Quý khách vui lòng chuyển khoản {}000₫ vào tài khoản 01111111XXX chi nhánh ĐốngXXX với nội dung {}".format(total, session["ma_don_hang"]))
            return redirect(url_for('bill_info'))
        city_vn = ["An Giang", "Bà Rịa", "Vũng Tàu","Bắc Giang","Bắc Kạn",'Bạc Liêu','Bắc Ninh','Bến Tre','Bình Định','Bình Dương','Bình Phước','Bình Thuận','Cà Mau','Cao Bằng','Đắk Lắk','Đắk Nông','Điện Biên','Đồng Nai','Đồng Tháp','Gia Lai','Hà Giang', 'Hà Nam','Hà Tĩnh','Hải Dương','Hậu Giang','Hòa Bình','Hưng Yên','Khánh Hòa','Kiên Giang','Kon Tum','Lai Châu','Lâm Đồng','Lạng Sơn','Lào Cai','Long An','Nam Định','Nghệ An','Ninh Bình','Ninh Thuận','Phú Thọ','Quảng Bình',	'Quảng Nam','Quảng Ngãi','Quảng Ninh','Quảng Trị','Sóc Trăng','Sơn La','Tây Ninh','Thái Bình','Thái Nguyên','Thanh Hóa','Thừa Thiên Huế','Tiền Giang','Trà Vinh','Tuyên Quang','Vĩnh Long','Vĩnh Phúc','Yên Bái','Phú Yên',	'Cần Thơ','Đà Nẵng','Hải Phòng','Hà Nội','TP HCM']
        return render_template('bill_info.html', id_bill = session["ma_don_hang"], city_vn = city_vn, cart = cart, products = product )
    else:
        flash("Vui lòng đăng nhập")
        return redirect(url_for("login"))

################################################################################################################################################

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 