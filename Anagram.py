"""CSC148 Exercise 7: Recursion Wrap-Up

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 7.
"""

##############################################################################
# Task 1: A variation on sorting
##############################################################################


def kth_smallest(lst, k):
    """Return the <k>-th smallest element in <lst>.

    Raise IndexError if k < 0 or k >= len(lst).
    Note: for convenience, k starts at 0, so kth_smallest(lst, 0) == min(lst).

    Precondition: <lst> does not contain duplicates.

    @type lst: list[int]
    @type k: int
    @rtype: int
    """
    kth_i = 0
    if k < 0 or k >= len(lst):
        raise IndexError
    else:
        if k == 0:
            return min(lst)
        else:
            pivot = list_pivot(lst)
            smaller, bigger = partition(lst, pivot)
            if k > len(smaller):
                kth_i = kth_smallest(bigger, k - len(smaller))
            elif k < len(smaller):
                kth_i = kth_smallest(smaller, k)
            elif k == len(smaller):
                return min(bigger)
    return kth_i


def list_pivot(lst):
    """Returns the mid pivot of the list.

    Iterates through the list and finds a value that is average
    of the list.

    @type lst: list
    @rtype: int
    """
    lst_total = 0
    for item in lst:
        lst_total += item
    pivot = lst_total//len(lst)
    return pivot


def partition(lst, pivot):
    """Return a partition of <lst> according to pivot.

    Return two lists, where the first is the items in <lst>
    that are <= pivot, and the second is the items in <lst>
    that are > pivot.

    @type lst: list
    @type pivot: object
    @rtype: (list, list)
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)
    tuple_ = (smaller, bigger)
    return tuple_


##############################################################################
# Task 2: Something a little different
##############################################################################
# The file of English words to use. The one we've provided doesn't contain
# plural forms. Assume this list is in alphabetical order.
FILE = 'dict.txt'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def anagrams(phrase):
    """Return a list of all anagrams of <phrase>.

    The anagrams are returned in alphabetical order.

    @type phrase: str
    @rtype: list[str]
    """
    words = _generate_word_list()
    letter_count = _generate_letter_count(phrase.lower())
    return _anagrams_helper(words, letter_count)


def _generate_word_list():
    """Read in English words from <FILE> and return them.

    The returned list is in alphabetical order.

    @rtype: list[str]
    """
    words = []
    with open(FILE) as f:
        for line in f.readlines():
            words.append(line.strip().lower())
    return words


def _generate_letter_count(phrase):
    """Return a dictionary counting the letter occurrences in <string>.

    All letters in <phrase> are converted to lower-case.
    The keys in the returned dictionary are the 26 lower-case letters,
    'a', 'b', 'c', etc.

    Precondition: <phrase> contains only letters.

    @type phrase: str
    @rtype: dict[str, int]
    """
    lower = phrase.lower()
    letter_count = {}
    for char in LETTERS:
        letter_count[char] = lower.count(char)
    return letter_count


def _anagrams_helper(words, letter_count):
    """Return all the anagrams using the given letters and allowed words.

    Each anagram must use all the letters, with correct occurrences, given by
    <letter_count>, and must use only the words appearing in <words>.

    Note: we're using a helper function here so that you don't need to
    recompute <words> for each recursive call.

    The anagrams are returned in alphabetical order.

    Preconditions:
    - letter_count has 26 keys (one per lowercase letter),
      and each value is a non-negative integer.

    @type words: list[str]
    @type letter_count: dict[str, int]
    @rtype: list[str]
    """
    anagrams_list = []

    if empty_keys(letter_count) is True:
        return ['']
    else:
        for word in words:
            if not _within_letter_count(word, letter_count):
                continue
            else:
                d1 = new_dictionary(letter_count, word)
                a_list = _anagrams_helper(words, d1)
                w_l = join_anagrams(a_list, word, d1)
                if empty_keys(d1):
                    anagrams_list += w_l
    return anagrams_list


def join_anagrams(a_list, word, d1):
    """Concatenates each word in a_list behind word in its respective order and
    appends the new word into a list and subtracts the the number of occurences
    of each char in word to d1. Returns the new list

    @type a_list: List[str]
    @type word: str
    @type d1: dict{str: int}
    @rtype: List[str]
    """
    i = 0
    n_list = []

    if a_list == ['']:
        return [word]
    else:
        while i != len(a_list):
            subtract_values(d1, a_list[i])
            n_list.append(word + ' ' + a_list[i])
            i += 1
    return n_list


def empty_keys(d):
    """Returns True if all value of keys in d is 0.

    Precondition: All keys in the dictionary must have an int as its value.

    @type d: dict{str: int}
    @rtype: Bool
    """
    for key in d:
        if d[key] != 0:
            return False
    return True


def new_dictionary(d1, phrase):
    """Subtracts the values in d1, according to the number of characters in
    word.

    Precondition: d1 must be a dictionary.

    @type d1: dict
    @type phrase: str
    @rtype: dict{str: int}
    """
    word = phrase.lower()
    new_d = {}
    for key in d1:
        new_d[key] = d1[key]
    for char in LETTERS:
        new_d[char] -= word.count(char)
    return new_d


def subtract_values(d, word):
    """Subtracts the value of the keys in d according to the number of times
    it occurs in word.

    Preconditions: d must be a dictionary, word must be a str.

    @type d: dict{str: int}
    @type word: str
    @rtype: None
    """
    for char in LETTERS:
        d[char] -= word.count(char)
        if d[char] < 0:
            d[char] = 0


def _within_letter_count(word, letter_count):
    """Return whether <word> can be made using letters in <letter_count>."""
    for char in LETTERS:
        if word.count(char) > letter_count[char]:
            return False
    return True


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
