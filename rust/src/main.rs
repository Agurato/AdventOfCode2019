mod day1;
mod day2;
mod day3;
mod day4;

fn main() {
    let items_1 = day1::fetch_input("res/1.txt").expect("Could not open file");
    println!("Step 1a: {}", day1::step_1a(&items_1));
    println!("Step 1b: {}", day1::step_1b(&items_1));

    let mut items_2 = day2::fetch_input("res/2.txt").expect("Could not open file");
    items_2[1] = 12;
    items_2[2] = 2;
    println!("Step 2a: {}", day2::step_2a(&mut items_2));
    items_2 = day2::fetch_input("res/2.txt").expect("Could not open file");
    println!("Step 2b: {}", day2::step_2b(&mut items_2).expect("oops"));

    let items_3 = day3::fetch_input("res/3.txt").expect("Could not open file");
    println!("Step 3a: {}", day3::step_3a(&items_3));

    let items_4 = (172851, 675869);
    println!("Step 4a: {}", day4::step_4a(items_4.0, items_4.1));
}
