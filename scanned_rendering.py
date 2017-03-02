import bpy
import numpy as np
import time

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

fov = 6 * np.pi / 180
camera.data.angle = fov
distance_camera = camera.data.lens * 0.5 * np.tan(fov / 2)

# Camer coordinates to unit vector, then multiply with the magnitude
camera.location = camera.location / (
    camera.location.magnitude) * distance_camera

a = 0.25
list_rotation_angles = []

parameter = np.arange(-2 * np.pi, 2 * np.pi, 0.628)
x_cam = np.cos(parameter) / (
    np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera
y_cam = np.sin(parameter) / (
    np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera
z_cam = -a * parameter / (
    np.sqrt(1 + (a**2) * (parameter**2))) * distance_camera



# Meshes paths, stored in list
PATHS = ["/home/gopalsharma/airplane_0627.off"]
# name of the shape, which you extract from the mesh, list "airplane_0627"
shape_name = ""
for mesh_path in PATHS:
    # shape_name = mesh_path.split("/")[-1][:-4]
    shape_name = "bathtub_scan_0001"
    bpy.ops.import_scene.obj(filepath="/home/gopalsharma/Downloads/TestSet/bathtub/bathtub_scan_0001.obj")
    cubedata = bpy.data.objects[shape_name]
    bpy.context.scene.objects.active = bpy.data.objects["bathtub_scan_0001"]
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
    for i, t in enumerate(parameter):
        camera.location = (x_cam[i], y_cam[i], z_cam[i])
        light.location = (x_cam[i], y_cam[i], z_cam[i])
        loc_camera = camera.matrix_world.to_translation()
        direction = point - camera.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_mode = 'XYZ'
        camera.rotation_euler = rot_quat.to_euler()
        light.rotation_euler = camera.rotation_euler
        bpy.data.scenes['Scene'].render.filepath = str(i) + '.png'
        bpy.ops.render.render(write_still=True)

print (time.time() - t1)
