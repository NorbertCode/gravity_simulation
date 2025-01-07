import numpy as np
from PIL import Image, ImageDraw
from point_object import PointObject
from center_object import CenterObject
from collision import Collision


class SimulationVisualizer:
    def __init__(self, resolution: list[int], meters_per_pixel: float,
                 center_obj_color: tuple[int], point_obj_color: tuple[int],
                 point_obj_end_color: tuple[int]):
        self._resolution = resolution
        self._meters_per_pixel = meters_per_pixel

        self._center_obj_color = center_obj_color
        self._point_obj_color = point_obj_color
        self._point_obj_end_color = point_obj_end_color

    def draw(self, center_obj: CenterObject, point_objs: list[PointObject],
             simulation_steps: list[list[np.array]]) -> Image.Image:
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        pixel_radius = round((center_obj.diameter / 2) / self._meters_per_pixel)
        img_center = [round(self._resolution[0] / 2), round(self._resolution[1] / 2)]
        draw_output.circle(img_center, pixel_radius, fill=self._center_obj_color)

        for step in simulation_steps:
            for obj_pos in step:
                if obj_pos is not np.nan:
                    obj_pos[1] *= -1  # Y axis has to be inverted
                    # This is because on the image it rises the lower it goes, which
                    # is the opposite of how it works in 2D geometry
                    pixel_pos = (obj_pos / self._meters_per_pixel).round()
                    draw_output.point(tuple(img_center + pixel_pos),
                                      self._point_obj_color)

        for obj in point_objs:
            obj_pos = obj.position * np.array([1, -1])  # Invert Y axis
            pos = img_center + (obj_pos / self._meters_per_pixel).round()
            draw_output.point(tuple(pos), self._point_obj_end_color)

        return output

    @staticmethod
    def generate_collision_report(collision_data: list[Collision]) -> str:
        """Presents the given collision data in a readable format"""
        output = ""
        for collision in collision_data:
            if len(collision.point_obj_indexes) > 1:
                objects = ""
                for obj in collision.point_obj_indexes:
                    objects += f"n={obj}, "
                output += f"Objects {objects[:-2]} collided at k={collision.step}\n"
            else:
                index = collision.point_obj_indexes[0]
                output += f"Object n={index} collided at k={collision.step}\n"

        return output
