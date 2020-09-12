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
