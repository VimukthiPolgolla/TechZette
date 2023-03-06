from flask import Blueprint, render_template, request, flash, url_for, session
from firebase import Firebase
from werkzeug.utils import redirect

sEmails = []
cEmails = []
shopEmails = []

config = {
    "apiKey": "AIzaSyBFxVQa0vfURd8O323Gv-iXdHBxeI3emD8",
    "authDomain": "techzette-9644e.firebaseapp.com",
    "databaseURL": "https://techzette-9644e-default-rtdb.firebaseio.com",
    "storageBucket": "techzette-9644e.appspot.com"
}

firebase = Firebase(config)

auth = Blueprint('auth', __name__)


@auth.route('/addItems', methods=['GET', 'POST'])
def addItems():
    global productArray, product
    email = session.get('e_mail', None)
    # email = request.args.get('Email', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_order = firebase.database().child("Orders")
    ref_db_orders = firebase.database().child("Orders")

    orderList = {}
    haveOrders = False

    ownerNames = []
    users = ref_db_order.get()
    for item in users.each():
        ownerNames.append(item.key())

    if email in ownerNames:
        haveOrders = True

    if haveOrders:
        productList = ref_db_orders.child(email).child('orders').get()
        # array stored with product names
        productArray = productList.val().split("+")
        # print(productArray[0])
        for i in range(len(productArray)):
            product = productArray[i].split("?")
            orderList[i] = product

    if request.method == 'POST':
        brand = request.form.get('brand')
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.form.get('image')
        category = request.form.get('category')

        if len(brand) < 1:
            flash('Brand name must be greater than 1 characters', category='error')
        elif len(name) < 2:
            flash('Product name must be greater than 1 character', category='error')
        elif len(description) < 7:
            flash('Description must be atleast 10 characters', category='error')
        elif len(image) < 2:
            flash('Image URL must be greater than 1 character', category='error')
        elif int(price) <= 0:
            flash('Price must be atleast LKR 1', category='error')
        else:
            # add user to database
            data = {
                'Brand': brand,
                'Name': name,
                'Description': description,
                'Price': price,
                'URL': image,
                'Owner': email,
                'Category': category
            }
            ref_db_items.child(name).set(data)
            flash('Item added Successfully!', category='success')
    if haveOrders:
        return render_template("addItems.html", Email=email, products=orderList, haveOrders=haveOrders, length=len(productArray))
    else:
        return render_template("addItems.html", Email=email, haveOrders=haveOrders)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    ref_db_sellers = firebase.database().child("Sellers")
    ref_db_customers = firebase.database().child("Customers")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sellerNames = ref_db_sellers.get()
        for sell in sellerNames.each():
            sEmails.append(sell.key())
        customerNames = ref_db_customers.get()
        for sell in customerNames.each():
            cEmails.append(sell.key())
        if email in sEmails:
            fullList = sellerNames.val()
            if fullList[email]["Password"] == password:
                session['e_mail'] = email
                return redirect(request.args.get("next") or url_for("auth.addItems", Email=email))
                # return redirect(request.args.get("next") or url_for("auth.addItems"))
            else:
                flash('Recheck your password!', category='error')
                return render_template("login.html")
        elif email in cEmails:
            fullList = customerNames.val()
            if fullList[email]["Password"] == password:
                session['e_mail'] = email
                # return redirect(request.args.get("next") or url_for("views.home", Email=email))
                return redirect(request.args.get("next") or url_for("views.ecommerce"))
            else:
                flash('Recheck your password!', category='error')
                return render_template("login.html")
        else:
            flash('Account not found!', category='error')

    return render_template("login.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    ref_db_sellers = firebase.database().child("Sellers")
    ref_db_seller = firebase.database().child("Sellers")
    ref_db_customers = firebase.database().child("Customers")
    ref_db_customer = firebase.database().child("Customers")

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        accType = request.form.get('acc_type')

        sellerNames = ref_db_seller.get()
        for sell in sellerNames.each():
            sEmails.append(sell.key())
        customerNames = ref_db_customer.get()
        for sell in customerNames.each():
            cEmails.append(sell.key())

        if len(email) < 4:
            flash('Username must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 3:
            flash('Password must be atleast 7 characters', category='error')
        else:
            # add user to database
            if email in sEmails:
                flash('User account already exists!', category='error')
            elif email in cEmails:
                flash('User account already exists!', category='error')
            else:
                if '.' in email:
                    flash('Use "dot" as word instead of character "."!', category='error')
                else:
                    if accType == 'seller':
                        seller = {
                            'Email': email,
                            'Name': firstName,
                            'Password': password1,
                        }
                        ref_db_sellers.child(email).set(seller)
                    else:
                        seller = {
                            'Email': email,
                            'Name': firstName,
                            'Password': password1,
                        }
                        ref_db_customers.child(email).set(seller)
                    flash('Account created!', category='success')

    return render_template("sign_up.html")


@auth.route('/sign-up2', methods=['GET', 'POST'])
def sign_up2():
    ref_db_sellers = firebase.database().child("Sellers")
    ref_db_seller = firebase.database().child("Sellers")
    ref_db_customers = firebase.database().child("Customers")
    ref_db_customer = firebase.database().child("Customers")

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        accType = request.form.get('acc_type')

        sellerNames = ref_db_seller.get()
        for sell in sellerNames.each():
            sEmails.append(sell.key())
        customerNames = ref_db_customer.get()
        for sell in customerNames.each():
            cEmails.append(sell.key())

        if len(email) < 4:
            flash('Username must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 3:
            flash('Password must be atleast 7 characters', category='error')
        else:
            # add user to database
            if email in sEmails:
                flash('User account already exists!', category='error')
            elif email in cEmails:
                flash('User account already exists!', category='error')
            else:
                if '.' in email:
                    flash('Use "dot" as word instead of character "."!', category='error')
                else:
                    if accType == 'seller':
                        seller = {
                            'Email': email,
                            'Name': firstName,
                            'Password': password1,
                        }
                        ref_db_sellers.child(email).set(seller)
                    else:
                        seller = {
                            'Email': email,
                            'Name': firstName,
                            'Password': password1,
                        }
                        ref_db_customers.child(email).set(seller)
                    flash('Account created!', category='success')

    return render_template("sign_up2.html")


@auth.route('/login2', methods=['GET', 'POST'])
def login2():
    ref_db_sellers = firebase.database().child("Sellers")
    ref_db_customers = firebase.database().child("Customers")
    ref_db_shops = firebase.database().child("Shops")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sellerNames = ref_db_sellers.get()
        for sell in sellerNames.each():
            sEmails.append(sell.key())
        shopNames = ref_db_shops.get()
        for sell in shopNames.each():
            shopEmails.append(sell.key())
        customerNames = ref_db_customers.get()
        for sell in customerNames.each():
            cEmails.append(sell.key())
        if email in shopEmails:
            fullList = shopNames.val()
            if fullList[email]["Password"] == password:
                session['e_mail'] = email
                return redirect(request.args.get("next") or url_for("auth.addItems2", Email=email))
                # return redirect(request.args.get("next") or url_for("auth.addItems"))
            else:
                flash('Recheck your password!', category='error')
                return render_template("login2.html")
        elif email in cEmails:
            fullList = customerNames.val()
            if fullList[email]["Password"] == password:
                session['e_mail'] = email
                # return redirect(request.args.get("next") or url_for("views.home", Email=email))
                return redirect(request.args.get("next") or url_for("views.partnerHomepage"))
            else:
                flash('Recheck your password!', category='error')
                return render_template("login2.html")
        else:
            flash('Account not found!', category='error')

    return render_template("login2.html")


@auth.route('/addItems2', methods=['GET', 'POST'])
def addItems2():
    global productArray, product
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_order = firebase.database().child("Orders_Shops")
    ref_db_orders = firebase.database().child("Orders_Shops")

    orderList = {}
    haveOrders = False

    ownerNames = []
    users = ref_db_order.get()
    for item in users.each():
        ownerNames.append(item.key())

    if email in ownerNames:
        haveOrders = True

    if haveOrders:
        productList = ref_db_orders.child(email).child('orders').get()
        # array stored with product names
        productArray = productList.val().split("+")
        # print(productArray[0])
        for i in range(len(productArray)):
            product = productArray[i].split("?")
            orderList[i] = product

    if request.method == 'POST':
        brand = request.form.get('brand')
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.form.get('image')
        category = request.form.get('category')

        if len(brand) < 1:
            flash('Brand name must be greater than 1 characters', category='error')
        elif len(name) < 2:
            flash('Product name must be greater than 1 character', category='error')
        elif len(description) < 7:
            flash('Description must be atleast 10 characters', category='error')
        elif len(image) < 2:
            flash('Image URL must be greater than 1 character', category='error')
        elif int(price) <= 0:
            flash('Price must be atleast LKR 1', category='error')
        else:
            # add user to database
            data = {
                'Brand': brand,
                'Name': name,
                'Description': description,
                'Price': price,
                'URL': image,
                'Owner': email,
                'Category': category
            }
            ref_db_items.child(name).set(data)
            flash('Item added Successfully!', category='success')
    if haveOrders:
        return render_template("addItems2.html", Email=email, products=orderList, haveOrders=haveOrders, length=len(productArray))
    else:
        return render_template("addItems2.html", Email=email, haveOrders=haveOrders)
