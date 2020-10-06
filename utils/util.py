from nltk import RegexpTokenizer


def tokenize(sentence):
    """
    Tokenize the given sentence in Portuguese.
    :param sentence: sentence to be tokenized, as a string
    """
    tokenizer_regexp = r'''(?ux)
        # the order of the patterns is important!!
        # more structured patterns come first
        [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+|    # emails
        (?:https?://)?\w{2,}(?:\.\w{2,})+(?:/\w+)*|                  # URLs
        (?:[\#@]\w+)|                     # Hashtags and twitter user names
        (?:[^\W\d_]\.)+|                  # one letter abbreviations, e.g. E.U.A.
        (?:[DSds][Rr][Aa]?)\.|            # common abbreviations such as dr., sr., sra., dra.
        (?:\B-)?\d+(?:[:.,]\d+)*(?:-?\w)*|
            # numbers in format 999.999.999,999, possibly followed by hyphen and alphanumerics
            # \B- avoids picks as F-14 as a negative number
        \.{3,}|                           # ellipsis or sequences of dots
        \w+|                              # alphanumerics
        -+|                               # any sequence of dashes
        \S                                # any non-space character
        '''
    tokenizer = RegexpTokenizer(tokenizer_regexp)

    return tokenizer.tokenize(sentence)
