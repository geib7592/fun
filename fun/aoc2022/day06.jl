function find_marker(stream, n)
    i = 1
    while !all_different(stream[i:i+n-1])
        i += 1
    end
    return i + n - 1
end

function all_different(letters)
    return length(unique(letters)) == length(letters)
end

s = readline("input_files/day06_hgp.txt")
println(find_marker(s, 4)) # 241 μs
println(find_marker(s, 14)) # 762 μs