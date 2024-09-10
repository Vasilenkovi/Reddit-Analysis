from django.test import SimpleTestCase
from django.http import HttpRequest
from .forms import Dataset_operation_form

# Create your tests here.
class Dataset_form_test(SimpleTestCase):

    def test_dataset_form(self):

        # Correct combinations of similar ids
        request = HttpRequest()
        request.POST.appendlist("prsr_27", "on")
        request.POST.appendlist("prsr_28", "on")

        form = Dataset_operation_form(request)
        self.assertTrue(form.clean())
        
        request = HttpRequest()
        request.POST.appendlist("prsc_65", "on")
        request.POST.appendlist("prsc_66", "on")

        form = Dataset_operation_form(request)
        self.assertTrue(form.clean())

        # Incorrect combination of ids
        request = HttpRequest()
        request.POST.appendlist("prsc_65", "on")
        request.POST.appendlist("prsr_28", "on")

        form = Dataset_operation_form(request)
        self.assertFalse(form.clean())