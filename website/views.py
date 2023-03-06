from flask import Blueprint, render_template, request, flash, url_for, session
from firebase import Firebase
from werkzeug.utils import redirect

views = Blueprint('views', __name__)

config = {
    "apiKey": "AIzaSyBFxVQa0vfURd8O323Gv-iXdHBxeI3emD8",
    "authDomain": "techzette-9644e.firebaseapp.com",
    "databaseURL": "https://techzette-9644e-default-rtdb.firebaseio.com",
    "storageBucket": "techzette-9644e.appspot.com"
}
firebase = Firebase(config)


@views.route('/', methods=['GET', 'POST'])
def home():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)

    return render_template("home.html", Email=email)


@views.route('/partnerHomepage', methods=['GET', 'POST'])
def partnerHomepage():
    email = session.get('e_mail', None)
    isShop = False
    shops = ['Chama Computers', 'Game Street', 'LaptopLK', 'Nanotek', 'Red Line', 'TechZone']
    for shop in shops:
        if email == shop:
            isShop = True

    return render_template("partnerHomepage.html", Email=email, isShop=isShop)


@views.route('/partners', methods=['GET', 'POST'])
def partners():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)

    return render_template("partners.html", Email=email)


@views.route('/ecommerce', methods=['GET', 'POST'])
def ecommerce():
    # email = request.args.get('Email', None)
    ref_db_sellers = firebase.database().child("Sellers")
    email = session.get('e_mail', None)
    sellerList = ref_db_sellers.get()
    isShop = False
    for seller in sellerList.val():
        if email == seller:
            isShop = True

    return render_template("ecommerce.html", Email=email, isShop=isShop)


@views.route('/cart', methods=['GET', 'POST'])
def cart():
    email = session.get('e_mail', None)
    ref_db_cartsss = firebase.database().child("Cart")
    ref_db_Caart = firebase.database().child("Cart")
    ref_db_Ittems = firebase.database().child("Items")

    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_cartt = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")
    ref_db_CARTT = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    if request.method == 'POST':
        Cart = request.form.get('cart')

        if email is None:
            flash('Please Login!', category='error')
        # remove from cart option
        else:
            if email in cartUsers:
                productsList = ref_db_cartt.child(email).get()
                if Cart in productsList.val():
                    item = {
                        'Quantity': None
                    }
                    ref_db_CART.child(email).child(Cart).set(item)

    haveCart = False

    ownerNames = []
    users = ref_db_Caart.get()
    for item in users.each():
        ownerNames.append(item.key())

    if email in ownerNames:
        haveCart = True

    if haveCart:
        productArray = []
        quantityArray = []
        cartList = ref_db_cart.child(email).get()
        for item in cartList.each():
            productArray.append(item.key())
        productQty = ref_db_cartsss.child(email).get().val()
        for i in range(len(productArray)):
            quantityArray.append(productQty[productArray[i]]['Quantity'])

        total = 0
        item_total_prices = []
        item_prices = []
        item_sellers = []
        item_images = []

        products = ref_db_Ittems.get()
        fullList = products.val()

        for i in range(len(productArray)):
            total = total + (int(fullList[productArray[i]]['Price'])) * (int(quantityArray[i]))
            item_total_prices.append(int(fullList[productArray[i]]['Price']) * (int(quantityArray[i])))
            item_prices.append(fullList[productArray[i]]['Price'])
            item_sellers.append(fullList[productArray[i]]['Owner'])
            item_images.append(fullList[productArray[i]]['URL'])

        session['total'] = total
        session['products'] = productArray
        session['sellers'] = item_sellers
        session['quantity'] = quantityArray
        return render_template('cart.html', name=email, products=productArray, total=total, prices=item_prices,
                               length=len(item_prices), haveCart=haveCart, images=item_images, quantity=quantityArray,
                               totalPrices=item_total_prices)
    else:
        return render_template('cart.html', name=email, haveCart=haveCart)


