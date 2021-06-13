import bpy, sys, os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty
from bpy.types import Operator


bl_info = {
    "name": "TMG_Export_Tools",
    "author": "Johnathan Mueller",
    "descrtion": "A panel to batch export selected objects to .fbx",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > TMG_Export Tab",
    "warning": "",
    "category": "Object"
}


class TMG_Export_Properties(bpy.types.PropertyGroup):
    exp_directory : bpy.props.StringProperty(name='Directory', description='Sets the folder directory path for the FBX models to export to')
    exp_use_selection : bpy.props.BoolProperty(default=True, description='If you want to export only selected or everything in your blend file (Might not work correctly)')
    exp_apply_unit_scale : bpy.props.BoolProperty(default=True, description='Takes into account current Blend Unit scale, else use FBX export scale')
    exp_use_tspace : bpy.props.BoolProperty(default=False, description='Apply global space transforms to object rotations, else only axis space is written to FBX')
    exp_embed_textures : bpy.props.BoolProperty(default=False, description='Inclued textures used in the materials')
    
    exp_apply_mesh : bpy.props.BoolProperty(default=False, description='Converts object to Mesh applying everything !WARNING! will apply all modifiers')
    exp_reset_location : bpy.props.BoolProperty(default=True, description='Sets Location values to 0')
    exp_reset_rotation : bpy.props.BoolProperty(default=False, description='Sets Rotation values to 0')
    exp_reset_scale : bpy.props.BoolProperty(default=False, description='Sets Scale values to 0')
    
    exp_rename_uvs : bpy.props.BoolProperty(default=False, description='Sets UV layer names to UVChannel_1 and UVChannel_2')
    exp_add_lightmap_uv : bpy.props.BoolProperty(default=False, description='Adds a 2nd UV layer for use as Lightmaps')
    exp_unwrap_lightmap_uv : bpy.props.BoolProperty(default=False, description='Unwraps UV layer 2 !WARNING! will unwrap the 2nd UV layer')


def _mode_switch(_mode):
    bpy.ops.object.mode_set(mode=_mode)
    return{"Finished"}


def _ob_switch(_ob, _objs, _path):
    _mode_switch('OBJECT')
    for _obj in bpy.context.selected_objects:
        _obj.select_set(state=False)
    _ob.select_set(state=True)
    bpy.context.scene.cursor.location = _ob.location
    bpy.context.view_layer.objects.active = _ob
    _reset_location(_ob, _path)
    for _obj in _objs:
        _obj.select_set(state=True)
    return{"Finished"}


def _reset_location(_ob, _path):
    scene = bpy.context.scene
    tmg_exp_vars = scene.tmg_exp_vars
    
    if scene.tmg_exp_vars.exp_reset_location:
        bpy.context.active_object.location = (0, 0, 0)
    
    if scene.tmg_exp_vars.exp_reset_rotation:
        bpy.context.active_object.rotation_euler = (0, 0, 0)
    
    if scene.tmg_exp_vars.exp_reset_scale:
        bpy.context.active_object.scale = (1, 1, 1)
        
    _apply_mesh(_ob, _path)
    return{'FINISHED'}


def _apply_mesh(_ob, _path):
    scene = bpy.context.scene
    tmg_exp_vars = scene.tmg_exp_vars
    
    if tmg_exp_vars.exp_apply_mesh:
        bpy.ops.object.convert(target='MESH')
    
    _unwrap(_ob, _path)
    return{'FINISHED'}


def _unwrap(_ob, _path):
    scene = bpy.context.scene
    tmg_exp_vars = scene.tmg_exp_vars
    
    for _int in range(0,2):
        if len(_ob.data.uv_layers)-1 < 1:
            if tmg_exp_vars.exp_add_lightmap_uv:
                bpy.ops.mesh.uv_texture_add()
            
            if tmg_exp_vars.exp_rename_uvs:
                _ob.data.uv_layers[0].name = 'UVChannel_1'
            
        if len(_ob.data.uv_layers)-1 > 0:
            if tmg_exp_vars.exp_rename_uvs:
                _ob.data.uv_layers[0].name = 'UVChannel_1'
                
            _ob.data.uv_layers[1].active = True
            
            if tmg_exp_vars.exp_rename_uvs:
                _ob.data.uv_layers[1].name = 'UVChannel_2'
    
    if tmg_exp_vars.exp_unwrap_lightmap_uv:
        _mode_switch('EDIT')
        bpy.context.scene.tool_settings.use_uv_select_sync = True
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
    _pack(_ob, _path)

    return{'FINISHED'}


def _pack(_ob, _path):
    scene = bpy.context.scene
    tmg_exp_vars = scene.tmg_exp_vars
    
    if tmg_exp_vars.exp_unwrap_lightmap_uv:
        bpy.ops.uv.pack_islands(margin=0.03)
        
    _mode_switch('OBJECT')
    _export(_ob, _path)
    return{'FINISHED'}


