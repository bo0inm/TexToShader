bl_info = {
    "name": "TexToShader",
    "author": "Bo0inM",
    "description": "Create shader node from general texture",
    "blender": (2, 80, 0),
    "version": (0, 4, 0),
    "location": "Node Editor > Add > Shader > Tex->Shader",
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
    bpy.types.NODE_MT_category_SH_NEW_SHADER.prepend(shaderMenu)
    # bpy.types.FILEBROWSER_MT_context_menu.prepend(BrowserMenu)


def unregister():
    bpy.utils.unregister_class(preferences.Pref_TtoS)
    bpy.utils.unregister_class(operators.ShaderOps)
    bpy.types.NODE_MT_category_SH_NEW_SHADER.remove(shaderMenu)
    # bpy.types.FILEBROWSER_MT_context_menu.remove(BrowserMenu)


if __name__ == "__main__":
    register()