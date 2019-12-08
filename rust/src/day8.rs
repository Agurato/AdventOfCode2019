use std::fs::File;
use std::io::prelude::*;

#[derive(Debug)]
struct Image {
    width: i32,
    height: i32,
    layers: Vec<Vec<i32>>,
}

impl Image {
    pub fn new(width: i32, height: i32, data: &Vec<i32>) -> Image {
        let layer_size: usize = (width * height) as usize;
        let mut layers = Vec::new();
        for chunk in data.chunks(layer_size) {
            layers.push(Vec::from(chunk));
        }

        Image {
            width: width,
            height: height,
            layers: layers,
        }
    }
}

pub fn fetch_input(path: &str) -> Result<Vec<i32>, &'static str> {
    let mut file = match File::open(path) {
        Err(_) => return Err("Error with filepath"),
        Ok(f) => f,
    };

    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("failed to read string");
    let commands: Vec<i32> = contents
        .chars()
        .map(|x| x.to_digit(10).expect("One value is incorrect") as i32)
        .collect();
    Ok(commands)
}

fn step_8a(image: Image) -> usize {

    let mut fewest_zero_digits = std::usize::MAX;
    let mut zero_digits: usize;
    let mut fewest_zero_digits_layer = &image.layers[0];

    for layer in &image.layers {

        zero_digits = layer.iter().filter(|x| **x == 0).count();
        if zero_digits < fewest_zero_digits {
            fewest_zero_digits = zero_digits;
            fewest_zero_digits_layer = &layer;
        }
    }

    fewest_zero_digits_layer.iter().filter(|x| **x == 1).count()
        * fewest_zero_digits_layer.iter().filter(|x| **x == 2).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_input() {
        fetch_input("res/8.txt");
    }

    #[test]
    fn test_step() {
        let img_data = fetch_input("res/8.txt").expect("Failed to load data");
        let (w, h) = (25, 6);
        let img = Image::new(w, h, &img_data);
        println!("{}", step_8a(img));
    }
    #[test]
    fn testcase() {
        let img = Image::new(3, 2, &vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]);
        println!("{:?}", img);
        println!("{}", step_8a(img));
    }
}
