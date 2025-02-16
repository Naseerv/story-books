from django.shortcuts import render,get_object_or_404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db.models import Q
import random
from django.template.defaultfilters import title

# Create your views here.
from .models import Story,Category

def story_list(request,category_slug=None):
    category=None
    categories=Category.objects.all()
    story=Story.objects.all()
    paginator=Paginator(story,1)
    page=request.GET.get('page')
    try:
        story=paginator.page(page)
    except PageNotAnInteger:
        story=paginator.page(1)
    except EmptyPage:
        story=paginator.page(paginator.num_pages)
    if category_slug:
        story=Story.objects.all()
        category=get_object_or_404(Category,slug=category_slug)
        story=story.filter(category=category)
        paginator = Paginator(story, 1)
        page = request.GET.get('page')
        try:
            story = paginator.page(page)
        except PageNotAnInteger:
            story = paginator.page(1)
        except EmptyPage:
            story = paginator.page(paginator.num_pages)
    all_story=list(Story.objects.all())
    recent_story=random.choice(all_story)
    return render(request,'story/story_list.html',{'categories':categories,
                                                   'story':story,
                                                   'category':category,
                                                   'page':page,
                                                   'recent_story':recent_story,
                                                   })

def story_detail(request,id):
    story=get_object_or_404(Story,id=id)
    return render(request,'story/story_detail.html',{'story':story})


def search_story(request):
    query=None
    results=[]
    if request.method=="GET":
        query=request.GET.get('search')
        results=Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    return render(request,'story/search.html',{'query':query,'results':results})