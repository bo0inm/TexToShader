import bpy
from bpy.props import StringProperty, IntProperty


class Pref_TtoS(bpy.types.AddonPreferences):
    bl_idname = __package__

    # node preferences
    gapX: IntProperty(
        name="Node X Gap",
        default=300,
        min=0,
        description="Gap between two nodes on X axis",
    )
    gapY: IntProperty(
        name="Node Y Gap",
        default=150,
        min=0,
        description="Gap between two nodes on Y axis",
    )
    # colorspace preferences
    color_colorspace: StringProperty(
        name="Color",
        default="sRGB",
        description="Default Colorspace for color images",
    )
    data_colorspace: StringProperty(
        name="Non-Color",
        default="Raw",
        description="Default Colorspace for Non-Color images",
    )
    # textName Properties
    # from node_warngler/utils/preferences.py
    base_color: StringProperty(
        name="Base Color",
        default="diffuse diff albedo base col color basecolor",
        description="Naming Components for Base Color maps",
    )
    sss_color: StringProperty(
        name="Subsurface Color",
        default="sss subsurface",
        description="Naming Components for Subsurface Color maps",
    )
    metallic: StringProperty(
        name="Metallic",
        default="metallic metalness metal mtl",
        description="Naming Components for metallness maps",
    )
    specular: StringProperty(
        name="Specular",
        default="specularity specular spec spc",
        description="Naming Components for Specular maps",
    )
    normal: StringProperty(
        name="Normal",
        default="normal nor nrm nrml norm",
        description="Naming Components for Normal maps",
    )
    bump: StringProperty(
        name="Bump", default="bump bmp", description="Naming Components for bump maps"
    )
    rough: StringProperty(
        name="Roughness",
        default="roughness rough rgh",
        description="Naming Components for roughness maps",
    )
    gloss: StringProperty(
        name="Gloss",
        default="gloss glossy glossiness",
        description="Naming Components for glossy maps",
    )
    displacement: StringProperty(
        name="Displacement",
        default="displacement displace disp dsp height heightmap",
        description="Naming Components for displacement maps",
    )
    transmission: StringProperty(
        name="Transmission",
        default="transmission transparency",
        description="Naming Components for transmission maps",
    )
    emission: StringProperty(
        name="Emission",
        default="emission emissive emit",
        description="Naming Components for emission maps",
    )
    alpha: StringProperty(
        name="Alpha",
        default="alpha opacity",
        description="Naming Components for alpha maps",
    )
    ambient_occlusion: StringProperty(
        name="Ambient Occlusion",
        default="ao ambientocclusion",
        description="Naming Components for AO maps",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "gapX")
        layout.prop(self, "gapY")
        layout.label(text="Default Colorspace: (Colorspace conversion need set correctly value)")
        layout.prop(self, "color_colorspace")
        layout.prop(self, "data_colorspace")
        layout.label(text="Texture Keywords:")
        layout.prop(self, "base_color")
        layout.prop(self, "sss_color")
        layout.prop(self, "metallic")
        layout.prop(self, "specular")
        layout.prop(self, "normal")
        layout.prop(self, "bump")
        layout.prop(self, "rough")
        layout.prop(self, "gloss")
        layout.prop(self, "displacement")
        layout.prop(self, "transmission")
        layout.prop(self, "emission")
        layout.prop(self, "alpha")
        layout.prop(self, "ambient_occlusion")
