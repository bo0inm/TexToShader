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
        default=100,
        min=0,
        description="Gap between two nodes on Y axis",
    )
    # colorspace preferences
    color_colorspace: StringProperty(
        name="Color",
        default="sRGB",
        description="""Default Colorspace for color images, must be set correctly value\n
            (For example, use OCIO , set to sRGB - Texture)""",
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
        description="Base Color maps",
    )
    ao: StringProperty(
        name="Ambient Occlusion",
        default="ao ambientocclusion",
        description="AO maps",
    )
    metallic: StringProperty(
        name="Metallic",
        default="metallic metalness metal mtl reflection refl",
        description="Metallness maps",
    )
    roughness: StringProperty(
        name="Roughness",
        default="roughness rough",
        description="Roughness maps",
    )
    ior: StringProperty(
        name="IOR",
        default="ior",
        description="IOR maps",
    )
    glossiness: StringProperty(
        name="Glossiness",
        default="gloss glossy glossiness",
        description="Glossiness maps(Invert roughness maps)",
    )
    alpha: StringProperty(
        name="Alpha",
        default="alpha opacity",
        description="Alpha maps",
    )
    normal: StringProperty(
        name="Normal",
        default="normal nor nrm nrml norm",
        description="Normal maps",
    )
    bump: StringProperty(
        name="Bump",
        default="bump bmp",
        description="Bump maps",
    )
    sss_weight: StringProperty(
        name="Subsurface Weight",
        default="sss subsurface",
        description="Subsurface weight maps",
    )
    sss_radius: StringProperty(
        name="Subsurface Radius",
        default="sss_color subsurface_color",
        description="Subsurface Radius (Color) maps",
    )
    tint: StringProperty(
        name="Tint",
        default="specular spec spc",
        description="Tint (Specular Color) maps",
    )
    transmission: StringProperty(
        name="Transmission",
        default="transmission transparency trans",
        description="Transmission maps",
    )
    emission: StringProperty(
        name="Emission",
        default="emission emissive emit",
        description="Emission maps",
    )
    displacement: StringProperty(
        name="Displacement",
        default="displacement displace disp dsp height heightmap",
        description="Displacement maps",
    )
    other: StringProperty(
        name="Other",
        default="",
        description="imported but not used",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "gapX")
        layout.prop(self, "gapY")
        layout.label(
            text="Default Colorspace: (Colorspace conversion need set correctly value)"
        )
        layout.prop(self, "color_colorspace")
        layout.prop(self, "data_colorspace")
        layout.label(text="Texture Keywords:")
        layout.prop(self, "base_color")
        layout.prop(self, "ao")
        layout.prop(self, "metallic")
        layout.prop(self, "roughness")
        layout.prop(self, "ior")
        layout.prop(self, "glossiness")
        layout.prop(self, "alpha")
        layout.prop(self, "normal")
        layout.prop(self, "bump")
        layout.prop(self, "sss_weight")
        layout.prop(self, "sss_radius")
        layout.prop(self, "tint")
        layout.prop(self, "transmission")
        layout.prop(self, "emission")
        layout.prop(self, "displacement")
        layout.prop(self, "other")
