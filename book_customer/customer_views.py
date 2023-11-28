import sys
from datetime import date
from itertools import count

import book
from book import settings
from django.shortcuts import render, redirect
from django.db import connection
from book_admin import models
from book_admin import forms
from book_admin.forms import UserForm, ProfileForm, BookForm, CustomerBookForm
from book_admin.models import User, Area, Book, Cart, Order, Order_detail, Wishlist, Sub_category, Language, Category, \
    Feedback
from django.contrib import messages

from book_customer.cart import c_Cart
from book_admin.functions import handle_uploaded_file


# Create your views here.


def c_home(request):
    b = Book.objects.filter(u_id=None)
    ub = Book.objects.filter(u_id__gt=0,is_available=1)
    feedback = Feedback.objects.all()

    u = User.objects.all().count()
    f = Feedback.objects.all().count()
    book = Book.objects.all().count()
    a = Area.objects.all().count()

    return render(request, "customer_home.html", {'book': b, 'userbook': ub, 'f': feedback, "user": u,
                                                  "feedback": f, "books": book, "area": a})


def c_login(request):
    return render(request, "customer_login.html")


def c_otppage(request):
    return render(request, "otp_page.html")


def grid(request, id):
    b = Book.objects.filter(b_id=id)
    return render(request, "grid_view.html", {'book': b})


def checkout(request):
    return render(request, "customer_checkout.html")


def detail(request, id):
    b = Book.objects.get(b_id=id)
    f = Feedback.objects.filter(b_id=id)
    fb = Feedback.objects.filter(b_id=id).count()
    related_book = Book.objects.filter(s_id=id)

    return render(request, "book_detail.html", {'rb': related_book, 'book': b, 'feed': f, 'count': fb})


'''
def c_delete(request, id):
    bi = Cart.objects.get(cart_id=id)
    bi.delete()
    return redirect("/c/cart/")
'''


def c_delete(request, id):
    if 'customer_id' in request.session:
        print("---- Login cart ------------")
        cart = Cart.objects.get(cart_id=id)
        cart.delete()
        return redirect("/c/cart/")

    else:
        cart = c_Cart(request)
        product = Book.objects.get(b_id=id)
        cart.remove(product)
        return redirect("/c/cart/")


from django.db.models import Sum


def cart(request):
    if 'customer_id' in request.session:
        id = request.session['customer_id']
        c = Cart.objects.filter(u_id_id=id)
        count = Cart.objects.filter(u_id_id=id).count()
        if count > 0:
            p = c.aggregate(subtotal=Sum('amount'))['subtotal']
            print("--------p -----", p)
            gt = p + int(0)
        else:
            p = 0
            gt = 0
        sum = 0
        for val in c:
            sum = sum + (val.amount * val.qty)
        print("----------", sum)
        shipping = sum + 0
        return render(request, "cart.html", {"item": c, "total": sum, "shipping": shipping, "subtotal": p, "gt": gt})
    else:
        cart = c_Cart(request)
        total = cart.get_total_price()
        print(total)
        return render(request, "cart.html", {"subtotal": total})
    return render(request, "cart.html")


