#version 330
in vec3 from_vert;
in vec3 to_vert;
in vec3 tangent_translate_from; //for type 0 (line) its is the tangent, for type 1 (sphere) it is translate
in vec3 tangent_translate_to;
in vec2 hold_transform_time;
in vec3 normal;
in vec3 light_direction;
in float width_scale; //for type 0 (line) its is the width, for type 1 (sphere) it is scale
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

uniform float time;

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

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

void main() { 
    vec3 vert = vec3(0.0);

    // type 0 is a line triangle
    // type 1 is a shaded sphere triangle
    // type 2 is a non-shaded triangle
    switch(type){
        case 0u:
            vec3 direction = normalize(cross(eye - from_vert, tangent_translate_from));
            vert = from_vert + direction*width_scale;
            color = in_color;
            break;
        
        case 1u:
            vert = from_vert*width_scale + tangent_translate_from;
            color = in_color*map(dot(normalize(vert - tangent_translate_from), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;

        case 2u:
            vert = from_vert*width_scale + tangent_translate_from;
            color = in_color;
            break;

        case 3u:
            if (time < hold_transform_time.x) {
                vert = from_vert*width_scale + tangent_translate_from;
                color = in_color*map(dot(normalize(vert - tangent_translate_from), light_direction), -1.0, 1.0, 0.0, 1.0);
            }
            else if (time < hold_transform_time.y ) {
                float tween = (time - hold_transform_time.x)/(hold_transform_time.y - hold_transform_time.x);
                vec3 tween_trans = (1.0-tween)*tangent_translate_from + tween*tangent_translate_to;
                vert = from_vert*width_scale + tween_trans;
                color = in_color*map(dot(normalize(vert - tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            }
            else {
                vert = from_vert*width_scale + tangent_translate_to;
                color = in_color*map(dot(normalize(vert - tangent_translate_to), light_direction), -1.0, 1.0, 0.0, 1.0);
            }
            break;

        case 255u:
            vert =  normal + to_vert;
            color = in_color;
            break;
    }

    gl_Position = perspective() * lookat() * vec4(vert, 1.0);
    uv = vert.xy;
    
}