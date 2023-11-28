import datetime
import sys
from django.shortcuts import render, redirect
from book_admin.forms import AreaForm, CategoryForm, Sub_CategoryForm, LanguageForm, BookForm, AdminForm, ImageForm
from book_admin.functions import handle_uploaded_file
from book_admin.models import Area, User, Category, Sub_category, Language, Book, Order, Order_detail, Wishlist, \
    Feedback
from django.contrib import messages
from book import settings


# Create your views here.
def show(request):
    return render(request, "export-table.html")


def show_area(request):
    if 'admin_id' in request.session:
        area = Area.objects.all()
        return render(request, "area.html", {'a': area})
    else:
        return render(request, "login.html")


def show_user(request):
    if 'admin_id' in request.session:
        user = User.objects.all()
        return render(request, "user.html", {'u': user})
    else:
        return render(request, "login.html")


def show_category(request):
    if 'admin_id' in request.session:
        category = Category.objects.all()
        return render(request, "category.html", {'c': category})
    else:
        return render(request, "login.html")


def show_sub_category(request):
    if 'admin_id' in request.session:
        sub_category = Sub_category.objects.all()
        return render(request, "sub_category.html", {'s': sub_category})
    else:
        return render(request, "login.html")


def show_language(request):
    if 'admin_id' in request.session:
        language = Language.objects.all()
        return render(request, "language.html", {'l': language})
    else:
        return render(request, "login.html")


def show_book(request):
    if 'admin_id' in request.session:
        book = Book.objects.all()
        return render(request, "book.html", {'b': book})
    else:
        return render(request, "login.html")


def show_order(request):
    if 'admin_id' in request.session:
        order = Order.objects.all()
        return render(request, "order.html", {'o': order})
    else:
        return render(request, "login.html")


def show_order_detail(request):
    if 'admin_id' in request.session:
        order_detail = Order_detail.objects.all()
        return render(request, "order_detail.html", {'od': order_detail})
    else:
        return render(request, "login.html")


def show_wishlist(request):
    if 'admin_id' in request.session:
        wishlist = Wishlist.objects.all()
        return render(request, "wishlist.html", {'w': wishlist})
    else:
        return render(request, "login.html")


def show_feedback(request):
    if 'admin_id' in request.session:
        feedback = Feedback.objects.all()
        return render(request, "feedback.html", {'f': feedback})
    else:
        return render(request, "login.html")


def destroy_area(request, aid):
    if 'admin_id' in request.session:
        ai = Area.objects.get(a_id=aid)
        ai.delete()
        return redirect("/area")
    else:
        return render(request, "login.html")


def update_area(request, ai):
    if 'admin_id' in request.session:
        aid = Area.objects.get(a_id=ai)
        form = AreaForm(request.POST, instance=aid)
        if form.is_valid():
            form.save()
            return redirect("/area")
        return render(request, 'Area-update.html', {'aid': aid})
    else:
        return render(request, "login.html")


def destroy_language(request, lid):
    if 'admin_id' in request.session:
        li = Language.objects.get(l_id=lid)
        li.delete()
        return redirect("/language")
    else:
        return render(request, "login.html")


def update_language(request, li):
    if 'admin_id' in request.session:
        lid = Language.objects.get(l_id=li)
        form = LanguageForm(request.POST, instance=lid)
        if form.is_valid():
            form.save()
            return redirect("/language")
        return render(request, 'Language-update.html', {'lid': lid})
    else:
        return render(request, "login.html")


def destroy_book(request, bid):
    if 'admin_id' in request.session:
        bi = Book.objects.get(b_id=bid)
        bi.delete()
        return redirect("/book")
    else:
        return render(request, "login.html")


