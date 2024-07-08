"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url
from django.conf.urls.static import static
from experiment import views
from django.conf import settings

urlpatterns = [
    path('', views.home_view),
    path('ccw/admin/', admin.site.urls),
    path('ccw/api/create_subject', views.create_subject),
    path('ccw/api/get_subject_info', views.get_subject_info),
    path('ccw/api/create_without_AI_subject', views.create_without_AI_subject),
    path('ccw/api/create_group_subject', views.create_group_subject),
    path('ccw/api/pre_survey', views.pre_survey),
    path('ccw/api/record_qualified_task', views.record_qualified_task),
    path('ccw/api/complete_qualification', views.complete_qualification),
    path('ccw/api/failed_qualification', views.failed_qualification),
    path('ccw/api/create_single_subject', views.create_single_subject),
    path('ccw/api/unqualified', views.unqualified),
    path('ccw/api/record_practice', views.record_practice),
    path('ccw/api/record_avatar', views.record_avatar),
    path('ccw/api/pairing', views.pairing),
    path('ccw/api/record_single_formal', views.record_single_formal),
    path('ccw/api/record_single_confidence', views.record_single_confidence),
    path('ccw/api/understanding_survey', views.understanding_survey),
    path('ccw/api/accountability_survey', views.accountability_survey),
    path('ccw/api/get_train', views.get_train),
    path('ccw/api/get_formal', views.get_formal),
    path('ccw/api/get_correct_answer', views.get_correct_answer),
    path('ccw/api/show_bonus', views.show_bonus),
    path('ccw/api/submittomtruk', views.submit_to_mtruk),
    path('ccw/api/formal_start', views.formal_start),
    path('ccw/api/gpt_response', views.get_gpt_response),
    path('ccw/api/post_survey', views.post_survey),
    path('ccw/erwtwt/import_defendant', views.import_defendant)
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)