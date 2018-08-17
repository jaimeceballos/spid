from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
   
from functools import wraps
  
from django.contrib.auth.models import Group,Permission,User
from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import Http404
   
def group_required(groups=[]):    
    def decorator(func):
        def inner_decorator(request,*args, **kwargs):
          
            for group in groups:
                if Group.objects.get(name=group) in request.user.groups.all():
                   return func(request, *args, **kwargs)
            
            return render(request,'./sinprivile.html')

        return wraps(func)(inner_decorator)

    return decorator