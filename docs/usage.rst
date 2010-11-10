=====
Usage
=====

The mothertongue application provides an abstract translation class that you can subclass your 
own models from to allow you to serve multilingual data.
This model works out the current language of the request using django's inbuilt translation 
modules and mothertongue's custom context processor. 
When the model is queried the relevant content based on the current request is returned.


In order to use mothertongue's model translation you can follow the example code below


An example model
~~~~~~~~~~~~~~~~~~~~~~
This demonstrates a model that utilises django-mothertongue to translate two of its fields::

    # import stuff we need from django
    from django.db import models
    from django.conf import settings
    from django.utils.translation import get_language, ugettext, ugettext_lazy as _
    
    # import translation stuff
    from mothertongue.models import MothertongueModelTranslate
    
    # Create your models here.
    class GenericPage(MothertongueModelTranslate):
        title = models.CharField(_('title'), max_length=200, help_text=_('Title for your page'))
        content = models.TextField(_('content'), blank=True, help_text=_('Copy for your page'))
        translations = models.ManyToManyField('GenericPageTranslation', blank=True, verbose_name=_('translations'))
        translation_set = 'genericpagetranslation_set'
        translated_fields = ['title','content',]
        
        def __unicode__(self):
            return u'%s' % self.title
    
    # chunks translations model
    class GenericPageTranslation(models.Model):
        generic_page_instance = models.ForeignKey('GenericPage', verbose_name=_('generic_page'))
        language = models.CharField(max_length=len(settings.LANGUAGES)-1, choices=settings.LANGUAGES[1:])
        title = models.CharField(_('title'), max_length=200, help_text=_('Title for your page'))
        content = models.TextField(_('content'), blank=True, help_text=_('Copy for your page'))
        
        class Meta(object):
            # ensures we can only have on translation for each language for each page
            unique_together = (('generic_page_instance', 'language'),)
        
        def __unicode__(self):
            return u'%s' % self.language



An example ``admin.py`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This basically adds an inline model to the sample model and allows you to add
a translation for a total of 2 languages (French and Spanish). The languages allowed
here are the same as those you specified in your settings file::

    # import stuff we need from django
    from django.contrib import admin
    from django.conf import settings
    
    # import app specific shit
    from myapp.models import GenericPage, GenericPageTranslation
    
    # create the inline to handle translation
    class GenericPageTranslationInline(admin.StackedInline):
        model = GenericPageTranslation
        extra = 1
        max_num = len(settings.LANGUAGES)-1
        fieldsets = (
            (None, {
                'fields': ['language',]
            }),
            ('Translation', {
                'fields': ['title','content'],
                'classes': ['collapse',],
            }),
        )
    
    # create the admin model
    class GenericPageAdmin(admin.ModelAdmin):
        fields = ['title', 'content',]
        inlines = (GenericPageTranslationInline,)
    
    # register with CMS
    admin.site.register(GenericPage, GenericPageAdmin)



An example ``views.py`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example show a very, very simple view and just grabs the first record 
in the database for translation, just for demonstration purposes::

    # import stuff from django
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from myapp.models import GenericPage
    
    # very simple homepage view for demo purposes.
    def home(request):
        
        home_copy = GenericPage.objects.all()[0]
        
        # render the response
        return render_to_response('default.html', {'home_copy':home_copy}, context_instance=RequestContext(request))



An example template file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

This example shows the displaying of the record retrieved in the example view
and shows you how to use the ``mothertongue_language_nav`` system::

    <h1>django-mothertongue example template</h1>
    
    <h2>Demo navigation</h2>
    <p>Persists current page, state and URL querystring when changing language via this nav</p>
    {% if mothertongue_language_nav %}
    <ul>
        {% for item in mothertongue_language_nav %}
    	<li class="lang lang-{{ item.code }}{% if item.last %} last{% endif %}">
    		<a href="{{ item.url }}">{{ item.name }}</a>
    	</li>
    	{% endfor %}
    </ul>
    {% endif %}
    
    <h2>Display of translated model data</h2>
    <h3>{{home_copy.title|safe}}</h3>
    <br/><br/>
    {{home_copy.content|safe}}
    
    <h2>Example link using the django url tag which persists the language prefix</h2>
    <a href="{% url home %}" title="Home" hreflang="{{LANGUAGE_CODE}}">Home</a>
