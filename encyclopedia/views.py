from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

import markdown2

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="Search Wiki")

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return redirect("entry", title=form.cleaned_data["query"])
        else:
            form = SearchForm()
    else:
        form = SearchForm()
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})


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
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("test passed")
        else:
            form = SearchForm()
    return render(request, "encyclopedia/index.html", {'form': form})
    # entry = util.get_entry(query)
    # if entry:
    #     return render(
    #         request,
    #         "encyclopedia/entry.html",
    #         {"title": query, "entry": markdown2.markdown(entry)},
    #     )
