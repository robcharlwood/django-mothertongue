# grab stuff we need from django
from django import db
from django.conf import settings
from django.db import IntegrityError
from django.template import RequestContext
from django.test import TestCase
from django.utils.translation import activate, get_language, ugettext, ugettext_lazy as _

# grab stuff we need from our project
from mothertongue.tests.models import TestModel, TestModelTranslation
from mothertongue.tests.test_utils import RequestFactory

# create class to test mothertongue
class TestMotherTongue(TestCase):
    
    # create setup method
    def setUp(self):
        
        # create base object
        self.g = TestModel(test_field_1='en title', test_field_2='en content')
        
        # save base object
        self.g.save()
        
        # add one translation for spanish
        self.t = TestModelTranslation(test_model_instance=self.g, language='es', test_field_1='es title', test_field_2='es content')
        
        # save first spanish translation
        self.t.save()
        
        # add a second record for french for the same object - this should add correctly as its not a duplicate and doesn't contradict the `unique-together` attribute
        self.t2 = TestModelTranslation(test_model_instance=self.g, language='fr', test_field_1='fr title', test_field_2='fr content')

        # save french translation
        self.t2.save()
        
        # Create the new request
        self.rf = RequestFactory()

    def tearDown(self):
        activate(settings.LANGUAGE_CODE)


# class to test model constraints
class TranslationModelsTestCase(TestMotherTongue):

    # method to test the constrains of unique fields i.e a model record should only have one translation for each language
    def test_unique_field_constraints(self):
                                
        # add a second record for spanish for the same base object - the `unique-together` attribute on the model should through an IntegrityError here
        t3 = TestModelTranslation(test_model_instance=self.g, language='es', test_field_1='es title duplicate', test_field_2='es content duplicate')
        
        # try and save the duplicate entry
        self.assertRaises(IntegrityError, t3.save)
        
    
    def test_translation_relationships(self):

        # check that our relationship is correct
        self.assertEqual(self.g, self.t.test_model_instance)
        self.assertEqual(self.g, self.t2.test_model_instance)
    

    def test_translation_count(self):
            
        # count translation records now associated with the base object - there should be two spanish and french        
        count = TestModelTranslation.objects.all().filter(test_model_instance=self.g).count()
        
        # check we have two translation records associated with our base object
        self.assertEqual(count, 2)
    
    def test_translation_result_set(self):
            
        # grab translation records now associated with the base object and order them by language so that we can confirm there is one french and one spanish translation
        translations = TestModelTranslation.objects.all().filter(test_model_instance=self.g).order_by('language')
                
        # check to make sure the records are what we expect
        self.assertEqual(translations[0].language, 'es')
        self.assertEqual(translations[1].language, 'fr')

    def test_language_returned(self):
        
        # set default language
        activate(settings.LANGUAGE_CODE)
        lang = get_language()
        
        # grab a record now and check language returned
        r = TestModel.objects.get(pk=self.g.pk)
        self.assertEqual(r.test_field_1, 'en title')
        self.assertEqual(r.test_field_2, 'en content')
        
        # activate spanish
        activate('es')
        
        # grab a record now and check language returned is spanish
        r = TestModel.objects.get(pk=self.g.pk)
        self.assertEqual(r.test_field_1, 'es title')
        self.assertEqual(r.test_field_2, 'es content')
    
        # activate french
        activate('fr')
        
        # grab a record now and check language returned is french
        r = TestModel.objects.get(pk=self.g.pk)
        self.assertEqual(r.test_field_1, 'fr title')
        self.assertEqual(r.test_field_2, 'fr content')



