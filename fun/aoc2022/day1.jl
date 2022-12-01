function find_top_three(fname)
    calories = tally_elves(fname)
    top_three = sortperm(calories, rev=true)[1:3]
    combined_calories = sum(calories[top_three])
    println("Elfs $top_three are the big bois; they have $combined_calories Calories of food.")
end

function find_big_boi_elf(fname)
    calories = tally_elves(fname)
    big_boi_elf = argmax(calories)
    bigness = maximum(calories)
    println("Elf #$big_boi_elf is the big boi; he has $bigness Calories of food.")
end

function tally_elves(fname)
    n = num_elves(fname)
    calories = zeros(n)
    i = 1
    for line in eachline(fname)
        if line != ""
            calories[i] += parse(Int64, line)
        else
            i += 1
        end
    end
    return calories
end

function num_elves(fname)
    n = 0
    for line in eachline(fname)
        if line == ""
            n += 1
        end
    end
    return n + 1
end

fname = "input_files/day1_hgp.txt"
find_big_boi_elf(fname)
find_top_three(fname)