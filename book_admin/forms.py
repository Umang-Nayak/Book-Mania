from django import forms
from book_admin.models import Area, Category, Sub_category, Language, Book, User
from parsley.decorators import parsleyfy


@parsleyfy
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["a_name", "a_pincode"]


@parsleyfy
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["c_name", "c_des"]


@parsleyfy
class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_category
        fields = ["s_name", "s_des", "c_id"]


@parsleyfy
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["l_name"]


@parsleyfy
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["u_fname", "u_lname", "u_contact", "u_address", "u_email", "u_password", "a_id"]


@parsleyfy
class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["u_fname", "u_lname", "u_contact", "u_address", "u_email", "a_id", 'is_admin']


@parsleyfy
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["u_fname", "u_lname", "u_contact", "u_address", "u_email"]


@parsleyfy
class ImageForm(forms.ModelForm,):
    b_img = forms.FileField()

    class Meta:
        model = Book
        fields = ["b_img"]


@parsleyfy
class BookForm(forms.ModelForm,):
    b_img = forms.FileField()

    class Meta:
        model = Book
        fields = ["b_name", "b_price", "b_qty", "b_img", "b_des", "s_id", "l_id", "is_available"]


class CustomerBookForm(forms.ModelForm,):
    b_img = forms.FileField()

    class Meta:
        model = Book
        fields = ["b_name", "b_price", "b_qty", "b_img", "b_des", "s_id", "l_id", "u_id", "is_available"]
