# import stuff we need from Python
import re, copy

# import stuff we need from django
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _

# returns a lang prefix for use in urls
def path_lang_prefix():
    lang = translation.get_language()
    if lang == settings.LANGUAGE_CODE:
        return '/'
    return '/%s/' % lang

# works out langs passed in url and returns relevant paths
def translate(path, code, get_params):

    # Strip existing code (if any) from path
    codes = [lang[0] for lang in settings.LANGUAGES]
    pattern = '|'.join(codes)
    pattern = '^/(%s)' % pattern
    path = re.sub(pattern, '', path)

    # Prepend a language code for all but default language
    defcode = settings.LANGUAGE_CODE
    if code == defcode and settings.PREFIX_DEFAULT_LOCALE is False:
        return u'%s%s' % (path, get_params)
    else:
        return '/%s%s%s' % (code, path, get_params)

# main context processor (should be included from users settings.py)
def router(request):

    # make a copy of the get params if any
    if len(request.GET) > 0:

        # take a copy of the get QueryDict
        get_params = u"?%s" % request.META['QUERY_STRING']

    else:

        # pass an empty query string back
        get_params = u''

    # Contextual language navigation
    language_nav = []
    num = len(settings.LANGUAGES)
    for i in range(num):
        lang = settings.LANGUAGES[i]
        language_nav.append({
            'code': lang[0],
            'name': _(lang[1]),
            'untranslated_name': lang[1],
            'url': translate(request.path, lang[0], get_params),
            'last': i==num-1})

    # return all required mothertongue data in global scope
    return {

        # mothertongue specific objects and data
        'mothertongue_path_lang_prefix': path_lang_prefix(),
        'mothertongue_language_nav':language_nav,

        # other useful django and localeurl objects and data
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': translation.get_language(),
        'django_language': request.session.get('django_language'),
    }
