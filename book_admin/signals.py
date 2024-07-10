import pandas as pd
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Area, Language, Category


@receiver(post_migrate)
def create_areas_from_csv(sender, **kwargs):
    if sender.name == 'book_admin':
        # Path to your CSV file
        csv_file_path = 'book_admin/data/area_pincode.csv'

        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Iterate over rows and create Area objects if they don't exist
        for index, row in df.iterrows():
            area_name = row['Area']
            pincode = row['Pincode']

            # Check if the area already exists
            area, created = Area.objects.get_or_create(a_name=area_name, a_pincode=pincode)

            # Optionally, you can print or log the creation status
            if created:
                print(f"Created Area: {area_name}, Pincode: {pincode}")
            else:
                print(f"Area already exists: {area_name}, Pincode: {pincode}")


@receiver(post_migrate)
def create_languages(sender, **kwargs):
    if sender.name == 'book_admin':

        list_of_languages = [
            "English",
            "Spanish",
            "Russian",
            "Hindi",
            "Japanese",
            "Chinese",
            "Gujarati",
            "Sanskrit",
            "Marathi"
        ]

        for language in list_of_languages:
            already, created = Language.objects.get_or_create(l_name=language)
            if created:
                print(f"Created Language: {language}")
            else:
                print(f"Language already exists: {language}")


@receiver(post_migrate)
def create_categories_from_csv(sender, **kwargs):
    if sender.name == 'book_admin':
        csv_file_path = 'book_admin/data/category-and-description.csv'
        df = pd.read_csv(csv_file_path)

        for index, row in df.iterrows():
            category_name = row['Category']
            category_description = row['Description']
            area, created = Category.objects.get_or_create(c_name=category_name, c_des=category_description)

            if created:
                print(f"Created Category: {category_name}")
            else:
                print(f"Category already exists: {category_name}")
