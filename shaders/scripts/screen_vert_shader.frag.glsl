#version 430
in vec3 vert;
in vec2 texture_coord;

out vec2 uv;

uniform mat4 projection_matrix;

void main() {
    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = texture_coord;
}

