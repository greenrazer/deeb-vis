#version 330
in vec3 from_vert;
in vec3 to_vert;
in vec3 translate_from; //for type 0 (line) its is the tangent, for type 1 (sphere) it is translate
in vec3 translate_to;
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

uniform mat3 change_matrix_0;
uniform vec3 change_bias_0;
uniform vec2 matrix_change_start_stop_time_0;
uniform vec2 bias_change_start_stop_time_0;
uniform vec2 activation_change_start_stop_time_0;
uniform mat3 change_matrix_1;
uniform vec3 change_bias_1;
uniform vec2 matrix_change_start_stop_time_1;
uniform vec2 bias_change_start_stop_time_1;
uniform vec2 activation_change_start_stop_time_1;

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
vec3 activation_function_0(vec3 val) {
    return (1.0 / (1.0 + exp(- val)));
}
void main() { 
    vec3 vert = vec3(0.0);
    vec3 before = vec3(0.0);
    vec3 after  = vec3(0.0);
    vec3 direction  = vec3(0.0);
    float tween_val = 0.0;

    // type 0 is a line triangle
    // type 1 is a shaded sphere triangle
    // type 2 is a non-shaded triangle
    // type 3 is to point animated shaded sphere triangle
    // type 4 is global function animated sphere triangle
    // type 5 is global function animated line triangle
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
            before = translate_from;
after  = change_matrix_0*translate_from;
tween_val = linearTweenValue(time, matrix_change_start_stop_time_0.x, matrix_change_start_stop_time_0.y);

if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_0;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_0.x, bias_change_start_stop_time_0.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_0.x, activation_change_start_stop_time_0.y);
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_1*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_1.x, matrix_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_1;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_1.x, bias_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_1.x, activation_change_start_stop_time_1.y);
}
            vec3 global_tween_trans = linearTween(tween_val, before, after);
            vert = from_vert*width_scale + global_tween_trans;
            color = in_color*map(dot(normalize(vert - global_tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;
        
        case 5u:
            before = from_vert;
after  = change_matrix_0*from_vert;
tween_val = linearTweenValue(time, matrix_change_start_stop_time_0.x, matrix_change_start_stop_time_0.y);

if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_0;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_0.x, bias_change_start_stop_time_0.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_0.x, activation_change_start_stop_time_0.y);
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_1*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_1.x, matrix_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_1;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_1.x, bias_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_1.x, activation_change_start_stop_time_1.y);
}
            vec3 position_tween_line = linearTween(tween_val, before, after);
            before = translate_from;
after  = change_matrix_0*translate_from;
tween_val = linearTweenValue(time, matrix_change_start_stop_time_0.x, matrix_change_start_stop_time_0.y);

if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_0;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_0.x, bias_change_start_stop_time_0.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_0.x, activation_change_start_stop_time_0.y);
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_1*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_1.x, matrix_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_1;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_1.x, bias_change_start_stop_time_1.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_1.x, activation_change_start_stop_time_1.y);
}
            vec3 position_tangent_line = linearTween(tween_val, before, after);

            direction = normalize(cross(camera_pos - position_tween_line, translate_from));
            vert = position_tween_line + direction*width_scale;
            color = in_color;
            break;

        case 255u:
            vert =  normal + to_vert;
            color = in_color;
            break;
    }
    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy; 
}