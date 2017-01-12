import bpy
import numpy as np
import time

if bpy.data.objects["Cube"]:
    bpy.data.objects['Cube'].select = True
    bpy.ops.object.delete()
t1 = time.time()

full_path_to_file = "/home/gopalsharma/airplane_0627.off"
bpy.ops.import_mesh.off(filepath=full_path_to_file)

cubedata = bpy.data.objects["airplane_0627"]
cubedata.select = True
bpy.ops.object.shade_smooth()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.remove_doubles()
bpy.ops.object.editmode_toggle()

bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

for scene in bpy.data.scenes:
    scene.render.resolution_x = 227
    scene.render.resolution_y = 227
    scene.render.resolution_percentage = 100
bpy.context.scene.world.horizon_color = (1, 1, 1)

D = bpy.data
D.objects["airplane_0627"].data.materials.append(D.materials["Material"])
bpy.context.object.active_material.diffuse_intensity = 0.6
bpy.context.object.active_material.specular_intensity = 0.0
bpy.context.object.active_material.ambient = 0.3
bpy.context.object.active_material.specular_shader = "PHONG"
# bpy.context.object.active_material.diffuse_intensity = 1.0
# bpy.context.object.active_material.diffuse_color = (1, 1, 1)

light = bpy.data.objects["Lamp"]
light.data.type = 'HEMI'
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
# scale = max(len_x, len_y, len_z)
cubedata.scale /= scale

fov = 8 * np.pi / 180
camera.data.angle = fov
distance_camera = camera.data.lens * 0.5 * np.tan(fov / 2)

# Camer coordinates to unit vector, then multiply with the magnitude
camera.location = camera.location / (
    camera.location.magnitude) * distance_camera

point = cubedata.matrix_world.to_translation()

print (point)
def look_at(loc_camera, point):
    direction = point - loc_camera
    rot_quat = direction.to_track_quat('-Z', 'Y')
    return rot_quat.to_euler()


a = 0.25
list_rotation_angles = []
# list_rotation_angles += [rotate_angle]

parameter = np.arange(-2 * np.pi, 2 * np.pi, 0.628)
t1 = time.time()

for i, t in enumerate(parameter):
    t = parameter[i]

    camera.select = True
    x = np.cos(t) / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera
    y = np.sin(t) / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera
    z = -a * t / (np.sqrt(1 + (a**2) * (t**2))) * distance_camera
    camera.location = (x, y, z)
    light.location = (x, y, z)
    loc_camera = camera.matrix_world.to_translation()
    direction = point - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_mode = 'XYZ'
    camera.rotation_euler = rot_quat.to_euler()
    light.rotation_euler = camera.rotation_euler
    bpy.data.scenes['Scene'].render.filepath = '/home/gopalsharma/temp/image_' + str(
            i) + '.jpg'
    bpy.ops.render.render(write_still=True)
print(time.time() - t1)
