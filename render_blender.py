import bpy

pi = 3.14159265
fov = 50

scene = bpy.data.scenes["Scene"]

# Set render resolution
scene.render.resolution_x = 480
scene.render.resolution_y = 359

full_path_to_file = "/home/gopalsharma/airplane_0627.off"
bpy.ops.import_scene.obj(filepath=full_path_to_file)

bpy.data.scenes['Scene'].render.filepath = '/home/gopalsharma/image.jpg'
bpy.ops.render.render(write_still=True)
