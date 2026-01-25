from books.models import Book
for b in Book.objects.filter(status='Approved'):
    b.status = 'Published'
    b.save()
print("Migrated books.")
