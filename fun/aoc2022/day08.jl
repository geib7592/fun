function solution(ifile; part)
    grid = read_grid(ifile)
    if part == 1
        # count visible
        return sum(Int64(is_visible(grid, i, j)) for i ∈ axes(grid, 1), j ∈ axes(grid, 2))
    elseif part == 2
        # find max scenic score
        return maximum(scenic_score(grid, i, j) for i ∈ axes(grid, 1), j ∈ axes(grid, 2))
    end
end

function read_grid(ifile)
    m = countlines(ifile)
    f = open(ifile, "r")
    row = readline(f)
    n = length(row)
    grid = zeros(Int64, m, n) 
    grid[1, :] = [row[j] for j=1:n]
    for i=2:m
        row = readline(f)
        grid[i, :] = [row[j] for j=1:n]
    end
    close(f)
    return grid
end

function is_visible(grid, i, j)
    left, right, bottom, top = neighbors(grid, i, j)
    return is_tallest(grid[i, j], left) || is_tallest(grid[i, j], right) || is_tallest(grid[i, j], bottom) || is_tallest(grid[i, j], top)
end

function neighbors(grid, i, j)
    left = grid[i, j-1:-1:1] # in order for part 2
    right = grid[i, j+1:end]
    bottom = grid[i-1:-1:1, j] # in order for part 2
    top = grid[i+1:end, j]
    return left, right, bottom, top
end

function is_tallest(tree, trees)
    return sum(tree .> trees) == length(trees)
end

function scenic_score(grid, i, j)
    left, right, bottom, top = neighbors(grid, i, j)
    return viewing_distance(grid[i, j], left) * 
           viewing_distance(grid[i, j], right) *
           viewing_distance(grid[i, j], bottom) *
           viewing_distance(grid[i, j], top)
end

function viewing_distance(tree, trees)
    if minimum([tree; trees]) == tree
        return 0
    end
    vd = findfirst(tree .<= trees)
    if vd === nothing
        return length(trees)
    end
    return vd
end

println(solution("input_files/day08_hgp.txt", part=1)) # 6.3 ms
println(solution("input_files/day08_hgp.txt", part=2)) # 13 ms