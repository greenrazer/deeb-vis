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