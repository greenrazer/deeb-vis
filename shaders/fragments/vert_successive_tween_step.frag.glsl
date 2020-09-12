if (tween_val == 1.0) {
    before = after;
    after  = <matrix>*after;
    tween_val = linearTweenValue(time, <matrix_time_start>, <matrix_time_end>);
}
if (tween_val == 1.0) {
    before = after;
    after  = after + <bias>;
    tween_val = linearTweenValue(time, <bias_time_start>, <bias_time_end>);
}
if (tween_val == 1.0) {
    before = after;
    after  = <activation>(after);
    tween_val = linearTweenValue(time, <activation_time_start>, <activation_time_end>);
}