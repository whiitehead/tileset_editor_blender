import bpy
import bpy_extras
import bpy_extras.view3d_utils
from mathutils import Vector, geometry, Euler
import math
from bpy.types import Operator, Context, Collection, Event, Object, Mesh
from typing import cast, Generator
from itertools import product
from . import adjacency_transforms
import re

# R means only rotate on Z axis
# RR means rotate on all axes (all 24 orienations of a cube)
# M means to mirror first
# Values are calculated as all possible outcomes of a translation rule. Mirror is always first then X then Y then Z
translation_rule_ops = {
    '': [''],
    'R': ['', 'Z1', 'Z2', 'Z3'],
    'RR': ['', 'X1', 'X2', 'X3', 'Y1', 'Y2', 'Y3', 'Z1', 'Z2', 'Z3', 'X1Y1', 'X1Y2', 'X1Y3', 'X1Z1', 'X1Z2', 'X1Z3', 'X2Y1', 'X2Y3', 'X2Z1', 'X2Z3', 'X3Y1', 'X3Y3', 'X3Z1', 'X3Z3'],
    'M': ['', 'M'],
    'MR': ['', 'Z1', 'Z2', 'Z3', 'M', 'MZ1', 'MZ2', 'MZ3'],
    'MRR': ['', 'X1', 'X2', 'X3', 'Y1', 'Y2', 'Y3', 'Z1', 'Z2', 'Z3', 'X1Y1', 'X1Y2', 'X1Y3', 'X1Z1', 'X1Z2', 'X1Z3', 'X2Y1', 'X2Y3', 'X2Z1', 'X2Z3', 'X3Y1', 'X3Y3', 'X3Z1', 'X3Z3', 'M', 'MX1', 'MX2', 'MX3', 'MY1', 'MY2', 'MY3', 'MZ1', 'MZ2', 'MZ3', 'MX1Y1', 'MX1Y2', 'MX1Y3', 'MX1Z1', 'MX1Z2', 'MX1Z3', 'MX2Y1', 'MX2Y3', 'MX2Z1', 'MX2Z3', 'MX3Y1', 'MX3Y3', 'MX3Z1', 'MX3Z3'],
}

op_parsing_pattern = re.compile(r'^M|[XYZ][123]')
op_validation_pattern  = re.compile(r'^M?([XYZ][123])*')

BLOCK_COLOR = (0.5, 0.5, 1.0, 0.2)

global_context: Context
tiles_collection: Collection
tile_instances_collection: Collection
blocks_collection: Collection
blocks: dict[str, int]
tile_mappings: dict[str, str] # key is a string of 8 numbers, val is collection name
tile_instances: dict[str, str] # key is stringified int tuple, val is collection name

def get_or_create_collection(context: Context, name: str) -> Collection:
    collection = bpy.data.collections.get(name)

    if collection is None:
        collection = bpy.data.collections.new(name)
        context.scene.collection.children.link(collection)

    assert collection
    return collection

def init_globals(context: Context):
    global global_context
    global_context = context

    global tiles_collection
    tiles_collection = get_or_create_collection(context, "Tiles")

    global blocks_collection
    blocks_collection = get_or_create_collection(context, "Blocks")
    
    global tile_instances_collection
    tile_instances_collection =get_or_create_collection(context, "TileInstances")
    
    global blocks
    if "blocks" not in blocks_collection:
        blocks_collection["blocks"] = {}
    blocks = blocks_collection["blocks"]

    global tile_mappings
    if "tile_mappings" not in tiles_collection:
        tiles_collection["tile_mappings"] = {}
    tile_mappings = tiles_collection["tile_mappings"]

    global tile_instances
    if "tile_instances" not in tile_instances_collection:
        tile_instances_collection["tile_instances"] = {}
    tile_instances = tile_instances_collection["tile_instances"]

def floor(vec: Vector) -> Vector:
    return Vector((math.floor(vec.x), math.floor(vec.y), math.floor(vec.z)))

def int_tuple_to_string(int_tuple: tuple[int, int, int]) -> str:
    x, y, z = int_tuple
    return f"({x}, {y}, {z})"

def vector_to_int_tuple(vec: Vector) -> tuple[int, int, int]:
    return (int(math.floor(vec.x)), int(math.floor(vec.y)), int(math.floor(vec.z)))

def vector_to_int_tuple_string(vec: Vector) -> str:
    return int_tuple_to_string(vector_to_int_tuple(vec))

def iterate_meshes(collection: Collection, recursive=False) -> Generator[Mesh, None, None]:
    for obj in collection.objects:
        if obj.type == 'MESH':
            yield cast(Mesh, obj.data)

def get_collection(name: str) -> Collection | None:
    return bpy.data.collections.get(name)


def get_floor_intersection(ray_origin: Vector, ray_direction: Vector) -> Vector:
    plane_normal = Vector((0, 0, 1))
    plane_point = Vector((0, 0, 0))
    pos = geometry.intersect_line_plane(ray_origin, ray_origin + ray_direction, plane_point, plane_normal)

    assert pos
    pos.z = 0
    return pos

