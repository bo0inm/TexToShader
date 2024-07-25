import bpy
from copy import copy
from bpy_extras.node_utils import connect_sockets
from bpy_extras.io_utils import ImportHelper


class Ops_TtoS(bpy.types.Operator):
    """Create shader nodes tree from texture"""

    bl_label = "Tex to Shader"
    bl_description = "Create shader nodes tree from texture"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    files: bpy.props.CollectionProperty(
        type=bpy.types.OperatorFileListElement, options={"HIDDEN", "SKIP_SAVE"}
    )

    @classmethod
    def poll(cls, context):
        """check shader node tree exist"""
        if context.space_data.node_tree is not None:
            return True
        return False

    # from node_warngler/utils/nodes.py/get_active_tree
    @staticmethod
    def getActiveTree(context):
        tree = context.space_data.node_tree
        path = []
        # Get nodes from currently edited tree.
        # If user is editing a group, space_data.node_tree is still the base level (outside group).
        # context.active_node is in the group though, so if space_data.node_tree.nodes.active is not
        # the same as context.active_node, the user is in a group.
        # Check recursively until we find the real active node_tree:
        if tree.nodes.active:
            while tree.nodes.active != context.active_node:
                tree = tree.nodes.active.node_tree
                path.append(tree)
        return tree.nodes

    @staticmethod
    def imageTpye(files, settings):
        """Check whether the file is of the specified type"""
        dataDict = {}

        # normalize fields
        fields = {
            "Base Color": [settings.base_color, settings.color_colorspace],
            "Ambient Occlusion": [settings.ao, settings.data_colorspace],
            "Metallic": [settings.metallic, settings.data_colorspace],
            "Roughness": [settings.roughness, settings.data_colorspace],
            "IOR": [settings.ior, settings.data_colorspace],
            "Glossiness": [settings.glossiness, settings.data_colorspace],
            "Alpha": [settings.alpha, settings.data_colorspace],
            "Normal": [settings.normal, settings.data_colorspace],
            "Bump": [settings.bump, settings.data_colorspace],
            "Subsurface Weight": [settings.sss_weight, settings.data_colorspace],
            "Subsurface Radius": [settings.sss_radius, settings.data_colorspace],
            "Tint": [settings.tint, settings.data_colorspace],  # Specular color
            "Transmission Weight": [settings.transmission, settings.data_colorspace],
            "Emission Strength": [
                settings.emission,
                settings.data_colorspace,
            ],
            "Displacement": [settings.displacement, settings.data_colorspace],
        }

        for key, value in fields.items():
            fields[key] = [
                list(filter(lambda x: x, value[0].lower().strip().split(" "))),
                value[1],
            ]

        # check file type
        name_fileList = [(file.name.lower(), file) for file in files]

        for key, values in fields.items():
            for name, file in name_fileList:
                if any(keyWord in name and keyWord != "" for keyWord in values[0]):
                    dataDict[key] = [file, values[1]]
                    name_fileList.remove((name, file))
                    break

        # add other files
        otherKeyWordsList = [
            keyWord for keyWord in settings.other.lower().strip().split(" ")
        ]
        if len(otherKeyWordsList) > 0:
            for name, file in name_fileList:
                if any(keyWord in name and keyWord != "" for keyWord in otherKeyWordsList):
                    dataDict[name] = [file, settings.data_colorspace]

        return dataDict

    @staticmethod
    def importImage(nodes, filepath, location, colorSpace="Raw", label=""):
        """Import image and create node"""
        node = nodes.new("ShaderNodeTexImage")

        node.label = label
        node.location = location
        node.hide = True

        node.image = bpy.data.images.load(filepath)
        node.image.colorspace_settings.name = colorSpace
        return node

    @staticmethod
    def addNode(nodes, nodeType, location, hide=False):
        """Create node"""
        node = nodes.new(nodeType)
        node.location = location
        node.hide = hide
        return node

    def pipeline(self, nodeTree, BSDFNode, OutputNode, settings, fileList):
        """Create node tree from texture"""

        # --- import textures ---
        def importTextures(Type):
            """import textures function"""
            if Type in fileList:
                texNodedir[Type] = self.importImage(
                    nodeTree,
                    self.directory + fileList[Type][0].name,
                    location,
                    fileList[Type][1],
                    Type,
                )

        location = copy(BSDFNode.location)
        texNodedir = {}

        location[0] -= settings.gapX * 2
        for fileItem in fileList:
            importTextures(fileItem)
            location[1] -= settings.gapY

        # return False if no textures imported
        if len(texNodedir) == 0:
            return False

        # --- add uv vector node ---
        location[0] -= max(settings.gapX * 1.5, 400)
        location[1] = BSDFNode.location[1]
        texCoord = self.addNode(nodeTree, "ShaderNodeTexCoord", location)
        location[0] += 200
        mapping = self.addNode(nodeTree, "ShaderNodeMapping", location)
        connect_sockets(texCoord.outputs["UV"], mapping.inputs["Vector"])

        # link textures vector
        for node in texNodedir.values():
            connect_sockets(mapping.outputs["Vector"], node.inputs["Vector"])

        node = None
        # --- texture effect node ---
        # AO texture just load if has both AO and Base Color
        if "Ambient Occlusion" in texNodedir:
            node = texNodedir.pop("Ambient Occlusion")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[0])

        if "Base Color" in texNodedir:
            node = texNodedir.pop("Base Color")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[0])

        if "Metallic" in texNodedir:
            node = texNodedir.pop("Metallic")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[1])

        roughness = False
        if "Roughness" in texNodedir:
            roughness = True
            node = texNodedir.pop("Roughness")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[2])

        if "Glossiness" in texNodedir:
            node = texNodedir.pop("Glossiness")

            # invert node
            location[0] = node.location[0] + settings.gapX
            location[1] = node.location[1]
            invert = self.addNode(nodeTree, "ShaderNodeInvert", location, True)
            connect_sockets(node.outputs["Color"], invert.inputs["Color"])

            if roughness is False:
                connect_sockets(invert.outputs["Color"], BSDFNode.inputs[2])

        if "IOR" in texNodedir:
            node = texNodedir.pop("IOR")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[3])

        if "Alpha" in texNodedir:
            node = texNodedir.pop("Alpha")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[4])

        normal = False
        if "Normal" in texNodedir:
            node = texNodedir.pop("Normal")
            normal = True

            # convert directX normal map to openGL (invert green channel)
            location[0] = node.location[0] + settings.gapX
            location[1] = node.location[1] + 20
            curves = self.addNode(nodeTree, "ShaderNodeRGBCurve", location, True)
            curves.mapping.curves[1].points[0].location[1] = 1
            curves.mapping.curves[1].points[1].location[1] = 0
            curves.label = "convert to directX normal"
            curves.mute = True
            connect_sockets(node.outputs["Color"], curves.inputs["Color"])

            # normal map node
            location[1] -= 40
            normal = self.addNode(nodeTree, "ShaderNodeNormalMap", location, True)
            connect_sockets(curves.outputs["Color"], normal.inputs["Color"])
            connect_sockets(normal.outputs["Normal"], BSDFNode.inputs[5])

        if "Bump" in texNodedir:
            node = texNodedir.pop("Bump")

            # bump node
            location[0] = node.location[0] + settings.gapX
            location[1] = node.location[1]
            bump = self.addNode(nodeTree, "ShaderNodeBump", location)
            connect_sockets(node.outputs["Color"], bump.inputs["Height"])

            if normal is False:
                connect_sockets(bump.outputs["Normal"], BSDFNode.inputs[5])

        if "Subsurface Weight" in texNodedir:
            node = texNodedir.pop("Subsurface Weight")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[7])

        if "Subsurface Radius" in texNodedir:
            node = texNodedir.pop("Subsurface Radius")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[8])

        if "Tint" in texNodedir:
            node = texNodedir.pop("Tint")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[12])

        if "Transmission Weight" in texNodedir:
            node = texNodedir.pop("Transmission Weight")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[17])

        if "Emission Strength" in texNodedir:
            node = texNodedir.pop("Emission Strength")
            connect_sockets(node.outputs["Color"], BSDFNode.inputs[27])

        if "Displacement" in texNodedir:
            node = texNodedir.pop("Displacement")

            # displacement node
            location[0] = BSDFNode.location[0] + settings.gapX
            location[1] = BSDFNode.location[1] - 300
            disp = self.addNode(nodeTree, "ShaderNodeDisplacement", location)
            connect_sockets(node.outputs["Color"], disp.inputs["Height"])

            # set displacement method and link to output
            bpy.context.object.active_material.displacement_method = "BOTH"
            connect_sockets(
                disp.outputs["Displacement"], OutputNode.inputs["Displacement"]
            )

        # BSDF link to output node
        connect_sockets(BSDFNode.outputs["BSDF"], OutputNode.inputs["Surface"])

        return True

    def execute(self, context):
        settings = context.preferences.addons[__package__].preferences
        nodeTree = self.getActiveTree(context)
        selectedNodes = [node for node in context.selected_nodes]
        BSDFNode = None
        OutputNode = None

        # git BDRF node, if not exist create one
        existBSDFNode = True
        for node in selectedNodes:
            if node.bl_idname == "ShaderNodeBsdfPrincipled":
                BSDFNode = node
                break

        if BSDFNode is None:
            existBSDFNode = False
            bpy.ops.node.add_node(use_transform=False, type="ShaderNodeBsdfPrincipled")
            BSDFNode = context.active_node

        # git Output node, if not exist create one
        existOutputNode = True
        for node in nodeTree:
            print(node.bl_idname)
            if node.bl_idname == "ShaderNodeOutputMaterial":
                OutputNode = node
                break

        if OutputNode is None:
            existOutputNode = False
            OutputNodelocal = [
                BSDFNode.location[0] + settings.gapX,
                BSDFNode.location[1],
            ]
            self.addNode(nodeTree, "ShaderNodeOutputMaterial", OutputNodelocal)
            OutputNode = context.active_node

        # create node tree
        fileList = self.imageTpye(self.files, settings)
        if len(fileList) == 0:
            return {"CANCELLED"}
        result = self.pipeline(nodeTree, BSDFNode, OutputNode, settings, fileList)

        # if no textures imported delete created node
        if result is False:
            if existBSDFNode is False:
                BSDFNode.select = True
                bpy.ops.node.delete()
            if existOutputNode is False:
                OutputNode.select = True
                bpy.ops.node.delete()

        return {"FINISHED"}


class ShaderOps(Ops_TtoS, ImportHelper):
    """shader node add menu used"""

    bl_idname = "node.ttos"


class BrowserOps(Ops_TtoS):
    """file browser right menu used"""

    bl_idname = "browser.ttos"

    def invoke(self, context, event):
        # TODO get files and directory from file browser
        print(context.selected_asset_files)
