import pytest
import errors
import numpy as np
from space_object import SpaceObject
from center_object import CenterObject
from point_object import PointObject


def test_space_object_defaults():
    space_obj = SpaceObject()
    np.testing.assert_array_equal(space_obj.position, np.array([0, 0]))
    assert space_obj.mass == 1.0


def test_space_object():
    space_obj = SpaceObject(np.array([123, 456]), 100)
    np.testing.assert_array_equal(space_obj.position, np.array([123, 456]))
    assert space_obj.mass == 100


def test_space_object_negative_mass():
    with pytest.raises(errors.NegativeMassError):
        _ = SpaceObject(mass=-1)


def test_center_object_defaults():
    center_obj = CenterObject()
    np.testing.assert_array_equal(center_obj.position, np.array([0, 0]))
    assert center_obj.mass == 1.0
    assert center_obj.diameter == 1.0


def test_center_object():
    center_obj = CenterObject(100, 200)
    np.testing.assert_array_equal(center_obj.position, np.array([0, 0]))
    assert center_obj.diameter == 100
    assert center_obj.mass == 200


def test_center_object_negative_diameter():
    with pytest.raises(errors.NegativeDiameterError):
        _ = CenterObject(diameter=-1)


def test_center_object_from_json():
    json_data = {
        "diameter": 100,
        "mass": 200
    }
    center_obj = CenterObject.from_json(json_data)
    assert center_obj.diameter == 100
    assert center_obj.mass == 200


def test_center_object_from_json_invalid_data():
    json_data = {
        "diameter": "100",
        "mass": 200
    }
    with pytest.raises(errors.InvalidCenterObjectDataError):
        _ = CenterObject.from_json(json_data)


def test_center_object_serialize():
    center_obj = CenterObject(100, 200)
    serialized = center_obj.serialize()
    assert serialized == {
        "diameter": 100,
        "mass": 200
    }


def test_point_object_defaults():
    point_obj = PointObject()
    np.testing.assert_array_equal(point_obj.position, np.array([0, 0]))
    assert point_obj.mass == 1.0
    np.testing.assert_array_equal(point_obj.velocity, np.array([0, 0]))


def test_point_object():
    point_obj = PointObject(np.array([123, 456]), 100, np.array([123, 456]))
    np.testing.assert_array_equal(point_obj.position, np.array([123, 456]))
    assert point_obj.mass == 100
    np.testing.assert_array_equal(point_obj.velocity, np.array([123, 456]))


def test_point_object_from_json():
    json_data = {
        "position": [123, 456],
        "mass": 100,
        "velocity": [123, 456]
    }
    point_obj = PointObject.from_json(json_data)
    np.testing.assert_array_equal(point_obj.position, np.array([123, 456]))
    assert point_obj.mass == 100
    np.testing.assert_array_equal(point_obj.velocity, np.array([123, 456]))


def test_point_object_from_json_invalid_data():
    json_data = {
        "position": [123, 456],
        "mass": 100,
        "velocity": [123, "456"]
    }
    with pytest.raises(errors.InvalidPointObjectDataError):
        _ = PointObject.from_json(json_data)


def test_point_object_serialize():
    point_obj = PointObject(np.array([123, 456]), 100, np.array([123, 456]))
    serialized = point_obj.serialize()
    assert serialized == {
        "velocity": [123, 456],
        "mass": 100,
        "position": [123, 456]
    }


def test_point_object_verify_vector_correct():
    assert PointObject._verify_vector(np.array([1, 2, 3.0, 5.2]))


def test_point_object_verify_vector_incorrect():
    assert not PointObject._verify_vector(np.array([1, 2, 3.0, "g"]))
