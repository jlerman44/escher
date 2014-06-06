import escher.server
from escher import (Builder, get_cache_dir, clear_cache, list_cached_maps,
                    list_cached_models)
from escher.plots import load_resource

import os
from os.path import join
import json
from pytest import raises
from tornado.httpclient import HTTPError

def test_get_cache_dir():
    d = get_cache_dir()
    assert os.path.isdir(d)
    d = get_cache_dir(name='maps')
    assert os.path.isdir(d)

def test_clear_cache():
    clear_cache()
    d = get_cache_dir(name='maps')
    assert len(os.listdir(d)) == 0
    d = get_cache_dir(name='models')
    assert len(os.listdir(d)) == 0

def test_list_cached_maps():
    clear_cache()
    Builder(map_name='iJO1366_central_metabolism')
    assert list_cached_maps() == ['iJO1366_central_metabolism']

def test_list_cached_models():
    clear_cache()
    Builder(model_name='iJO1366')
    assert list_cached_models() == ['iJO1366']
        
def test_load_resource(tmpdir):
    assert load_resource('{"r": "val"}', 'name') == '{"r": "val"}'
    
    directory = os.path.abspath(os.path.dirname(__file__))
    assert load_resource(join(directory, 'example.json'), 'name').strip() == '{"r": "val"}'
    
    url = "https://zakandrewking.github.io/escher/maps/v1/iJO1366_central_metabolism.json"
    _ = json.loads(load_resource(url, 'name'))
        
    with raises(HTTPError):
        load_resource("http://www.asodivhowef.com", 'name')
       
    with raises(HTTPError):
        load_resource("https://www.asodivhowef.com", 'name')

    with raises(ValueError) as err:
        p = join(str(tmpdir), 'dummy')
        with open(p, 'w') as f:
            f.write('dummy')
        load_resource(p, 'name')
        assert 'not a valid json file' in err.value

def test_Builder():
    b = Builder(map_json='{"r": "val"}', model_json='{"r": "val"}')
    b.embedded_html(dev=True, enable_editing=True, height=100)
    b.standalone_html(dev=True)
    b.display_in_notebook(height=200)

    # download
    b = Builder(map_name='iJO1366_central_metabolism', model_name='iJO1366')
    assert b.loaded_map_json is not None
    assert b.loaded_model_json is not None
    b.embedded_html(dev=True, enable_editing=True, height=100)
    b.standalone_html(dev=True)
    b.display_in_notebook(height=200)

    # data
    b = Builder(map_name='iJO1366_central_metabolism', model_name='iJO1366',
                reaction_data=[{'GAPD': 123}, {'GAPD': 123}])
    b = Builder(map_name='iJO1366_central_metabolism', model_name='iJO1366',
                metabolite_data=[{'nadh_c': 123}, {'nadh_c': 123}])

    assert type(b.the_id) is unicode
    assert len(b.the_id) == 10
