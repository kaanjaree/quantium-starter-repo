import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app():
    app = import_app("dash_app")  
    return app

def test_header_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods Sales Visualizer"

def test_graph_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-graph")
    assert graph is not None

def test_region_picker_is_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    radio_items = dash_duo.find_element("#region-filter")
    assert radio_items is not None
