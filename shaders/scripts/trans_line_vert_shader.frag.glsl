#version 430
in vec3 before_vert;
in vec3 curr_vert;
in vec3 after_vert;

in float width;
in vec3 in_color;
in uint type;

out vec2 uv;
out vec3 color;

uniform float time;
uniform mat4 projection_matrix;
uniform vec3 camera_pos;

<uniforms>

float linearTweenValue(float value, float start, float stop) {
    if (value < start) {
        return 0.0;
    }
    else if (value < stop) {
        float total = (stop - start);
        if(total == 0) {
            return 1.0;
        }
        return (value - start)/total;
    }
    else {
        return 1.0;
    }
}

vec3 linearTween(float value, vec3 a, vec3 b){
    return (1.0-value)*a + value*b;
}

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

<activations>

void main() {
    vec3 before = vec3(0.0);
    vec3 after  = vec3(0.0);

    vec3 b4_vert = vec3(0.0);
    vec3 at_vert = vec3(0.0);
    vec3 aft_vert = vec3(0.0);
    float tween_val = 0.0;

    switch(type){
        case 0u:
            // Start
            <curr_vert_matrix_transform>
            at_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);
            break;

        case 1u:
            // Middle
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            at_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);
            break;

        case 2u:
            // End
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            at_vert = linearTween(tween_val, before, after);
            break;
    }

    vec3 tangent_v = tangent(b4_vert, at_vert, aft_vert, type);
    vec3 direction = normalize(cross(camera_pos - at_vert, tangent_v));
    float scaled_width = width*length(camera_pos - curr_vert);
    vec3 vert = at_vert + direction*scaled_width/2;

    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy; 
    color = in_color;
}

