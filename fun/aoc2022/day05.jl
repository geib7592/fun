function rearrange_crates(ifile; part)
    # get initial stacks
    stacks = initial_stacks(ifile)
    # display(stacks)

    open(ifile) do f
        # get to first move
        line = readline(f)
        while line != ""
            line = readline(f)
        end

        while !eof(f)
            # get move command
            line = readline(f)
            n, i, j = parse_move_line(line)
            # println("move $n from $i to $j")

            # do moves
            stacks = move_crates(stacks, n, i, j, part=part)
            # display(stacks)
        end
    end

    return stacks
end

function parse_move_line(line)
    # parse lines of form `move n crates from i to j`
    i1 = findnext(' ', line, 1)
    i2 = findnext(' ', line, i1+1)
    n = parse(Int64, line[i1+1:i2-1])

    i1 = findnext(' ', line, i2+1)
    i2 = findnext(' ', line, i1+1)
    i = parse(Int64, line[i1+1:i2-1])

    i1 = findnext(' ', line, i2+1)
    i2 = findnext(' ', line, i1+1)
    j = parse(Int64, line[i1+1:end])
    return n, i, j
end

function move_crates(stacks, n, i, j; part)
    if part == 1
        for _=1:n
            # move top crate in stack `i` to stack `j`
            pushfirst!(stacks[j], popfirst!(stacks[i]))
        end
    elseif part == 2
        # move all `n` crates at once
        crates = stacks[i][1:n]
        for k=1:n
            popfirst!(stacks[i])
            pushfirst!(stacks[j], crates[n-k+1])
        end
    end
    return stacks
end

function initial_stacks(ifile)
    # get number of stacks
    n_stacks = 0
    open(ifile) do f
        line = readline(f)
        while line[2] != '1'
            line = readline(f)
        end
        n_stacks = parse(Int64, line[end-1])
    end
    
    # initialize empty stacks vector
    stacks = Vector{Vector{Char}}()
    for i=1:n_stacks
        push!(stacks, Vector{Char}()) 
    end

    # fill stacks
    stack_cols = 2:4:(2 + 4*(n_stacks - 1))
    open(ifile) do f
        line = readline(f)
        while line[2] != '1'
            for i=1:n_stacks
                crate = line[stack_cols[i]]
                if crate != ' '
                    push!(stacks[i], crate)
                end
            end
            line = readline(f)
        end
    end
    return stacks
end

function print_top_crates(stacks)
    for stack in stacks
        print(stack[1])    
    end
    println()
end

print_top_crates(rearrange_crates("input_files/day05_hgp.txt", part=1)) # 137 μs
print_top_crates(rearrange_crates("input_files/day05_hgp.txt", part=2)) # 150 μs