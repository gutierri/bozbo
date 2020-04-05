import json
from configparser import ConfigParser

import faker
from bottle import Bottle, response


def routers(cfg='routes.cfg'):
    config = ConfigParser()
    config.read_file(open(cfg))

    sections = config.sections()
    endpoints = ['/{}'.format(section_to_endpoint.replace(':', '/'))
                 for section_to_endpoint in sections]

    map_urls_patterns = {endpoints[i]: dict(config.items(section))
                         for i, section in enumerate(sections)}

    return map_urls_patterns


def view(resp_data, props=[]):
    fake = faker.Faker()

    resp = {k: getattr(fake, k)() for k in resp_data}

    if len(props) == 2:
        resp = [{k: getattr(fake, k)() for k in resp_data}
                for _ in range(0, int(props[1]))]

    def _view(*args, **kwargs):
        response.content_type = 'application/json'
        return json.dumps(resp)
    return _view


def builder_actions(r):
    response_list = []
    for router_endpoint, router_props in r.items():
        props = []
        if 'list' in router_props and 'count' in router_props:
            props = [router_props['list'], router_props['count']]
        response_list.append([router_endpoint,
                              router_props['methods'].split('\n'),
                              view(router_props['response'].split('\n'),
                                   props)])
    return response_list


def app(setup_routers='routes.cfg'):
    app = Bottle()
    for build_action in builder_actions(routers(setup_routers)):
        app.route(build_action[0], build_action[1], build_action[2])
    return app
