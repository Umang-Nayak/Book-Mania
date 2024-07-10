from django.db import models


# Create your models here.
class Area(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_name = models.CharField(max_length=100)
    a_pincode = models.IntegerField()

    class Meta:
        db_table = "area"

    def __str__(self):
        return f"{self.a_name} - {self.a_pincode}"


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_fname = models.CharField(max_length=20)
    u_lname = models.CharField(max_length=20)
    u_contact = models.CharField(max_length=13)
    u_address = models.CharField(max_length=50)
    u_email = models.EmailField(max_length=100)
    u_password = models.CharField(max_length=50)
    is_admin = models.IntegerField(null=True)
    a_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.u_email}"


class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_des = models.CharField(max_length=1000)

    class Meta:
        db_table = "category"

    def __str__(self):
        return f"{self.c_name}"


class Sub_category(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=20)
    s_des = models.CharField(max_length=500)
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_category"

    def __str__(self):
        return f"{self.c_id.c_name} - {self.s_name}"


class Language(models.Model):
    l_id = models.AutoField(primary_key=True)
    l_name = models.CharField(max_length=20)

    class Meta:
        db_table = "language"

    def __str__(self):
        return f"{self.l_name}"


class Book(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_name = models.CharField(max_length=200)
    b_price = models.IntegerField(null=False)
    b_qty = models.IntegerField(null=False)
    b_img = models.CharField(max_length=100)
    b_des = models.CharField(max_length=500)
    s_id = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    l_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_available = models.IntegerField(null=True)

    class Meta:
        db_table = "book"

    def __str__(self):
        return f"{self.b_name}"


class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    o_date = models.DateField(null=False)
    o_status = models.IntegerField(null=False)
    payment_status = models.IntegerField(null=False)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField(null=False)

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"{self.u_id.u_email} | {self.o_date} | {self.o_status}"


class Order_detail(models.Model):
    od_id = models.AutoField(primary_key=True)
    Qty = models.IntegerField(null=False)
    Amount = models.IntegerField(null=False)
    Total_amount = models.IntegerField(null=False)
    o_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = "order_detail"

    def __str__(self):
        return f"{self.b_id.b_name} | {self.Amount}"


class Wishlist(models.Model):
    w_id = models.AutoField(primary_key=True)
    b_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "wishlist"

    def __str__(self):
        return f"{self.b_id.b_name} - {self.u_id.u_email}"


class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_date = models.CharField(max_length=10)
    f_des = models.CharField(max_length=500)
    b_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "feedback"

    def __str__(self):
        return f"{self.b_id.b_name} - {self.u_id.u_email} - {self.f_des}"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.PROTECT)
    b_id = models.ForeignKey(Book, on_delete=models.PROTECT)
    qty = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    added_date = models.DateField(null=False)

    class Meta:
        db_table = "cart"

    def __str__(self):
        return f"{self.b_id.b_name} - {self.u_id.u_email} - {self.amount}"
