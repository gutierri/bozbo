import json
import ConfigParser

import faker
from bottle import Bottle, response


def routers(cfg='routes.cfg'):
    config = ConfigParser.RawConfigParser()
    config.readfp(open(cfg))

    sections = config.sections()
    sections_props = config.items
    endpoints = ['/{}'.format(endpoint.replace(':', '/'))
                 for endpoint in sections]

    props = {endpoints[i]: dict(sections_props(section))
             for i, section in enumerate(sections)}

    return props


def view(resp_data, props=[]):
    fake = faker.Faker()
    resp = {k: getattr(fake, k)() for k in resp_data}
    if len(props) == 2:
        resp = [{k: getattr(fake, k)() for k in resp_data}
                for _ in range(0, int(props[1]))]

    def _view():
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
