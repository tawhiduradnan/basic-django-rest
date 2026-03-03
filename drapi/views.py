""""
views.py

App: drapi
Model: AiQuest
Serializer: AiQuestSerializers

This file documents the evolution of building REST APIs in Django REST Framework.

API Architecture Progression:

1️⃣ Pure Django (Manual JSON handling)
2️⃣ Function-Based Views (@api_view)
3️⃣ Class-Based APIView
4️⃣ GenericAPIView + Mixins
5️⃣ Concrete Generic Views
6️⃣ ModelViewSet + Router  ← CURRENT PRODUCTION STANDARD

Only the final stage (ModelViewSet) is used in URLs.
Previous stages are kept for learning reference only.
"""

# ============================================================
# Imports
# ============================================================

# Only required for Stage 1 (Pure Django)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io


from .models import AiQuest
from .serializers import AiQuestSerializers

# DRF Base Classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Generic Views + Mixins
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

# ViewSets (Final Stage)
from rest_framework import viewsets

from rest_framework.permissions import IsAdminUser


# ============================================================
# 🟡 STAGE 1 — PURE DJANGO (Manual JSON Handling)
# ============================================================

"""
✔ Uses:
    - HttpResponse
    - JSONRenderer
    - JSONParser
    - Manual error handling
    - @csrf_exempt

❌ No DRF automation
❌ No browsable API
❌ Fully manual CRUD
"""


# -------------------------------
# GET ALL
# -------------------------------
# def AiQuest_info(request):
#     ai = AiQuest.objects.all()
#     serializer = AiQuestSerializers(ai, many=True)
#     return HttpResponse(
#         JSONRenderer().render(serializer.data),
#         content_type='application/json'
#     )


# # -------------------------------
# # GET BY ID
# # -------------------------------
# def AiQuest_ins(request, pk):
#     try:
#         ai = AiQuest.objects.get(id=pk)
#     except AiQuest.DoesNotExist:
#         return HttpResponse(
#             JSONRenderer().render({'error': 'Record not found'}),
#             content_type='application/json',
#             status=404
#         )

#     serializer = AiQuestSerializers(ai)
#     return HttpResponse(
#         JSONRenderer().render(serializer.data),
#         content_type='application/json'
#     )


# # -------------------------------
# # POST, PUT, DELETE
# # -------------------------------
# @csrf_exempt
# def aiquest_create_manual(request):

#     # ---------- POST ----------
#     if request.method == 'POST':
#         stream = io.BytesIO(request.body)
#         python_data = JSONParser().parse(stream)
#         serializer = AiQuestSerializers(data=python_data)

#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(
#                 JSONRenderer().render({'message': 'Data inserted'}),
#                 content_type='application/json'
#             )

#         return HttpResponse(
#             JSONRenderer().render(serializer.errors),
#             content_type='application/json',
#             status=400
#         )

#     # ---------- PUT ----------
#     if request.method == 'PUT':
#         stream = io.BytesIO(request.body)
#         python_data = JSONParser().parse(stream)
#         id = python_data.get('id')

#         if not id:
#             return HttpResponse(
#                 JSONRenderer().render({'error': 'ID is required'}),
#                 content_type='application/json',
#                 status=400
#             )

#         try:
#             ai = AiQuest.objects.get(id=id)
#         except AiQuest.DoesNotExist:
#             return HttpResponse(
#                 JSONRenderer().render({'error': 'Record not found'}),
#                 content_type='application/json',
#                 status=404
#             )

#         serializer = AiQuestSerializers(ai, data=python_data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(
#                 JSONRenderer().render({'message': 'Data updated'}),
#                 content_type='application/json'
#             )

#         return HttpResponse(
#             JSONRenderer().render(serializer.errors),
#             content_type='application/json',
#             status=400
#         )

#     # ---------- DELETE ----------
#     if request.method == 'DELETE':
#         stream = io.BytesIO(request.body)
#         python_data = JSONParser().parse(stream)
#         id = python_data.get('id')

#         if not id:
#             return HttpResponse(
#                 JSONRenderer().render({'error': 'ID is required'}),
#                 content_type='application/json',
#                 status=400
#             )

#         try:
#             ai = AiQuest.objects.get(id=id)
#         except AiQuest.DoesNotExist:
#             return HttpResponse(
#                 JSONRenderer().render({'error': 'Record not found'}),
#                 content_type='application/json',
#                 status=404
#             )

#         ai.delete()
#         return HttpResponse(
#             JSONRenderer().render({'message': 'Data deleted'}),
#             content_type='application/json'
#         )

