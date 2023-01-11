function find_marker(stream, n)
    i = 1
    while length(Set(stream[i:i+n-1])) != n
        i += 1
    end
    return i + n - 1
end

s = readline("input_files/day06_hgp.txt")
println(find_marker(s, 4)) # 160 μs
println(find_marker(s, 14)) # 688 μs