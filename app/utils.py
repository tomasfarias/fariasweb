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
