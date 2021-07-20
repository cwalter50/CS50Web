
from . import util
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown2 import Markdown

import random

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))


class Post(forms.Form):
    title = forms.CharField(label="title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = Markdown().convert(page)
                    
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': form
                    }

                    return render(request, "encyclopedia/entry.html", context)
                if item.lower() in i.lower(): 
                    searched.append(i)
                    context = {
                        'searched': searched, 
                        'form': form
                    }
            if len(searched) == 0:
                return render(request, "encyclopedia/error.html", {
                    "message": "No Pages found in search",
                    "form":form
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    'searched': searched, 
                        'form': form
                })

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })


def entry(request, title):
    # Displays the requested entry page, if it exists
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = Markdown().convert(page) 

        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
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

def create(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "Page already exists"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                page_converted = Markdown().convert(page)

                context = {
                    'title': title,
                    'form': Search(),
                    'page': page_converted
                    
                }

                return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/create.html", {"form": Search(), "post": Post()})



def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)

        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea':page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = Markdown().convert(page)

            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }

            return render(request, "encyclopedia/entry.html", context)



def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = Markdown().convert(page)

        context = {
            'form': Search(),
            'page': page_converted,
            'title': page_random
        }

        return render(request, "encyclopedia/entry.html", context)
