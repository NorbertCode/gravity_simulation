import center_object
import point_object
from PIL import Image, ImageDraw


class Simulation:
    def __init__(self, resolution, meters_per_pixel, center_object, point_objects):
        self._resolution = resolution
        self._meters_per_pixel = meters_per_pixel
        self._center_object = center_object
        self._point_objects = point_objects

    def draw(self, center_object, point_objects):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        image_center = (self._resolution[0] / 2, self._resolution[1] / 2)
        pixel_radius = (self._center_object.diameter / 2) / self._meters_per_pixel
        center_obj_fill_color = (255, 255, 255)
        draw_output.circle(image_center, pixel_radius, fill=center_obj_fill_color)

        point_obj_fill_color = (0, 255, 0)
        for obj in point_objects:
            obj_position = (obj.position[0] / self._meters_per_pixel,
                             obj.position[1] / self._meters_per_pixel)
            draw_output.point(obj_position, point_obj_fill_color)

        output.show()


test_objs = [point_object.PointObject((200, 200), 100, None),
             point_object.PointObject((750, 750), 500, None),
             point_object.PointObject((200, 750), 1000, None)]
sim = Simulation((128, 128), 10, center_object.CenterObject(100, 0), test_objs)
sim.draw(sim._center_object, sim._point_objects)
