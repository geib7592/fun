function solution(ifile; part)
    positions = init_positions(ifile)
    # display_grid(positions)

    dirs = [[0  1]]
    push!(dirs, [0 -1])
    push!(dirs, [-1  0])
    push!(dirs, [ 1  0])

    max_rounds = Inf
    if part == 1 
        max_rounds = 10
    end

    round = 1
    while round ≤ max_rounds
        println(round)
        positions_prev = copy(positions)
        positions, dirs = play_round(positions, dirs)
        if part == 2
            if positions == positions_prev
                return round
            end
        end
        round += 1
        # display_grid(positions)
    end
    return sum(1 .- full_grid(positions))
end

function init_positions(ifile)
    y = 0
    positions = []
    for line ∈ eachline(ifile)
        for x ∈ eachindex(line)
            if line[x] == '#'
                if isempty(positions)
                    positions = [x y]
                else
                    positions = [positions; x y]
                end
            end
        end
        y -= 1
    end
    return [reshape(positions[i, :], (1, 2)) for i ∈ axes(positions, 1)]
end

function play_round(positions, dirs)
    # get proposed moves
    proposed = [propose_move(p, positions, dirs) for p ∈ positions]

    # only move if proposition is unique
    uniques = findall(j->length(findall(i->proposed[i] == proposed[j], 1:length(proposed))) == 1, 1:length(proposed))
    for i=uniques
        positions[i] = proposed[i]
    end

    # next round starts with next direction
    dirs = circshift(dirs, -1)
    return positions, dirs
end

function propose_move(p_elf, positions, dirs)
    neighbors = [p for p ∈ neighbor_coords(p_elf) if p ∈ positions]
    if isempty(neighbors)
        return p_elf
    end
    for dir ∈ dirs
        if findfirst(isequal(0), dir) == CartesianIndex(1, 1)
            neighbor_coords_dir = [[p_elf[1]+i p_elf[2]+dir[2]] for i=-1:1]
        else
            neighbor_coords_dir = [[p_elf[1]+dir[1] p_elf[2]+i] for i=-1:1]
        end
        if isempty([p for p ∈ neighbor_coords_dir if p ∈ neighbors])
            return p_elf + dir
        end
    end
end

function neighbor_coords(p)
    return [[p[1]+i p[2]+j] for i=-1:1, j=-1:1 if [i j] ≠ [0 0]]
end

function full_grid(positions, N, S, W, E)
    return [[x y] ∈ positions for x=W:E, y=S:N]
end
function full_grid(positions)
    N, S, W, E = minimal_rectangle(positions)
    return full_grid(positions, N, S, W, E)
end

function display_grid(positions, N, S, W, E)
    grid = full_grid(positions, N, S, W, E)
    for i=size(grid, 2):-1:1
        println()
        for j ∈ axes(grid, 1)
            if grid[j, i]
                print("#")
            else
                print(".")
            end
        end
    end
    println()
end
function display_grid(positions)
    N, S, W, E = minimal_rectangle(positions)
    display_grid(positions, N, S, W, E)
end

function minimal_rectangle(positions)
    W = E = positions[1][1]
    N = S = positions[1][2]
    for p ∈ positions
        if p[1] > E
            E = p[1]
        end
        if p[1] < W
            W = p[1]
        end
        if p[2] > N
            N = p[2]
        end
        if p[2] < S
            S = p[2]
        end
    end
    return N, S, W, E
end

# println(solution("input_files/test.txt"; part=1))
# println(solution("input_files/test.txt"; part=2))
# println(solution("input_files/day23_hgp.txt"; part=1))
println(solution("input_files/day23_hgp.txt"; part=2))