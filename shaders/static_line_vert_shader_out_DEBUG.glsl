#version 430
in vec3 before_vert;
in vec3 curr_vert;
in vec3 after_vert;

in float width;
in vec3 in_color;
in uint type;

out vec2 uv;
out vec3 color;

uniform mat4 projection_matrix;
uniform vec3 camera_pos;


vec3 tangent(vec3 prev, vec3 at, vec3 next, uint type) {
    switch(type) {
        case 0u:
            return normalize(next - at);
        case 1u:
            vec3 v1 = normalize(prev - at);
            vec3 v2 = normalize(next - at);

            float d = dot(v1,v2);
            if (abs(d) == 1.0){
                return v2;
            }
            
            return normalize(v2 - v1);
        case 2u:
            return normalize(at - prev);
    }   
}

void main() { 
    vec3 tangent_v = tangent(before_vert, curr_vert, after_vert, type);
    float scaled_width = width*length(camera_pos - curr_vert);
    vec3 direction = normalize(cross(camera_pos - curr_vert, tangent_v));
    vec3 vert = curr_vert + direction*scaled_width/2;

    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy; 
    color = in_color;
}

