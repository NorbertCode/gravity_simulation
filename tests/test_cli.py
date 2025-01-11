import numpy as np
from cli import CommandLineInterface
from config_data import ConfigData
from center_object import CenterObject
from point_object import PointObject


def test_load_config_from_input_valid(monkeypatch):
    inputs = iter([
        "10", "256", "256", "100",  # General output configuration
        "200", "1000",  # Center object configuration
        "1", "100", "100", "200", "200", "10"  # Point objects configuration
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    config = CommandLineInterface._load_config_from_input()
    assert isinstance(config, ConfigData)
    assert config.steps == 10
    assert config.resolution == (256, 256)
    assert config.meters_per_pixel == 100
    assert isinstance(config.center_obj, CenterObject)
    assert config.center_obj.diameter == 200
    assert config.center_obj.mass == 1000
    assert len(config.point_objs) == 1
    assert isinstance(config.point_objs[0], PointObject)
    np.testing.assert_array_equal(config.point_objs[0].position, [100, 100])
    assert config.point_objs[0].mass == 10
    np.testing.assert_array_equal(config.point_objs[0].velocity, [200, 200])


def test_load_config_from_input_invalid_general(monkeypatch):
    inputs = iter([
        "a", "10", "256", "b", "10", "256", "256", "100",  # General output configuration
        "200", "1000",  # Center object configuration
        "1", "100", "100", "200", "200", "10"  # Point objects configuration
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    config = CommandLineInterface._load_config_from_input()
    assert isinstance(config, ConfigData)
    assert config.steps == 10
    assert config.resolution == (256, 256)
    assert config.meters_per_pixel == 100
    assert isinstance(config.center_obj, CenterObject)
    assert config.center_obj.diameter == 200
    assert config.center_obj.mass == 1000
    assert len(config.point_objs) == 1
    assert isinstance(config.point_objs[0], PointObject)
    np.testing.assert_array_equal(config.point_objs[0].position, [100, 100])
    assert config.point_objs[0].mass == 10
    np.testing.assert_array_equal(config.point_objs[0].velocity, [200, 200])


def test_load_config_from_input_invalid_center_obj(monkeypatch):
    inputs = iter([
        "10", "256", "256", "100",  # General output configuration
        "200", "a", "200", "1000",  # Center object configuration
        "1", "100", "100", "200", "200", "10"  # Point objects configuration
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    config = CommandLineInterface._load_config_from_input()
    assert isinstance(config, ConfigData)
    assert config.steps == 10
    assert config.resolution == (256, 256)
    assert config.meters_per_pixel == 100
    assert isinstance(config.center_obj, CenterObject)
    assert config.center_obj.diameter == 200
    assert config.center_obj.mass == 1000
    assert len(config.point_objs) == 1
    assert isinstance(config.point_objs[0], PointObject)
    np.testing.assert_array_equal(config.point_objs[0].position, [100, 100])
    assert config.point_objs[0].mass == 10
    np.testing.assert_array_equal(config.point_objs[0].velocity, [200, 200])


def test_load_config_from_input_invalid_point_obj_amount(monkeypatch):
    inputs = iter([
        "10", "256", "256", "100",  # General output configuration
        "200", "1000",  # Center object configuration
        "a", "3.5", "1", "100", "100", "200", "200", "10"  # Point objects configuration
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    config = CommandLineInterface._load_config_from_input()
    assert isinstance(config, ConfigData)
    assert config.steps == 10
    assert config.resolution == (256, 256)
    assert config.meters_per_pixel == 100
    assert isinstance(config.center_obj, CenterObject)
    assert config.center_obj.diameter == 200
    assert config.center_obj.mass == 1000
    assert len(config.point_objs) == 1
    assert isinstance(config.point_objs[0], PointObject)
    np.testing.assert_array_equal(config.point_objs[0].position, [100, 100])
    assert config.point_objs[0].mass == 10
    np.testing.assert_array_equal(config.point_objs[0].velocity, [200, 200])


def test_load_config_from_input_invalid_point_obj(monkeypatch):
    inputs = iter([
        "10", "256", "256", "100",  # General output configuration
        "200", "1000",  # Center object configuration
        # Point objects configuration
        "1", "100", "a", "100", "100",
        "200", "200", "10"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    config = CommandLineInterface._load_config_from_input()
    assert isinstance(config, ConfigData)
    assert config.steps == 10
    assert config.resolution == (256, 256)
    assert config.meters_per_pixel == 100
    assert isinstance(config.center_obj, CenterObject)
    assert config.center_obj.diameter == 200
    assert config.center_obj.mass == 1000
    assert len(config.point_objs) == 1
    assert isinstance(config.point_objs[0], PointObject)
    np.testing.assert_array_equal(config.point_objs[0].position, [100, 100])
    assert config.point_objs[0].mass == 10
    np.testing.assert_array_equal(config.point_objs[0].velocity, [200, 200])
