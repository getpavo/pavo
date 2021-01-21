import os
from jackman.helpers import is_yaml, load_yaml


def test_is_yaml_false():
    assert is_yaml('/dummy_project/empty.notyaml') is False
    assert is_yaml('/dummy_project/empty.yaml.not') is False


def test_is_yaml_yml():
    assert is_yaml('/dummy_project/mock.yml') is True
    assert is_yaml('/dummy_project/mock.test.yml') is True


def test_is_yaml_yaml():
    assert is_yaml('/dummy_project/mock.yaml') is True
    assert is_yaml('/dummy_project/mock.test.yml') is True


def test_load_yaml_unusable_file(caplog):
    items = load_yaml('/dummy_project/file.notyaml')
    assert items == {}
    assert caplog.records
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert record.msg == 'Unable to read data from "/dummy_project/file.notyaml". It is not a yaml-file.'


def test_load_yaml_file_not_exists(caplog):
    items = load_yaml('/dummy_project/notexists.yaml')
    assert items == {}
    assert caplog.records
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert type(record.msg) == FileNotFoundError


def test_load_yaml_file_exists():
    items = load_yaml(f'{os.path.dirname(os.path.abspath(__file__))}/dummy.yaml')
    check_items = {
        'foo': 'bar',
        'lorem': [
            'ipsum',
            'dolor',
            'sit',
            'amet'
        ]
    }
    assert items == check_items

