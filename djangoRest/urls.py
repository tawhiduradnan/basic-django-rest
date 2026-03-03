"""
urls.py

Project URL Configuration
App: drapi
Primary Model: AiQuest

====================================================================
Django REST Framework – URL Routing Architecture
====================================================================

This file demonstrates routing evolution aligned with the API stages
defined in views.py.

Only the final stage (ModelViewSet + Router) is ACTIVE.

All other routes remain commented for learning reference and
architectural comparison.

Active Stage:
✔ Stage 6 — ModelViewSet + DefaultRouter (Production Standard)

Commented Stages:
1️⃣ Pure Django Views
2️⃣ Function-Based Views (@api_view)
3️⃣ APIView (Class-Based Views)
4️⃣ GenericAPIView + Mixins
5️⃣ Concrete Generic Views
"""

# ============================================================
# Core Django Imports
# ============================================================

from django.contrib import admin
from django.urls import include, path

# App Views
from drapi import views

# DRF Router
from rest_framework.routers import DefaultRouter

# ============================================================
# Router Configuration (Stage 6 – Production Standard)
# ============================================================

"""
DefaultRouter automatically generates:

GET       /aiquest/
POST      /aiquest/
GET       /aiquest/{id}/
PUT       /aiquest/{id}/
PATCH     /aiquest/{id}/
DELETE    /aiquest/{id}/

No manual URL patterns required.
"""
router = DefaultRouter()
# Register ModelViewSet
# basename is required when queryset is defined inside ViewSet
router.register('aiquest', views.Aiquest_Model_View_Set, basename='teacher')


# ============================================================
# URL Patterns
# ============================================================

urlpatterns = [

    # Django Admin Panel
    path('admin/', admin.site.urls),

    # DRF Login/Logout for Browsable API
    path('api-auth/', include('rest_framework.urls')),

    # ============================================================
    # 🔵 PREVIOUS STAGES (Commented for Learning Reference)
    # ============================================================

    # -------------------------------
    # Stage 1 — Pure Django Views
    # -------------------------------
    # path('aiinfo/', views.AiQuest_info),
    # path('aiinfo/<int:pk>', views.AiQuest_ins),

    # -------------------------------
    # Stage 2 — Function-Based View
    # -------------------------------
    # (Not separately mapped here; would require manual mapping)

    # -------------------------------
    # Stage 3 — APIView (Class-Based)
    # -------------------------------
    # path('aicreate/<int:pk>', views.AiquestCreate.as_view()),
    # path('aicreate/', views.AiQuestCreate.as_view(), name='aicreate'),

    # -------------------------------
    # Stage 4 — GenericAPIView + Mixins
    # -------------------------------
    # (Would require separate list/detail mappings)

    # -------------------------------
    # Stage 5 — Concrete Generic Views
    # -------------------------------
    # path('ailistcreate/', views.AiQuest_List_Create.as_view(),
    #      name='ai_list_create'),

    # path('airetreive/<int:pk>',
    #      views.Aiquest_Retrieve_Update_Destroy.as_view(),
    #      name='ai_retrieve_update_destroy'),

    # Alternative Combined Mapping Example
    # path('aiquest/', views.AiQuest_List_Create.as_view()),
    # path('aiquest/<int:pk>',
    #      views.Aiquest_Retrieve_Update_Destroy.as_view()),

    # ============================================================
    # 🟢 Stage 6 — ModelViewSet (ACTIVE)
    # ============================================================

    # Automatically generated RESTful routes
    path('', include(router.urls)),
]