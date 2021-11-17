import json
import logging
import re
from argparse import ArgumentParser

from django.core.management import BaseCommand
from django.db.transaction import atomic

from runewords.models import Rune, RuneWord

log = logging.getLogger('d2help')

RE_RUNES = re.compile(
    r'^(?P<name>\w+) - #(?P<num>\d+)\s+(?:--|(?:[\w-]+\.gif\s*)+)'
    r'\s*(?P<effect>.+)\s*$',
)


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('runes_file', type=str)
        parser.add_argument('runewords_file', type=str)

    @staticmethod
    def camel_case_split(s):
        words = [[s[0]]]
        for c in s[1:]:
            if words[-1][-1].islower() and c.isupper():
                words.append(list(c))
            else:
                words[-1].append(c)

        return [''.join(word) for word in words]

    def load_runes(self, runes_file: str):
        log.info('Loading runes')

        with open(runes_file) as f:
            saved = set()
            for line in f:
                match = RE_RUNES.match(line.strip())
                if match:
                    rune = Rune(
                        name=match.group('name'),
                        num=match.group('num'),
                        effect=match.group('effect')
                    )
                    rune.save()
                    saved.add(int(rune.num))
                    log.info('Saving rune {} ({})'.format(rune.name, rune.num))
            needed = set(range(1, max(saved) + 1))
            if saved != needed:
                raise ValueError('Not saved runes: {}'.format(needed - saved))

    def parse_rune_word(self, elem):
        runes_raw = elem['runes'].strip().split('\n')
        effect = elem['effects'].strip()
        name = runes_raw[0]
        if len(runes_raw[1].strip().split(' ')) == 1:
            word = runes_raw[1]
            lvl_idx = 4
        else:
            word = runes_raw[1].strip().split(' ')[0]
            lvl_idx = 3
        runes = self.camel_case_split(word)
        weapons = runes_raw[3]
        char_level = int(runes_raw[lvl_idx].split(':')[-1].strip())
        rune_word = RuneWord(
            name=name,
            effect=effect,
            weapons=weapons,
            char_level=char_level,
        )

        return rune_word, runes

    def load_rune_words(self, file):
        with open(file) as f:
            data = json.load(f)
        for elem in data:
            try:
                rune_word, runes = self.parse_rune_word(elem)
            except Exception:
                log.exception('Error parsing rune word {}'.format(elem))
                raise
            print('Saving runeword {} {}'.format(rune_word.name, runes))
            rune_word.save()
            for rune in runes:
                try:
                    rune = Rune.objects.get(name=rune)
                except Rune.DoesNotExist:
                    raise RuntimeError('Unknown rune {}'.format(rune))
                rune_word.runes.add(rune)
                rune_word.save()

    @atomic
    def handle(self, runes_file: str, runewords_file: str, *args, **options):
        Rune.objects.all().delete()
        RuneWord.objects.all().delete()
        self.load_runes(runes_file)
        self.load_rune_words(runewords_file)