def creg(request):
    area = Area.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        print("-------------------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/c/clogin')
            except:
                print('------------------------', sys.exc_info())

    else:
        form = User()

    return render(request, 'customer_registration.html', {'form': form, 'area': area})


def customer_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = User.objects.filter(u_email=email, u_password=password).count()
        print("-------------------", email, "---------------------", password)
        if val == 1:
            data = User.objects.filter(u_email=email, u_password=password)
            for item in data:
                request.session['customer_id'] = item.u_id
                request.session['customer_fname'] = item.u_fname
                request.session['customer_lname'] = item.u_lname
                request.session['customer_email'] = item.u_email
                request.session['customer_pass'] = item.u_password

                if 'cart' in request.session:
                    product_ids = request.session['cart'].keys()
                    print("----------", product_ids)
                    products = Book.objects.filter(b_id__in=product_ids)
                    for product in product_ids:
                        val = request.session['cart'][product]
                        count = 0
                        list1 = []
                        for item in val:
                            list1.append(val[item])
                            print("++++++++++++++++++++++++++", list1[0])
                            count = count + 1
                            if count == 4:
                                cc1 = Cart.objects.filter(b_id_id=list1[0]).count()
                                print(cc1)
                                if cc1 == 0:
                                    d = date.today()
                                    uid = request.session["customer_id"]
                                    c = Cart(u_id_id=uid, b_id_id=list1[0], qty=int(list1[1]),
                                             amount=int(list1[1] * list1[2]), added_date=d)
                                    c.save()
                                else:
                                    c = Cart.objects.get(b_id_id=list1[0])
                                    c.qty = c.qty + int(list1[1])
                                    c.save()

                    cart = c_Cart(request)
                    cart.clear()

                if request.POST.get("remember"):
                    response = redirect("/c/main/")
                    response.set_cookie('cookie_cemail', request.POST["email"], 3600 * 24 * 365 * 2)
                    response.set_cookie('cookie_cpassword', request.POST["password"], 3600 * 24 * 365 * 2)
                    return response

            return redirect('/c/main/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/c/clogin/')
    else:
        if request.COOKIES.get("cookie_cemail"):
            return render(request, "customer_login.html",
                          {'customer_email_cookie': request.COOKIES['cookie_cemail'],
                           'customer_password_cookie': request.COOKIES['cookie_cpassword']})
        else:
            return render(request, "customer_login.html")


def customer_logout(request):
    try:
        del request.session['customer_id']
        del request.session['customer_fname']
        del request.session['customer_lname']
        del request.session['customer_email']

    except:
        pass
    return redirect("/c/clogin/")


import random
from django.core.mail import send_mail


def c_forgot(request):
    return render(request, "customer_forgot.html")


def otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['cemail']

    request.session['semail'] = e

    obj = User.objects.filter(u_email=e).count()

    if obj == 1:
        val = User.objects.filter(u_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'otp_page.html')

    else:
        messages.error(request, "Invalid Email")
        return render(request, "customer_forgot.html")


def change_password(request):
    if request.method == "POST":

        T_otp = request.POST['sotp']
        T_pass = request.POST['new_password']
        T_cpass = request.POST['confirm_password']

        if T_pass == T_cpass:

            e = request.session['semail']
            val = User.objects.filter(u_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                User.objects.filter(u_email=e).update(otp_used=1, u_password=T_pass)
                return redirect("/c/clogin")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "otp_page.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "otp_page.html")

    else:
        return redirect("/c/c_forgot")


import math
from .cart import c_Cart


def insert_cart(request, id):
    print("inside cart function")

    if request.method == "POST":
        print("-----------------------inside post")
        if 'customer_id' in request.session:

            try:
                u = request.session["customer_id"]
                val = Cart.objects.filter(u_id=u, b_id_id=id).count()
                if val == 1 or val > 1:
                    ct = Cart.objects.get(b_id_id=id, u_id=u)
                    print("----------", ct.u_id)
                    q = request.POST.get('qty')
                    if "demo_vertical2" in request.POST:
                        q = request.POST["demo_vertical2"]
                    total = int(ct.b_id.b_price) * int(q)
                    ct.amount = int(total) + int(ct.amount)
                    ct.qty = int(q) + int(ct.qty)
                    ct.save()
                else:
                    if "qty" in request.POST:
                        qty = request.POST["qty"]
                        print("0000000000000000000000000000000000", qty)
                    else:
                        qty = 1

                    if "demo_vertical2" in request.POST:
                        qty = request.POST["demo_vertical2"]

                    if "price" in request.POST:
                        print("------ price --------", request.POST["price"])
                        p = math.ceil(float(request.POST["price"]))

                    d = date.today().strftime("%Y-%m-%d")
                    print("-------------", u, qty, math.ceil(p), d)

                    # ccount = Cart.objects.filter(b_id=id).count()
                    # if ccount > 0:
                    #     obj = Cart.objects.get(b_id_id=id)
                    #     obj.qty = obj.qty + qty
                    #     obj.amount = obj.amount + (obj.b_id.b_price * qty)
                    #     obj.save()
                    # else:
                    #     print("--- Else -----")
                    C = Cart(u_id_id=u, b_id_id=id, qty=qty, amount=math.ceil(p), added_date=d)
                    C.save()


            except:
                print("-------", sys.exc_info())
            return redirect('/c/cart/')
        else:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&77")
            try:
                prd_id = id
                if "qty" in request.POST:
                    qty = request.POST["qty"]
                else:
                    qty = 1

                d = date.today()
                # prd_id = request.POST['product_id']

                if "product_name" in request.POST:
                    prd_name = request.POST['product_name']
                    amt = request.POST['amount']
                else:
                    data = Book.objects.get(b_id=id)
                    prd_name = data.b_name
                    amount = data.b_price

                    amt = data.b_price

                print("----", qty, "---------", amt)
                total = int(qty) * int(amt)

                cart = c_Cart(request)

                product_ids = request.session['cart'].keys()
                print("----------", product_ids)

                product = Book.objects.get(b_id=id)
                print(product)

                cart.add(product=product, quantity=int(qty))
                print(cart)


            except:
                print("-------", sys.exc_info())

            return redirect('/c/cart/')
        return render(request, "book_detail.html")


def update_qty(request, id):
    if 'customer_id' in request.session:
        print("----------inside function-----------")
        qty = request.GET.get('qty')
        val = Cart.objects.get(cart_id=id)

        b= Book.objects.get(b_id=val.b_id_id)
        print("==============",qty,"=================",b.b_qty)
        if int(qty) > int(b.b_qty):
            messages.error(request,"Not Enough Quantity available")
        else:
            new_qty = int(qty)
            total = new_qty * int(val.b_id.b_price)
            Cart.objects.filter(cart_id=id).update(qty=new_qty, amount=total)
            print("==============================================", val)

        return redirect('/c/cart/')

    else:
        cart = c_Cart(request)
        qty = int(request.GET.get('qty'))
        print("++++++++++++++++++++++++++++++++",qty)
        book = Book.objects.get(b_id=id)
        cart.add(product=book, quantity=qty , update_quantity=True)
        return redirect('/c/cart/')


def search(request):
    if request.method == "POST":
        name = request.POST["b_name"]
        prod = Book.objects.filter(b_name=name)
        pro = Book.objects.filter(b_name=name).count()
        if pro == 0:
            return render(request, 'search_error.html')
    else:
        print("++++++++++++++++++++++++++++++")
        prod = Book.objects.all()
    return render(request, 'new_books.html', {'book': prod})


from django.http import JsonResponse


def autosuggest(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(b_name__istartswith=request.GET.get('term'))

        names = list()

        for x in qs:
            names.append(x.b_name)
        return JsonResponse(names, safe=False)
    return render(request, "customer_header.html")


def c_profile(request):
    ui = request.session['customer_id']
    uid = User.objects.get(u_id=ui)
    form = ProfileForm(request.POST, instance=uid)

    print("*******************", form.errors)
    if form.is_valid():
        try:
            request.session['customer_fname'] = uid.u_fname
            request.session['customer_lname'] = uid.u_lname
            request.session['customer_email'] = uid.u_email

            print("new session fname-----------------", request.session['customer_fname'])
            print("new session lname-----------------", request.session['customer_lname'])
            print("new session email-----------------", request.session['customer_email'])


            form.save()
            return redirect("/c/main")

        except:
            print("+++", sys.exc_info())
    return render(request, 'customer_profile.html', {'uid': uid})


def c_checkout(request):
    if 'customer_id' in request.session:
        ui = request.session['customer_id']
        c = Cart.objects.filter(u_id_id=ui)
        uid = User.objects.get(u_id=ui)

        p = c.aggregate(subtotal=Sum('amount'))['subtotal']
        gt = p + 0

        sum = 0
        for val in c:
            sum = sum + (val.amount * val.qty)
        print("----------", sum)
        shipping = sum + 0
        return render(request, "customer_checkout.html",
                      {"item": c, "total": sum, "shipping": shipping, "subtotal": p, "gt": gt, "uid": uid})
    else:
        return redirect("/c/clogin/")


def orderlist(request):
    o = Order.objects.all()
    return render(request, "customer_orderlist.html", {'book': o})


def sort_product(request):
    sid = request.GET.get('sort')
    print("Ajax value -----" + sid)

    if 'customer_id' in request.session:
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)
        book_list = []
        for data in w:
            book_list.append(data['b_id'])
    else:
        book_list = []

    # subcat_id = request.session['s_id']
    # print("-----------session ---",request.session['s_id'])
    if sid == '1':

        print("----------- SORT PRODUCTS------" + sid)
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("product_price")

        if 'sub_id' in request.session:
            print("--------- subcategory found ----------")
            id = request.session['sub_id']
            results = Book.objects.filter(u_id_id=None, s_id=id).order_by("b_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
            print('------------==================--------------------', sub)
            sub_ids = [d['s_id'] for d in sub]

            results = Book.objects.filter(s_id_id__in=sub_ids, u_id_id=None).order_by("b_price")

        else:
            results = Book.objects.filter(u_id_id=None).order_by("b_price")
    else:
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("-product_price")
        print("----------- SORT PRODUCTS------" + sid + "---", 'sub_id' in request.session)
        if 'sub_id' in request.session:
            id = request.session['sub_id']
            results = Book.objects.filter(u_id_id=None, s_id=id).order_by("-b_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
            print('------------==================--------------------', sub)
            sub_ids = [d['s_id'] for d in sub]

            results = Book.objects.filter(s_id_id__in=sub_ids, u_id_id=None).order_by("-b_price")
        else:
            results = Book.objects.filter(u_id_id=None).order_by("-b_price")
    return render(request, 'sort.html', {'p': results, 'w': book_list})


def sort_product_list(request):
    sid = request.GET.get('sort')
    print("List Ajx value -----" + sid)
    uid = request.session['customer_id']
    w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
    print("--------------------", w)
    book_list = []
    for data in w:
        book_list.append(data['b_id'])
    # subcat_id = request.session['s_id']
    # print("-----------session ---",request.session['s_id'])
    if sid == '1':

        print("----------- SORT PRODUCTS------" + sid)
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("product_price")

        if 'sub_id' in request.session:
            print("--------- subcategory found ----------")
            id = request.session['sub_id']
            results = Book.objects.filter(u_id_id=None,is_available=1, s_id=id).order_by("b_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
            print('------------==================--------------------', sub)
            sub_ids = [d['s_id'] for d in sub]

            results = Book.objects.filter(s_id_id__in=sub_ids , is_available=1, u_id_id=None).order_by("b_price")

        else:
            results = Book.objects.filter(u_id_id=None, is_available=1).order_by("b_price")
    else:
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("-product_price")
        print("----------- SORT PRODUCTS------" + sid + "---", 'sub_id' in request.session)
        if 'sub_id' in request.session:
            id = request.session['sub_id']
            results = Book.objects.filter(u_id_id=None, s_id=id, is_available=1).order_by("-b_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
            print('------------==================--------------------', sub)
            sub_ids = [d['s_id'] for d in sub]
            results = Book.objects.filter(s_id_id__in=sub_ids, u_id_id=None, is_available=1).order_by("-b_price")
        else:
            results = Book.objects.filter(u_id_id=None, is_available=1).order_by("-b_price")
    return render(request, 'new_book_list_sort.html', {'p': results, 'w': book_list})


def sort_product1(request):
    sid = request.GET.get('sort')
    print("Sort Product1 Ajx value -----" + sid)
    # subcat_id = request.session['s_id']
    # print("-----------session ---",request.session['s_id'])
    if sid == '1':
        print("----------- SORT PRODUCTS------" + sid)
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("product_price")
        results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("b_price")
        if 'a_id' in request.session:
            id = request.session['a_id']
            user = User.objects.filter(a_id_id=id).values('u_id')
            u_ids = [d['u_id'] for d in user]
            results = Book.objects.filter(u_id_id__in=u_ids, is_available=1).order_by("b_price")
        else:
            results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("b_price")
    else:
        if 'a_id' in request.session:
            id = request.session['a_id']
            user = User.objects.filter(a_id_id=id).values('u_id')
            u_ids = [d['u_id'] for d in user]
            results = Book.objects.filter(u_id_id__in=u_ids, is_available=1).order_by("-b_price")
        else:
            results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("-b_price")

    return render(request, 'customer_grid_sort.html', {'p': results})


def customer_sort_list(request):
    sid = request.GET.get('sort')
    print("Sort Product1 Ajx value -----" + sid)
    # subcat_id = request.session['s_id']
    # print("-----------session ---",request.session['s_id'])
    if sid == '1':
        print("----------- SORT PRODUCTS------" + sid)
        # results = Product.objects.filter(subcat_id=subcat_id).order_by("product_price")
        results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("b_price")
        if 'a_id' in request.session:
            id = request.session['a_id']
            user = User.objects.filter(a_id_id=id).values('u_id')
            u_ids = [d['u_id'] for d in user]
            results = Book.objects.filter(u_id_id__in=u_ids, is_available=1).order_by("b_price")
        else:
            results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("b_price")
    else:
        if 'a_id' in request.session:
            id = request.session['a_id']
            user = User.objects.filter(a_id_id=id).values('u_id')
            u_ids = [d['u_id'] for d in user]
            results = Book.objects.filter(u_id_id__in=u_ids, is_available=1).order_by("-b_price")
        else:
            results = Book.objects.filter(u_id__gt=0, is_available=1).order_by("-b_price")

    return render(request, 'used_books_sort_list.html', {'p': results})


import razorpay


def ch(request):
    if request.method == 'POST':
        amount = 100
        currency = 'INR'
        client = razorpay.Client(auth=("rzp_test_Khgr98NxlZvmvM", "w9KZCzpdapUOkyBxDPreZeDZ"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, 'customer_checkout.html')


def place_orde1(request):
    print("==============================================")
    if request.session.has_key('customer_id'):
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['customer_id']
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", uid)
        ca = Cart.objects.filter(u_id_id=uid)
        p = request.POST.get('price')
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", p)

        print("======================", ord)
        amt = 0
        for val in ca:
            amt = amt + (int(val.b_id.b_price) * int(val.qty))
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = Order(u_id_id=uid, total_amount=amt, o_date=date1, payment_status='2', o_status=0)
        o.save()
        id = Order.objects.latest('o_id')
        print("---------************-----------order id--", id)
        c = Cart.objects.filter(u_id_id=uid)
        c1 = Cart.objects.filter(u_id_id=uid).count()
        print("+++++++++++++++++++++++++++++++++++", c1)
        if c1 >= 1:
            for data in c:
                pid = data.b_id_id
                qty = data.qty
                pri = data.b_id.b_price
                total = int(qty) * pri
                print("0000000000000000000000000000000000", total)
                od = Order_detail(Qty=int(qty), b_id_id=pid, o_id_id=id.o_id, Total_amount=total, Amount=amt)
                od.save()
            e = request.session['customer_email']
            obj = User.objects.filter(u_email=e).count()
            val = User.objects.get(u_email=e)
            print("---------------------------------------------", val)
            if obj == 1:
                ord1 = Order_detail.objects.filter(o_id_id=id)
                subject = 'Order Conformation'
                message = f'Dear {val.u_fname} {val.u_lname}, \n\n\t Your order has been accepted and will arrive soon. Order details are as follows:'
                message += f'\n------------------------------------'
                message += f'\n  Product name'
                message += f'\n------------------------------------'
                for data in ord1:
                    print("---------------------------------", data)
                    message += f'\n {data.b_id.b_name}'
                message += f'\n------------------------------------'
                message += f'\n  Total \t\t\t {amt}'
                message += f'\n------------------------------------'
                message += f'\n\n Thank uou,\n Regards Book Mania'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e, ]
                send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "customer_checkout.html")
        c_delete = Cart.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/c/cprofile/")
    return render(request, 'Client_checkout.html')


def place_orde(request):
    print("==============================================")
    if request.session.has_key('customer_id'):
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['customer_id']
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", uid)
        ca = Cart.objects.filter(u_id_id=uid)
        print("======================", ord)
        amt = 0
        for val in ca:
            amt = amt + (int(val.b_id.b_price) * int(val.qty))
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = Order(u_id_id=uid, total_amount=amt, o_date=date1, payment_status='1', o_status=0)
        o.save()
        id = Order.objects.latest('o_id')
        print("---------*********-----------order id--", id)
        c = Cart.objects.filter(u_id_id=uid)
        c1 = Cart.objects.filter(u_id_id=uid).count()
        print("+++++++++++++++++++++++++++++++++++", c1)
        if c1 >= 1:
            for data in c:
                pid = data.b_id_id
                qty = data.qty
                pri = data.b_id.b_price
                total = int(qty) * pri
                print("0000000000000000000000000000000000", total)
                od = Order_detail(Qty=int(qty), b_id_id=pid, o_id_id=id.o_id, Total_amount=total, Amount=amt)
                od.save()


                b = Book.objects.get(b_id=pid)
                b.b_qty = b.b_qty - qty
                print("---- QTY ----", b.b_qty)
                b.save()


            e = request.session['customer_email']
            obj = User.objects.filter(u_email=e).count()
            val = User.objects.get(u_email=e)
            print("---------------------------------------------", val)
            if obj == 1:
                ord1 = Order_detail.objects.filter(o_id_id=id)
                subject = 'Order Conformation'
                message = f'Dear {val.u_fname} {val.u_lname}, \n\n\t Your order has been accepted and will arrive soon. Order details are as follows:'
                message += f'\n---------------------------------------------------------------------'
                message += f'\n  Product name'
                message += f'\n----------------------------------------------------------------------'
                for data in ord1:
                    print("---------------------------------", data)
                    message += f'\n {data.b_id.b_name}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n  Total \t\t\t {amt}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n\n Thank uou,\n Regards Book Mania'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e, ]
                send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "customer_checkout.html")
        c_delete = Cart.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/c/cprofile/")
    return render(request, 'Client_checkout.html')


def place_order_customer(request, id):
    print("==============================================Inside function")
    if request.session.has_key('customer_id'):
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['customer_id']

        # b1=request.POST.get('b_id')
        print("666666666666666666666666666666666666666666666666666666666666666", id)
        # b = Book.objects.get(u_id_id=uid)
        # print("********************************************************",b1)

        b = Book.objects.get(b_id=id)
        print("888888888888888888888888888888888888888888888888", b.b_id)

        p = request.POST.get('price')
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", p)

        print("======================", ord)
        amt = 0
        amt = amt + (int(p) * 1)
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = Order(u_id_id=uid, total_amount=int(amt), o_date=date1, payment_status='1', o_status=0)
        o.save()
        o_id = Order.objects.latest('o_id')
        print("-------+++++++++++++++++**********-------------order id--", o_id.o_id)
        # print("+++++++++++++++++++++++++++++++++++", c1)
        od = Order_detail(Qty=1, b_id_id=id, o_id_id=o_id.o_id, Total_amount=amt, Amount=amt)
        od.save()
        print("+++++++ order details save ++++++++++++")
        e = request.session['customer_email']
        obj = User.objects.filter(u_email=e).count()
        val = User.objects.get(u_email=e)
        print("---------------------------------------------", val)
        if obj == 1:
            ord1 = Order_detail.objects.filter(o_id_id=id)
            subject = 'Order Conformation'
            message = f'Dear {val.u_fname} {val.u_lname}, \n\n\t Your order has been accepted and will arrive soon. Order details are as follows:'
            message += f'\n---------------------------------------------------------------------'
            message += f'\n  Product name'
            message += f'\n----------------------------------------------------------------------'
            for data in ord1:
                print("---------------------------------", data)
                message += f'\n {b.b_name}'
            message += f'\n----------------------------------------------------------------------'
            message += f'\n  Total \t\t\t {amt}'
            message += f'\n----------------------------------------------------------------------'
            message += f'\n\n Thank uou,\n Regards Book Mania'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "customer_checkout.html")
        c_delete = Cart.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/c/cprofile/")
    return render(request, 'customer_checkout2.html')


def place_order_customer1(request, id):
    print("==============================================Inside function")
    if request.session.has_key('customer_id'):
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['customer_id']

        # b1=request.POST.get('b_id')
        print("666666666666666666666666666666666666666666666666666666666666666", id)
        # b = Book.objects.get(u_id_id=uid)
        # print("********************************************************",b1)

        b = Book.objects.get(b_id=id)
        print("888888888888888888888888888888888888888888888888", b.b_id)

        p = request.POST.get('price')
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", p)

        print("======================", ord)
        amt = 0
        amt = amt + (int(p) * 1)
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = Order(u_id_id=uid, total_amount=int(amt), o_date=date1, payment_status='2', o_status=0)
        o.save()
        o_id = Order.objects.latest('o_id')
        print("-------+++++++++++++++++**********-------------order id--", o_id.o_id)
        # print("+++++++++++++++++++++++++++++++++++", c1)
        od = Order_detail(Qty=1, b_id_id=id, o_id_id=o_id.o_id, Total_amount=amt, Amount=amt)
        od.save()
        print("+++++++ order details save ++++++++++++")
        e = request.session['customer_email']
        obj = User.objects.filter(u_email=e).count()
        val = User.objects.get(u_email=e)
        print("---------------------------------------------", val)
        if obj == 1:
            ord1 = Order_detail.objects.filter(o_id_id=id)
            subject = 'Order Conformation'
            message = f'Dear {val.u_fname} {val.u_lname}, \n\n\t Your order has been accepted and will arrive soon. Order details are as follows:'
            message += f'\n---------------------------------------------------------------------'
            message += f'\n  Product name'
            message += f'\n----------------------------------------------------------------------'
            for data in ord1:
                print("---------------------------------", data)
                message += f'\n {b.b_name}'
            message += f'\n----------------------------------------------------------------------'
            message += f'\n  Total \t\t\t {amt}'
            message += f'\n----------------------------------------------------------------------'
            message += f'\n\n Thank uou,\n Regards Book Mania'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "customer_checkout.html")
        c_delete = Cart.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/c/cprofile/")
    return render(request, 'customer_checkout2.html')


def pay_cancel(request):
    return render(request, 'Payment_cancel.html')


def c_wishlist(request):
    if "customer_id" in request.session:
        id = request.session['customer_id']
        u = Wishlist.objects.filter(u_id_id=id)
    else:
        return redirect("/c/clogin/")
    return render(request, "customer_wishlist.html", {'us': u})


def cl_wishlist(request):
    if "customer_id" in request.session:
        if request.method == "POST":
            try:
                d = date.today().strftime("%Y-%m-%d")
                pid = request.POST.get("b_id")
                print("-----------------------------", pid)
                uid = request.session['customer_id']
                f = Wishlist.objects.filter(b_id_id=pid, u_id_id=uid).count()
                print("+++++++++++++++++++++++++++++++++++++", f)
                ab = int(1)
                if f == ab:
                    messages.error(request, "You Can't add! Item is already exist in wishlist")
                    return redirect('/c/cwishlist/')
                else:
                    obj = Wishlist(b_id_id=pid, u_id_id=uid)
                    obj.save()
                    return redirect('/c/cwishlist/')
            except:
                print("===============", sys.exc_info())
        return render(request, "customer_wishlist.html")
    else:
        return redirect("/c/clogin/")


def c_dwishlist(request, id):
    if 'customer_id' in request.session:
        wh = Wishlist.objects.get(w_id=id)
        wh.delete()
        return redirect("/c/cwishlist/")
    else:

        return redirect("/c/cwishlist/")


def customer_sell_page(request):
    sub_category = Sub_category.objects.all()
    language = Language.objects.all()
    if 'customer_id' in request.session:
        ui = request.session['customer_id']
        if request.method == "POST":
            form = CustomerBookForm(request.POST, request.FILES)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    handle_uploaded_file(request.FILES['b_img'])
                    form.save()
                    return redirect('/c/main/')
                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Book()

        return render(request, 'customer_sell_page.html',
                      {'form': form, 'sub_category': sub_category, 'language': language, 'ui': ui})
    else:
        return redirect("/c/clogin/")

def order_list1(request):
    if 'customer_id' in request.session:
        b = Book.objects.filter(u_id=request.session['customer_id']).values('b_id')
        print("-----------------------", b)
        o = Order_detail.objects.filter(b_id__in=b).values('o_id')
        print("-----------", o)
        order = Order.objects.filter(o_id__in=o)
        # order = Order.objects.filter(u_id=request.session['customer_id'])
        return render(request, "customer_order_list.html", {'o': order})
    else:
        return redirect("/c/clogin/")


def show_order_detail1(request, id):
    if 'customer_id' in request.session:
        od = Order_detail.objects.filter(o_id=id)
        return render(request, 'customer_show_list.html', {'order_detail': od})
    else:
        return render(request, "login.html")


def about_us(request):
    u = User.objects.all().count()
    f = Feedback.objects.all().count()
    b = Book.objects.all().count()
    a = Area.objects.all().count()

    feedback = Feedback.objects.all()

    return render(request, "customer_about_us.html", {"user": u, "feedback": f, "book": b, "area": a, "f": feedback})


def load_menu(request):
    c = Category.objects.all()
    s = Sub_category.objects.all()
    return render(request, "test.html", {"c": c, 's': s})


# def load_menu1(request):
#     w = Wishlist.objects.all().count()
#     print("777777777777777777777777777777777777777777",w)
#     return render(request, "test.html", {'w':w})

def customer_books(request):
    category = Category.objects.all()
    area = Area.objects.all()
    b = Book.objects.filter(u_id__gt=0, is_available=1)
    if 'sub_id' in request.session:
        del request.session['sub_id']

    if 'cat_id' in request.session:
        del request.session['cat_id']

    if 'a_id' in request.session:
        del request.session['a_id']

    return render(request, "customer_books.html", {'book': b, 'c': category, 'a': area})


def New_Books(request, id):
    category = Category.objects.all()
    sub = Sub_category.objects.get(s_id=id)
    b = Book.objects.filter(u_id_id=None, s_id_id=id)
    if 'customer_id' in request.session:
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)
        book_list = []
        for data in w:
            book_list.append(data['b_id'])
        print("--------------------------", book_list)
        request.session['sub_id'] = id
        print("------------- session set for sort ------------")
        return render(request, "new_books.html", {'book': b, 'c': category, 's': sub, 'books': book, 'w': book_list})
    else:
        return render(request, "new_books.html", {'book': b, 'c': category, 's': sub, 'books': book})


