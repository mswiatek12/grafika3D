"""
Projekt końcowy - Programowanie Grafiki 3D
Interaktywna aplikacja 3D z OpenGL w Pythonie
Autor: [Student]
Data: 2025-11-30
Funkcjonalności:
- Scena 3D z wieloma obiektami
- Oświetlenie Phonga (ambient + diffuse + specular)
- Teksturowane obiekty
- Interaktywna kamera
- Chmury, które można podnosić/obniżać
- Zmiana parametrów oświetlenia
"""
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from PIL import Image
import os
WIDTH, HEIGHT = 1280, 720
camera_pos = np.array([0.0, 5.0, 15.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = -90.0
pitch = 0.0
last_x = WIDTH / 2
last_y = HEIGHT / 2
first_mouse = True
cloud_height = 12.0  
cloud_speed = 0.5
mouse_button_pressed = False
light_ambient = [0.3, 0.3, 0.3, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [10.0, 15.0, 10.0, 1.0]
material_ambient = [0.2, 0.2, 0.2, 1.0]
material_diffuse = [0.8, 0.8, 0.8, 1.0]
material_specular = [1.0, 1.0, 1.0, 1.0]
material_shininess = 50.0
textures = {}
delta_time = 0.0
last_frame = 0.0
def load_texture(filename):
    try:
        img = Image.open(filename)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(img.getdata()), np.uint8)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        if img.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 
                        0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        elif img.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 
                        0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        print(f"✓ Załadowano teksturę: {filename}")
        return texture_id
    except Exception as e:
        print(f"✗ Błąd ładowania tekstury {filename}: {e}")
        return create_default_texture()
def create_default_texture():
    size = 64
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            if (i // 8 + j // 8) % 2 == 0:
                data[i, j] = [255, 255, 255]
            else:
                data[i, j] = [200, 200, 200]
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id
def init_textures():
    global textures
    textures['ground'] = create_ground_texture()
    textures['cloud'] = create_cloud_texture()
    textures['cube'] = create_cube_texture()
    textures['sphere'] = create_sphere_texture()
def create_ground_texture():
    size = 128
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            variation = np.random.randint(-20, 20)
            data[i, j] = [34 + variation, 139 + variation, 34 + variation]
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    return texture_id
def create_cloud_texture():
    size = 128
    data = np.zeros((size, size, 4), dtype=np.uint8)
    center = size / 2
    for i in range(size):
        for j in range(size):
            dist = math.sqrt((i - center)**2 + (j - center)**2)
            max_dist = center
            if dist < max_dist:
                alpha = int(255 * (1 - (dist / max_dist) ** 0.5))
                brightness = 240 + int(15 * np.random.random())
                data[i, j] = [brightness, brightness, brightness, alpha]
            else:
                data[i, j] = [255, 255, 255, 0]
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return texture_id
def create_cube_texture():
    size = 64
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            data[i, j] = [178, 34, 34]  
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id
def create_sphere_texture():
    size = 64
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            data[i, j] = [65, 105, 225]  
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id
def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glClearColor(0.53, 0.81, 0.92, 1.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)
    init_textures()
def draw_ground():
    glBindTexture(GL_TEXTURE_2D, textures['ground'])
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0)
    glVertex3f(-50, 0, -50)
    glTexCoord2f(10, 0)
    glVertex3f(50, 0, -50)
    glTexCoord2f(10, 10)
    glVertex3f(50, 0, 50)
    glTexCoord2f(0, 10)
    glVertex3f(-50, 0, 50)
    glEnd()
    glPopMatrix()
def draw_cube(x, y, z, size=1.0):
    glBindTexture(GL_TEXTURE_2D, textures['cube'])
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1); glVertex3f(1, -1, -1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(1, 1, -1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1); glVertex3f(1, -1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, -1, 1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(1, 1, -1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(1, -1, 1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, -1)
    glEnd()
    glPopMatrix()
def draw_sphere(x, y, z, radius=1.0):
    glBindTexture(GL_TEXTURE_2D, textures['sphere'])
    glPushMatrix()
    glTranslatef(x, y, z)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 32, 32)
    gluDeleteQuadric(quad)
    glPopMatrix()
def draw_cloud(x, y, z, scale=1.0):
    glDisable(GL_BLEND)  
    cloud_ambient = [0.9, 0.9, 0.95, 1.0]
    cloud_diffuse = [0.95, 0.95, 1.0, 1.0]
    cloud_specular = [0.5, 0.5, 0.5, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, cloud_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, cloud_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, cloud_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, 20.0)
    glColor3f(1.0, 1.0, 1.0)  
    glBindTexture(GL_TEXTURE_2D, textures['cloud'])
    cloud_spheres = [
        (0.0, 0.0, 0.0, 1.8),
        (-1.2, -0.2, 0.3, 1.5),
        (1.3, -0.1, -0.2, 1.6),
        (-0.5, -0.3, -0.8, 1.3),
        (0.6, -0.2, 0.9, 1.4),
        (-0.8, 0.5, 0.5, 1.4),
        (0.9, 0.6, 0.2, 1.5),
        (0.2, 0.7, -0.6, 1.3),
        (-1.0, 0.4, -0.4, 1.2),
        (1.1, 0.5, 0.7, 1.3),
        (0.0, 1.2, 0.0, 1.2),
        (-0.6, 1.0, 0.4, 1.0),
        (0.7, 1.1, -0.3, 1.1),
        (0.3, 1.4, 0.2, 0.9),
        (-1.5, 0.2, 0.0, 0.9),
        (1.6, 0.3, 0.1, 1.0),
        (0.0, -0.4, 0.5, 1.1),
        (-0.3, 0.8, -1.0, 0.8),
        (0.4, 0.6, 1.1, 0.9)
    ]
    for px, py, pz, radius in cloud_spheres:
        glPushMatrix()
        glTranslatef(x + px * scale, y + py * scale, z + pz * scale)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, radius * scale, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, material_shininess)
    glColor3f(1.0, 1.0, 1.0)
def draw_legend():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.75)
    glBegin(GL_QUADS)
    glVertex2f(10, HEIGHT - 290)
    glVertex2f(340, HEIGHT - 290)
    glVertex2f(340, HEIGHT - 10)
    glVertex2f(10, HEIGHT - 10)
    glEnd()
    glColor4f(1.0, 1.0, 0.0, 0.9)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(10, HEIGHT - 290)
    glVertex2f(340, HEIGHT - 290)
    glVertex2f(340, HEIGHT - 10)
    glVertex2f(10, HEIGHT - 10)
    glEnd()
    glColor4f(0.5, 0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    glVertex2f(20, HEIGHT - 55)
    glVertex2f(330, HEIGHT - 55)
    glVertex2f(20, HEIGHT - 135)
    glVertex2f(330, HEIGHT - 135)
    glVertex2f(20, HEIGHT - 170)
    glVertex2f(330, HEIGHT - 170)
    glVertex2f(20, HEIGHT - 220)
    glVertex2f(330, HEIGHT - 220)
    glVertex2f(20, HEIGHT - 255)
    glVertex2f(330, HEIGHT - 255)
    glEnd()
    glColor3f(1.0, 1.0, 0.0)
    draw_simple_text(20, HEIGHT - 35, "STEROWANIE", 2.0)
    glColor3f(0.7, 0.9, 1.0)
    draw_simple_text(20, HEIGHT - 70, "KAMERA:", 1.2)
    glColor3f(1.0, 1.0, 1.0)
    draw_simple_text(30, HEIGHT - 88, "WASD - Ruch", 1.0)
    draw_simple_text(30, HEIGHT - 103, "LPM + Mysz - Obrot", 1.0)
    draw_simple_text(30, HEIGHT - 118, "Spacja/Shift - Gora/Dol", 1.0)
    glColor3f(0.7, 1.0, 0.8)
    draw_simple_text(20, HEIGHT - 150, "CHMURY:", 1.2)
    glColor3f(1.0, 1.0, 1.0)
    draw_simple_text(30, HEIGHT - 163, "Strzalki ^ v", 1.0)
    glColor3f(1.0, 0.9, 0.7)
    draw_simple_text(20, HEIGHT - 185, "OSWIETLENIE:", 1.2)
    glColor3f(1.0, 1.0, 1.0)
    draw_simple_text(30, HEIGHT - 198, "1/2 - Ambient", 1.0)
    draw_simple_text(30, HEIGHT - 210, "3/4 - Diffuse", 1.0)
    glColor3f(1.0, 1.0, 0.7)
    draw_simple_text(20, HEIGHT - 230, "SWIATLO:", 1.2)
    glColor3f(1.0, 1.0, 1.0)
    draw_simple_text(30, HEIGHT - 243, "I/K/J/L/U/O", 1.0)
    glColor3f(1.0, 0.6, 0.6)
    draw_simple_text(20, HEIGHT - 270, "ESC - Wyjscie", 1.2)
    glDisable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def draw_simple_text(x, y, text, scale=1.0):
    char_map = {
        'A': [[0,1,1,1,0],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
        'B': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0]],
        'C': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]],
        'D': [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
        'E': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,1,1,1]],
        'F': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0]],
        'G': [[0,1,1,1,0],[1,0,0,0,0],[1,0,1,1,1],[1,0,0,0,1],[0,1,1,1,0]],
        'H': [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
        'I': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
        'J': [[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
        'K': [[1,0,0,0,1],[1,0,0,1,0],[1,1,1,0,0],[1,0,0,1,0],[1,0,0,0,1]],
        'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
        'M': [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]],
        'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
        'O': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
        'P': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0]],
        'R': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,1,0],[1,0,0,0,1]],
        'S': [[0,1,1,1,1],[1,0,0,0,0],[0,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
        'T': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
        'U': [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
        'V': [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]],
        'W': [[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,0,1,1],[1,0,0,0,1]],
        'Y': [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
        'Z': [[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]],
        '1': [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0]],
        '2': [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[1,1,1,1,1]],
        '3': [[1,1,1,1,0],[0,0,0,0,1],[0,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
        '4': [[1,0,0,1,0],[1,0,0,1,0],[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0]],
        '/': [[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]],
        '-': [[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]],
        ':': [[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0]],
        '^': [[0,0,1,0,0],[0,1,0,1,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
        ' ': [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    }
    current_x = x
    for char in text.upper():
        if char in char_map:
            pattern = char_map[char]
            for row_idx, row in enumerate(pattern):
                for col_idx, pixel in enumerate(row):
                    if pixel:
                        px = current_x + col_idx * scale
                        py = y - row_idx * scale
                        glBegin(GL_POINTS)
                        glVertex2f(px, py)
                        glEnd()
            current_x += 6 * scale
        else:
            current_x += 4 * scale
def draw_scene():
    global cloud_height
    draw_ground()
    draw_cloud(-10, cloud_height, -10, 1.8)
    draw_cloud(10, cloud_height + 2, -8, 1.5)
    draw_cloud(-8, cloud_height - 2, 10, 2.0)
    draw_cloud(12, cloud_height + 3, 12, 1.6)
    draw_cloud(0, cloud_height, -15, 2.2)
    draw_cloud(-15, cloud_height + 1, 0, 1.4)
    draw_cloud(15, cloud_height - 1, 5, 1.7)
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()
    glEnable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    target = camera_pos + camera_front
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              target[0], target[1], target[2],
              camera_up[0], camera_up[1], camera_up[2])
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    draw_scene()
    draw_legend()
def key_callback(window, key, scancode, action, mods):
    global camera_pos, cloud_height, light_ambient, light_diffuse, light_position
    if action == glfw.PRESS or action == glfw.REPEAT:
        camera_speed = 0.5
        if key == glfw.KEY_W:
            camera_pos += camera_speed * camera_front
        if key == glfw.KEY_S:
            camera_pos -= camera_speed * camera_front
        if key == glfw.KEY_A:
            camera_pos -= np.cross(camera_front, camera_up) * camera_speed
        if key == glfw.KEY_D:
            camera_pos += np.cross(camera_front, camera_up) * camera_speed
        if key == glfw.KEY_SPACE:
            camera_pos[1] += camera_speed
        if key == glfw.KEY_LEFT_SHIFT:
            camera_pos[1] -= camera_speed
        if key == glfw.KEY_UP:
            cloud_height += cloud_speed
            print(f"Wysokość chmur: {cloud_height:.1f}")
        if key == glfw.KEY_DOWN:
            cloud_height -= cloud_speed
            print(f"Wysokość chmur: {cloud_height:.1f}")
        if key == glfw.KEY_1:  
            light_ambient[0] = min(1.0, light_ambient[0] + 0.1)
            light_ambient[1] = min(1.0, light_ambient[1] + 0.1)
            light_ambient[2] = min(1.0, light_ambient[2] + 0.1)
            glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
            print(f"Ambient: {light_ambient[0]:.2f}")
        if key == glfw.KEY_2:  
            light_ambient[0] = max(0.0, light_ambient[0] - 0.1)
            light_ambient[1] = max(0.0, light_ambient[1] - 0.1)
            light_ambient[2] = max(0.0, light_ambient[2] - 0.1)
            glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
            print(f"Ambient: {light_ambient[0]:.2f}")
        if key == glfw.KEY_3:  
            light_diffuse[0] = min(1.0, light_diffuse[0] + 0.1)
            light_diffuse[1] = min(1.0, light_diffuse[1] + 0.1)
            light_diffuse[2] = min(1.0, light_diffuse[2] + 0.1)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            print(f"Diffuse: {light_diffuse[0]:.2f}")
        if key == glfw.KEY_4:  
            light_diffuse[0] = max(0.0, light_diffuse[0] - 0.1)
            light_diffuse[1] = max(0.0, light_diffuse[1] - 0.1)
            light_diffuse[2] = max(0.0, light_diffuse[2] - 0.1)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            print(f"Diffuse: {light_diffuse[0]:.2f}")
        if key == glfw.KEY_I:  
            light_position[2] -= 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_K:  
            light_position[2] += 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_J:  
            light_position[0] -= 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_L:  
            light_position[0] += 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_U:  
            light_position[1] += 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_O:  
            light_position[1] -= 1.0
            print(f"Pozycja światła: ({light_position[0]:.1f}, {light_position[1]:.1f}, {light_position[2]:.1f})")
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
def mouse_callback(window, xpos, ypos):
    global first_mouse, last_x, last_y, yaw, pitch, camera_front, mouse_button_pressed
    if not mouse_button_pressed:
        first_mouse = True
        return
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False
        return
    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x = xpos
    last_y = ypos
    sensitivity = 0.05
    xoffset *= sensitivity
    yoffset *= sensitivity
    yaw += xoffset
    pitch += yoffset
    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0
    front = np.array([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ])
    camera_front = front / np.linalg.norm(front)
def mouse_button_callback(window, button, action, mods):
    global mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouse_button_pressed = True
        elif action == glfw.RELEASE:
            mouse_button_pressed = False
def print_controls():
    print("\n" + "="*60)
    print("STEROWANIE APLIKACJĄ 3D")
    print("="*60)
    print("\nKAMERA:")
    print("  W/S/A/D       - Poruszanie kamerą (przód/tył/lewo/prawo)")
    print("  SPACJA        - Kamera w górę")
    print("  SHIFT         - Kamera w dół")
    print("  MYSZ          - Obracanie kamery")
    print("\nCHMURY:")
    print("  STRZAŁKA GÓRA - Podnieś chmury")
    print("  STRZAŁKA DÓŁ  - Obniż chmury")
    print("\nOŚWIETLENIE:")
    print("  1/2           - Zwiększ/zmniejsz oświetlenie Ambient")
    print("  3/4           - Zwiększ/zmniejsz oświetlenie Diffuse")
    print("\nPOZYCJA ŚWIATŁA:")
    print("  I/K           - Przesuń światło przód/tył")
    print("  J/L           - Przesuń światło lewo/prawo")
    print("  U/O           - Przesuń światło góra/dół")
    print("\nINNE:")
    print("  ESC           - Wyjście z programu")
    print("="*60 + "\n")
def main():
    if not glfw.init():
        print("Błąd inicjalizacji GLFW")
        return
    window = glfw.create_window(WIDTH, HEIGHT, "Projekt 3D - Grafika Komputerowa", None, None)
    if not window:
        glfw.terminate()
        print("Błąd tworzenia okna")
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    init_opengl()
    print_controls()
    global delta_time, last_frame
    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
    print("\nProgram zakończony.")
if __name__ == "__main__":
    main()
