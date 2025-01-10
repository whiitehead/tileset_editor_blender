cube = ['0', '1', '2', '3', '4', '5', '6', '7']

# rotations
rotation = (2, 3, 6, 7, 0, 1, 4, 5)

def rotate_x_1(cube):
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

def rotate_x_2(cube):
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

def rotate_x_3(cube):
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

def rotate_y_1(cube):
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

def rotate_y_2(cube):
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

def rotate_y_3(cube):
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

def rotate_z_1(cube):
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

def rotate_z_2(cube):
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

def rotate_z_3(cube):
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

def mirror_x(cube):
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

def mirror_y(cube):
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

def mirror_z(cube):
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

def rotate(axis: str, cube: list[int]):
    case axis