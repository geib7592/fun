function solution(ifile; part)
    s = 0
    data = read(ifile, String)
    if part == 1
        pairs = split(data, "\n\n")
        for i ∈ eachindex(pairs)
            lines = split(pairs[i], "\n")

            # read signals
            x = eval(Meta.parse(lines[1]))
            y = eval(Meta.parse(lines[2]))

            # determine if in right order
            check = in_order(x, y)
            if check ≥ 0
                s += i
            end
        end
        return s
    elseif part == 2
        lines = eval.(Meta.parse.(split(replace(data, "\n\n" => "\n"), "\n")))
        dividers = [[[2]], [[6]]]
        for d ∈ dividers
            push!(lines, d)
        end
        s = sort(lines, lt=in_order_TF)
        return prod(findfirst(isequal(d), s) for d ∈ dividers)
    end
end

function in_order(x, y)
    for i ∈ eachindex(x)
        if i > length(y)
            return -1
        end
        left = x[i]
        right = y[i]
        if typeof(left) == typeof(right) <: Integer
            if left < right
                return 1
            elseif left > right
                return -1
            else
                continue
            end
        elseif typeof(left) <: Integer
            left = [left]
        elseif typeof(right) <: Integer
            right = [right]
        end
        check = in_order(left, right) 
        if check != 0
            return check
        end
    end
    if length(y) > length(x)
        return 1
    end
    return 0
end

function in_order_TF(x, y)
    return in_order(x, y) == 1
end

println(solution("input_files/day13_hgp.txt"; part=1)) # 0.2 s
println(solution("input_files/day13_hgp.txt"; part=2)) # 0.2 s