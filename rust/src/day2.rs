use itertools::Itertools;
use std::fs::File;
use std::io::prelude::*;

pub fn fetch_input(path: &str) -> Result<Vec<i32>, &'static str> {
    let mut file = match File::open(path) {
        Err(_) => return Err("Error with filepath"),
        Ok(f) => f,
    };

    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("failed to read string");
    let commands: Vec<i32> = contents
        .split(",")
        .map(|x| x.parse::<i32>().expect("One value is incorrect"))
        .collect();
    Ok(commands)
}

pub fn step_2a(items: &mut Vec<i32>) -> i32 {
    let mut ptr = 0;
    let mut result_pos: usize;

    loop {
        let result = match items[ptr] {
            1 => Some(items[items[ptr + 1] as usize] + items[items[ptr + 2] as usize]),
            2 => Some(items[items[ptr + 1] as usize] * items[items[ptr + 2] as usize]),
            99 => None,
            _ => panic!("unexpected opcode"),
        };
        match result {
            Some(r) => {
                result_pos = items[ptr + 3] as usize;
                items[result_pos] = r;
            }
            None => return items[0],
        };
        ptr += 4;
    }
}

pub fn step_2b(items: &Vec<i32>) -> Option<i32> {
    let mut mem: Vec<i32>;
    let combinaisons: Vec<(i32, i32)> = (0..99).cartesian_product(0..99).collect();
    for (noun, verb) in combinaisons {
        mem = items.to_vec();
        mem[1] = noun;
        mem[2] = verb;

        if step_2a(&mut mem) == 19690720 {
            return Some(100 * noun + verb);
        }
    }
    None
}
