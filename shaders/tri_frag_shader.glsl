#version 330
#define PI 3.14159265359

in vec2 uv;
in vec3 color;

out vec4 f_color;

vec2 cart2polar(vec2 a)
{
    float theta = atan(a.y,a.x);
    return vec2(length(a), mod(theta, 2.0*PI));
}

vec4 colorWheel(float radius, float theta)
{
    float h = theta;
    float s = -exp(-3.0*radius) + 1.0;
    float v = 1.0;

    float c = v*s;
    float x = c*(1-abs(mod(3*theta/PI, 2) - 1));
    float m = v - c;

    vec3 rgbprime = vec3(0.0);

    if(0.0 <= theta && theta < PI/3.0) {
        rgbprime = vec3(c,x,0.0);
    }
    else if(theta < 2.0*PI/3.0) {
        rgbprime = vec3(x,c,0.0);
    }
    else if(theta < PI) {
        rgbprime = vec3(0.0,c,x);
    }
    else if(theta < 4.0*PI/3.0) {
        rgbprime = vec3(0.0,x,c);
    }
    else if(theta < 5.0*PI/3.0) {
        rgbprime = vec3(x,0.0,c);
    }
    else if(theta < 2.0*PI) {
        rgbprime = vec3(c,0.0,x);
    }

    return vec4((rgbprime.x + m),
                (rgbprime.y + m),
                (rgbprime.z + m),
                1.0);
}

void main() {
    vec2 polaruv = cart2polar(uv);
    vec4 color4 = colorWheel(polaruv.x, polaruv.y);
    if (color.x == 1.0) {
        color4.z += 0.001;
    }
    f_color = vec4(color, 1.0);
}