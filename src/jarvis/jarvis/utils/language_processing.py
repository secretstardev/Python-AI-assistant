# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import nltk
import logging


def is_positive_answer(answer):
    return answer in ['yes', 'y', 'oui', 'true']


def is_negative_answer(answer):
    return answer in ['no', 'n']


def create_parts_of_speech(text):
    tokens = nltk.word_tokenize(text)
    return nltk.pos_tag(tokens)


def is_question_with_modal(parts_of_speech):
    grammar = 'QS: {<MD><PRP><VB>}'
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(parts_of_speech)
    for subtree in result.subtrees():
        if subtree.label() in ['MD', 'WD', 'QS']:
            return True


def is_question_with_inversion(parts_of_speech):
    grammar = 'QS: {<VBP><PRP>}'
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(parts_of_speech)
    for subtree in result.subtrees():
        if subtree.label() in ['QS']:
            return True


def _extract_verb(parts_of_speech):
    for part in parts_of_speech:
        if part[1] in ['VB']:
            return part[0]
    return ' '


def _extract_modal(parts_of_speech):
    for part in parts_of_speech:
        if part[1] in ['MD']:
            return part[0]
    return ' '


def _extract_noun(parts_of_speech):
    for part in parts_of_speech:
        if part[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
            return part[0]
    return ' '


# Construct Response Body
def create_response(sentence):

    parts_of_speech = create_parts_of_speech(sentence)

    # Extract speech parts
    verb = _extract_verb(parts_of_speech)
    modal = _extract_modal(parts_of_speech)
    noun = _extract_noun(parts_of_speech)

    # Question type classification
    if is_question_with_modal(parts_of_speech):
        logging.info('The user speech has a modal question')
        answer = 'I ' + modal + ' ' + verb + ' ' + noun
    elif is_question_with_inversion(parts_of_speech):
        logging.info('The user speech has an inverse question')
        answer = 'I ' + ' ' + verb + ' ' + noun
    else:
        logging.info('Unclassified question type')
        answer = ''

    return re.sub('\s\s+', ' ', answer)


def create_positive_response(sentence):
    positive_response = create_positive_response(sentence)
    if positive_response:
        return 'Yes, ' + positive_response


def create_negative_response(sentence):
    negative_response = create_positive_response(sentence)
    if negative_response:
        return 'No, ' + negative_response