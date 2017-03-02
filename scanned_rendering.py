import bpy
import numpy as np
import time
import os
if bpy.data.objects["Cube"]:
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()
t1 = time.time()

light = bpy.data.objects["Lamp"]
light.data.type = 'HEMI'
camera = bpy.data.objects["Camera"]

for scene in bpy.data.scenes:
    scene.render.resolution_x = 227
    scene.render.resolution_y = 227
    scene.render.resolution_percentage = 100
bpy.context.scene.world.horizon_color = (1, 1, 1)
# list(bpy.data.objects)

fov = 10 * np.pi / 180
camera.data.angle = fov
distance_camera = camera.data.lens * 0.5 * np.tan(fov / 2)

# Camer coordinates to unit vector, then multiply with the magnitude
camera.location = camera.location / (
    camera.location.magnitude) * distance_camera

a = 0.25
list_rotation_angles = []

# parameter = np.arange(-2 * np.pi, 2 * np.pi, 0.628)
# x_cam = np.cos(parameter) / (
#     np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera
# y_cam = np.sin(parameter) / (
#     np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera
# z_cam = -a * parameter / (
#     np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera

thetas = np.arange(0, 360, 30) * np.pi / 180.0
phi = 60 * np.pi / 180.0
x_cam = distance_camera * np.cos(thetas) * np.sin(phi)
y_cam = distance_camera * np.sin(thetas) * np.cos(phi)
z_cam = distance_camera * np.cos(phi)
PATHS = []
for root, subdirs, files in os.walk("/home/gopalsharma/Downloads/TestSet/"):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith(".obj"):
                PATHS += [file_path]

shape_name = ""
for mesh_path in PATHS:
    shape_name = mesh_path.split("/")[-1][:-4]
    # shape_name = "bathtub_scan_0001"
    bpy.ops.import_scene.obj(filepath=mesh_path)
    cubedata = bpy.data.objects[shape_name]
    bpy.context.scene.objects.active = bpy.data.objects[shape_name]
    cubedata.select = True
    # bpy.ops.object.editmode_toggle()
    # bpy.ops.object.shade_smooth()
    # bpy.ops.mesh.remove_doubles()
    # bpy.ops.object.editmode_toggle()

    bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

    D = bpy.data
    D.objects[shape_name].data.materials.append(D.materials["Material"])
    bpy.context.object.active_material.diffuse_intensity = 0.6
    bpy.context.object.active_material.specular_intensity = 0.0
    bpy.context.object.active_material.ambient = 0.3
    bpy.context.object.active_material.specular_shader = "PHONG"

    obj_coor = [c.co for c in cubedata.data.vertices]
    x_mesh, y_mesh, z_mesh = [], [], []
    for e in obj_coor:
        x_mesh += [e[0]]
        y_mesh += [e[1]]
        z_mesh += [e[2]]

    min_x = min(x_mesh)
    max_x = max(x_mesh)
    min_y = min(y_mesh)
    max_y = max(y_mesh)
    min_z = min(z_mesh)
    max_z = max(z_mesh)

    len_x = max_x - min_x
    len_y = max_y - min_y
    len_z = max_z - min_z

    scale = np.sqrt(len_x**2 + len_y**2 + len_z**2)
    cubedata.scale /= scale
    point = cubedata.matrix_world.to_translation()
    image_path = mesh_path[:-4] + "_"
    for i, t in enumerate(thetas):
        camera.location = (x_cam[i], y_cam[i], z_cam)
        light.location = (x_cam[i], y_cam[i], z_cam)
        loc_camera = camera.matrix_world.to_translation()
        direction = point - camera.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_mode = 'XYZ'
        camera.rotation_euler = rot_quat.to_euler()
        light.rotation_euler = camera.rotation_euler
        bpy.data.scenes['Scene'].render.filepath = mesh_path[:-4] + "_" + str(i).zfill(3) + '.png'
        bpy.ops.render.render(write_still=True)

print (time.time() - t1)