# op should have already been validated
def execute_op(op: str, cube: list[int]):
    if op[0] == "M":
        adjacency_transforms.mirror_x(cube)
    else:
        adjacency_transforms.rotate(op[0], int(op[1]), cube)

def cube_to_str(c: list[int]) -> str:
    return "".join(str(num) for num in c)

def list_to_dictation_string(l: list[str|int], final_separator="or") -> str:
    out = ""
    length = len(l)
    for i in range(length):
        if i == length - 1:
            out += final_separator + " " + str(l[i])
        out += str(l[i]) + ", "
    return out

# Adds a simple check sum to collection then checks if it is dirty
def check_for_changes(collection: Collection) -> bool:
    char_sum_name = "char_count"
    if char_sum_name not in collection:
        collection[char_sum_name] = -1
    
    char_sum = 0
    for child_collection in collection.children:
        for char in child_collection.name:
            char_sum += ord(char)
    
    if collection[char_sum_name] == char_sum:
        return False
    
    collection[char_sum_name] = char_sum
    return True

def parent_collection(child: Collection, parent: Collection):
    for potential_parent in bpy.data.collections:
        if child.name in potential_parent.children:
            potential_parent.children.unlink(child)

    parent.children.link(child)


def parent_object(child: Object, parent: Collection):
    for potential_parent in child.users_collection:
        potential_parent.objects.unlink(child)
    
    parent.objects.link(child)


def mouse_to_world_ray(mouse_x: int, mouse_y: int) -> tuple[Vector, Vector]:
    region = global_context.region
    rv3d = global_context.region_data
    mouse_coords = mouse_x, mouse_y
    ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse_coords)
    ray_direction = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse_coords)

    return ray_origin, ray_direction


def destroy_collection(collection: Collection):
    for obj in list(collection.objects):
        collection.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    
    for parent in bpy.data.collections:
        if collection in parent.children.values():
            parent.children.unlink(collection)
    
    bpy.data.collections.remove(collection)

