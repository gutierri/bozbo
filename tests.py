import io
import unittest
from unittest.mock import patch

from webtest import TestApp
from bozbo import routers, builder_actions, app


class TestFakeSetup(unittest.TestCase):
    @patch('builtins.open')
    def tests_router_patterns(self, mock_cfg):
        mock_cfg.return_value = io.StringIO('''[events]
                                               [favorites]''')
        router_patterns = routers()

        self.assertCountEqual(['/events', '/favorites'],
                              router_patterns.keys())

    @patch('builtins.open')
    def test_dynamic_router_patterns(self, mock_cfg):
        mock_cfg.return_value = io.StringIO('''[events]
                                               [events:<id>]
                                               [events:<id>:delete]''')

        router_patterns = routers()

        self.assertCountEqual(['/events', '/events/<id>',
                               '/events/<id>/delete'], router_patterns.keys())

    @patch('builtins.open')
    def test_props_router(self, mock_cfg):
        mock_cfg.return_value = io.StringIO('''[events]
                                               methods = post
                                                         get
                                                         put

                                               response = name
                                                          address''')

        router_patterns = routers()

        self.assertCountEqual(['methods', 'response'],
                              router_patterns['/events'].keys())

    @patch('builtins.open')
    def test_builder_router_actions(self, mock_cfg):
        # TODO: tests assert view func
        mock_cfg.return_value = io.StringIO('''[events]
                                               methods = post
                                                         get
                                                         put

                                               response = name
                                                          address''')

        router_patterns = routers()

        actions = builder_actions(router_patterns)

        self.assertEqual(len(actions[0]), 3)
        self.assertEqual(actions[0][0], '/events')
        self.assertEqual(actions[0][1], ['post', 'get', 'put'])


class TestFakeAPI(unittest.TestCase):
    @patch('builtins.open')
    def test_function_simple_router(self, mock_cfg):
        mock_cfg.return_value = io.StringIO('''[endpoint]'
                                               methods = get
                                               response = name''')

        api = app()

        resp = TestApp(api).get('/endpoint')

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        self.assertCountEqual(['name'], resp.json.keys())

    @patch('builtins.open')
    def test_function_simple_list_router(self, mock_cfg):
        mock_cfg.return_value = io.StringIO('''[endpoint]'
                                               methods=get
                                               list=1
                                               count=2
                                               response=name

                                               [endpoint:<idx>]
                                               methods=get
                                               response=name

                                               [endpoint:<idx>:path]
                                               methods=get
                                               response=name''')

        api = app()

        client = TestApp(api)

        self.assertEqual(200, client.get('/endpoint').status_code)
        self.assertEqual('application/json',
                         client.get('/endpoint').content_type)
        self.assertEqual(len(client.get('/endpoint').json), 2)

        self.assertEqual(client.get('/endpoint/1').status_code, 200)
        self.assertEqual(client.get('/endpoint/1/path').status_code, 200)
