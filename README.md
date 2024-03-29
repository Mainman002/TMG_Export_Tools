# TMG_Export_Tools
A Blender 4.x addon for batch exporting models to fbx, obj, and gltf

[Current Release 0.2.0](https://github.com/Mainman002/TMG_Export_Tools/releases/tag/0.2.0)

v0.1.2 Video Tutorial
https://youtu.be/aSEHSHSX51k

### Features include
* Select export path with blender's File Browser
* Export models into separate folders based on export type
* Export models into separate folders based on collections
* Game engine suggested defaults { UE4, Unity, Godot }
* Export format selector { FBX, GLB, GLTF_Embedded, GLTF+Bin+Textures }
* Export all selected objects to separate model files (Based on Parent / Object name)
* Supported object types to export { Mesh, Armature, Empty, Camera }
* Apply Unit Scale, Use Space Transform, and Embed Textures (default FBX settings)
* Visual Geometry to Mesh, Location to World Origin
* Rename UV layers to match UE4's lightmap workflow (UVChannel_1, UVChannel_2)
* Rename UV layers to match Unity's lightmap workflow (UV1, UV2)
* Rename UV layers to match Godot's lightmap workflow (UV1, UV2)
* Add Lightmap UV layer_2, then "Lightmap Pack" UV islands
* Unwrap objects to individual UV areas or unwrap to a combined UV area

### More features to come later as I work out a few things ;)

### Preview Image
![Screenshot 2023-04-03 at 9 09 36 AM](https://user-images.githubusercontent.com/11281480/229534929-e6182082-2fdb-4a2e-8217-e00a8a205310.png)
