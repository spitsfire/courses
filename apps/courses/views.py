from django.shortcuts import render, reverse, redirect, HttpResponse
from django.contrib import messages
from .models import Course, Description, Comment

def index(request):
    context = {
        "courses": Course.objects.all()
        }
    return render(request, 'courses/index.html', context)

def create(request):
    errors = Course.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('courses:home'))
    else:
        course = Course.objects.create(
            name=request.POST['course_name']
        )
        desc = Description.objects.create(content=request.POST['desc'])
        course.description = desc
        course.save()
        messages.success(request, "Course successfully added!")
        print(messages.success)
        return redirect(reverse('courses:home'))

def delete_page(request,id):
    context = {
        "course": Course.objects.get(id=id)
    }
    return render(request,'courses/delete.html', context)

def delete(request):
    id = request.POST['id']
    course = Course.objects.get(id=id)
    course.delete()
    return redirect(reverse('courses:home'))

def comments(request,id):
    context = {
        "course": Course.objects.get(id=id),
        "comments": Comment.objects.filter(course=Course.objects.get(id=id)).all()
    }
    return render(request,'courses/comments.html', context)

def create_comment(request, id):
    errors = Comment.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('courses:show_comments', kwargs={'id': id}))
    else:
        Comment.objects.create(
            content=request.POST['content'],
            course = Course.objects.get(id=id)
        )
        return redirect(reverse('courses:show_comments', kwargs={'id': id}))