use std::ops::Range;

fn has_two_same_digits(input: &String) -> bool {
    for c in input.chars().collect::<Vec<char>>().windows(2) {
        if c[0] == c[1] {
            return true;
        }
    }
    false
}

fn valid(input: &String) -> bool {
    let clause1 = input.chars().count() == 6;
    let clause3 = has_two_same_digits(&input);
    let clause4 = {
        let mut sorted = input.chars().collect::<Vec<char>>();
        sorted.sort();

        sorted == input.chars().collect::<Vec<char>>()
    };

    clause1 && clause3 && clause4
}

pub fn step_4a(min: i32, max: i32) -> usize {
    Range {
        start: min,
        end: max,
    }
    .into_iter()
    .map(|i| valid(&i.to_string()))
    .filter(|i| *i)
    .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid() {
        let testcases = vec![
            "333333".to_string(),
            "223450".to_string(),
            "123789".to_string(),
        ];
        let results = vec![true, false, false];
        for (testcase, result) in testcases.iter().zip(results) {
            assert!(valid(&testcase) == result, "code {} is invalid", &testcase);
        }
    }
}
