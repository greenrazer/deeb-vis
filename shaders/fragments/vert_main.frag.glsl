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
            <matrix_step_sphere_transform>
            tween_trans = linearTween(tween_val, before, after);
            vert = from_vert*width_scale + tween_trans;
            color = in_color*map(dot(normalize(vert - tween_trans), light_direction), -1.0, 1.0, 0.0, 1.0);
            break;
        
        case 5u:
            tangent_v = tangent(before_vert, from_vert, after_vert, 0u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*width_scale;
            color = in_color;
            break;

        case 6u:
            tangent_v = tangent(before_vert, from_vert, after_vert, 1u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*width_scale;
            color = in_color;
            break;

        case 7u:
            tangent_v = tangent(before_vert, from_vert, after_vert, 2u);
            direction = normalize(cross(camera_pos - from_vert, tangent_v));
            vert = from_vert + direction*width_scale;
            color = in_color;
            break;

        case 8u:
            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 0u);
            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*width_scale;
            color = in_color;
            break;

        case 9u:
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            <after_vert_matrix_transform>
            aft_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 1u);

            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*width_scale;
            color = in_color;
            break;

        case 10u:
            <b4_vert_matrix_transform>
            b4_vert = linearTween(tween_val, before, after);

            <curr_vert_matrix_transform>
            curr_vert = linearTween(tween_val, before, after);

            tangent_v = tangent(b4_vert, curr_vert, aft_vert, 2u);
            direction = normalize(cross(camera_pos - curr_vert, tangent_v));
            vert = curr_vert + direction*width_scale;
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