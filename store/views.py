from .models import Product, Category, Comment
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer




class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer= CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class ProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


# فیلد 'تعداد' را باید اضافه کنم
class CategoryProductsView(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        my_data = Product.objects.filter(category=category)
        products = ProductSerializer(my_data, many=True, context={'request': request})
        return Response(products.data)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        global product
        product = Product.objects.get(id=product_id)
        comments = product.product_comments.filter(is_reply=False)
        product_serializer = ProductSerializer(product, context={'request': request})
        comments_serializer = CommentSerializer(comments, context={'request': request}, many=True)
        global my_data
        my_data = {'product': product_serializer.data, 'comments': comments_serializer.data}
        return Response(my_data)
    
    def post(self, request, *args, **kwargs):
        comment = request.data
        new_comment = Comment.objects.create(
            product = product,
            author = request.user,
            reply = comment['reply'],
            is_reply = False,
            body = comment['body'],
        )
        new_comment.save()
        return Response(my_data)


class AllProducts(APIView):
    def get(self, request):
        if request.GET.get('search'):
            products = Product.objects.filter(title__contains=request.GET['search'])
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)


class AddReply(APIView):
    def get(self, request, product_id, comment_id):
        global product, comment
        product = Product.objects.get(id=product_id)
        comment = Comment.objects.get(id=comment_id)
        product_serializer = ProductSerializer(product)
        comment_serializer = CommentSerializer(comment)
        return Response({'product': product_serializer.data, 'The desired comment': comment_serializer.data})

    def post(self, request, product_id, comment_id):
        reply_comment = request.data
        Comment.objects.create(
            author = request.user,
            product = product,
            reply = comment,
            body = reply_comment['body'],
            is_reply = True,
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

