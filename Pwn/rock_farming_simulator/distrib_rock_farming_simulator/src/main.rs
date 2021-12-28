/** Basic idea: some kind of cookie-clicker like game,
  * where the state is incremented by a thread looping on sleep(1).
  * The bug will be due to a [REDACTED] in lib.rs, I think.
  * And of course the theme is enslaving ponies to mine rocks.
  */
use std::collections::HashMap;
use pancurses::{initscr, endwin, Window, Input, noecho, chtype};
use std::thread;
use std::time::Duration;
use std::sync::mpsc;
use std::thread::JoinHandle;
use rockfarming_simulator::*;
use crate::Cmd::*;

/// Helper functions for UI
macro_rules! sleep_ms { ($s:expr) => (thread::sleep(Duration::from_millis($s))) }
fn draw_window(window: &Window, info: HashMap<String,u32>) {
    let (y,x) = window.get_cur_yx();
    window.draw_box('|', '-');
    window.mv(1, 2);
    window.addstr(&format!(" Wallet: ${}", info["money"]));
    if info["income"] != 0 { window.addstr(&format!(" (+${}/day)", info["income"])); }
    if info["slaves"] != 0 { window.addstr(&format!(" -- ponies helping you: {}", info["slaves"])); }
    window.addstr(" |");
    let end = window.get_cur_x();
    window.addstr("                                      "); // amazing hacks
    window.mv(2,1);
    window.hline('-', end-2);
    window.mvaddch(2, end-1, '/');
    window.addstr("                                      "); // amazing hacks
    window.mv(y,x);
    window.refresh();
}
fn println_relative(window: &Window, s: &str) {
    let (y,x) = window.get_cur_yx();
    window.addstr(s);
    window.mv(y+1, x);
    window.refresh();
}
fn press_any_key(window: &Window) {
    window.mv(window.get_cur_y() + 2, 5);
    sleep_ms!(500);
    println_relative(window, "[Press any key to return]");
    window.getch();
}

/** `Screen` is an mpsc wrapper around pancurses::Window. I made it as a workaround to get a
  * multithreaded ncurses UI; you can ignore its internals for the purposes of this challenge. */
struct Screen {
    runtime: JoinHandle<()>,
    pub tx: mpsc::Sender<Vec<Cmd>>,
    recv_char: mpsc::Receiver<Input>,
    recv_pos: mpsc::Receiver<(i32,i32)>,
}
/// I only need a small subset of the pancurses API; Cmd represents the actions I need.
enum Cmd {
    Chgat(i32, chtype, i16),
    Println(String),
    Move(i32,i32),
    Update(HashMap<String,u32>),
    PressAnyKey,
    Getch,
    Clear,
    Quit,
    Pos
}
/// A mess of enums, pipes, syntactic sugar, held together by a thread.
impl Screen {
    fn new() -> Screen {
        let (tx,rx) = mpsc::channel();
        let (send_char, recv_char) = mpsc::channel();
        let (send_pos, recv_pos) = mpsc::channel();
        /* The pancurses window is stored inside the closure `Screen.runtime`. mpsc pipes
         * are used to modify the state of the window && to return information from it.*/
        Screen {
            runtime: thread::spawn(move || {
                let window = initscr();
                window.keypad(true);
                window.nodelay(false);
                noecho();
                while let Ok(cmds) = rx.recv() {
                    let mut cont = true;
                    for cmd in cmds {
                        match cmd {
                            Chgat(n, ch, attr) => {window.chgat(n, ch, attr);},
                            Pos => {send_pos.send(window.get_cur_yx()).unwrap();},
                            // minor bug: PressAnyKey will lock the UI. Not really relevant.
                            PressAnyKey => press_any_key(&window),
                            Println(s) => println_relative(&window, &s),
                            Move(y,x) => {window.mv(y,x);},
                            Update(info) => draw_window(&window, info),
                            Getch => {send_char.send(window.getch().unwrap()).unwrap();},
                            Clear => {window.clear();},
                            Quit => cont = false
                        }
                    }
                    if !cont { break; }
                }
                window.delwin();
                endwin();
            }), tx, recv_char, recv_pos }
    }
    fn send(&self, cmds: Vec<Cmd>) {
        self.tx.send(cmds).unwrap();
    }
    fn pos(&self) -> (i32,i32) {
        self.send(vec![Pos]);
        self.recv_pos.recv().unwrap()
    }
    fn getch(&self) -> Input {
        self.send(vec![Getch]);
        self.recv_char.recv().unwrap()
    }
    fn mv(&self, y: i32, x: i32) {
        self.send(vec![Move(y,x)]);
    }
    fn clear(&self, info: HashMap<String,u32>) {
        self.send(vec![Clear, Move(4,3), Update(info)]);
    }
    fn puts(&self, s: String) {
        self.send(vec![Println(s)]);
    }
    fn kill(self) {
        self.tx.send(vec![Quit]).unwrap();
        self.runtime.join().unwrap();
    }
}

