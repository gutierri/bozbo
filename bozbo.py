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
    if len(props) is 2:
        resp = [{k: getattr(fake, k)() for k in resp_data}
                for _ in range(0, int(props[1]))]

    def _view():
        response.content_type = 'application/json'
        return json.dumps(resp)
    return _view

def builder_actions(r):
    x = []
    for k, v in r.items():
        props = []
        if 'list' in v and 'count' in v:
            props = [v['list'], v['count']]
        x.append([k, v['methods'].split('\n'),
                  view(v['response'].split('\n'), props)])
    return x


def app(setup_routers='routes.cfg'):
    app = Bottle()
    for build_action in builder_actions(routers(setup_routers)):
        app.route(build_action[0], build_action[1], build_action[2])
    return app


if __name__ == '__main__':
    app_main = app()
    app_main.run(host='localhost', port=8080)