def New_book1(request):
    category = Category.objects.all()
    b = Book.objects.filter(u_id_id=None)

    if 'customer_id' in request.session:
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)

        if 'sub_id' in request.session:
            del request.session['sub_id']

        if 'cat_id' in request.session:
            del request.session['cat_id']

        book_list = []
        for data in w:
            book_list.append(data['b_id'])

        print("--------------------------", book_list)

        return render(request, "new_books.html", {'book': b, 'c': category, 'w': book_list})
    else:
        return render(request, "new_books.html", {'book': b, 'c': category})


def list(request):
    category = Category.objects.all()
    b = Book.objects.filter(u_id_id=None)

    if "customer_id" in request.session:
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)

        book_list = []
        for data in w:
            book_list.append(data['b_id'])
        return render(request, "list_view.html", {'book': b, 'c': category, 'w': book_list})
    else:
        return render(request, "list_view.html", {'book': b, 'c': category})

def customer_list(request):
    category = Category.objects.all()
    area = Area.objects.all()
    b = Book.objects.filter(u_id__gt=0, is_available= 1)
    return render(request, "customer_list.html", {'book': b, 'c': category, 'a': area})


def cat_book(request, id):
    sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
    sub_ids = [d['s_id'] for d in sub]
    b = Book.objects.filter(s_id_id__in=sub_ids, u_id_id=None)
    print('------------==================--------------------', b)
    category = Category.objects.all()


    if "customer_id" in request.session:
        request.session['cat_id'] = id
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)
        book_list = []
        for data in w:
            book_list.append(data['b_id'])
        print('------------==================--------------------', sub)


        return render(request, "new_books.html", {'book': b, 'c': category,'w': book_list})
    else:
        return render(request, "new_books.html", {'book': b, 'c': category})


