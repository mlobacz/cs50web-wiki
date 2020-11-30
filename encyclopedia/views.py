from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

import markdown2

from . import util


class AlreadyExistsError(Exception):
    """Raised when an entry already exists."""

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=20, label="Title")
    # TODO: format this form somehow
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 10}),
        label="Page content in Markdown",
    )


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
        return render(
            request, "encyclopedia/search.html", {"entries": matching_entries}
        )


def new(request):
    """Allows user to add new entry to the wiki."""
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                raise AlreadyExistsError(f"{title} entry already exists!")
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title=title, content=content)
                return redirect("encyclopedia:entry", title=title)
    return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})
