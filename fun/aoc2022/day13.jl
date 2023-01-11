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

"""
    in_order(x, y)

 1 - correct order
 0 - tie
-1 - incorrect order
"""
function in_order(x, y)
    for i ∈ eachindex(x)
        # x is longer than y → incorrect
        if i > length(y)
            return -1
        end

        # compare ith elements of x and y
        left = x[i]
        right = y[i]

        # deal with possible types
        if typeof(left) == typeof(right) <: Integer
            # regular integer ordering
            if left < right
                return 1
            elseif left > right
                return -1
            else
                # equal, go to next element
                continue
            end
        elseif typeof(left) <: Integer
            # right must be a list, change left
            left = [left]
        elseif typeof(right) <: Integer
            # left must be a list, change right
            right = [right]
        end

        # recursively run check on left and right
        check = in_order(left, right) 
        if check != 0
            return check
        end
    end

    # y is longer than x → correct
    if length(y) > length(x)
        return 1
    end

    # otherwise, tie
    return 0
end

function in_order_TF(x, y)
    return in_order(x, y) == 1
end

println(solution("input_files/day13_hgp.txt"; part=1)) # 0.2 s
println(solution("input_files/day13_hgp.txt"; part=2)) # 0.2 s