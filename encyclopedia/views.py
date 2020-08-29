from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title.strip())
    if page is None:
        page = "# 404 Page not found"
    page = markdown(page)

    return render(request, "encyclopedia/entry.html", {
        "page": page,
        "title": title
    })

def search(request):
    query = request.GET.get('q').strip()
    entry_list = util.list_entries()
    if query in entry_list:
        return redirect("entry", title=query)

    found_entries = []
    for entry in entry_list:
        if query.lower() in entry.lower():
            found_entries.append(entry)
    return render(request, "encyclopedia/search.html", {
        "found_entries": found_entries,
        "query": query
    })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    name = request.POST.get("name").strip()
    text = request.POST.get("text").strip()
    if len(name) == 0 or len(text) == 0:
        return render(request, "encyclopedia/new.html", {
            "alert_message": "Please fill in all fields. All field are required to submit new wiki entry.",
            "name": name,
            "text": text
        })
    entries = util.list_entries()
    if name in entries:
        return render(request, "encyclopedia/new.html", {
            "alert_message": "Entry already exists.",
            "name": name,
            "text": text
        })
    util.save_entry(name, text)
    return redirect("entry", title=name)

def edit(request, title):

    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "name": title,
            "text": entry
        })

    text = request.POST.get("text").strip()

    if len(text) == 0:
        return render(request, "encyclopedia/new.html", {
            "alert_message": "Please fill in all fields. All field are required to submit new wiki entry.",
            "name": title,
            "text": entry
        })
    
    util.save_entry(title, text)
    return redirect("entry", title=title)

    