def cat_book1(request, id):
    sub = Sub_category.objects.filter(c_id_id=id).values('s_id')
    sub_ids = [d['s_id'] for d in sub]
    b = Book.objects.filter(s_id_id__in=sub_ids, u_id_id=None)
    print('------------==================--------------------', b)
    category = Category.objects.all()

    if "customer_id" in request.session:
        request.session['cat_id'] = id
        uid = request.session['customer_id']
        w = Wishlist.objects.filter(u_id_id=uid).values('b_id')
        print("--------------------", w)
        book_list = []
        for data in w:
            book_list.append(data['b_id'])
        print('------------==================--------------------', sub)

        return render(request, "list_view.html", {'book': b, 'c': category, 'w': book_list})
    else:
        return render(request, "list_view.html", {'book': b, 'c': category})


def location_book(request, id):
    user = User.objects.filter(a_id_id=id).values('u_id')
    area = Area.objects.all()
    request.session['a_id'] = id
    # print('------------==================--------------------',sub)
    # [{s:1},{s:2}]
    u_ids = [d['u_id'] for d in user]
    # b = Book.objects.filter(s_id_id_in=sub_ids
    b = Book.objects.filter(u_id_id__in=u_ids, is_available=1)
    print('------------==================--------------------', b)
    category = Category.objects.all()

    return render(request, "customer_books.html", {'book': b, 'c': category, 'a': area})


