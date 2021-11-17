from django.http import HttpRequest
from django.shortcuts import render

from runewords.models import RuneWord, Rune


def get_rune_words(request: HttpRequest):
    rune_words = RuneWord.objects.all().order_by('char_level', 'name')
    runes = '|'.join([
        "{} ({})".format(r.name, r.num)
        for r in Rune.objects.all().order_by('num')
    ])
    context = dict(rune_words=rune_words, runes=runes)
    return render(request, 'rune_words.html', context=context)
