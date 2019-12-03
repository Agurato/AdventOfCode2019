use std::fs::File;
use std::io::prelude::*;
use std::ops::Range;
/*
    From instructions, construct a list of segments belonging to
    wire1 and wire2, then check for collisions between every segment.
*/
#[derive(Copy, Debug, Clone)]
pub struct Point {
    x: i32,
    y: i32,
}

#[derive(Copy, Debug, Clone)]
pub struct Segment {
    start: Point,
    stop: Point,
}

impl std::ops::Add for Point {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Segment {
    fn vert(self) -> bool {
        self.start.x == self.stop.x
    }

    fn horiz(self) -> bool {
        !self.vert()
    }

    fn intersection(self, other: Self) -> Option<Point> {
        // println!("Intersecting {:?} with {:?}", self, other);
        //segment vertical
        if self.vert() && other.horiz() {
            println!("Vertical: {} {}", other.start.x, other.stop.x);
            let bounds_1 = (Range{start: other.start.y, end:other.stop.y}).contains(&self.start.y);
            let bounds_2 = (Range{start: self.start.x, end:self.stop.x}).contains(&other.start.x);
            println!("{}{}", bounds_1, bounds_2);
            if bounds_1 && bounds_2 {
                return Some(Point{x: other.start.x, y: self.start.y});
            }
        }

        //segment horizontal
        if self.horiz() && other.vert() {
            println!("Horizontal: {} {}", other.start.x, other.stop.x);
            let bounds_1 = (Range{start: other.start.x, end:other.stop.x}).contains(&self.start.x);
            let bounds_2 = (Range{start: self.start.y, end:self.stop.y}).contains(&other.start.y);
            if bounds_1 && bounds_2 {
                return Some(Point{x: self.start.x, y: other.start.y});
            }
        } 
        None
    }
}

pub fn fetch_input(path: &str) -> Result<Vec<Vec<String>>, &'static str> {
    let mut file = match File::open(path) {
        Err(_) => return Err("Error with filepath"),
        Ok(f) => f,
    };

    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("failed to read string");

    let wires: Vec<Vec<String>> = contents
        .split("\n")
        .map(|x| x.split(",").map(|s| s.to_string()).collect())
        .collect();

    Ok(wires)
}

pub fn get_segments(wires: Vec<Vec<String>>) -> Result<Vec<Vec<Segment>>, &'static str> {
    let mut wire_displacements: Vec<Vec<Point>> = Vec::new();

    // Transform U30 into (0, 30)
    for wire in &wires {
        wire_displacements.push(
            wire.iter()
                .map(|x| {
                    let value = x[1..].parse::<i32>().expect("Could not parse integer");
                    return match x.chars().nth(0) {
                        Some('U') => Point { x: 0, y: value },
                        Some('D') => Point { x: 0, y: -value },
                        Some('L') => Point { x: value, y: 0 },
                        Some('R') => Point { x: -value, y: 0 },
                        _ => panic!("unrecognized direction"),
                    };
                })
                .collect(),
        );
    }

    let mut wire_segments: Vec<Vec<Segment>> = vec![Vec::new(); wire_displacements.len()];
    let mut carry;

    for (wire_displacement, wire_segment) in wire_displacements.iter().zip(wire_segments.iter_mut())
    {
        carry = Point { x: 0, y: 0 };
        for displacement in wire_displacement {
            wire_segment.push(Segment {
                start: carry,
                stop: carry + *displacement,
            });
            carry = carry + *displacement;
        }
    }
    Ok(wire_segments)
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_1() {
        let wires: Vec<Vec<String>> = vec![
            vec![
                "R8".to_string(),
                "U5".to_string(),
                "L5".to_string(),
                "D3".to_string(),
            ],
            vec![
                "U7".to_string(),
                "R6".to_string(),
                "D4".to_string(),
                "L4".to_string(),
            ],
        ];
        // fetch_input("res/3.txt");
        // println!("{:?}", get_segments(wires));
        let segments = get_segments(wires).expect("Error getting segments");
        for segment in &segments[0] {
            for segment_2 in &segments[1] {
                println!("{:?}", segment.intersection(*segment_2));
            }
        }
        // assert_eq!(wire1[0], "R8");
    }
}
