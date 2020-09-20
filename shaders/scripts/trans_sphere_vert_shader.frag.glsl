#version 430
in vec3 curr_vert;
in vec3 translate;
in float scale;
in vec3 in_color;

out vec2 uv;
out vec3 color;

uniform float time;
uniform mat4 projection_matrix;
uniform vec3 camera_pos;
uniform vec3 light_direction;

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

<activations>

void main() { 
    vec3 before = vec3(0.0);
    vec3 after  = vec3(0.0);
    float tween_val = 0.0;

    <matrix_step_sphere_transform>
    
    float scaled_vert = scale*length(camera_pos - curr_vert);
    vec3 tween_trans = linearTween(tween_val, before, after);
    vec3 vert = curr_vert*scaled_vert + tween_trans;
    gl_Position = projection_matrix * vec4(vert, 1.0);
    uv = vert.xy; 
    color = in_color*map(dot(normalize(vert - tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
}

