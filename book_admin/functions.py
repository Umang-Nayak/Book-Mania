def handle_uploaded_file(f):
    with open('book_admin/static/assets/img/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            