#version 330
in vec3 from_vert;
in vec3 to_vert;

in vec3 before_vert;
in vec3 after_vert;

in vec3 translate_from;
in vec3 translate_to;

in vec2 point_transform_start_stop_time;
in vec3 normal;
in vec3 light_direction;
in float width_scale;
in vec3 in_color;
in uint type;

out vec2 uv;
out vec3 color;

uniform float time;
uniform mat4 projection_matrix;
uniform vec3 camera_pos;

<uniforms>

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

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
    vec3 vert = vec3(0.0);
    vec3 before = vec3(0.0);
    vec3 after  = vec3(0.0);
    vec3 direction  = vec3(0.0);
    vec3 tween_trans = vec3(0.0);
    vec3 tangent_v = vec3(0.0);

    vec3 b4_vert = vec3(0.0);
    vec3 curr_vert = vec3(0.0);
    vec3 aft_vert = vec3(0.0);
    float tween_val = 0.0;

    float scaled_width_scale = width_scale*length(camera_pos - from_vert);

    // type 0 is a line triangle
    // type 1 is a shaded sphere triangle
    // type 2 is a non-shaded triangle
    // type 3 is to point animated shaded sphere triangle
    // type 4 is global function animated sphere triangle
    // type 5-7 is static line triangle
    // type 8-10 is global function animated line triangle
    switch(type){
        case 0u:
            direction = normalize(cross(camera_pos - from_vert, translate_from));
            vert = from_vert + direction*width_scale;
            color = in_color;
            break;
        
        case 1u:
            vert = from_vert*width_scale + translate_from;
            color = in_color*map(dot(normalize(vert - translate_from), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;

        case 2u:
            vert = from_vert*width_scale + translate_from;
            color = in_color;
            break;

        case 3u:
            float point_tween_val = linearTweenValue(time, point_transform_start_stop_time.x, point_transform_start_stop_time.y);
            vec3 point_tween_trans = linearTween(point_tween_val, translate_from, translate_to);
            vert = from_vert*width_scale + point_tween_trans;
            color = in_color*map(dot(normalize(vert - point_tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;
        
        case 4u:
            <matrix_step_sphere_transform>
            tween_trans = linearTween(tween_val, before, after);
            vert = from_vert*scaled_width_scale + tween_trans;
            color = in_color*map(dot(normalize(vert - tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;
        
        case 5u:
            // Start
            tangent_v = tangent(before_vert, from_vert, after_vert, 0u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 6u:
            // Middle
            tangent_v = tangent(before_vert, from_vert, after_vert, 1u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 7u:
            // End
            tangent_v = tangent(before_vert, from_vert, after_vert, 2u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 8u:
            // Start
            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 0u);
            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 9u:
            // Middle
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 1u);

            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 10u:
            // End
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 2u);
            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*scaled_width_scale/2;
            color = in_color;
            break;

        case 255u:
            vert =  normal + to_vert + before_vert + after_vert;
            color = in_color;
            break;
    }
    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy; 
}

