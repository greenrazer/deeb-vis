#version 330
in vec3 in_vert;
in vec3 tangent;
in float width;
in vec3 in_color;
in uint type;

out vec2 uv;
out vec3 color;

uniform float z_near;
uniform float z_far;
uniform float fovy;
uniform float ratio;

uniform vec3 center;
uniform vec3 eye;
uniform vec3 up;

mat4 perspective() {
    float zmul = (-2.0 * z_near * z_far) / (z_far - z_near);
    float ymul = 1.0 / tan(fovy * 3.14159265 / 360);
    float xmul = ymul / ratio;

    return mat4(
        xmul, 0.0, 0.0, 0.0,
        0.0, ymul, 0.0, 0.0,
        0.0, 0.0, -1.0, -1.0,
        0.0, 0.0, zmul, 0.0
    );
}

mat4 lookat() {
    vec3 forward = normalize(center - eye);
    vec3 side = normalize(cross(forward, up));
    vec3 upward = cross(side, forward);

    return mat4(
        side.x, upward.x, -forward.x, 0,
        side.y, upward.y, -forward.y, 0,
        side.z, upward.z, -forward.z, 0,
        -dot(eye, side), -dot(eye, upward), dot(eye, forward), 1
    );
}

void main() {
    float num = 0.1;
    
    if (type == 0u){
        num = 0.0;
    }

    vec3 direction = normalize(cross(eye - in_vert, tangent));
    vec3 vert = in_vert + direction*width;

    gl_Position = perspective() * lookat() * vec4(vert, 1.0);
    uv = vert.xy + vec2(num);
    color = in_color;
}