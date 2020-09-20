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
uniform mat3 change_matrix_2;
uniform vec3 change_bias_2;
uniform vec2 matrix_change_start_stop_time_2;
uniform vec2 bias_change_start_stop_time_2;
uniform vec2 activation_change_start_stop_time_2;


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

vec3 activation_function_0(vec3 val) {
    return (1.0 / (1.0 + exp(- val)));
}

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
            before = curr_vert;
after  = change_matrix_0*curr_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            at_vert = linearTween(tween_val, before, after);

            before = after_vert;
after  = change_matrix_0*after_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            aft_vert = linearTween(tween_val, before, after);
            break;

        case 1u:
            // Middle
            before = before_vert;
after  = change_matrix_0*before_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            b4_vert = linearTween(tween_val, before, after);

            before = curr_vert;
after  = change_matrix_0*curr_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            at_vert = linearTween(tween_val, before, after);

            before = after_vert;
after  = change_matrix_0*after_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            aft_vert = linearTween(tween_val, before, after);
            break;

        case 2u:
            // End
            before = before_vert;
after  = change_matrix_0*before_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
            b4_vert = linearTween(tween_val, before, after);

            before = curr_vert;
after  = change_matrix_0*curr_vert;
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
}if (tween_val == 1.0) {
    before = after;
    after  = change_matrix_2*after;
    tween_val = linearTweenValue(time, matrix_change_start_stop_time_2.x, matrix_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + change_bias_2;
    tween_val = linearTweenValue(time, bias_change_start_stop_time_2.x, bias_change_start_stop_time_2.y);
}
if (tween_val == 1.0) {
    before = after;
    after  = activation_function_0(after);
    tween_val = linearTweenValue(time, activation_change_start_stop_time_2.x, activation_change_start_stop_time_2.y);
}
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