def location_book1(request, id):
    user = User.objects.filter(a_id_id=id).values('u_id')
    area = Area.objects.all()
    request.session['a_id'] = id
    u_ids = [d['u_id'] for d in user]
    b = Book.objects.filter(u_id_id__in=u_ids, is_available=1)
    print('------------==================--------------------', b)
    category = Category.objects.all()

    return render(request, "customer_list.html", {'book': b, 'c': category, 'a': area})


def pay_success(request, id):
    place_orde(request)
    return render(request, 'Payment_success.html')


def payment_success(request, id):
    place_orde1(request)
    return render(request, "Payment_success.html")


def payment_success_customer(request, id):
    b1 = request.POST.get("b_id")
    place_order_customer(request, b1)
    return render(request, "Payment_success.html")


def payment_success_customer1(request, id):
    b1 = request.POST.get("b_id")
    print("555555555555555555555555555555555555555555555", b1)

    place_order_customer1(request, b1)
    return render(request, "Payment_success.html")


def success(request):
    return render(request, "Payment_success.html")


def customer_detail(request, id):
    b = Book.objects.get(b_id=id)
    f = Feedback.objects.filter(b_id=id)
    fb = Feedback.objects.filter(b_id=id).count()

    return render(request, "customer_book_detail.html", {'book': b, 'feed': f, 'count': fb})


