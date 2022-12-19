function solution(ifile)
    cycle = 0
    X = 1
    signal_strength = 0
    open(ifile, "r") do f
        while !eof(f)
            cmd = split(readline(f))
            cycle += 1
            print_pixel(cycle, X)
            if mod(cycle-19, 40) == 0
                signal_strength += (cycle + 1)*X
            end
            if cmd[1] == "addx"
                cycle += 1
                X += parse(Int64, cmd[2])
                print_pixel(cycle, X)
                if mod(cycle-19, 40) == 0
                    signal_strength += (cycle + 1)*X
                end
            end
        end
    end
    return signal_strength
end

function print_pixel(cycle, X)
    if mod(cycle, 40) ∈ [X-1, X, X+1] 
        print("#")
    else
        print(".")
    end
    if mod(cycle, 40) == 0
        println()
    end
end

println(solution("input_files/day10_hgp.txt")) # 34 μs