def update_book(request, bi):
    if 'admin_id' in request.session:
        sub_category = Sub_category.objects.all()
        language = Language.objects.all()
        bid = Book.objects.get(b_id=bi)
        form = BookForm(request.POST, instance=bid)
        print("--------------------------",form.errors)
        if form.is_valid():
            form.save()
            return redirect("/book")
        return render(request, 'Book-update.html', {'bid': bid, 'sub_category': sub_category, 'language': language})
    else:
        return render(request, "login.html")


def update_image(request, bi):
    if 'admin_id' in request.session:
        bid = Book.objects.get(b_id=bi)

        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES, instance=bid)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    handle_uploaded_file(request.FILES['b_img'])
                    form.save()
                    return redirect('/book/')

                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Book()

        return render(request, 'update_image.html', {'form': form,'bid':bid})
    else:
        return render(request, "login.html")


def destroy_category(request, cid):
    if 'admin_id' in request.session:
        ci = Category.objects.get(c_id=cid)
        ci.delete()
        return redirect("/category")
    else:
        return render(request, "login.html")


def update_category(request, ci):
    if 'admin_id' in request.session:
        cid = Category.objects.get(c_id=ci)
        form = CategoryForm(request.POST, instance=cid)
        if form.is_valid():
            form.save()
            return redirect("/category")
        return render(request, 'Category-update.html', {'cid': cid})
    else:
        return render(request, "login.html")


def destroy_sub_category(request, sid):
    if 'admin_id' in request.session:
        si = Sub_category.objects.get(s_id=sid)
        si.delete()
        return redirect("/sub_category")
    else:
        return render(request, "login.html")


def update_sub_category(request, si):
    if 'admin_id' in request.session:
        category = Category.objects.all()
        sid = Sub_category.objects.get(s_id=si)
        form = Sub_CategoryForm(request.POST, instance=sid)
        if form.is_valid():
            form.save()
            return redirect("/sub_category")
        return render(request, 'Sub_category-update.html', {'sid': sid, 'category': category})
    else:
        return render(request, "login.html")


def destroy_feedback(request, fid):
    if 'admin_id' in request.session:
        fi = Feedback.objects.get(f_id=fid)
        fi.delete()
        return redirect("/feedback")
    else:
        return render(request, "login.html")


def destroy_wishlist(request, wid):
    if 'admin_id' in request.session:
        wi = Wishlist.objects.get(w_id=wid)
        wi.delete()
        return redirect("/wishlist")
    else:
        return render(request, "login.html")


def destroy_user(request, uid):
    if 'admin_id' in request.session:
        ui = User.objects.get(u_id=uid)
        ui.delete()
        return redirect("/user")
    else:
        return render(request, "login.html")


from django.db import connection
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response


# from Order.models import order


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {"customers": 10})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # qs = Company.objects.all()

        cursor = connection.cursor()
        cursor.execute(
            '''select b.b_name as name , sum(Total_amount) as total from Order_detail o join book b where o.b_id_id = b.b_id GROUP by b.b_id;''')
        qs = cursor.fetchall()

        labels = []
        default_items = []

        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


from django.db.models import Sum


def show_dashboard(request):
    if 'admin_id' in request.session:
        u = User.objects.all().count()
        o = Order.objects.all().count()
        b = Book.objects.all().count()
        i = Order.objects.aggregate(total=Sum('total_amount'))
        i = i['total']

        date = datetime.date.today()
        today = Order.objects.filter(o_date=date)

        return render(request, "index.html", {"user": u, "order": o, "book": b, "income": i, "t": today})
    else:
        return render(request, "login.html")


def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = User.objects.filter(u_email=email, u_password=password, is_admin=1).count()
        print("-------------------", email, "---------------------", password)
        if val == 1:
            data = User.objects.filter(u_email=email, u_password=password, is_admin=1)
            for item in data:
                request.session['admin_id'] = item.u_id
                request.session['admin_fname'] = item.u_fname
                request.session['admin_lname'] = item.u_lname
                request.session['admin_email'] = item.u_email
                request.session['admin_pass'] = item.u_password

                if request.POST.get("remember"):
                    response = redirect("/dashboard/")
                    response.set_cookie('cookie_aemail', request.POST["email"], 3600 * 24 * 365 * 2)
                    response.set_cookie('cookie_apassword', request.POST["password"], 3600 * 24 * 365 * 2)
                    return response

            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
    else:
        if request.COOKIES.get("cookie_aemail"):
            return render(request, "login.html", {'admin_email_cookie': request.COOKIES['cookie_aemail'],
                                                  'admin_password_cookie': request.COOKIES['cookie_apassword']})
        else:
            return render(request, "login.html")


