function solution(ifile; part)
    if part == 1
        N = 2
    elseif part == 2
        N = 10
    end
    rope = ones(N, 2)
    all_T_pos = [1, 1]
    for line in eachline(ifile)
        dir, reps = split(line)
        for _=1:parse(Int64, reps)
            update_H_pos!(rope, dir)
            for i=2:N
                update_i_pos!(rope, i)
            end
            all_T_pos = hcat(all_T_pos, rope[end, :])
            # display_rope(rope, 6)
        end
    end
    return size(unique(all_T_pos, dims=2), 2)
end

function update_H_pos!(rope, dir)
    if dir == "R"
        rope[1, 1] += 1
    elseif dir == "L"
        rope[1, 1] -= 1
    elseif dir == "U"
        rope[1, 2] += 1
    elseif dir == "D"
        rope[1, 2] -= 1
    else
        error("Invalid direction $dir.")
    end
end

function update_i_pos!(rope, i)
    Δ = rope[i-1, :] - rope[i, :]
    if abs(Δ[1]) > 1 || abs(Δ[2]) > 1
        rope[i, :] += sign.(Δ)
    end
end

function display_rope(rope, N)
    println()
    for i=N-1:-1:1
        for j=1:N
            is_rope = false
            for k ∈ axes(rope, 1)
                if rope[k, :] == [j, i]
                    if k == 1
                        print("H")
                    else
                        print(k-1)
                    end
                    is_rope = true
                    break
                end
            end
            if !is_rope
                print(".")
            end
        end
        println()
    end
end

println(solution("input_files/day09_hgp.txt", part=1)) # 48 ms
println(solution("input_files/day09_hgp.txt", part=2)) # 69 ms