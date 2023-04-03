import bpy, sys, os
from . TMG_Export_Tools import *


# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Thank you all that download, suggest, and request features
# As well as the whole Blender community. You're all epic :)


bl_info = {
    "name": "TMG_Export_Tools",
    "author": "Johnathan Mueller",
    "descrtion": "A panel to batch export selected objects to fbx, obj, and gltf",
    "blender": (2, 90, 0),
    "version": (0, 1, 8),
    "location": "View3D (ObjectMode) > Sidebar > TMG > Export_Tools Tab",
    "warning": "",
    "category": "Object"
}

classes = (
    ## Properties
    TMG_Export_Properties,
    
    ## Panels
    OBJECT_PT_TMG_Export_Panel,

    ## Operators
    OBJECT_PT_TMG_Select_Directory,
    OBJECT_OT_TMG_Reset_Properties,
    OBJECT_PT_TMG_Export,
)

def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.tmg_exp_vars = bpy.props.PointerProperty(type=TMG_Export_Properties)

def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)

if __name__ == "__main__":
    register()