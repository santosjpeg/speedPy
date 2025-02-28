import pygame
import moderngl as mgl
from array import array

VERT_SHADER: str = '''
#version 430 core

in vec2 vert;
in vec2 texcoord;
out vec2 UV;

void main() {
    UV = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

FRAG_SHADER: str = '''
#version 430 core

in vec2 UV;
out vec4 COLOR;

uniform sampler2D tex;
uniform sampler2D bg_tex;
uniform float time;
uniform vec2 pre_scaled_screen_size;
const vec2 bg_size = textureSize(bg_tex, 0);
const vec2 texel_size_screen = 1.0 / pre_scaled_screen_size;
const vec2 texel_size = 1.0 / bg_size;

const vec2 n[4] = {
    vec2(-1, 0),
    vec2(1, 0),
    vec2(0, -1),
    vec2(0, 1)
};

const vec4 BG = vec4(53.0/255.0, 101.0/255.0, 77.0/255.0, 1.0); 
const vec4 POKER_BLACK = vec4(28.0/255.0, 28.0/255.0, 30.0/255.0, 1.0);
const vec4 POKER_RED = vec4(199.0/255.0, 44.0/255.0, 72.0/255.0, 1.0);
const vec4 POKER_WHITE = vec4(242.0/255.0, 242.0/255.0, 242.0/255.0, 1.0);
const vec4 POKER_BORDER = vec4(211.0/255.0, 211.0/255.0, 211.0/255.0, 1.0);
const vec4 GRAY = vec4(0.5, 0.5, 0.5, 1.0);

vec4 customBilinear(sampler2D tex_sample, vec2 uv) {
    // Get the texture size
    vec2 texture_size = vec2(textureSize(tex_sample, 0));   
    // Calculate the box filter size in texel units
    vec2 box_size = clamp(fwidth(uv) * texture_size, vec2(1e-5), vec2(1.0));
    // Scale uv by texture size to get texel coordinate
    vec2 tx = uv * texture_size - 0.5 * box_size;
    // Compute offset for pixel-sized box filter
    vec2 tx_offset = clamp((fract(tx) - (vec2(1.0) - box_size)) / box_size, vec2(0.0), vec2(1.0));
    // Compute bilinear sample uv coordinates
    vec2 b_uv = (floor(tx) + vec2(0.5) + tx_offset) / texture_size;
    // Sample the texture using the original uv coordinates
    vec4 color = texture(tex_sample, b_uv);
    // Set the output color
    return color;
}

void main() {
    vec2 uv = UV;
    COLOR = vec4(customBilinear(tex, uv).rgb, 1.0);
    if (COLOR == BG) {
        vec2 tx = uv * pre_scaled_screen_size;
        vec2 tx_floor = floor(tx);
        
        for (int i = 0; i < n.length(); i++) {
            if (vec4(customBilinear(tex, ((tx + n[i]) / pre_scaled_screen_size)).rgb, 1.0) == POKER_BLACK) {
                COLOR = GRAY;
                return;
            } else if (vec4(customBilinear(tex, ((tx + n[i]) / pre_scaled_screen_size)).rgb, 1.0) == POKER_WHITE) {
                COLOR = POKER_BLACK;
                return;
            } else if (vec4(customBilinear(tex, ((tx + n[i]) / pre_scaled_screen_size)).rgb, 1.0) == POKER_RED) {
                COLOR = POKER_BLACK;
                return;
            }
        }
        
        uv = tx / bg_size;
        //COLOR = vec4(customBilinear(bg_tex, vec2(uv.x + time*0.05, uv.y + time*0.05)).rgb, 1.0);
        COLOR = vec4(customBilinear(bg_tex, vec2(uv)).rgb, 1.0);
        
        if (vec4(customBilinear(tex, (UV - texel_size_screen*6)).rgb, 1.0) != BG) {
            COLOR = mix(COLOR, POKER_BLACK, 0.4);
        }
    }
}
'''

class Renderer:
    def __init__(self, bg_surf: pygame.Surface):
        self.ctx: mgl.Context = mgl.create_context()
        self.quad_buffer: mgl.Buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))
        self.program: mgl.Program = self.ctx.program(vertex_shader=VERT_SHADER, fragment_shader=FRAG_SHADER)
        self.render_object: mgl.VertexArray = self.ctx.vertex_array(self.program,
                                                                    [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.bg_tex: mgl.Texture = self.surf_to_texture(bg_surf)
        self.program['tex'] = 0
        self.program['bg_tex'] = 1
        self.bg_tex.use(1)

    def handle_quit(self) -> None:
        self.bg_tex.release()

    def surf_to_texture(self, surf: pygame.Surface) -> mgl.Texture:
        tex: mgl.Texture = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (mgl.LINEAR, mgl.LINEAR)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def render_surf(self, surf: pygame.Surface,
                    pre_scaled_screen_size: tuple[int, int]) -> None:
        self.program['pre_scaled_screen_size'] = pre_scaled_screen_size

        # convert the pygame surface (where origin is topleft) into frame texture
        frame_tex: mgl.Texture = self.surf_to_texture(surf)
        frame_tex.use(0)

        # render the shader object
        self.render_object.render(mode=mgl.TRIANGLE_STRIP)

        pygame.display.flip()
        frame_tex.release()
