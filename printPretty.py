#!/usr/bin/python3

import json
import sys
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter
from pprint import pformat
from colorama import init
from colorama import Fore, Back, Style


def pprint_color(obj):
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))


def find_json(text, start=0):
    text = text.replace("\\", "/")
    while True:
        start = text.find('{', start)
        if start == -1:
            return -1, -1, -1
        stop = text.find('}', start + 1) + 1
        while not text[start:stop].count('}') == text[start:stop].count('{'):  # selbe anzahl { }
            how_many_brackets = text[start:stop].count('{') - text[start:stop].count('}')
            for _ in range(how_many_brackets):
                stop = text.find('}', stop)
                if stop == -1:
                    return -1, -1, -1
                else:
                    stop += 1
        try:
            result = json.loads(text[start:stop])
            return result, start, stop
        except ValueError:
            print("******* could not parse json")
            return -1, -1, -1


def extract_js_out_of_the_text_and_print(text):
    # search jsons
    js = []
    start = 0
    while True:
        jst, start, stop = find_json(text, start)
        if not (start == -1 and stop == -1):
            js.append({'js': jst, 'start': start, 'stop': stop})
            start = stop + 1
        else:
            break

    start = 0
    for i in range(len(js)):
        print(analyze_text(text[start:js[i]["start"]]))
        pprint_color(js[i]['js'])
        start = js[i]['stop'] + 1

    print(analyze_text(text[start:]))


def analyze_text(text):
    text = text.replace("ERROR", Back.RED + "ERROR" + Style.RESET_ALL)
    text = text.replace("INFO", Back.GREEN + "INFO" + Style.RESET_ALL)
    text = text.replace("WARN", Back.YELLOW + "WARN" + Style.RESET_ALL)
    return text


init()

try:
    buff = ''
    while True:
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):
            line = buff[:-1]
            # print(line)
            extract_js_out_of_the_text_and_print(line)
            buff = ''

except KeyboardInterrupt:
    sys.stdout.flush()