def _export(_ob, _path):
    scene = bpy.context.scene
    tmg_exp_vars = scene.tmg_exp_vars
    _new_path = str(_path + _ob.name + '.fbx')
    
    bpy.ops.export_scene.fbx(
    filepath=_new_path, 
    filter_glob='*.fbx', 
    use_selection=scene.tmg_exp_vars.exp_use_selection, 
    apply_unit_scale=scene.tmg_exp_vars.exp_apply_unit_scale, 
    apply_scale_options='FBX_SCALE_NONE', 
    object_types={'ARMATURE', 'EMPTY', 'MESH', 'OTHER'}, 
    axis_forward='-Z', 
    axis_up='Y', 
    mesh_smooth_type='EDGE', 
    use_tspace=scene.tmg_exp_vars.exp_use_tspace, 
    embed_textures=scene.tmg_exp_vars.exp_embed_textures,
    )
    
    _ob_location_reset(_ob)
    return{'FINISHED'}


def _ob_location_reset(_ob):
    bpy.context.active_object.location = bpy.context.scene.cursor.location
    return{'FINISHED'}


def _loop(_objs, _path):
    for _int in range(0, len(_objs)):
        _ob_switch(_objs[_int], _objs, _path)
    return{'FINISHED'}


def main(_directory):
    print('\nSTART EXPORT TO')
    
    _check = os.path.exists(_directory)
    
    if not _check:
        os.mkdir(path=_directory)
    
    _path = _directory
    print(str('Directory: ' + _path))
    
    for _obj in bpy.context.selected_objects:
        if _obj.type != 'MESH':
            _obj.select_set(state=False)
    
    _objs = bpy.context.selected_objects
    
    _loop(_objs, _path)
    
    print("\nFINISHED EXPORT TO")
    print(str('Directory: ' + _path))
    return{'FINISHED'}


class OBJECT_OT_TMG_Reset_Properties(bpy.types.Operator):
    bl_idname = 'wm.object_tmg_reset_properties'
    bl_label = 'Reset Properties'
    bl_description = 'Resets FBX properties to default values.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        scene = context.scene
        tmg_exp_vars = scene.tmg_exp_vars
        
        scene.tmg_exp_vars.exp_use_selection = True
        scene.tmg_exp_vars.exp_apply_unit_scale = True
        scene.tmg_exp_vars.exp_use_tspace = False
        scene.tmg_exp_vars.exp_embed_textures = False
        
        scene.tmg_exp_vars.exp_apply_mesh = False
        scene.tmg_exp_vars.exp_reset_location = True
        scene.tmg_exp_vars.exp_reset_rotation = False
        scene.tmg_exp_vars.exp_reset_scale = False
        scene.tmg_exp_vars.exp_rename_uvs = False
        scene.tmg_exp_vars.exp_add_lightmap_uv = False
        scene.tmg_exp_vars.exp_unwrap_lightmap_uv = False
        
        return {'FINISHED'}
    

class OBJECT_PT_TMG_Select_Directory(Operator, ImportHelper):
    """Select folder directory path for exported fbx models."""
    bl_idname = "object.tmg_select_directory"
    bl_label = "Export to Directory"
    
    directory : bpy.props.StringProperty(subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    # ImportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        scene = context.scene
        tmg_exp_vars = scene.tmg_exp_vars
#        scene.custompath = self.filepath
        scene.tmg_exp_vars.exp_directory = self.directory
        
        if bpy.context.selected_objects:
            return main(self.directory)
        return{'FINISHED'}


class OBJECT_PT_TMG_Export_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_tmg_export_panel'
    bl_category = 'TMG Export'
    bl_label = 'FBX Export Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        scene = context.scene
        tmg_exp_vars = scene.tmg_exp_vars
        
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)

        row.prop(tmg_exp_vars, 'exp_directory', text='')
        row.operator('object.tmg_select_directory', text='', icon='FILE_FOLDER')
        row.operator('wm.object_tmg_reset_properties', text='', icon='FILE_REFRESH')
            
        box = col.box()
        box_col = box.column(align=True)
        
        box_col.label(text='FBX Export Settings')
        box_col.prop(tmg_exp_vars, 'exp_use_selection', text='Use Selection')
        box_col.prop(tmg_exp_vars, 'exp_apply_unit_scale', text='Apply Unit Scale')
        box_col.prop(tmg_exp_vars, 'exp_use_tspace', text='Use TSpace')
        box_col.prop(tmg_exp_vars, 'exp_embed_textures', text='Embed Textures')
        
        box_col = box.column(align=True)
        
        box_col.label(text='Object Export Settings')
        box_col.prop(tmg_exp_vars, 'exp_apply_mesh', text='Apply Mesh')
        box_col.prop(tmg_exp_vars, 'exp_reset_location', text='Reset Location')
        box_col.prop(tmg_exp_vars, 'exp_reset_rotation', text='Reset Rotation')
        box_col.prop(tmg_exp_vars, 'exp_reset_scale', text='Reset Scale')
        
        box_col = box.column(align=True)
        
        box_col.label(text='UV Export Settings')
        box_col.prop(tmg_exp_vars, 'exp_rename_uvs', text='Rename UV Layers')
        box_col.prop(tmg_exp_vars, 'exp_add_lightmap_uv', text='Add Lightmap UV Layer')
        box_col.prop(tmg_exp_vars, 'exp_unwrap_lightmap_uv', text='Unwrap Lightmap UV Layer')
        


classes = (
    TMG_Export_Properties,
    OBJECT_PT_TMG_Export_Panel,
    OBJECT_PT_TMG_Select_Directory,
    OBJECT_OT_TMG_Reset_Properties,
)


def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.tmg_exp_vars = bpy.props.PointerProperty(type=TMG_Export_Properties)


def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)
#        del bpy.types.Scene.tmg_exp_vars


if __name__ == "__main__":
    register()




