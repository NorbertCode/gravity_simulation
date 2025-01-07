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
    def generate_report(collision_data: list[Collision],
                        sim_steps: list[list[np.array]],
                        point_objs: list[PointObject]) -> str:
        """Presents the given collision data in a readable format"""
        obj_output = "Objects:\n"
        for index in range(len(sim_steps[0])):
            start_pos = sim_steps[0][index].round(2)
            start_pos_str = f"start position = ({start_pos[0]}, {start_pos[1]})"
            end_pos = point_objs[index].position.round(2)
            end_pos_str = f"end position = ({end_pos[0]}, {end_pos[1]})"
            obj_output += f"n={index}, {start_pos_str}, {end_pos_str}\n"

        col_output = "\nCollisions:\n"
        for collision in collision_data:
            objects = ""
            for obj in collision.point_obj_indexes:
                objects += f"n={obj}, "
            col_output += f"{objects[:-2]} at k={collision.step}\n"

        return obj_output + col_output