def customer_checkout(request):
    print("00000000000000000000000000000000000000000inside function")
    if 'customer_id' in request.session:
        ui = request.session['customer_id']
        uid = User.objects.get(u_id=ui)
        p = request.POST.get('price')
        b = request.POST.get('b_id')
        print("999999999999999999999999999999999999999999999999999999", p)
        print("******************************************", b)
        sum = p
        return render(request, "customer_checkout2.html", {"subtotal": sum, "uid": uid, "book": b})
    else:
        return render(request,"customer_login.html")


def category(request):
    category = Category.objects.all()
    return render(request, "category.html", {'c': category})


def Mybook(request):
    if 'customer_id' in request.session:
        b = Book.objects.filter(u_id_id=request.session['customer_id'], is_available=1)
        total = Book.objects.filter(u_id_id=request.session['customer_id'], is_available=1) .count()
        return render(request, "my_books.html", {'book': b,'total': total})
    else:
        return redirect('/c/clogin/')


def insert_feedback(request):
    if 'customer_id' in request.session:
        if request.method == "POST":
            try:
                d = date.today()
                disc = request.POST.get("f_des")
                id = request.POST.get("b_id")
                id1 = request.POST.get("service_id")
                uid = request.session["customer_id"]
                f = Feedback(u_id_id=uid, f_date=d, f_des=str(disc), b_id_id=id)
                f.save()
                return redirect('/c/cdetail/%s' % id)

            except:
                print("---------------", sys, sys.exc_info())
        else:
            pass
        return render(request, "customer_book_detail.html")
    else:
        return redirect("/c/clogin/")


