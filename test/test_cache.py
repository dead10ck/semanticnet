import pytest
import uuid

def test_cache_by(populated_graph):
    # add another node with the same type to make sure it works for multiple nodes
    # with the same attribute
    populated_graph.add_node({"type": "A"}, '2b673235a0b94935ab8b6b9de178d341')

    # cache by the attribute "type"
    populated_graph.cache_nodes_by("type")

    in_cache = populated_graph._node_cache
    out_cache = {
        "type": {
            "B": [{
                "id": uuid.UUID('2cdfebf3-bf95-47f1-9f04-12ccdfbe03b7'),
                'type': 'B'
            }],
            "A": [
                {
                    "id": uuid.UUID('3caaa8c0-9148-493d-bdf0-2c574b95526c'),
                    "type": "A"
                },
                {
                    "id": uuid.UUID('2b673235a0b94935ab8b6b9de178d341'),
                    "type": "A"
                }
            ],
            "C": [{
                "id": uuid.UUID('3cd197c2-cf5e-42dc-9ccd-0c2adcaf4bc2'),
                'type': 'C'
            }]
        }
    }
    assert in_cache == out_cache

def test_cache_by_build_false(populated_graph):
    populated_graph.cache_nodes_by("type", build=False)

    assert (
        populated_graph._node_cache ==
        {
            "type": {}
        }
    )

def test_add_node_with_cache(populated_graph):
    populated_graph.cache_nodes_by("type")

    ### get all nodes with attr "type"
    input_ = populated_graph.get_nodes_by_attr("type")
    output = {
        "A": [
            {
                "id": uuid.UUID('3caaa8c0-9148-493d-bdf0-2c574b95526c'),
                "type": "A"
            }
        ],
        "B": [{
            "id": uuid.UUID('2cdfebf3-bf95-47f1-9f04-12ccdfbe03b7'),
            'type': 'B'
        }],
        "C": [{
            "id": uuid.UUID('3cd197c2-cf5e-42dc-9ccd-0c2adcaf4bc2'),
            'type': 'C'
        }]
    }

    assert input_ == output

    # Add a new node of the same type as another. Should be in the cache.
    populated_graph.add_node({"type": "A"}, '2b673235a0b94935ab8b6b9de178d341')
    input_ = populated_graph.get_nodes_by_attr("type", "A")
    output = [
        {
            "id": uuid.UUID('3caaa8c0-9148-493d-bdf0-2c574b95526c'),
            "type": "A"
        },
        {
            "id": uuid.UUID('2b673235a0b94935ab8b6b9de178d341'),
            "type": "A"
        }
    ]

    assert input_ == output

    # add a new node with an attribute that we are not caching.
    # Should NOT be in the cache
    populated_graph.add_node({"label": "test"}, 'fa02d5e82ed54baf828558c70317f20e')
    input_ = populated_graph._node_cache
    output = {
        "type": {
            "A": [
                {
                    "id": uuid.UUID('3caaa8c0-9148-493d-bdf0-2c574b95526c'),
                    "type": "A"
                },
                {
                    "id": uuid.UUID('2b673235a0b94935ab8b6b9de178d341'),
                    "type": "A"
                }
            ],
            "B": [{
                "id": uuid.UUID('2cdfebf3-bf95-47f1-9f04-12ccdfbe03b7'),
                'type': 'B'
            }],
            "C": [{
                "id": uuid.UUID('3cd197c2-cf5e-42dc-9ccd-0c2adcaf4bc2'),
                'type': 'C'
            }]
        }
    }

    assert input_ == output

def test_set_node_attribute_with_cache(populated_graph):
    populated_graph.cache_nodes_by("type")
    populated_graph.set_node_attribute('3caaa8c09148493dbdf02c574b95526c', 'type', 'B')

    a_nodes = populated_graph.get_nodes_by_attr("type", "A")
    b_nodes = populated_graph.get_nodes_by_attr("type", "B")

    node_a = populated_graph.get_node('3caaa8c09148493dbdf02c574b95526c')

    assert node_a not in a_nodes
    assert node_a in b_nodes

def test_remove_node_with_cache(populated_graph):
    populated_graph.add_node({"type": "A"}, '2b673235a0b94935ab8b6b9de178d341')
    populated_graph.cache_nodes_by("type")
    populated_graph.remove_node('3caaa8c09148493dbdf02c574b95526c')

    input_ = populated_graph.get_nodes_by_attr("type", "A")
    output = [{
        "id": uuid.UUID('2b673235a0b94935ab8b6b9de178d341'),
        "type": "A"
    }]

    assert input_ == output