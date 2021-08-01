from productCreate.models import Products, Category, SubCategory,ProductSize

def categories(request):
    hello = Category.objects.all()
    return {'categories': hello}