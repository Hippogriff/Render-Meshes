import bpy
import mathutils
from mathutils import Vector

import bpy

o = bpy.context.object
vcos = [ o.matrix_world * v.co for v in o.data.vertices ]
findCenter = lambda l: ( max(l) + min(l) ) / 2

x,y,z  = [ [ v[i] for v in vcos ] for i in range(3) ]
center = [ findCenter(axis) for axis in [x,y,z] ]

print( center )

# to get the coordiantes of the object use the command
# http://blender.stackexchange.com/questions/5210/pointing-the-camera-in-a-particular-direction-programmatically
# obj_camera = bpy.data.objects["object name"]
# >> obj_camera.matrix_world.to_translation()
# I just need to decide the field of view.
# Position of the Camera
# Lighting of the images/background
# Path for the helix
# 
