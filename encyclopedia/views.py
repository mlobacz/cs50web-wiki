from random import choice

import markdown2
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from . import util


class AlreadyExistsError(Exception):
    """Raised when an entry already exists."""


class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea())


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())


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


def edit(request, title):
    """Allows user to edit existing entry."""
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title=title, content=new_content)
            return redirect("encyclopedia:entry", title=title)
    return render(
        request,
        "encyclopedia/edit.html",
        {"title": title, "form": EditEntryForm({"content": util.get_entry(title)})},
    )


def random(request):
    """Redirects user to randomly selected entry."""
    return redirect("encyclopedia:entry", title=choice(util.list_entries()))
