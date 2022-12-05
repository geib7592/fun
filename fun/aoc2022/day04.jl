function count_overlaps(fname; part)
    count = 0
    for line in eachline(fname) # this was 1000x faster than readdlm(fname, ',')
        elf1, elf2 = parse_line(line)
        elf1 = string_to_list(elf1)
        elf2 = string_to_list(elf2)
        if part == 1
            if elf2[findall(in(elf1), elf2)] == elf2 || elf1[findall(in(elf2), elf1)] == elf1
                count += 1
            end
        elseif part == 2
            if !isempty(findall(in(elf1), elf2))
                count += 1
            end
        end
    end
    return count
end

function parse_line(line)
    # comma separated line
    i = indexof(',', line)
    return line[1:i-1], line[i+1:end]
end

function string_to_list(s)
    # string of form A-B
    i = indexof('-', s)
    return parse(Int64, s[1:i-1]):parse(Int64, s[i+1:end])
end

"""
    i = indexof(c, s)

Find index of character `c` in string `s`.
[For some reason this was faster than `indexin(c, s)`]
"""
function indexof(c, s)
    i = 1
    while s[i] != c
        i += 1
    end
    return i
end

println(count_overlaps("input_files/day04_hgp.txt", part=1)) # 198 μs
println(count_overlaps("input_files/day04_hgp.txt", part=2)) # 194 μs