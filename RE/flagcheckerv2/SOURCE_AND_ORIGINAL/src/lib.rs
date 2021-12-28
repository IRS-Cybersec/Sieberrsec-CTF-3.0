mod utils;

use wasm_bindgen::prelude::*;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
pub fn check_flag(flag: &str) -> bool {
    let mut it = flag.chars().rev();
    macro_rules! check_char {
        ($e:expr, $c:expr) => {
            match it.next() {
                Some(c) => if c == $c { $e } else { false },
                None => false
            }
        };
    }
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(
    check_char!(true,
    'I'),
    'R'),
    'S'),
    '{'),
    'i'),
    'f'),
    '_'),
    'o'),
    'n'),
    'l'),
    'y'),
    '_'),
    'i'),
    't'),
    '_'),
    'w'),
    'a'),
    's'),
    '_'),
    'a'),
    'l'),
    'l'),
    '_'),
    't'),
    'h'),
    'i'),
    's'),
    '_'),
    's'),
    'i'),
    'm'),
    'p'),
    'l'),
    'e'),
    '}')
}
