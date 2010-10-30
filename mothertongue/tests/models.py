# import stuff we need from django
from django.db import models
from django.conf import settings
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

# import translation stuff from mothertongue package
from mothertongue.models import MothertongueModelTranslate

# Create generic test model.
class TestModel(MothertongueModelTranslate):
    test_field_1 = models.CharField(_('test_field_1'), max_length=200)
    test_field_2 = models.TextField(_('test_field_2'), blank=True)
    translations = models.ManyToManyField('TestModelTranslation', blank=True, verbose_name=_('translations'))
    translation_set = 'testmodeltranslation_set'
    translated_fields = ['test_field_1','test_field_2',]
    
    def __unicode__(self):
        return u'%s' % self.test_field_1

# create a generic test tranlsations model        
class TestModelTranslation(models.Model):
    test_model_instance = models.ForeignKey('TestModel', verbose_name=_('test_model'))
    language = models.CharField(max_length=len(settings.LANGUAGES)-1, choices=settings.LANGUAGES[1:])
    test_field_1 = models.CharField(_('test_field_1'), max_length=200)
    test_field_2 = models.TextField(_('test_field_2'), blank=True)
    
    class Meta(object):
        unique_together = (('test_model_instance', 'language'),)
    
    def __unicode__(self):
        return u'%s' % self.language