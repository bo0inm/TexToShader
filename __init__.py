bl_info = {
    "name": "TexToShader",
    "author": "Bo0inM",
    "description": "Create shader nodes based on the name of the texture files",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
    "location": "Node Editor > Add > Tex->Shader",
    "doc_url": "https://github.com/bo0inm/TexToShader",
    "category": "Node",
}

import bpy
from . import operators
from . import preferences


def shaderMenu(self, context):
    self.layout.operator(operators.ShaderOps.bl_idname, text="Tex->Shader")
    self.layout.separator()


def BrowserMenu(self, context):
    self.layout.operator(operators.BrowserOps.bl_idname, text="Tex->Shader")
    self.layout.separator()


def register():
    bpy.utils.register_class(preferences.Pref_TtoS)
    bpy.utils.register_class(operators.ShaderOps)
    bpy.types.NODE_MT_shader_node_add_all.prepend(shaderMenu)
    # bpy.types.FILEBROWSER_MT_context_menu.prepend(BrowserMenu)


def unregister():
    bpy.utils.unregister_class(preferences.Pref_TtoS)
    bpy.utils.unregister_class(operators.ShaderOps)
    bpy.types.NODE_MT_shader_node_add_all.remove(shaderMenu)
    # bpy.types.FILEBROWSER_MT_context_menu.remove(BrowserMenu)


if __name__ == "__main__":
    register()
