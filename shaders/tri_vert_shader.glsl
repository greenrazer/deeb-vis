#version 330
in vec3 from_vert;
in vec3 to_vert;
in vec3 tangent_translate_from; //for type 0 (line) its is the tangent, for type 1 (sphere) it is translate
in vec3 tangent_translate_to;
in vec2 point_transform_start_stop_time;
in vec3 normal;
in vec3 light_direction;
in float width_scale; //for type 0 (line) its is the width, for type 1 (sphere) it is scale
in vec3 in_color;
in uint type;

out vec2 uv;
out vec3 color;

uniform float time;

uniform mat4 projection_matrix;

uniform vec3 camera_pos;

uniform mat3 change_matrix;
uniform vec3 change_bias;
uniform vec2 matrix_change_start_stop_time;
uniform vec2 bias_change_start_stop_time;
uniform vec2 activation_function_change_start_stop_time;


float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

vec3 activation_function(vec3 a) {
  return 1.0/(1.0 + exp(-a));
}

float linearTweenValue(float value, float start, float stop) {
    if (value < start) {
        return 0.0;
    }
    else if (value < stop) {
        return (value - start)/(stop - start);
    }
    else {
        return 1.0;
    }
}

vec3 linearTween(float value, vec3 a, vec3 b){
    return (1.0-value)*a + value*b;
}

void main() { 
    vec3 vert = vec3(0.0);

    // type 0 is a line triangle
    // type 1 is a shaded sphere triangle
    // type 2 is a non-shaded triangle
    // type 3 is to point animated sphere triangle
    // type 4 is global function animated sphere triangle
    switch(type){
        case 0u:
            vec3 direction = normalize(cross(camera_pos - from_vert, tangent_translate_from));
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
            float point_tween_val = linearTweenValue(time, point_transform_start_stop_time.x, point_transform_start_stop_time.y);
            vec3 point_tween_trans = linearTween(point_tween_val, tangent_translate_from, tangent_translate_to);
            vert = from_vert*width_scale + point_tween_trans;
            color = in_color*map(dot(normalize(vert - point_tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;
        
        case 4u:
            vec3 before = tangent_translate_from;
            vec3 after  = change_matrix*tangent_translate_from;

            float global_tween_val = linearTweenValue(time, matrix_change_start_stop_time.x, matrix_change_start_stop_time.y);
            if (global_tween_val == 1.0) {
                before = after;
                after  = after + change_bias;
                global_tween_val = linearTweenValue(time, bias_change_start_stop_time.x, bias_change_start_stop_time.y);
                if (global_tween_val == 1.0) {
                    before = after;
                    after  = activation_function(after);
                    global_tween_val = linearTweenValue(time, activation_function_change_start_stop_time.x, activation_function_change_start_stop_time.y);
                }
            }

            vec3 global_tween_trans = linearTween(global_tween_val, before, after);
            vert = from_vert*width_scale + global_tween_trans;
            color = in_color*map(dot(normalize(vert - global_tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;

        case 255u:
            vert =  normal + to_vert;
            color = in_color;
            break;
    }

    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy;
    
}