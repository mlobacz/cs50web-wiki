"""
Encyclopedia app views module.
"""

from random import choice

import markdown2
from django import forms
from django.http import Http404
from django.shortcuts import redirect, render

from . import util


class AlreadyExistsError(Exception):
    """Raised when an entry already exists."""


class NewEntryForm(forms.Form):
    """
    Form for adding new entry to the encyclopedia.
    """

    title = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea())


class EditEntryForm(forms.Form):
    """
    For for editing new entry in the encyclopedia.
    """

    content = forms.CharField(widget=forms.Textarea())


def index(request):
    """
    Renders encyclopedia index page.
    """
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    """Renders requested wiki entry. Returns 404 if not found."""
    entry_content = util.get_entry(title)
    if not entry_content:
        raise Http404(f"{title} entry was not found in the Wiki.")
    return render(
        request,
        "encyclopedia/entry.html",
        {"title": title, "entry": markdown2.markdown(entry_content)},
    )


def search(request):
    """
    Redirects to page matching search query
    or returns list of entries containing query string.
    """
    query = request.GET["q"]
    if util.get_entry(query):
        return redirect("encyclopedia:entry", title=query)
    matching_entries = [entry for entry in util.list_entries() if query in entry]
    return render(request, "encyclopedia/search.html", {"entries": matching_entries})


def new(request):
    """Allows user to add new entry to the wiki."""
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                raise AlreadyExistsError(f"{title} entry already exists!")
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
