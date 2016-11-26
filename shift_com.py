import bpy
import numpy as np

if bpy.data.objects["Cube"]:
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()
full_path_to_file = "/home/gopalsharma/model.obj"
bpy.ops.import_scene.obj(filepath=full_path_to_file)

cubedata = bpy.data.objects["model"]
bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

bpy.data.objects['model'].select = True
# to select the object in the viewport,
# this way you can also select multiple objects

# additionally you can use
bpy.context.scene.objects.active = bpy.data.objects['model']
# to make it the acive selected object

camera = bpy.data.objects["Camera"]
list(bpy.data.objects)

obj_coor = [c.co for c in cubedata.data.vertices]
x, y, z = [], [], []
for e in obj_coor:
    x += [e[0]]
    y += [e[1]]
    z += [e[2]]

min_x = min(x)
max_x = max(x)
min_y = min(y)
max_y = max(y)
min_z = min(z)
max_z = max(z)

len_x = max_x - min_x
len_y = max_y - min_y
len_z = max_z - min_z

scale = np.sqrt(len_x**2 + len_y**2 + len_z**2)
cubedata.scale /= scale
fov = 5 * np.pi / 180
distance_camera = camera.data.lens * 2 * np.tan(fov / 2)
camera.data.angle = fov
camera.location.magnitude = distance_camera


def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()


point = cubedata.matrix_world.to_translation()
"""
This will generate rendered images
"""
a = 0.25
parameter = np.arange(-2 * np.pi, 2 * np.pi, 0.628)
for i, t in enumerate(parameter):
    x = np.cos(t) / (np.sqrt(1 + (a**2) * (t**2)))
    y = np.sin(t) / (np.sqrt(1 + (a**2) * (t**2)))
    z = -a * t / (np.sqrt(1 + (a**2) * (t**2)))
    camera.location = (x, y, z)
    camera.location.magnitude =
    look_at(camera, point)
    bpy.data.scenes[
        'Scene'].render.filepath = '/home/gopalsharma/image_' + str(i) + '.jpg'
    bpy.ops.render.render(write_still=True)
