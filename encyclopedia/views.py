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