class voxel_editor(bpy.types.WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    # The prefix of the idname should be your add-on name.
    bl_idname = "tileset_editor.voxel_editor"
    bl_label = "Voxel Editor"
    bl_description = (
        "Placeholder"
    )
    bl_icon = 'MESH_CUBE'
    bl_widget = None
    bl_keymap = (
        ("tileset_editor.place_cube", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
    )

    def draw_settings(context, layout, tool): # type: ignore
        layout.label(text="Cube Placement Settings")


def register():
    bpy.utils.register_tool(cast(bpy.types.WorkSpaceTool, voxel_editor), separator=True, group=True)

def unregister():
    bpy.utils.unregister_tool(voxel_editor)


class OBJECT_OT_build_adjacency_mappings(Operator):
    """Place a Cube at the Cursor"""
    bl_idname = "tileset_editor.build_adjacency_mappings"
    bl_label = "Build adjacency mappings"
    bl_options = {'REGISTER', 'UNDO'}

    def validate_adjacency_rule(self, s: str) -> bool:
        if len(s) != 8:
            self.report({'ERROR'}, f"{s} is not a valid adjacency string. It must be 8 characters long.")
            return False
        if not s.isdigit():
            self.report({'ERROR'}, f"{s} is not a valid adjacency string. It may only contain numbers.")
            return False
        return True
    

    def validate_translation_rule(self, s: str) -> bool:
        if s not in translation_rule_ops:
            self.report({'ERROR'}, f"{s} is not a valid translation rule. It must be {list_to_dictation_string(list(translation_rule_ops.keys()))}")
            return False
        return True

    def build_adjacency_mappings(self):
        tile_mappings.clear()
        
        for tile_collection in tiles_collection.children:
            tile_rules = tile_collection.name.split("_")

            if len(tile_rules) == 1:
                tile_rules.append("")

            adjacency_rule, translation_rule = tile_rules

            if not self.validate_adjacency_rule(adjacency_rule):
                continue

            if not self.validate_translation_rule(translation_rule):
                continue

            adjacency_list_original = list(map(int, adjacency_rule))

            for ops in translation_rule_ops[translation_rule]:
                assert op_validation_pattern.fullmatch(ops) # can remove this validation at end of this project
                adjacency_list = adjacency_list_original.copy()
                for op in op_parsing_pattern.findall(ops):
                    execute_op(op, adjacency_list)

                adjacency_string = ''.join(map(str, adjacency_list))

                if adjacency_string not in tile_mappings:
                    tile_mappings[adjacency_string] = tile_collection.name + "," +  ops

class OBJECT_OT_place_cube(Operator):
    """Place a Cube at the Cursor"""
    bl_idname = "tileset_editor.place_cube"
    bl_label = "Place Cube"
    bl_options = {'REGISTER', 'UNDO'}

    
    

    def create_cube(self, pos: tuple[int, int, int]) -> Object:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(Vector(pos) + Vector((0.5, 0.5, 0.5))))
        bpy.ops.object.transform_apply(location=True)
        cube = global_context.active_object
        assert cube

        cube.color = BLOCK_COLOR
        cube.show_wire = True
        cube.visible_shadow = False
        cube.display_type = 'WIRE'
        return cube


    def get_mesh_intersection(self, ray_origin: Vector, ray_direction: Vector, collection: Collection) -> Vector | None:
        nearest_distance = math.inf
        nearest_pos = None

        for obj in collection.objects:
            if obj.type == 'MESH':
                hit, pos, norm, _ = obj.ray_cast(ray_origin, ray_direction)
                if hit:
                    distance = (pos - ray_origin).length
                    if distance < nearest_distance:
                        print(f"{pos} {norm}")
                        # This will make it snap to grid properly
                        nearest_pos = Vector((
                            round(pos.x, 4) + math.copysign(0.0001, norm.x),
                            round(pos.y, 4) + math.copysign(0.0001, norm.y),
                            round(pos.z, 4) + math.copysign(0.0001, norm.z),
                        ))

        return nearest_pos
    
    
    


    def destroy_adjacent_tile_instances(self, cube_mesh: Mesh):
        for vert in cube_mesh.vertices:
            tile_instance_key = vector_to_int_tuple_string(vert.co)
            if tile_instance_key in tile_instances:
                tile_instance_collection = get_collection(tile_instances[tile_instance_key])
                if tile_instance_collection is not None:
                    destroy_collection(tile_instance_collection)
                del tile_instances[tile_instance_key]


    # This is actually a regular collection with linked meshes but I'm gonna call it an instance collection anyway
    # Blender's instance collections don't work for me because I need linked mesh editing
    # Also, "link" lacks a decent noun. Instances is more descriptive as "link" describes a relationship, not the thing that is linked to the original
    def create_instance_collection(self, collection: Collection, offset: Vector, ops: str) -> Collection:
        rotation_vector = Vector()
        mirror = False
        for op in op_parsing_pattern.findall(ops):
            match op[0]:
                case 'M':
                    mirror = True
                case 'X':
                    rotation_vector.x = math.pi * float(op[1]) / 2
                case 'Y':
                    rotation_vector.y = math.pi * float(op[1]) / 2
                case 'Z':
                    rotation_vector.z = math.pi * float(op[1]) / 2

        rotation = Euler(rotation_vector.to_tuple())
        base_offset = Vector((-0.5, -0.5, -0.5))
        base_offset.rotate(rotation)
        instance_collection = bpy.data.collections.new(f"{collection.name}_instance_{ops}")
        for obj in collection.objects:
            if obj.type == 'MESH':
                mesh_instance = obj.copy()
                mesh_instance.data = obj.data
                mesh_instance.location = base_offset + offset
                mesh_instance.rotation_euler = Euler(rotation_vector.to_tuple())
                parent_object(mesh_instance, instance_collection)
        
        return instance_collection


    def build_adjacent_tile_instances(self, cube_mesh: Mesh):
        for vert in cube_mesh.vertices:
            tile_instance_key = vector_to_int_tuple_string(vert.co)

            if tile_instance_key in tile_instances:
                continue

            adjacency_string = ""
            for offset in product([-1, 0], repeat=3):
                block_key = vector_to_int_tuple_string(vert.co + Vector(offset))
                if block_key in blocks:
                    adjacency_string += '1'
                else:
                    adjacency_string += '0'

            # still adding for an attempt to fill because the adjacency will not change
            if adjacency_string not in tile_mappings:
                tile_instances[tile_instance_key] = ""
                continue

            tile_collection_name, ops = tile_mappings[adjacency_string].split(",")
            tile_collection = get_collection(tile_collection_name)
            assert tile_collection

            tile_instance_collection = self.create_instance_collection(tile_collection, vert.co, ops)
            assert tile_instance_collection

            tile_instances[tile_instance_key] = tile_instance_collection.name
            parent_collection(tile_instance_collection, tile_instances_collection)
    

    def invoke(self, context: Context, event: Event) -> set[str]:
        init_globals(context)

        ray_origin, ray_direction = mouse_to_world_ray(event.mouse_region_x, event.mouse_region_y)
        pos = self.get_mesh_intersection(ray_origin, ray_direction, blocks_collection)

        if pos is None:
            pos = get_floor_intersection(ray_origin, ray_direction)

        block_pos_key = vector_to_int_tuple_string(pos)

        if block_pos_key in blocks:
            # this is low key an error but it barely happens so I just handle it here and move on
            print("block already there")
            return {'FINISHED'}

        cube = self.create_cube(vector_to_int_tuple(pos))
        blocks[block_pos_key] = 1

        parent_object(cube, blocks_collection)

        if check_for_changes(tiles_collection):
            bpy.ops.tileset_editor.build_adjacency_mappings() # type: ignore
            # self.build_adjacency_mappings()
            # bpy.ops.object.build_adjacency_mappings()

        cube_mesh = cast(Mesh, cube.data)
        self.destroy_adjacent_tile_instances(cube_mesh)
        self.build_adjacent_tile_instances(cube_mesh)
        
        return {'FINISHED'}


class OBJECT_PT_tilemap_editor_settings(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tilemap Editor Settings"
    bl_idname = "OBJECT_PT_tilemap_editor_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tilemap Editor"

    def draw(self, context):
        layout = self.layout

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")