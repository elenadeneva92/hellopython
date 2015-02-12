#!/user/bin/env python
""" String matching module"""


def presuffix_heuristic(pattern):
    """Calculates the presuffix for all suffix of pattern"""
    presuffixes = [None] * (len(pattern) + 1)
    presuffixes[len(pattern) - 1] = 0
    presuffixes[len(pattern)] = 0

    for i in range(len(pattern) - 2, -1, -1):
        j = len(pattern) - presuffixes[i + 1]
        while pattern[i] != pattern[j-1] and presuffixes[j] > 0:
            j = len(pattern) - presuffixes[j]
        if pattern[i] == pattern[j-1]:
            presuffixes[i] = len(pattern) - j + 1
        else:
            presuffixes[i] = 0

    return presuffixes


def goodsuffix_heuristic(pattern):
    """Linear calculation of good suffic heuristic"""

    presuffix = presuffix_heuristic(pattern)
    goodsuffixes = [None] * (len(pattern) + 1)

    for i in range(1, len(pattern)+1):
        goodsuffixes[i] = len(pattern) - presuffix[0]

    for i in range(0, len(pattern)):
        k = len(pattern) - presuffix[i] - i
        j = len(pattern) - presuffix[i]

        if goodsuffixes[j] > k:
            goodsuffixes[j] = k

    return goodsuffixes


def bad_suffix_heuristic(pattern):
    """Bad suffix heuristic implementation"""
    bad_suffixes = {}
    for i in range(0, len(pattern)):
        bad_suffixes[pattern[i]] = i
    return bad_suffixes


def search(text, pattern):
    """Find the index of pattern in text or return -1, if such doesn't exist"""
    bad_suffixes = bad_suffix_heuristic(pattern)
    good_suffixes = goodsuffix_heuristic(pattern)

    i = 0
    while i <= len(text) - len(pattern):
        print("Try from {}".format(i))
        j = len(pattern) - 1
        while j >= 0 and text[i+j] == pattern[j]:
            j = j - 1
        if j == -1:
            return i
        else:
            if not text[i+j] in bad_suffixes:
                bad_suffix_step = j + 1
            elif bad_suffixes[text[i+j]] <= j:
                bad_suffix_step = j - bad_suffixes[text[i+j]]
            else:
                bad_suffix_step = 1

            step = max(good_suffixes[j+1], bad_suffix_step)
            i += step
    return -1


def main():
    """ Start point"""
    input_pattern = input("Pattern:")
    print(presuffix_heuristic(input_pattern))
    print(goodsuffix_heuristic(input_pattern))
    input_text = input("Text:")
    index = search(input_text, input_pattern)
    if index != -1:
        print("Index found on {}".format(index))
    else:
        print("Index not found")

if __name__ == '__main__':
    main()
