KEY = 811589153

function solution(ifile; part)
    init_data = parse.(Int64, readlines(ifile))
    n_mix = 1
    if part == 2
        init_data *= KEY
        n_mix = 10
    end
    N = length(init_data)
    indices = collect(1:N)
    for _=1:n_mix
        for i=1:N
            moveby = init_data[i]
            idx = findfirst(isequal(i), indices)
            deleteat!(indices, idx)
            ins = idx + moveby
            if ins == 1 && moveby != 0
                push!(indices, i)
            else
                insert!(indices, mod1(ins, N-1), i)
            end
        end
    end
    new_data = [init_data[i] for i=indices]
    zero_idx = findfirst(isequal(0), new_data)
    return sum(new_data[mod1(zero_idx + i, N)] for i=[1000, 2000, 3000])
end

println(solution("input_files/day20_hgp.txt", part=1)) # 5 ms
println(solution("input_files/day20_hgp.txt", part=2)) # 60 ms