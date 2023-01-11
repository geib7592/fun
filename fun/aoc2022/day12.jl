function solution(ifile; part)
    T = load_terrain(ifile)
    pos = indexin(-1, T)[1]
    paths = []
    return path_lengths(pos, T, paths, 0)
end

function min_path(pos, T)
    if T[pos] == -2
        push!(paths, l)
    else
        pos_U = CartesianIndex(pos[1]-1, pos[2])
        pos_D = CartesianIndex(pos[1]+1, pos[2])
        pos_L = CartesianIndex(pos[1],   pos[2]-1)
        pos_R = CartesianIndex(pos[1],   pos[2]+1)
        for new_pos ∈ [pos_U, pos_D, pos_L, pos_R]
            try T[new_pos]
                if T[new_pos] ≤ T[pos] + 1
                    path_lengths(new_pos, T, paths, l+1)
                end
            catch
            end
        end
    end
end

function load_terrain(ifile)
    T = []
    for line ∈ eachline(ifile)
        if isempty(T)
            T = char_to_elev.(collect(line))'
        else
            T = vcat(T, char_to_elev.(collect(line))')
        end
    end
    return T
end

function char_to_elev(c)
    if c == 'S'
        # current position
        return -1
    elseif c == 'E'
        # goal
        return -2
    else
        # 'a' = 97 ↦ 0, 'A' = 65 ↦ 26
        return convert(Int64, c) - 97 + 58*isuppercase(c)
    end
end

println(solution("input_files/test.txt"; part=1))
# println(solution("input_files/test.txt"; part=2))