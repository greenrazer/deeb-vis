#version 430
in vec2 uv;

out vec4 f_color;

uniform sampler2D Texture;

void main() {
    f_color = vec4(texture(Texture, uv).rgb, 0.5);
}