
def rotate_x_1(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[1]
    cube[1] = cube[3]
    cube[3] = cube[2]
    cube[2] = temp0

    temp4   = cube[4]
    cube[4] = cube[5]
    cube[5] = cube[7]
    cube[7] = cube[6]
    cube[6] = temp4

def rotate_x_2(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[3]
    cube[3] = temp0

    temp1   = cube[1]
    cube[1] = cube[2]
    cube[2] = temp1

    temp4   = cube[4]
    cube[4] = cube[7]
    cube[7] = temp4

    temp5   = cube[5]
    cube[5] = cube[6]
    cube[6] = temp5

def rotate_x_3(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[2]
    cube[2] = cube[3]
    cube[3] = cube[1]
    cube[1] = temp0

    temp4   = cube[4]
    cube[4] = cube[6]
    cube[6] = cube[7]
    cube[7] = cube[5]
    cube[5] = temp4

def rotate_y_1(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[4]
    cube[4] = cube[5]
    cube[5] = cube[1]
    cube[1] = temp0

    temp2   = cube[2]
    cube[2] = cube[6]
    cube[6] = cube[7]
    cube[7] = cube[3]
    cube[3] = temp2

def rotate_y_2(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[5]
    cube[5] = temp0

    temp1   = cube[1]
    cube[1] = cube[4]
    cube[4] = temp1

    temp2   = cube[2]
    cube[2] = cube[7]
    cube[7] = temp2

    temp3   = cube[3]
    cube[3] = cube[6]
    cube[6] = temp3

def rotate_y_3(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[1]
    cube[1] = cube[5]
    cube[5] = cube[4]
    cube[4] = temp0

    temp2   = cube[2]
    cube[2] = cube[3]
    cube[3] = cube[7]
    cube[7] = cube[6]
    cube[6] = temp2

def rotate_z_1(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[2]
    cube[2] = cube[6]
    cube[6] = cube[4]
    cube[4] = temp0

    temp1   = cube[1]
    cube[1] = cube[3]
    cube[3] = cube[7]
    cube[7] = cube[5]
    cube[5] = temp1

def rotate_z_2(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[6]
    cube[6] = temp0

    temp1   = cube[1]
    cube[1] = cube[7]
    cube[7] = temp1

    temp2   = cube[2]
    cube[2] = cube[4]
    cube[4] = temp2

    temp3   = cube[3]
    cube[3] = cube[5]
    cube[5] = temp3

def rotate_z_3(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[4]
    cube[4] = cube[6]
    cube[6] = cube[2]
    cube[2] = temp0

    temp1   = cube[1]
    cube[1] = cube[5]
    cube[5] = cube[7]
    cube[7] = cube[3]
    cube[3] = temp1

def rotate(axis: str, count: int, cube: list[int]):
    assert len(cube) == 8

    match (count):
        case 0:
            return
        case 1:
            match axis:
                case 'X':
                    rotate_x_1(cube)
                case 'Y':
                    rotate_y_1(cube)
                case 'Z':
                    rotate_z_1(cube)
                case _:
                    raise ValueError(f"{axis} is not valid axis. Must be 'X', 'Y', or 'Z'")
        case 2:
            match axis:
                case 'X':
                    rotate_x_2(cube)
                case 'Y':
                    rotate_y_2(cube)
                case 'Z':
                    rotate_z_2(cube)
                case _:
                    raise ValueError(f"{axis} is not valid axis. Must be 'X', 'Y', or 'Z'")
        case 3:
            match axis:
                case 'X':
                    rotate_x_3(cube)
                case 'Y':
                    rotate_y_3(cube)
                case 'Z':
                    rotate_z_3(cube)
                case _:
                    raise ValueError(f"{axis} is not valid axis. Must be 'X', 'Y', or 'Z'")
        case _:
            raise ValueError("rotation_count is the number of 90 degree rotations. Must be 0, 1, 2, or 3.")

def mirror_x(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[4]
    cube[4] = temp0

    temp1   = cube[1]
    cube[1] = cube[5]
    cube[5] = temp1

    temp2   = cube[2]
    cube[2] = cube[6]
    cube[6] = temp2

    temp3   = cube[3]
    cube[3] = cube[7]
    cube[7] = temp3

def mirror_y(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[2]
    cube[2] = temp0

    temp1   = cube[1]
    cube[1] = cube[3]
    cube[3] = temp1

    temp4   = cube[4]
    cube[4] = cube[6]
    cube[6] = temp4

    temp5   = cube[5]
    cube[5] = cube[7]
    cube[7] = temp5

def mirror_z(cube: list[int]):
    temp0   = cube[0]
    cube[0] = cube[1]
    cube[1] = temp0

    temp2   = cube[2]
    cube[2] = cube[3]
    cube[3] = temp2

    temp4   = cube[4]
    cube[4] = cube[5]
    cube[5] = temp4

    temp6   = cube[6]
    cube[6] = cube[7]
    cube[7] = temp6

def mirror(axis: str, cube: list[int]):
    assert len(cube) == 8

    match axis:
        case 'X':
            mirror_x(cube)
        case 'Y':
            mirror_y(cube)
        case 'Z':
            mirror_z(cube)
        case _:
            raise ValueError(f"{axis} is not valid axis. Must be 'X', 'Y', or 'Z'")




# r1 = [''.join(i) for i in product(('X', 'Y', 'Z'), ('1', '2', '3'))]
# r2 = [''.join(i) for i in product(('X', 'Y', 'Z'), ('1', '2', '3'), r1)]
# r3 = [''.join(i) for i in product(('X', 'Y', 'Z'), ('1', '2', '3'), r2)]

# rotations = r1 + r2



# for rotation_string in rotations:
#     cube_copy = cube.copy()
#     for op in iterate_op_string():
#         rotate(op[0], op[1], cube_copy)
    
#     key = cube_to_str(cube_copy)
#     if key not in adjacency:
#         adjacency[key] = rotation_string

# print(rotations)
# print(len(adjacency))
# print(adjacency)

# op_strings_r = ['', 'Z1', 'Z2', 'Z3']
# op_strings_rr = list(adjacency.values())
# op_strings_mr = ['', 'Z1', 'Z2', 'Z3', 'M', 'MZ1', 'MZ2', 'MZ3']
# op_strings_mrr = op_strings_rr + [('M' + val) for val in op_strings_rr]


# print(op_strings_r)
# print(op_strings_rr)
# print(op_strings_mr)
# print(op_strings_mrr)



# def get_rotations(s: str):
#     for axis in ('X', 'Y', 'Z'):
#         for rotation_count in range(1, 4):
#             rotations.append(s + axis + str(rotation_count))

# for i in range(3):
#     for j in range(i):
#         for axis in ('X', 'Y', 'Z'):
#             for rotation_count in range(1, 4):
#                 rotations.append(f"{axis}{rotation_count}")


