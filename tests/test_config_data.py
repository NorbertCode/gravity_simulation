import pytest
import json
import numpy as np
import errors
from config_data import ConfigData
from center_object import CenterObject
from point_object import PointObject


@pytest.fixture
def valid_sim_config():
    return {
        "steps": 100,
        "resolution": [128, 128],
        "meters_per_pixel": 1,
        "center_object": {
            "diameter": 1,
            "mass": 1
        },
        "point_objects": [
            {
                "velocity": [0, 0],
                "mass": 1,
                "position": [0, 0]
            }
        ]
    }


@pytest.fixture
def invalid_steps_sim_config():
    return {
        "steps": "1",
        "resolution": [128, 128],
        "meters_per_pixel": 1,
        "center_object": {
            "diameter": 1,
            "mass": 1
        },
        "point_objects": [
            {
                "velocity": [0, 0],
                "mass": 1,
                "position": [0, 0]
            }
        ]
    }


@pytest.fixture
def invalid_resolution_sim_config():
    return {
        "steps": 1,
        "resolution": [128, "128"],
        "meters_per_pixel": 1,
        "center_object": {
            "diameter": 1,
            "mass": 1
        },
        "point_objects": [
            {
                "velocity": [0, 0],
                "mass": 1,
                "position": [0, 0]
            }
        ]
    }


@pytest.fixture
def invalid_meters_per_pixel_sim_config():
    return {
        "steps": 1,
        "resolution": [128, 128],
        "meters_per_pixel": "1",
        "center_object": {
            "diameter": 1,
            "mass": 1
        },
        "point_objects": [
            {
                "velocity": [0, 0],
                "mass": 1,
                "position": [0, 0]
            }
        ]
    }


def test_from_json_valid(tmp_path, valid_sim_config):
    config_file = tmp_path / "config.json"
    with config_file.open("w") as file:
        json.dump(valid_sim_config, file, indent=4)

    config = ConfigData.from_json(str(config_file))
    assert config.steps == 100
    np.testing.assert_array_equal(config.resolution, [128, 128])
    assert config.meters_per_pixel == 1
    assert config.center_obj.diameter == 1
    assert config.center_obj.mass == 1
    np.testing.assert_array_equal(config.point_objs[0].velocity, [0, 0])
    assert config.point_objs[0].mass == 1
    np.testing.assert_array_equal(config.point_objs[0].position, [0, 0])


def test_from_json_invalid_steps(tmp_path, invalid_steps_sim_config):
    config_file = tmp_path / "config.json"
    with config_file.open("w") as file:
        json.dump(invalid_steps_sim_config, file)

    with pytest.raises(errors.InvalidStepsError):
        ConfigData.from_json(str(config_file))


def test_from_json_invalid_resolution(tmp_path, invalid_resolution_sim_config):
    config_file = tmp_path / "config.json"
    with config_file.open("w") as file:
        json.dump(invalid_resolution_sim_config, file)

    with pytest.raises(errors.InvalidResolutionError):
        ConfigData.from_json(str(config_file))


def test_from_json_invalid_meter_per_pixel(tmp_path,
                                           invalid_meters_per_pixel_sim_config):
    config_file = tmp_path / "config.json"
    with config_file.open("w") as file:
        json.dump(invalid_meters_per_pixel_sim_config, file)

    with pytest.raises(errors.InvalidMetersPerPixelError):
        ConfigData.from_json(str(config_file))


def test_from_json_no_file():
    with pytest.raises(errors.UnableToOpenConfigError):
        ConfigData.from_json("non_existent_file.json")


def test_save_data_to_json(tmp_path, valid_sim_config):
    saved_config = ConfigData(valid_sim_config["steps"], valid_sim_config["resolution"],
                        valid_sim_config["meters_per_pixel"],
                        CenterObject.from_json(valid_sim_config["center_object"]),
                        [PointObject.from_json(valid_sim_config["point_objects"][0])])

    config_file = tmp_path / "config.json"
    saved_config.save_data_to_json(str(config_file))

    loaded_config = ConfigData.from_json(str(config_file))

    assert saved_config.steps == loaded_config.steps
    assert saved_config.resolution == loaded_config.resolution
    assert saved_config.meters_per_pixel == loaded_config.meters_per_pixel
    assert saved_config.center_obj.diameter == loaded_config.center_obj.diameter
    assert saved_config.center_obj.mass == loaded_config.center_obj.mass
    np.testing.assert_array_equal(saved_config.point_objs[0].velocity,
                                  loaded_config.point_objs[0].velocity)
    assert saved_config.point_objs[0].mass == loaded_config.point_objs[0].mass
    np.testing.assert_array_equal(saved_config.point_objs[0].position,
                                  loaded_config.point_objs[0].position)
