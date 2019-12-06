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

pub fn step_5a(items: &mut Vec<i32>, input: i32) {
    let mut ip = 0;

    loop {
        let op: String = format!("{:05}", items[ip]);
        let opcode = &op[3..];
        let params = op[..3].chars().rev();

        let mut addrs: Vec<usize> = Vec::with_capacity(3);

        if ip < items.len() - 1 {
            for (param, offset) in params.zip(1..4) {
                match param {
                    '0' => addrs.push(items[ip + offset] as usize), //position mode: the number corresponds to the address of the value
                    '1' => addrs.push(ip + offset as usize), //immediate mode: the number corresponds to itself. We provide the address of the number.
                    _ => panic!("unknown mode"),
                }
            }
        }

        let (result, ip_jump): (Option<i32>, usize) = match opcode {
            "01" => {
                items[addrs[2]] = items[addrs[0]] + items[addrs[1]];
                (None, 4)
            }
            "02" => {
                items[addrs[2]] = items[addrs[0]] * items[addrs[1]];
                (None, 4)
            }
            "03" => {
                items[addrs[0]] = input;
                (None, 2)
            }
            "04" => (Some(items[addrs[0]]), 2),
            "99" => (None, 0),
            _ => panic!("invalid opcode {}", op),
        };

        if (result, ip_jump) == (None, 0) {
            println!("DONE.");
            return ();
        }

        match result {
            Some(r) => println!("OUTPUT: {}", r),
            None => (),
        };

        ip += ip_jump;
    }
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_5a() {
        let mut program = vec![1002, 4, 3, 4, 33];
        let input = 3;
        step_5a(&mut program, input);

        assert!(program[4] == 99);
    }
}