def order_list(request):
    if 'customer_id' in request.session:
        order = Order.objects.filter(u_id=request.session['customer_id'])
        return render(request, "order_list.html", {'o': order})
    else:
        return render(request, "customer_login.html")


def show_order_detail(request, id):
    if 'customer_id' in request.session:
        od = Order_detail.objects.filter(o_id=id)
        return render(request, 'show_list.html', {'order_detail': od})
    else:
        return render(request, "login.html")


def accept_order(request, id):
    if 'customer_id' in request.session:
        o = Order.objects.get(o_id=id)
        print("--000-------------", o)
        o.o_status = '1'
        o.save()
        o1 = Order_detail.objects.get(o_id=id)
        print("666666666666666666666666666666666666666666666666666666666666", o1.b_id)

        bk = Book.objects.get(b_id=o1.b_id_id)
        bk.is_available = 0
        bk.save()

        e = o.u_id.u_email
        print("--------------------------------", e)
        subject = 'Order Status'
        message = f'Dear {o.u_id.u_fname} {o.u_id.u_lname}, We have accept your order, Order is reach you soon.' \
                  f'your order id is {o.o_id}'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/c/main/')

    else:
        return render(request, "customer_show_list.html")


def reject_order(request, id):
    if 'customer_id' in request.session:
        o = Order.objects.get(o_id=id)
        o.o_status = '2'
        o.save()
        if o.payment_status == 1:
            e = o.u_id.u_email
            print("--------------------------------", e)
            subject = 'Order Status'
            message = f'Dear {o.u_id.u_fname} {o.u_id.u_lname}, We have regret to inform you, your order has been  \
             rejected  due to some technical issue.'

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list)
        else:
            e = o.u_id.u_email
            print("--------------------------------", e)
            subject = 'Order Status'
            message = f'Dear {o.u_id.u_fname} {o.u_id.u_lname}, We have regret to inform you, your order has been rejected  due to some technical issue. ' \
                      f'We will refund your amount in few days '

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list)
        return redirect('/c/main/')
    else:
        return render(request, "customer_show_list.html")


def customer_update_pass(request):
    if 'customer_id' in request.session:
        print("Umang")
        area = Area.objects.all()
        User_lemail = request.session['customer_email']
        passw = request.session['customer_pass']
        id1 = request.session['customer_id']
        T_pass = request.POST['pass']
        T_cpass = request.POST['cpass']

        val = User.objects.filter(u_email=User_lemail, u_password=passw, u_id=id1).count()
        user = User.objects.get(u_id=id1)
        print("------------------------------", val)

        if T_pass == T_cpass:
            val = User.objects.filter(u_email=User_lemail).count()
            if val == 1:
                User.objects.filter(u_email=User_lemail).update(u_password=T_pass)
                return redirect("/c/clogin/")
            else:
                messages.error(request, "Something went Wrong")
                return render(request, "set_password.html")
        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, 'customer_profile.html', {'uid': user, 'area': area})
    else:
        return render(request, "customer_login.html")


def destroy_used_book(request, bid):
    print("----------- Book delete --------------")
    bi = Book.objects.get(b_id=bid)
    bi.delete()

    return redirect('/c/mybook')
