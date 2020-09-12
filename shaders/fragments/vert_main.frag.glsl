void main() { 
    vec3 vert = vec3(0.0);

    // type 0 is a line triangle
    // type 1 is a shaded sphere triangle
    // type 2 is a non-shaded triangle
    // type 3 is to point animated sphere triangle
    // type 4 is global function animated sphere triangle
    // type 5 is global function animated line triangle
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
            <matrix_step_transform>
            vec3 global_tween_trans = linearTween(tween_val, before, after);
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