import bpy
import numpy as np
import time

# if bpy.data.objects["Cube"]:
#     bpy.data.objects['Cube'].select = True
#     bpy.ops.object.delete()
# full_path_to_file = "/home/gopalsharma/model.obj"
# bpy.ops.import_scene.obj(filepath=full_path_to_file)

cubedata = bpy.data.objects["Cube"]
# bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

# bpy.data.objects['Cube'].select = True

# bpy.context.scene.objects.active = bpy.data.objects['Cube']

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

fov = 15 * np.pi / 180
camera.data.angle = fov
distance_camera = camera.data.lens * 0.5 * np.tan(fov / 2)

# Camer coordinates to unit vector, then multiply with the magnitude
camera.location = camera.location / (
    camera.location.magnitude) * distance_camera

point = cubedata.matrix_world.to_translation()


def look_at(camera, point, i):
    loc_camera = camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    camera.rotation_euler = rot_quat.to_euler()
    bpy.data.scenes[
        'Scene'].render.filepath = '/home/gopalsharma/image_' + str(i) + '.jpg'
    bpy.ops.render.render(write_still=True)
    return camera


"""
This will generate rendered images
"""
a = 0.25
parameter = np.arange(-2 * np.pi, 2 * np.pi, 0.628)
for i, t in enumerate(parameter):
    x = np.cos(t) / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera
    y = np.sin(t) / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera
    z = -a * t / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera

    if camera == None:
        print("Trolled!!")
    camera.location = (x, y, z)
    camera = look_at(camera, point, i)
    break