def admin_logout(request):
    if 'admin_id' in request.session:
        try:
            del request.session['admin_id']
            del request.session['admin_fname']
            del request.session['admin_lname']
            del request.session['admin_email']
        except:
            pass
        return redirect("/login/")
    else:
        return render(request, "login.html")


def insert(request):
    if 'admin_id' in request.session:
        return render(request, "form-insert.html")
    else:
        return render(request, "login.html")


def insert_Area(request):
    if 'admin_id' in request.session:
        if request.method == "POST":
            form = AreaForm(request.POST)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    form.save()
                    return redirect('/area')
                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Area()

        return render(request, 'Area-insert.html', {'form': form})
    else:
        return render(request, "login.html")


def insert_Category(request):
    if 'admin_id' in request.session:
        if request.method == "POST":
            form = CategoryForm(request.POST)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    form.save()
                    return redirect('/category')
                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Category()

        return render(request, 'Category-insert.html', {'form': form})
    else:
        return render(request, "login.html")


def insert_Sub_Category(request):
    if 'admin_id' in request.session:
        category = Category.objects.all()
        if request.method == "POST":
            form = Sub_CategoryForm(request.POST)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    form.save()
                    return redirect('/sub_category')

                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Sub_category()

        return render(request, 'Sub_Category-insert.html', {'form': form, 'category': category})
    else:
        return render(request, "login.html")


def insert_Language(request):
    if 'admin_id' in request.session:
        if request.method == "POST":
            form = LanguageForm(request.POST)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    form.save()
                    return redirect('/language')
                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Language()

        return render(request, 'Language-insert.html', {'form': form})
    else:
        return render(request, "login.html")


def insert_Book(request):
    if 'admin_id' in request.session:
        sub_category = Sub_category.objects.all()
        language = Language.objects.all()

        if request.method == "POST":
            form = BookForm(request.POST, request.FILES)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    handle_uploaded_file(request.FILES['b_img'])
                    form.save()
                    return redirect('/book/')

                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Book()

        return render(request, 'Book-insert.html', {'form': form,
                                                    'sub_category': sub_category,
                                                    'language': language})
    else:
        return render(request, "login.html")


from django.core.mail import send_mail
import random


def forgot(request):
    return render(request, "forgot.html")


def sendotp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = User.objects.filter(u_email=e).count()

    if obj == 1:
        val = User.objects.filter(u_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'set_password.html')

    else:
        messages.error(request, "Invalid Email")
        return render(request, "forgot.html")


