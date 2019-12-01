use std::fs::File;
use std::io::prelude::*;

fn fetch_input(path: &str) -> Result<Vec<i32>, &'static str> {
    let mut file = match File::open(path) {
        Err(_) => return Err("Error with filepath"),
        Ok(f) => f,
    };

    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("failed to read string");
    let commands: Vec<i32> = contents
        .split("\n")
        .map(|x| x.parse::<i32>().expect("One value is incorrect"))
        .collect();
    Ok(commands)
}

fn step_1a(items: &Vec<i32>) -> i32 {
    items.iter().map(|x| (x / 3) - 2).sum()
}

fn step_1b(items: &Vec<i32>) -> i32 {
    let get_fuel_per_module = |mass| {
        let mut supplementary_fuel: i32 = (mass / 3) - 2;
        let mut total_fuel = supplementary_fuel;
        while supplementary_fuel >= 0 {
            supplementary_fuel = (supplementary_fuel / 3) - 2;
            if supplementary_fuel > 0 {
                total_fuel += supplementary_fuel
            }
        }

        total_fuel
    };

    items
        .iter()
        .map(|x| get_fuel_per_module(x))
        .sum()
}

fn main() {
    let items = fetch_input("res/1.txt").expect("Could not open file");
    println!("Step 1: {}", step_1a(&items));
    println!("Step 1b: {}", step_1b(&items));
}