@views.route('/checkout', methods=['GET', 'POST'])
def checkout():
    ref_db_cart = firebase.database().child("Cart")
    email = session.get('e_mail', None)
    quantity = session.get('quantity', None)
    total = session.get('total', None)
    products = session.get('products', None)
    sellers = session.get('sellers', None)

    if request.method == 'POST':
        name = request.form.get('firstName')
        address = request.form.get('address')
        contact = request.form.get('number')
        payment = request.form.get('payment_type')  # output is cash

        if len(name) < 1:
            flash('Name must be greater than 1 characters', category='error')
        elif len(address) < 2:
            flash('Address must be greater than 2 character', category='error')
        elif len(contact) < 2:
            flash('Contact must be greater than 1 characters', category='error')
        elif payment != 'cash':
            flash('Select payment method', category='error')
        else:

            for i in range(len(products)):
                ref_db_order = firebase.database().child("Orders")
                orders = ref_db_order.get()
                ownerNames = []
                for item in orders.each():
                    ownerNames.append(item.key())
                if sellers[i] in ownerNames:
                    ref_db_orderss = firebase.database().child("Orders")
                    ref_db_orders = firebase.database().child("Orders")
                    orderList = ref_db_orderss.child(sellers[i]).get()
                    ord = orderList.val()['orders'] + '+' + name + '?' + address + '?' + contact + '?' + products[
                        i] + '?' + payment + '?' + quantity[i]
                    item = {
                        'orders': ord
                    }
                    ref_db_orders.child(sellers[i]).set(item)
                    ref_db_cart.child(email).set(None)
                else:
                    item = {
                        'orders': name + '?' + address + '?' + contact + '?' + products[i] + '?' + payment + '?' + quantity[i]
                    }
                    ref_db_orders = firebase.database().child("Orders")
                    ref_db_orders.child(sellers[i]).set(item)
                    ref_db_cart.child(email).set(None)
            flash('Ordered Successfully!', category='success')
            return redirect(request.args.get("next") or url_for("views.ecommerce"))

    return render_template('checkout.html', email=email, total=total)


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/product', methods=['GET', 'POST'])
def product():
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    email = session.get('e_mail', None)
    Product = session.get('product', None)

    products = ref_db_items.get()
    fullList = products.val()

    Brand = fullList[Product]['Brand']
    Desc = fullList[Product]['Description']
    Name = fullList[Product]['Name']
    Owner = fullList[Product]['Owner']
    Price = fullList[Product]['Price']
    Image = fullList[Product]['URL']

    names = []
    cartUsers = []

    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    if request.method == 'POST':
        qty = request.form.get('quantity')

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Product).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Product).set(item)
                flash('Added successfully!', category='success')

    return render_template('product.html', Email=email, Brand=Brand, Desc=Desc, Name=Name, Owner=Owner, Price=Price,
                           Image=Image)


@views.route('/laptops', methods=['GET', 'POST'])
def laptops():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("laptops.html", nameList=names, productList=fullList, Email=email)


@views.route('/accessories', methods=['GET', 'POST'])
def accessories():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    return render_template("accessories.html", Email=email)


@views.route('/processors', methods=['GET', 'POST'])
def processors():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("processors.html", nameList=names, productList=fullList, Email=email)


@views.route('/memory', methods=['GET', 'POST'])
def memory():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("memory.html", nameList=names, productList=fullList, Email=email)


@views.route('/graphic', methods=['GET', 'POST'])
def graphic():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("graphic.html", nameList=names, productList=fullList, Email=email)


@views.route('/monitors', methods=['GET', 'POST'])
def monitors():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("monitors.html", nameList=names, productList=fullList, Email=email)


@views.route('/motherboard', methods=['GET', 'POST'])
def motherboard():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("motherboard.html", nameList=names, productList=fullList, Email=email)


@views.route('/mouse', methods=['GET', 'POST'])
def mouse():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("mouse.html", nameList=names, productList=fullList, Email=email)


@views.route('/storages', methods=['GET', 'POST'])
def storages():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("storages.html", nameList=names, productList=fullList, Email=email)


@views.route('/other', methods=['GET', 'POST'])
def other():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items")
    ref_db_cart = firebase.database().child("Cart")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_CART = firebase.database().child("Cart")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("other.html", nameList=names, productList=fullList, Email=email)


@views.route('/contacts')
def contacts():
    return render_template("contacts.html")


@views.route('/about2')
def about2():
    return render_template('about2.html')


@views.route('/contacts2')
def contacts2():
    return render_template("contacts2.html")


@views.route('/cart2', methods=['GET', 'POST'])
def cart2():
    email = session.get('e_mail', None)
    ref_db_cartsss = firebase.database().child("Cart_Shops")
    ref_db_Caart = firebase.database().child("Cart_Shops")
    ref_db_Ittems = firebase.database().child("Items_Shops")

    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_cartt = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")
    ref_db_CARTT = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    if request.method == 'POST':
        Cart = request.form.get('cart')

        if email is None:
            flash('Please Login!', category='error')
        # remove from cart option
        else:
            if email in cartUsers:
                productsList = ref_db_cartt.child(email).get()
                if Cart in productsList.val():
                    item = {
                        'Quantity': None
                    }
                    ref_db_CART.child(email).child(Cart).set(item)

    haveCart = False

    ownerNames = []
    users = ref_db_Caart.get()
    for item in users.each():
        ownerNames.append(item.key())

    if email in ownerNames:
        haveCart = True

    if haveCart:
        productArray = []
        quantityArray = []
        cartList = ref_db_cart.child(email).get()
        for item in cartList.each():
            productArray.append(item.key())
        productQty = ref_db_cartsss.child(email).get().val()
        for i in range(len(productArray)):
            quantityArray.append(productQty[productArray[i]]['Quantity'])

        total = 0
        item_total_prices = []
        item_prices = []
        item_sellers = []
        item_images = []

        products = ref_db_Ittems.get()
        fullList = products.val()

        for i in range(len(productArray)):
            total = total + (int(fullList[productArray[i]]['Price'])) * (int(quantityArray[i]))
            item_total_prices.append(int(fullList[productArray[i]]['Price']) * (int(quantityArray[i])))
            item_prices.append(fullList[productArray[i]]['Price'])
            item_sellers.append(fullList[productArray[i]]['Owner'])
            item_images.append(fullList[productArray[i]]['URL'])

        session['total'] = total
        session['products'] = productArray
        session['sellers'] = item_sellers
        session['quantity'] = quantityArray
        return render_template('cart2.html', name=email, products=productArray, total=total, prices=item_prices,
                               length=len(item_prices), haveCart=haveCart, images=item_images, quantity=quantityArray,
                               totalPrices=item_total_prices)
    else:
        return render_template('cart2.html', name=email, haveCart=haveCart)


