import string


def title_to_url(title):
    """
    Converts a title string to a valid string for a url. White space will be
    replaced by dash, case will be set to lower and all punctuation marks will
    be removed.

    :param title: the title string.
    :type title: str
    :return: a valid url string.
    :rtype: str
    """
    new = title.lower()
    new = new.translate(str.maketrans('', '', string.punctuation))
    new = new.replace(' ', '-')

    return new


def post_preview(body, char_limit):
    """
    Returns a preview of the post body. Will include all complete words as
    long as char_limit is not surpassed. If any words are omitted due to going
    over the character limit, appends '...' at the end.

    :param body: the post body.
    :type body: str
    :param char_limit: the character limit for the preview.
    :type char_limit: int
    :return: a string with all words from body that fit in char_limit.
    :rtype: str
    """
    if len(body) <= char_limit:
        return body

    preview = body[:char_limit]

    last_char = char_limit - 1
    while preview[last_char].isalpha():
        preview = preview[:last_char]
        last_char -= 1

    while not preview[last_char].isalpha():
        preview = preview[:last_char]
        last_char -= 1

    preview += '...'

    return preview
