import json
import re


def get_descriptions():
    descriptions = []

    with open("settlements.json", "r") as infile:
        data = json.load(infile)

    for listing in data:
        try:
            listing = listing["pdp_listing_detail"]
            desc = listing["sectioned_description"]["description"].replace('\n', ' ').strip()
            descriptions.append(desc)
        except:
            continue

    return "\n".join(descriptions)


# def located_at():
#     descriptions = get_descriptions()
#     # matches = re.findall(r'[lL]ocated (.*?
#
#
#


def pos_regex_matches(doc, pattern, search_type="tag"):
    """
    Extract sequences of consecutive tokens from a spacy-parsed doc whose
    part-of-speech tags match the specified regex pattern.

    Args:
        doc (``textacy.Doc`` or ``spacy.Doc`` or ``spacy.Span``)
        pattern (str): Pattern of consecutive POS tags whose corresponding words
            are to be extracted, inspired by the regex patterns used in NLTK's
            `nltk.chunk.regexp`. Tags are uppercase, from the universal tag set;
            delimited by < and >, which are basically converted to parentheses
            with spaces as needed to correctly extract matching word sequences;
            white space in the input doesn't matter.

            Examples (see ``constants.POS_REGEX_PATTERNS``):

            * noun phrase: r'<DET>? (<NOUN>+ <ADP|CONJ>)* <NOUN>+'
            * compound nouns: r'<NOUN>+'
            * verb phrase: r'<VERB>?<ADV>*<VERB>+'
            * prepositional phrase: r'<PREP> <DET>? (<NOUN>+<ADP>)* <NOUN>+'

    Yields:
        ``spacy.Span``: the next span of consecutive tokens from ``doc`` whose
            parts-of-speech match ``pattern``, in order of apperance
    """
    # standardize and transform the regular expression pattern...
    pattern = re.sub(r"\s", "", pattern)
    pattern = re.sub(r"<([A-Z]+)\|([A-Z]+)>", r"( (\1|\2))", pattern)
    pattern = re.sub(r"<([A-Z]+)>", r"( \1)", pattern)

    if search_type == "pos":
        tags = " " + " ".join(tok.pos_ for tok in doc)
    else:
        tags = " " + " ".join(tok.tag_ for tok in doc)

    for m in re.finditer(pattern, tags):
        yield doc[tags[0 : m.start()].count(" ") : tags[0 : m.end()].count(" ")]


def pattern(pat):
    import spacy

    # from textacy.extract import pos_regex_matches

    nlp = spacy.load("en")

    descrip = get_descriptions()
    doc = nlp(descrip)
    matches = pos_regex_matches(doc, pat)
    for m in matches:
        print(m)


def same_string(string1, string2):
    common = ""

    for i in range(0, len(string1) + 1):
        part1 = string1[0:i]
        part2 = string2[0:i]
        if part1 == part2:
            common = part1
        else:
            return common

    return common


def commify_adjectives(filename):
    nouns = {}
    out = []

    with open(filename, "r") as infile:
        lines = [l.strip() for l in infile.readlines()]

    # for l1, l2 in zip(lines[1::2], lines[::2]):
    for line in lines:
        words = line.split(" ")
        last = words[-1]
        if last not in nouns:
            nouns[last] = []
        nouns[last].append(" ".join(words[0:-1]))

    for noun, adjs in nouns.items():
        # adjs = sorted(adjs)
        out.append(', '.join(adjs) + " " + noun)

        # if len(nouns) == 1:
        #     out.append(adj + " " + nouns[0])
        # elif len(nouns) == 2:
        #     out.append(adj + " " + " and ".join(nouns))
        # else:
        #     out.append(adj + " " + ", ".join(nouns[0:-2]) + " and " + nouns[-1])

    out = sorted(out)
    for o in out:
        print(o)

def commify_nouns(filename):
    adjectives = {}
    out = []

    with open(filename, "r") as infile:
        lines = [l.strip() for l in infile.readlines()]

    # for l1, l2 in zip(lines[1::2], lines[::2]):
    for line in lines:
        words = line.split(" ")
        first = words[0]
        if first not in adjectives:
            adjectives[first] = []
        adjectives[first].append(" ".join(words[1:]))

    for adj, nouns in adjectives.items():
        # nouns =
        if len(nouns) == 1:
            out.append(adj + " " + nouns[0])
        elif len(nouns) == 2:
            out.append(adj + " " + " and ".join(nouns))
        else:
            out.append(adj + " " + ", ".join(nouns[0:-2]) + " and " + nouns[-1])

    out = sorted(out)
    for o in out:
        print(o)


def chunks():
    import spacy

    nlp = spacy.load("en")
    descriptions = get_descriptions()
    doc = nlp(descriptions)

    for chunk in doc.noun_chunks:
        print(chunk.text)


def find_in_sentence(pat):
    import spacy

    nlp = spacy.load("en")
    descriptions = get_descriptions()
    doc = nlp(descriptions)
    for sentence in doc.sents:
        if pat in sentence.text.lower():
            print(sentence.text.strip())


def sort_sentences():
    import spacy

    nlp = spacy.load("en")
    descriptions = get_descriptions()
    doc = nlp(descriptions)
    sents = []
    for sentence in doc.sents:
        # sents.append(sentence.text.strip())
        s = sentence.text.strip()
        if not re.search(r'^[A-Z0-9]', s):
            continue
        if not re.search(r'[.!]$', s):
            continue
        print(s)



# pattern(r'<DT> <JJ> <NNS>|<DT> <JJ> <NN>')
# commify("adj_nouns.txt")

# find_in_sentence('minute')
sort_sentences()
# chunks()
# commify_adjectives('adj_nouns.txt')
