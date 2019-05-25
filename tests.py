#!/usr/bin/env python
import io
import unittest

from webtest import TestApp
from mock import patch

from bozbo import routers, builder_actions, app


class TestFakeAPI(unittest.TestCase):
    def test_builder_routers(self):
        router01 = ('[events]' '\n'
                    '[favorites]')
        with patch('__builtin__.open', return_value=io.BytesIO(router01)) as _:
            endpoints_01 = routers()

        router02 = ('[events]'      '\n'
                    '[events:<id>]' '\n'
                    '[events:<id>:delete]')
        with patch('__builtin__.open', return_value=io.BytesIO(router02)) as _:
            endpoints_02 = routers()

        self.assertEqual(['/events', '/favorites'], endpoints_01.keys())
        self.assertEqual(['/events', '/events/<id>', '/events/<id>/delete'],
                         sorted(endpoints_02.keys()))

    def test_props_routers(self):
        router03 = ('[events]'        '\n'
                    'methods = post'  '\n'
                    '          get'   '\n'
                    '          put'   '\n'
                    'response = name' '\n'
                    '        address' '\n')
        with patch('__builtin__.open', return_value=io.BytesIO(router03)) as _:
            r = routers()
        self.assertEqual(['methods', 'response'], r['/events'].keys())

    def test_builder_actions(self):
        # TODO: tests assert view func
        router03 = ('[events]'           '\n'
                    'methods = post'     '\n'
                    '          get'      '\n'
                    '          put'      '\n'
                    'response = name'    '\n'
                    '           address' '\n')
        with patch('__builtin__.open', return_value=io.BytesIO(router03)) as _:
            r = routers()
        actions = builder_actions(r)
        self.assertEqual(len(actions[0]), 3)
        self.assertEqual(actions[0][0], '/events')
        self.assertEqual(actions[0][1], ['post', 'get', 'put'])

    def test_function_simple_router(self):
        router03 = ('[endpoint]'    '\n'
                    'methods = get' '\n'
                    'response = name')
        with patch('__builtin__.open', return_value=io.BytesIO(router03)) as _:
            app_ = app()
        app_main = TestApp(app_)
        self.assertEqual(app_main.get('/endpoint').status_code, 200)
        self.assertEqual(app_main.get('/endpoint').content_type,
                         'application/json')
        self.assertEqual(app_main.get('/endpoint').json.keys(), ['name'])

    def test_function_simple_list_router(self):
        router03 = ('[endpoint]'      '\n'
                    'methods = get'   '\n'
                    'list = 1'        '\n'
                    'count = 2'       '\n'
                    'response = name' '\n'
                    '[endpoint:<idx>]' '\n'
                    'methods = get'   '\n'
                    'response = name' '\n'
                    '[endpoint:<idx>:path]' '\n'
                    'methods = get'   '\n'
                    'response = name' '\n')
        with patch('__builtin__.open', return_value=io.BytesIO(router03)) as _:
            app_ = app()
        app_main = TestApp(app_)
        self.assertEqual(app_main.get('/endpoint').status_code, 200)
        self.assertEqual(app_main.get('/endpoint').content_type,
                         'application/json')
        self.assertEqual(len(app_main.get('/endpoint').json), 2)

        self.assertEqual(app_main.get('/endpoint/1').status_code, 200)
        self.assertEqual(app_main.get('/endpoint/1/path').status_code, 200)