#     return HttpResponse(
#         JSONRenderer().render({'error': 'Only GET, POST, PUT, DELETE allowed'}),
#         content_type='application/json',
#         status=405
#     )


# # ============================================================
# # 🟡 STAGE 2 — FUNCTION-BASED VIEW (@api_view)
# # ============================================================

# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def aiquest_fbv(request, pk=None):

#     if request.method == 'GET':
#         if pk:
#             ai = AiQuest.objects.get(id=pk)
#             serializer = AiQuestSerializers(ai)
#             return Response(serializer.data)

#         ai = AiQuest.objects.all()
#         serializer = AiQuestSerializers(ai, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = AiQuestSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Successfully saved data'})
#         return Response(serializer.errors)

#     if request.method == 'PUT':
#         ai = AiQuest.objects.get(pk=pk)
#         serializer = AiQuestSerializers(ai, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Full Data Updated'})
#         return Response(serializer.errors)

#     if request.method == 'PATCH':
#         ai = AiQuest.objects.get(pk=pk)
#         serializer = AiQuestSerializers(ai, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Partial Data Updated'})
#         return Response(serializer.errors)

#     if request.method == 'DELETE':
#         ai = AiQuest.objects.get(pk=pk)
#         ai.delete()
#         return Response({'msg': 'Successfully deleted data'})


# # ============================================================
# # 🟡 STAGE 3 — CLASS-BASED VIEW (APIView)
# # ============================================================

# class AiquestCreate(APIView):

#     def get(self, request, pk=None, format=None):
#         if pk:
#             ai = AiQuest.objects.get(id=pk)
#             serializer = AiQuestSerializers(ai)
#             return Response(serializer.data)

#         ai = AiQuest.objects.all()
#         serializer = AiQuestSerializers(ai, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = AiQuestSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Successfully saved data'})
#         return Response(serializer.errors)

#     def put(self, request, pk=None, format=None):
#         ai = AiQuest.objects.get(pk=pk)
#         serializer = AiQuestSerializers(ai, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Full Data Updated'})
#         return Response(serializer.errors)

#     def patch(self, request, pk=None, format=None):
#         ai = AiQuest.objects.get(pk=pk)
#         serializer = AiQuestSerializers(ai, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Partial Data Updated'})
#         return Response(serializer.errors)

#     def delete(self, request, pk=None, format=None):
#         ai = AiQuest.objects.get(pk=pk)
#         ai.delete()
#         return Response({'msg': 'Successfully deleted data'})


# ============================================================
# 🟡 STAGE 4 — GenericAPIView + Mixins
# ============================================================
# ✔ Reusable logic
# ✔ Less repetition
# ✔ Cleaner structure
# ❌ Slightly verbose
# ============================================================

"""
class AiQuest_List_Create(GenericAPIView,
                          ListModelMixin,
                          CreateModelMixin):

    queryset = AiQuest.objects.all()
    serializer_class = AiQuestSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""
# ============================================================
# 🟡 STAGE 5 – Concrete Generic Views
# ============================================================
"""
Even cleaner.

Classes used:
- ListCreateAPIView
- RetrieveUpdateDestroyAPIView

Automatically handles CRUD with minimal code.
"""


class AiQuest_List_Create(ListCreateAPIView):
    """
    Handles:
    GET  /aiquest/
    POST /aiquest/
    """
    queryset = AiQuest.objects.all()
    serializer_class = AiQuestSerializers


class Aiquest_Retrieve_Update_Destroy(RetrieveUpdateDestroyAPIView):
    """
    Handles:
    GET     /aiquest/<pk>/
    PUT     /aiquest/<pk>/
    PATCH   /aiquest/<pk>/
    DELETE  /aiquest/<pk>/
    """
    queryset = AiQuest.objects.all()
    serializer_class = AiQuestSerializers


# ============================================================
# 🟢 STAGE 6 – MODEL VIEW SET (FINAL PRODUCTION VERSION)
# ============================================================
"""
ModelViewSet automatically provides:

- list()
- retrieve()
- create()
- update()
- partial_update()
- destroy()

When connected with a Router,
all URLs are generated automatically.

This is the most scalable and clean approach.
"""


class Aiquest_Model_View_Set(viewsets.ModelViewSet):
    """
    Complete CRUD API for AiQuest model.

    Router will automatically generate endpoints:
    - GET      /aiquest/
    - POST     /aiquest/
    - GET      /aiquest/{id}/
    - PUT      /aiquest/{id}/
    - PATCH    /aiquest/{id}/
    - DELETE   /aiquest/{id}/
    """

    queryset = AiQuest.objects.all()
    serializer_class = AiQuestSerializers
    permission_classes=[IsAdminUser]
