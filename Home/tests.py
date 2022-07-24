
from django.urls import resolve , reverse
from django.test import SimpleTestCase 
from Home.views import  creatorprofile, categorie, contact, productform, showblog
# Create your tests here.
class TestUrls(SimpleTestCase):

      # For blog
    def test_case_blog_url(self):
        url=reverse('blog')
        self.assertEquals(resolve(url).func,showblog)

    # For creatorprofile
    def test_case_blog_detail_url(self):
        url=reverse('creatorprofile')
        self.assertEquals(resolve(url).func,creatorprofile)

      # For categorie
    def test_case_categorie_detail_url(self):
        url=reverse('categorie')
        self.assertEquals(resolve(url).func,categorie)
    
    # For signuplogin
    def test_case_signuplogin_detail_url(self):
        url=reverse('contact')
        self.assertEquals(resolve(url).func,contact)

    # For contact
    def test_case_contact_detail_url(self):
        url=reverse('productform')
        self.assertEquals(resolve(url).func,productform)