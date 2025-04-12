from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def add_founded_term(request):
    return render(request, "founded_term_add.html")


def send_founded_term(request):
    if request.method == "POST":
        cache.clear()
        search_text = request.POST.get("search_text")
        context = {"text": search_text}
        if len(search_text) == 0:
            context["success"] = False
            context["comment"] = "Вы не ввели ключевое слово"
        else:
            terms = terms_work.get_define(search_text)
            if len(terms) == 0:
                context["success"] = False
                context["comment"] = "Не удалось найти подходящий термин"
            else:
                context["success"] = True
                context["comment"] = "Список подходящих терминов и их определений:"
                context["terms"] = terms
        return render(request, "founded_term_list.html", context)