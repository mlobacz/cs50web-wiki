from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    """Renders requested wiki entry. Returns 404 if not found."""
    entry = util.get_entry(title)
    if not entry:
        raise Http404(f"{title} entry was not found in the Wiki.")
    return render(
        request,
        "encyclopedia/entry.html",
        {"title": title, "entry": markdown2.markdown(entry)},
    )


def search(request):
    """Redirects to page matching search query or returns list of entries containing query string."""
    query = request.GET["q"]
    if util.get_entry(query):
        return redirect("encyclopedia:entry", title=query)
    else:
        matching_entries = [entry for entry in util.list_entries() if query in entry]
        return render(request, "encyclopedia/search.html", {"entries": matching_entries})

def new(request):
    return render(request, "encyclopedia/new.html")