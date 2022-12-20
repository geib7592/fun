struct Monkey{V<:AbstractVector, S<:AbstractString, I<:Integer}
    items::V
    op1::S 
    op2::S 
    div::I
    throw_true::I
    throw_false::I
end

function solution(ifile; part)
    # read file
    monkeys = init_monkeys(ifile)

    # least common multiple of monkey divisors
    N = 1
    for m ∈ monkeys
        N *= m.div
    end

    # number of rounds
    if part == 1
        n_rounds = 20
    elseif part == 2
        n_rounds = 10000
    end

    # count inspections
    inspections = zeros(length(monkeys))
    for _=1:n_rounds
        monkeys, round_inspections = play_round(monkeys, N; part)
        inspections += round_inspections
    end

    return prod(sort(inspections, rev=true)[1:2])
end

function play_round(monkeys, N; part)
    inspections = zeros(length(monkeys))
    for i ∈ eachindex(monkeys)
        m = monkeys[i]
        for item ∈ m.items
            if part == 1
                new_item = div(op(m, item), 3)
            elseif part == 2
                new_item = mod(op(m, item), N)
            end
            if rem(new_item, m.div) == 0
                push!(monkeys[m.throw_true].items, new_item)
            else
                push!(monkeys[m.throw_false].items, new_item)
            end
            inspections[i] += 1
        end
        for _=1:length(m.items)
            pop!(m.items)
        end
    end
    return monkeys, inspections
end

function op(m::Monkey, old)
    if m.op2 == "old"
        n = old
    else
        n = parse(Int64, m.op2)
    end

    if m.op1 == "+"
        return old + n
    elseif m.op1 == "*"
        return old * n
    end
end

function init_monkeys(ifile)
    monkeys = []
    open(ifile, "r") do f
        while !eof(f)
            # mokey # line
            readline(f)

            # get items
            line = split(readline(f))
            items = parse.(Int64, chopsuffix.(line[3:end], ","))

            # get operation
            line = split(readline(f))
            op1 = line[5] # + or *
            op2 = line[6] # number of `old`

            # get divisor
            line = split(readline(f))
            div = parse(Int64, line[4])

            # get monkey to throw to if true
            line = split(readline(f))
            throw_true = parse(Int64, line[6]) + 1

            # get monkey to throw to if false
            line = split(readline(f))
            throw_false = parse(Int64, line[6]) + 1

            # add to list
            push!(monkeys, Monkey(items, op1, op2, div, throw_true, throw_false))

            # read blank line
            readline(f)
        end
    end
    return monkeys
end

println(solution("input_files/day11_hgp.txt", part=1)) # 405 μs
println(solution("input_files/day11_hgp.txt", part=2)) # 206 ms