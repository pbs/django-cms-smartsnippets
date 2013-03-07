"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.sites.models import Site
from django.core.exceptions import NON_FIELD_ERRORS


class TemplateCodeValidationTest(TestCase):

    def setUp(self):
        self.username = 'test_smartsnippets_user'

        try:
            User.objects.get(username__exact=self.username)
        except User.DoesNotExist:
            User.objects.create_superuser(
                username=self.username, password='x',
                email='%s@smartsnippets.com' % self.username)

        self.client = Client()
        self.assertTrue(self.client.login(username=self.username,
                                          password='x'))
        self.site_id = Site.objects.get_or_create(domain="example.com",
                                                  name="example.com")[0].id

        self.snippet_test = 'smartsnippet_name4test'
        self.add_url = '/admin/smartsnippets/smartsnippet/add/'

    def _build_vars(self, is_regular, data, variables):
        prefix, var_type = ('-', 'widget') \
            if is_regular else ('-2-', 'choices')
        count = data['variables%sTOTAL_FORMS' % prefix]
        for var_tuple in variables:
            count_prefix = '%s%d-' % (prefix, count)
            data.update({
                'variables%sname' % count_prefix: var_tuple[0],
                'variables%s%s' % (count_prefix, var_type): var_tuple[1],
            })
            if len(var_tuple) == 3:
                data['variables%sDELETE' % count_prefix] = var_tuple[2]
            count += 1

        data['variables%sTOTAL_FORMS' % prefix] = count
        return data

    def _add_variables_forms(self, regular_vars, dropdwn_vars):
        data = {
            'variables-TOTAL_FORMS': 0, 'variables-INITIAL_FORMS': 0,
            'variables-2-TOTAL_FORMS': 0, 'variables-2-INITIAL_FORMS': 0,
        }
        data.update(self._build_vars(True, data, regular_vars))
        data.update(self._build_vars(False, data, dropdwn_vars))

        return data

    def _build_data(self, name, code, sites,
                    regular_vars=[], dropdwn_vars=[]):
        data = {
            'name': name,
            'template_code': code,
            'sites': sites,
        }
        data.update(self._add_variables_forms(regular_vars, dropdwn_vars))
        return data

    def _trigger_validation(self, post_data, expected_string_err='error'):
        response = self.client.post(self.add_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_string_err)
        return response

    def assertValidationOnField(self, field, message, response):
        field_errs = response.context['adminform'].form.errors
        self.assertTrue(field in field_errs)
        self.assertIn(message, field_errs[field])

    def assertValidationFormFromInlines(self, message, resp):
        self.assertEqual(resp.context['inline_admin_formsets'][0].formset
            .get_form_error(), message)

    def assertValidationOnNonField(self, message, resp):
        errors = [e for e in resp.context['adminform'].form
                  .errors[NON_FIELD_ERRORS] if message in e]
        self.assertTrue(True if errors else False)

    def test_required_template_code_validation(self):
        ss_data = self._build_data(self.snippet_test, '', [self.site_id])

        response = self._trigger_validation(ss_data, 'errors')

        self.assertValidationOnField('template_code',
                                     'This field is required.', response)

    def test_variables_name_duplication(self):

        ss_data = self._build_data(
            self.snippet_test, 'some {{code}}',
            [self.site_id],
            [('code', 'TextField')],
            [('code', 'choice1, choice2'), ('code2', 'choice1, choice2')])

        resp = self._trigger_validation(ss_data)
        msg = 'Please correct the duplicate values below.'
        self.assertValidationFormFromInlines(msg, resp)

    def test_required_variables(self):
        ss_data = self._build_data(
            self.snippet_test, 'some {{code}} {{some}} {{more}} {{code}}',
            [self.site_id],
            [('code', 'TextField'), ('some', 'ImageField')],
            [('code2', 'choice5, choice6')])

        resp = self._trigger_validation(ss_data)

        self.assertValidationOnNonField('Undefined variables', resp)

    def test_required_variables_but_marked_for_deletion(self):
        ss_data = self._build_data(
            self.snippet_test, 'some {{code}} {{some}} {{more}} {{code}}',
            [self.site_id],
            [('code', 'TextField'), ('some', 'ImageField', True)],
            [('code2', 'choice5, choice6'), ('more', 'one choice')])

        resp = self._trigger_validation(ss_data)
        msg = 'Needed variables marked for deletion'
        self.assertValidationOnNonField(msg, resp)

    def tearDown(self):
        user = User.objects.get(username__exact=self.username)
        user.delete()