/// class representing the selectable menus in the UI
struct Menu<'a> {
    items: &'a [String], // use a slice instead of a Vec to force the list to be immutable. (unless the caller chooses to clone it anyway)
}
impl Menu <'_> {
    fn new(items: &[String]) -> Menu {
        Menu { items }
    }
    fn get_opt(&self, screen: &Screen) -> usize {
        let (y,x) = screen.pos();
        let mut shortcuts = HashMap::<char,usize>::new();
        for (i, item) in self.items.iter().enumerate() {
            // fill up shortcuts
            let c = item.chars().next().unwrap();
            shortcuts.insert(c.to_lowercase().next().unwrap(), i);
            shortcuts.insert(c.to_uppercase().next().unwrap(), i);
            // display the menu
            let i = i as i32;
            screen.send(vec![Move(y+i,x),
                Println(format!(" - {}", item)),
                Move(y+i,x+3),
                Chgat(1,pancurses::A_UNDERLINE,0)
            ]);
        }
        let mut selected = 0i32; // we're returning this
        loop {
            selected = selected.rem_euclid(self.items.len() as i32); // python's modulo
            for i in 0..self.items.len() {
                let i = i as i32;
                screen.send(vec![Move(y+i,x+4),
                    Chgat(-1, if i == selected { pancurses::A_REVERSE } else { pancurses::A_NORMAL },0)
                ]);
            }
            screen.mv(y+selected, x+1);
            match screen.getch() {
                Input::KeyUp => selected -= 1, // note that this is an intentional underflow!
                Input::KeyDown => selected += 1,
                Input::Character(c) => {
                    if let Some(i) = shortcuts.get(&c) { break *i; }
                    else if c == '\n' { break selected as usize; }
                }
                _ => ()
            }
        }
    }
}

/// Main UI loop
fn main () {
    let screen = Screen::new();
    let screen_tx = screen.tx.clone();
    let mut game = Game::new(move |info| screen_tx.send(vec![Update(info)]).unwrap());
    let mut lazy = vec![];

    // some helper macros for i/o
    macro_rules! press_any_key { () => {
        screen.send(vec![PressAnyKey]);
    } }
    macro_rules! print_delay_s { ($s:expr) => {
        screen.puts($s); sleep_ms!(100)
    } }
    macro_rules! print_delay { ($s:expr) => { print_delay_s!($s.to_string()); } }
    macro_rules! clear { () => {
        screen.clear(game.summary());
    } }

    // options for the main menu
    let options = vec![
        String::from("Toss over rocks for cash"),
        String::from("Show the state of your farm"),
        String::from("Buy a pony to assist in rockfarming"),
        String::from("Haggle with the Princesses for a flag"),
        String::from("Quit your career and run off into the Badlands"),
    ];
    let menu = Menu::new(&options);

    // typical incredibly bloated switch-case you can find in any C program
    loop {
        clear!();
        print_delay!("Welcome to the rock farm!");
        print_delay!("Over here, you can do a few things:");
        let opt = menu.get_opt(&screen);
        clear!();
        match opt {
            0 => { // get money
                print_delay!("You scour your surroundings for rocks...");
                let income = game.toss_rocks();
                sleep_ms!(700);
                print_delay_s!(if income > 0 {
                    format!("...and find enough to scrounge up ${}!", income)
                } else { // copilot suggested this one
                    "...but you find nothing. You're a rock-star, aren't you?".to_string()
                });
                press_any_key!();
            }
            1 => { // show the sorrowful state of the farm
                for s in game.to_string().split('\n') { screen.puts(s.to_string()); }
                press_any_key!();
            }
            2 => { // buy pones
                print_delay!("You walk into a stable...");
                if game.market.is_empty() {
                    print_delay!("...but there's nothing to buy!");
                } else {
                    let details = game.market.iter().map(|s| s.to_string()).collect::<Vec<String>>();
                    let listing = Menu::new(&details);
                    let ind = listing.get_opt(&screen);
                    let pony = game.market.swap_remove(ind);
                    screen.mv(details.len() as i32 + 5, 3);
                    match game.add_slave(pony) {
                        Ok((t,job)) => {
                            print_delay!(&format!("Hired! The pony will arrive in {} days.", t));
                            lazy.push(job);
                        }
                        Err(p) => {
                            print_delay!(&format!("You receive a dark glare. You don't have enough money to bring {} home.", &p.name));
                            game.market.push(p);
                        }
                    }
                }
                press_any_key!();
            }
            3 => { // !! get the flag !!
                print_delay!("The Princess says...");
                let res = game.get_flag();
                sleep_ms!(2000);
                screen.puts(res.unwrap_or("You have been banished from Equestria.".to_string()));
                press_any_key!();
                screen.kill();
                break
            }
            _ => { // quit
                screen.kill();
                break
            }
        }
    }
}
