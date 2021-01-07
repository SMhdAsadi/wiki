from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import markdown
import random as rand

from . import util


def getSearchResult(query):
    if len(query) == 0:
        return []

    result = []
    entries = util.list_entries()
    if query in entries:
        return query
    
    for entry in entries:
        if query.lower() in entry.lower():
            result.append(entry)
    return result

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryNames = util.list_entries()
    if not title in entryNames:
        return render(request, 'encyclopedia/error.html', {
            'title': title,
            'error': f"url: 'wiki/{title}' doesn't exist, please enter valid URLs."
        })
    else:
        content = util.get_entry(title)
        html = markdown(content)
        return render(request, "encyclopedia/wiki.html", {"title": title, "content": html})

def edit(request, title):
    if request.method == "POST":
        data = request.POST
        title, content = data["title"], data["content"]
        util.save_entry(data["title"], data["content"])
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": data["title"]}))


    entryNames = util.list_entries()
    if not title in entryNames:
        return render(request, 'encyclopedia/error.html', {
            'title': title,
            'error': f"url: 'wiki/{title}' doesn't exist, please enter valid URLs."
        })
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

def random(request):
    entryNames = util.list_entries()
    title = entryNames[rand.randrange(len(entryNames))]
    content = util.get_entry(title)
    html = markdown(content)
    return render(request, "encyclopedia/wiki.html", {"title": title, "content": html})

def search(request):
    data = request.GET
    query = data["q"]
    
    searchResult = getSearchResult(query)
    if type(searchResult) == str:
        content = util.get_entry(searchResult)
        html = markdown(content)
        return render(request, "encyclopedia/wiki.html", {"title": searchResult, "content": html})
    
    return render(request, "encyclopedia/search.html", {"items": searchResult, "query": query})
        

def new(request):
    if request.method == 'POST':
        data = request.POST
        entries = util.list_entries()
        if data["title"].lower() in map(lambda entry: entry.lower(), entries):
            return render(request, 'encyclopedia/error.html', {
                'title': "Duplicate Page",
                'error': f"{data['title']} already exists!"
            })
        else:
            util.save_entry(data["title"], data["content"])
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": data["title"]}))

    return render(request, "encyclopedia/new.html")