def set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['npassword']
        T_cpass = request.POST['cpassword']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = User.objects.filter(u_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                User.objects.filter(u_email=e).update(otp_used=1, u_password=T_pass)
                return redirect("/login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "set_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/forgot_password")


def show_profile(request):
    if 'admin_id' in request.session:
        area = Area.objects.all()
        ui = request.session['admin_id']
        uid = User.objects.get(u_id=ui)
        form = AdminForm(request.POST, instance=uid)
        print("*******************", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/dashboard/")
            except:
                print("+++", sys.exc_info())
        return render(request, 'profile.html', {'uid': uid, 'area': area})
    else:
        return render(request, "login.html")


def update_pass(request):
    if 'admin_id' in request.session:
        print("Umang")
        area = Area.objects.all()
        User_lemail = request.session['admin_email']
        passw = request.session['admin_pass']
        id1 = request.session['admin_id']
        T_pass = request.POST['pass']
        T_cpass = request.POST['cpass']

        val = User.objects.filter(u_email=User_lemail, u_password=passw, u_id=id1).count()
        user = User.objects.get(u_id=id1)
        print("------------------------------", val)

        if T_pass == T_cpass:
            val = User.objects.filter(u_email=User_lemail).count()
            if val == 1:
                User.objects.filter(u_email=User_lemail).update(u_password=T_pass)
                return redirect("/dashboard/")
            else:
                messages.error(request, "Something went Wrong")
                return render(request, "set_password.html")
        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, 'profile.html', {'uid': user , 'area':area})
    else:
        return render(request, "login.html")


def order_report1(request):
    if 'admin_id' in request.session:
        # sql = "SELECT 1 as o_item_id, (SELECT product.p_name as name FROM product WHERE p_id = order_item.p_id_id) as name,sum(o_item_amount) as total FROM order_item JOIN product on order_item.o_item_id = product.p_id GROUP BY p_id_id;"
        sql = "SELECT 1 as od_id, b.b_name as name, sum(Amount) as total FROM order_detail i JOIN book b where b.b_id = i.b_id_id GROUP by b_id_id"
        od = Order_detail.objects.raw(sql)
        return render(request, "order_sell.html", {'order': od})
    else:
        return render(request, "login.html")


from django.utils.dateparse import parse_date


def order_report2(request):
    if 'admin_id' in request.session:
        if request.method == "POST":
            print("hello---------------")
            s_d = request.POST.get('start_date')
            e_d = request.POST.get('end_date')
            start = parse_date(s_d)
            end = parse_date(e_d)
            od = Order.objects.filter(o_date__range=[start, end])
            # sql = "SELECT * FROM order_table o JOIN order_item i where o.order_id = i.order_id_id and o.order_date >= %s and o.order_date <= %s;"
            # ord = Order_item.objects.raw(sql,[s_d,e_d])
        else:
            od = Order.objects.all()
        return render(request, "order_sell2.html", {'order': od})
    else:
        return render(request, "login.html")


def order_report3(request):
    if 'admin_id' in request.session:
        sc = Sub_category.objects.all()
        if request.method == "POST":
            pr1 = request.POST.get('s_id')
            print("-------------------", pr1)
            b = Book.objects.filter(s_id=pr1)

        else:
            b = Book.objects.all()

        return render(request, 'order_sell3.html', {'book': b, 'scat': sc})
    else:
        return render(request, "login.html")


def order_report4(request):
    if 'admin_id' in request.session:
        c = Category.objects.all()
        if request.method == "POST":
            pr1 = request.POST.get('c_id')
            print("-------------------", pr1)
            s = Sub_category.objects.filter(c_id=pr1)

        else:
            s = Sub_category.objects.all()

        return render(request, 'order_sell4.html', {'sub_category': s, 'cat': c})
    else:
        return render(request, "login.html")


def order_report5(request):
    if 'admin_id' in request.session:
        a = Area.objects.all()
        if request.method == "POST":
            pr1 = request.POST.get('a_id')
            print("-------------------", pr1)
            u = User.objects.filter(a_id=pr1)

        else:
            u = User.objects.all()

        return render(request, 'order_sell5.html', {'user': u, 'area': a})
    else:
        return render(request, "login.html")


def accept_order(request, id):
    if 'admin_id' in request.session:
        o = Order.objects.get(o_id=id)
        o.o_status = '1'
        o.save()
        e = o.u_id.u_email
        print("--------------------------------", e)
        subject = 'Order Status'
        message = f'Dear {o.u_id.u_fname} {o.u_id.u_lname}, We have accept your order, Order is reach you soon.' \
                  f'your order id is {o.o_id}'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/order/')
    else:
        return render(request, "login.html")


def reject_order(request, id):
    if 'admin_id' in request.session:
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
        return redirect('/order/')
    else:
        return render(request, "login.html")