@views.route('/chama', methods=['GET', 'POST'])
def chama():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("chama.html", nameList=names, productList=fullList, Email=email)


@views.route('/product2', methods=['GET', 'POST'])
def product2():
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    email = session.get('e_mail', None)
    Product = session.get('product', None)

    products = ref_db_items.get()
    fullList = products.val()

    Brand = fullList[Product]['Brand']
    Desc = fullList[Product]['Description']
    Name = fullList[Product]['Name']
    Owner = fullList[Product]['Owner']
    Price = fullList[Product]['Price']
    Image = fullList[Product]['URL']

    names = []
    cartUsers = []

    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    if request.method == 'POST':
        qty = request.form.get('quantity')

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Product).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Product).set(item)
                flash('Added successfully!', category='success')

    return render_template('product2.html', Email=email, Brand=Brand, Desc=Desc, Name=Name, Owner=Owner, Price=Price,
                           Image=Image)


@views.route('/laptoplk', methods=['GET', 'POST'])
def laptoplk():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("laptoplk.html", nameList=names, productList=fullList, Email=email)


@views.route('/street', methods=['GET', 'POST'])
def street():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("street.html", nameList=names, productList=fullList, Email=email)


@views.route('/nanotek', methods=['GET', 'POST'])
def nanotek():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("nanotek.html", nameList=names, productList=fullList, Email=email)


@views.route('/redline', methods=['GET', 'POST'])
def redline():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("redline.html", nameList=names, productList=fullList, Email=email)


@views.route('/techzone', methods=['GET', 'POST'])
def techzone():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        if request.form.get('cart') is not None:
            Cart = request.form.get('cart')
            qty = request.form.get('quantity')
        else:
            session['product'] = request.form.get('product')
            # return render_template("product.html")
            return redirect(request.args.get("next") or url_for("views.product2"))

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            # if user found in cart database
            if email in cartUsers:
                item = {
                    'Quantity': qty
                }
                ref_db_CART.child(email).child(Cart).set(item)
                flash('Added Successfully!', category='success')
            # if new user
            else:
                item = {
                    'Quantity': qty
                }
                ref_db_cart.child(email).child(Cart).set(item)
                flash('Added successfully!', category='success')

    return render_template("techzone.html", nameList=names, productList=fullList, Email=email)


@views.route('/checkout2', methods=['GET', 'POST'])
def checkout2():
    ref_db_cart = firebase.database().child("Cart_Shops")
    email = session.get('e_mail', None)
    quantity = session.get('quantity', None)
    total = session.get('total', None)
    products = session.get('products', None)
    sellers = session.get('sellers', None)

    if request.method == 'POST':
        name = request.form.get('firstName')
        address = request.form.get('address')
        contact = request.form.get('number')
        payment = request.form.get('payment_type')  # output is cash

        if len(name) < 1:
            flash('Name must be greater than 1 characters', category='error')
        elif len(address) < 2:
            flash('Address must be greater than 2 character', category='error')
        elif len(contact) < 2:
            flash('Contact must be greater than 1 characters', category='error')
        elif payment != 'cash':
            flash('Select payment method', category='error')
        else:

            for i in range(len(products)):
                ref_db_order = firebase.database().child("Orders_Shops")
                orders = ref_db_order.get()
                ownerNames = []
                for item in orders.each():
                    ownerNames.append(item.key())
                if sellers[i] in ownerNames:
                    ref_db_orderss = firebase.database().child("Orders_Shops")
                    ref_db_orders = firebase.database().child("Orders_Shops")
                    orderList = ref_db_orderss.child(sellers[i]).get()
                    ord = orderList.val()['orders'] + '+' + name + '?' + address + '?' + contact + '?' + products[
                        i] + '?' + payment + '?' + quantity[i]
                    item = {
                        'orders': ord
                    }
                    ref_db_orders.child(sellers[i]).set(item)
                    ref_db_cart.child(email).set(None)
                else:
                    item = {
                        'orders': name + '?' + address + '?' + contact + '?' + products[i] + '?' + payment + '?' + quantity[i]
                    }
                    ref_db_orders = firebase.database().child("Orders_Shops")
                    ref_db_orders.child(sellers[i]).set(item)
                    ref_db_cart.child(email).set(None)
            flash('Ordered Successfully!', category='success')
            return redirect(request.args.get("next") or url_for("views.partners"))

    return render_template('checkout2.html', email=email, total=total)


