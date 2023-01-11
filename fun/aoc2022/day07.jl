function solution(ifile; part)
    if part == 1
        filesystem = read_filesystem(ifile)
        dirs = get_dirs(filesystem)
        s = 0
        for dir ∈ dirs
            ds = dir_size(dir, filesystem)
            if ds ≤ 100000
                s += ds
            end
        end
        return s
    end
end

function read_filesystem(ifile)
    filesystem = Dict{String, Int64}()
    dir = "/"
    open(ifile, "r") do f
        # d = open("debug.txt", "w")
        line = readline(f)
        while !eof(f)
            # write(d, "Current dir: $dir\n")
            if line == "\$ cd .."
                # write(d, "Moving to parent directory.\n")
                dir = move_to_parent(dir)
                line = readline(f)
            elseif line[1:4] == "\$ cd"
                # write(d, "Moving to ", line[6:end], ".\n")
                dir = move_to(line[6:end], dir)
                line = readline(f)
            elseif line == "\$ ls"
                # write(d, "Listing directory contents.\n")
                while !eof(f)
                    line = readline(f)
                    if line[1] == '$'
                        break
                    elseif line[1:3] != "dir"
                        fsize, fname = get_file_info(line) 
                        # write(d, "Adding $fname.\n")
                        filesystem[string(dir, fname)] = fsize
                    end
                end
            end
        end
        # close(d)
    end
    return filesystem
end

function get_file_info(line)
    i = 1
    while line[i] != ' '
        i += 1
    end
    return parse(Int64, line[1:i-1]), line[i+1:end]
end

function move_to(new_dir, working_dir)
    if new_dir == "/"
        return new_dir
    else
        return string(working_dir, new_dir, "/")
    end
end

function move_to_parent(dir)
    if dir == "/"
        return dir
    end
    i = length(dir) - 1
    while dir[i] != '/'
        i -= 1
    end
    return dir[1:i]
end

function get_dirs(filesystem)
    return unique(base_dir(filename) for filename ∈ keys(filesystem))
end

function base_dir(filename)
    i = length(filename)
    while filename[i] != '/'
        i -= 1
    end
    return filename[1:i]
end
        
function dir_size(dir, filesystem)
    s = 0
    for filename ∈ keys(filesystem)
        if length(filename) >= length(dir)
            if filename[1:length(dir)] == dir
                s += filesystem[filename]
            end
        end
    end
    return s
end

solution("input_files/day07_hgp.txt", part=1)
# solution("input_files/test.txt", part=1)