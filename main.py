from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import subprocess
import threading

app = Ursina()
window.fullscreen = True

grass_texture = load_texture('assets/tes_block.png')
stone_texture = load_texture('assets/stonemez.png')
biome_texture = load_texture('assets/grassmez.png')
sky_texture = load_texture('assets/skygradient.png')
arm_texture = load_texture('assets/arm_texture.png')

block_pick = 1
chunks = {}
chunk_size = 3
render_distance = 1

def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3

    load_chunks_around_player()
    unload_chunks_far_from_player()

def load_chunks_around_player():
    player_chunk_x = int(player.x // chunk_size)
    player_chunk_z = int(player.z // chunk_size)

    for dz in range(-render_distance, render_distance + 1):
        for dx in range(-render_distance, render_distance + 1):
            chunk_coords = (player_chunk_x + dx, player_chunk_z + dz)
            if chunk_coords not in chunks:
                generate_chunk(*chunk_coords)

def unload_chunks_far_from_player():
    player_chunk_x = int(player.x // chunk_size)
    player_chunk_z = int(player.z // chunk_size)

    chunks_to_unload = []
    for chunk_coords in chunks.keys():
        chunk_x, chunk_z = chunk_coords
        if abs(chunk_x - player_chunk_x) > render_distance or abs(chunk_z - player_chunk_z) > render_distance:
            chunks_to_unload.append(chunk_coords)

    for chunk_coords in chunks_to_unload:
        destroy_chunk(*chunk_coords)

def generate_chunk(chunk_x, chunk_z):
    chunk = []
    for z in range(chunk_size):
        for x in range(chunk_size):
            voxel = Voxel(position=(x + chunk_x * chunk_size, 0, z + chunk_z * chunk_size))
            chunk.append(voxel)
    chunks[(chunk_x, chunk_z)] = chunk

def destroy_chunk(chunk_x, chunk_z):
    chunk = chunks.pop((chunk_x, chunk_z), None)
    if chunk:
        for voxel in chunk:
            destroy(voxel)

def play_chuck_script():
    subprocess.run(["chuck", "dirt_break.ck"])

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='Grass_block',
            origin_y=0.5,
            texture=texture,
            color=color.color(1, 0, random.uniform(0.9, 1), 1,),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                threading.Thread(target=play_chuck_script).start()
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3: voxel = Voxel(position=self.position + mouse.normal, texture=biome_texture)

            if key == 'left mouse down':
                threading.Thread(target=play_chuck_script).start()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=1800,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(330, -10, 0),
            position=Vec2(0.7, -0.6)
        )

    def active(self):
        self.position = Vec2(0.68, -0.58)

    def passive(self):
        self.position = Vec2(0.7, -0.6)

player = FirstPersonController()
camera.fov = 110  # Set the field of view to 110 degrees
sky = Sky()
hand = Hand()

generate_chunk(0, 0)  # Generate the initial chunk
app.run()
