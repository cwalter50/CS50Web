
from . import util
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown2 import Markdown

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            if item in entries:
                page = util.get_entry(item)
                page_converted = Markdown().convert(page)

                return render(request, "encyclopedia/entry.html", {
                    'page': page_converted,
                    'title': item,
                    'form': Search()
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Displays the requested entry page, if it exists
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = Markdown().convert(page) 

        context = {
            'page': page_converted,
            'title': title
            # 'form': Search()
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    # return render(request, "encyclopedia/entry.html", {
    #     "title":title.capitalize()
    # })
    #  return HttpResponse(f"Hello, {title.capitalize()}!")


# def entry(request, title):
#     """ Displays the requested entry page, if it exists """

#     entry_md = util.get_entry(title)

#     if entry_md != None:
#         # Title exists, convert md to HTML and return rendered template
#         entry_HTML = Markdown().convert(entry_md)
#         return render(request, "encyclopedia/entry.html", {
#           "title": title,
#           "entry": entry_HTML,
#           "search_form": SearchForm(),
#           })
#     else:
#         # Page does not exist, get links for similar titles:
#         related_titles = util.related_titles(title)

#         return render(request, "encyclopedia/error.html", {
#           "title": title,
#           "related_titles": related_titles,
#           "search_form": SearchForm(),
#           })


