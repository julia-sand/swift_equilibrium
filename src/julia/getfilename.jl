macro get_file_name(args...)
    parts = []

    for arg in args
        name = String(arg)
        val = esc(arg)

        push!(parts, :(
            begin
                v = $val
                v_str = v == sqrt(2) ? "1-4" : replace(string(v), "." => "-")
                string($name, v_str, "_")
            end
        ))
    end

    return :(join(($(parts...),)) * ".csv")
end
