from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
from rest_framework import status
import numpy as np

# Create your views here.


class NotFoundException(Exception):
    pass


def function2(arr, kth):
    return np.percentile(arr, kth)


def function1(x, kth):
    y = x['scores']
    j = y.split(',')
    ans = []
    for i in range(0, len(j)):
        ans.append(float(j[i]))
    rr = function2(ans, kth)
    return rr


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_product(self, pid):
        try:
            product = Product.objects.get(id=pid)
            return product
        except:
            raise NotFoundException()

    def get(self, request, pid, kth):
        try:
            product = self.get_product(pid)
            serializer = ProductSerializer(product)
            rr = function1(serializer.data, kth)
            # print(serializer.data)
            return Response(rr)

        except NotFoundException:
            return Response(status=status.HTTP_404_NOT_FOUND)
