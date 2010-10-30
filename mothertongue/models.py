# import stuff we need from django
from django.db import models
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.utils import translation

# import package specific stuff
from django.conf import settings

# class to handle translated models
class MothertongueModelTranslate(models.Model):
    """
    Models that extend this class will have the ability to define:
    - translation_set, e.g: 'contenttranslation_set', the many to many 
      manager name for the translation models for this model.
    - translated_fields = e.g: ['content',] - the fields that may be 
      translated. A match is found if a translation exists with a 'language' 
      the same as the current language, e.g: 'es' and a matching name.
    """
    class Meta(object):
        abstract = True   
            
    def __getattribute__(self, name):
        """
        Specialise to look for translated content, note we use super's
        __getattribute__ within this function to avoid a recursion error.
        """
        get = lambda p:super(MothertongueModelTranslate, self).__getattribute__(p)
        translated_fields = get('translated_fields')
        if name in translated_fields:
            try:                
                translation_set = get('translation_set')
                code = translation.get_language()
                translated_manager = get(translation_set)
                translated_object = translated_manager.get(language=code)
                return getattr(translated_object, name)
            except Exception:
                return get(name)
        else:
            return get(name)