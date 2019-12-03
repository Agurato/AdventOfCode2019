use std::fs::File;
use std::io::prelude::*;

/*
    From instructions, construct a list of segments belonging to
    wire1 and wire2, then check for collisions between every segment.
*/
pub fn fetch_input(path: &str) -> Result<Vec<Vec<(i32, i32)>>, &'static str> {
    let mut file = match File::open(path) {
        Err(_) => return Err("Error with filepath"),
        Ok(f) => f,
    };

    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("failed to read string");

    let wires: Vec<Vec<&str>> = contents
        .split("\n")
        .map(|x| x.split(",").collect())
        .collect();

    let mut wire_segment_lists: Vec<Vec<(i32, i32)>> = Vec::new();
    let mut tmp;
    for wire in &wires {
        tmp = wire
            .iter()
            .map(|x| {
                let value = x[1..].parse::<i32>().expect("Could not parse integer");
                return match x.chars().nth(0) {
                    Some('U') => (0, value),
                    Some('D') => (0, -value),
                    Some('L') => (value, 0),
                    Some('R') => (-value, 0),
                    _ => panic!("unrecognized direction"),
                };
            })
            .collect();
        wire_segment_lists.push(tmp);
    }
    println!("{:?}", wire_segment_lists[0]);
    println!("{:?}", wire_segment_lists[1]);
    Ok(wire_segment_lists)
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_1() {
        let wire1 = ["R8", "U5", "L5", "D3"];
        fetch_input("res/3.txt");
        assert_eq!(wire1[0], "R8");
    }
}