# class to test the response from the context processor when requests are made
class MotherTongueContextProcessorTestCase(TestMotherTongue):
    
    # test context processor on urls
    def test_url_en(self):
        
        # create mock request for english
        request = self.rf.get('/')
        context = RequestContext(request)
        self.assertEqual(context['LANGUAGE_CODE'], 'en')
        self.assertEqual(context['mothertongue_path_lang_prefix'], '/')
        self.assertEqual(context['request'].META['PATH_INFO'], '/')
        self.assertNotEqual(context['mothertongue_language_nav'], '')
        self.assertEqual(context['LANGUAGES'], settings.LANGUAGES)

    def test_url_es(self):
      
        # Create mock request for spanish
        request = self.rf.get('/es/')
        context = RequestContext(request)
        self.assertEqual(context['LANGUAGE_CODE'], 'es')
        self.assertEqual(context['mothertongue_path_lang_prefix'], '/es/')
        self.assertEqual(context['request'].META['PATH_INFO'], '/es/')
        self.assertNotEqual(context['mothertongue_language_nav'], '')
        self.assertEqual(context['LANGUAGES'], settings.LANGUAGES)

    def test_url_fr(self):
        
        # Create mock request for french
        request = self.rf.get('/fr/')
        context = RequestContext(request)
        self.assertEqual(context['LANGUAGE_CODE'], 'fr')
        self.assertEqual(context['mothertongue_path_lang_prefix'], '/fr/')
        self.assertEqual(context['request'].META['PATH_INFO'], '/fr/')
        self.assertNotEqual(context['mothertongue_language_nav'], '')
        self.assertEqual(context['LANGUAGES'], settings.LANGUAGES)
    
    def test_url_with_querystring_en(self):
            
        # create mock request for english
        request = self.rf.get('/?page=1&person=robcharlwood')
        context = RequestContext(request)
        self.assertEqual(context['mothertongue_language_nav'][0]['url'], '/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][1]['url'], '/es/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][2]['url'], '/fr/?page=1&person=robcharlwood')
     
    def test_url_with_querystring_es(self):
        
        # create mock request for spanish
        request = self.rf.get('/es/?page=1&person=robcharlwood')
        context = RequestContext(request)
        self.assertEqual(context['mothertongue_language_nav'][0]['url'], '/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][1]['url'], '/es/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][2]['url'], '/fr/?page=1&person=robcharlwood')
      
    def test_url_with_querystring_fr(self):
        
        # create mock request for french
        request = self.rf.get('/fr/?page=1&person=robcharlwood')
        context = RequestContext(request)
        self.assertEqual(context['mothertongue_language_nav'][0]['url'], '/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][1]['url'], '/es/?page=1&person=robcharlwood')
        self.assertEqual(context['mothertongue_language_nav'][2]['url'], '/fr/?page=1&person=robcharlwood')
    

class TestCache(TestMotherTongue):
    # this approch to testing query counts is largly stolen from the
    # select_related tests:
    # (http://www.djangoproject.com/documentation/models/select_related/)
    def setUp(self):
        super(TestCache, self).setUp()
        # The test runner sets settings.DEBUG to False, but we want to
        # gather queries so we'll set it to True
        settings.DEBUG = True
        # this should always be the last thing to happen before the
        # tests
        db.reset_queries()

    def tearDown(self):
        super(TestCache, self).tearDown()
        settings.DEBUG = False

    def test_model_fetch(self):
        # getting the model instance hit the DB
        r = TestModel.objects.get(pk=self.g.pk)
        self.assertEqual(1, len(db.connection.queries))

    def test_one_field_access(self):
        # the first field access hits the DB
        r = TestModel.objects.get(pk=self.g.pk)
        r.test_field_1
        self.assertEqual(2, len(db.connection.queries))

    def test_two_access_main(self):
        # the second field access is cached, so the DB is not hit
        activate(settings.LANGUAGE_CODE)
        r = TestModel.objects.get(pk=self.g.pk)
        r.test_field_1
        r.test_field_1
        self.assertEqual(2, len(db.connection.queries))

    def test_two_access_foreign(self):
        activate('es')
        r = TestModel.objects.get(pk=self.g.pk)
        r.test_field_1
        r.test_field_1
        self.assertEqual(2, len(db.connection.queries))

    def test_two_access_nonexistent(self):
        activate('xx')
        r = TestModel.objects.get(pk=self.g.pk)
        r.test_field_1
        r.test_field_1
        self.assertEqual(2, len(db.connection.queries))