@views.route('/pcbuild', methods=['GET', 'POST'])
def pcbuild():
    # email = request.args.get('Email', None)
    email = session.get('e_mail', None)
    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    productsArray = []
    priceArray = []

    if request.method == 'POST':
        Processor = request.form.get('processor')
        Memory = request.form.get('memory')
        Graphic = request.form.get('graphic')
        Monitor = request.form.get('monitor')
        Motherboard = request.form.get('motherboard')
        Storage = request.form.get('storage')
        PowerSupply = request.form.get('powersupply')
        Other = request.form.get('other')

        productsArray.append(Processor)
        productsArray.append(Memory)
        productsArray.append(Graphic)
        productsArray.append(Monitor)
        productsArray.append(Motherboard)
        productsArray.append(Storage)
        productsArray.append(PowerSupply)
        productsArray.append(Other)

        Total = 0

        for Product in productsArray:
            priceArray.append(fullList[Product]['Price'])
            Total = Total + int(fullList[Product]['Price'])

        session['Build_Total'] = Total
        session['Build_Prices'] = priceArray
        session['Build_Products'] = productsArray
        return redirect(request.args.get("next") or url_for("views.viewBuild", Email=email))

    return render_template('pcbuild.html', nameList=names, productList=fullList, Email=email)


@views.route('/viewBuild', methods=['GET', 'POST'])
def viewBuild():
    email = session.get('e_mail', None)
    prices = session.get('Build_Prices', None)
    Products = session.get('Build_Products', None)
    total = session.get('Build_Total', None)

    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")

    products = ref_db_items.get()

    names = []
    cartUsers = []

    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    if request.method == 'POST':

        if email is None:
            flash('Please Login!', category='error')
        # add to cart option
        else:
            for Product in Products:
                ref_db_cart = firebase.database().child("Cart_Shops")
                ref_db_CART = firebase.database().child("Cart_Shops")
                if email in cartUsers:
                    item = {
                        'Quantity': '1'
                    }
                    ref_db_CART.child(email).child(Product).set(item)
                # if new user
                else:
                    item = {
                        'Quantity': '1'
                    }
                    ref_db_cart.child(email).child(Product).set(item)
            flash('Added successfully!', category='success')

    return render_template('viewBuild.html', Email=email, prices=prices, products=Products, total=total)


@views.route('/remove2', methods=['GET', 'POST'])
def remove2():
    email = session.get('e_mail', None)

    ref_db_items = firebase.database().child("Items_Shops")
    ref_db_cart = firebase.database().child("Cart_Shops")
    ref_db_carts = firebase.database().child("Cart_Shops")
    ref_db_CART = firebase.database().child("Cart_Shops")
    ref_db_Items = firebase.database().child("Items_Shops")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        deleteItem = request.form.get('deleteItem')
        item = {
            'Brand': None,
            'Category': None,
            'Description': None,
            'Name': None,
            'Owner': None,
            'Price': None,
            'URL': None,
        }
        ref_db_Items.child(deleteItem).set(item)
        flash('Deleted successfully!', category='success')

    return render_template('remove2.html', nameList=names, productList=fullList, Email=email)


@views.route('/remove', methods=['GET', 'POST'])
def remove():
    email = session.get('e_mail', None)

    ref_db_items = firebase.database().child("Items")
    ref_db_carts = firebase.database().child("Cart")
    ref_db_Items = firebase.database().child("Items")

    names = []
    cartUsers = []

    products = ref_db_items.get()
    for item in products.each():
        names.append(item.key())

    cartList = ref_db_carts.get()
    for item in cartList.each():
        cartUsers.append(item.key())

    fullList = products.val()

    if request.method == 'POST':
        deleteItem = request.form.get('deleteItem')
        item = {
            'Brand': None,
            'Category': None,
            'Description': None,
            'Name': None,
            'Owner': None,
            'Price': None,
            'URL': None,
        }
        ref_db_Items.child(deleteItem).set(item)
        flash('Deleted successfully!', category='success')

    return render_template('remove.html', nameList=names, productList=fullList, Email=email)
