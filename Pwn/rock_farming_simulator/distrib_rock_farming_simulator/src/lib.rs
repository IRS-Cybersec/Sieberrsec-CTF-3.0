#![feature(linked_list_cursors)]
use std::collections::{LinkedList,HashMap};
use std::sync::{Arc,Mutex};
use std::thread;
use std::thread::JoinHandle;
use std::time::Duration;
use std::mem::drop;
use std::process::Command;
use rand::Rng;
macro_rules! sleep_seconds { ($s:expr) => (thread::sleep(Duration::from_secs($s))) }

/// A single worker
pub struct Slave {
    pub name: String,
    income: u32,
    expiry: u32,
    value: u32,
    owned: bool
}
/// This is what you see when pressing S or B
impl ToString for Slave {
    fn to_string(&self) -> String {
        let mut s = format!("{} provides ${}/day, ", self.name, self.income);
        // note: do not show expiry date while unpurchased
        if self.owned { s.push_str(&format!("and will move on to the Elysium Fields after {} days.", self.expiry)); }
        else { s.push_str(&format!("and costs ${} to hire.", self.value)); }
        s
    }
}
/// Give the stats of each slave a little bit of randomness
impl Slave {
    pub fn new(name: String, income: i32, expiry: i32) -> Slave {
        let mut rng = rand::thread_rng();
        let income = (income+rng.gen_range(-2..=2)).max(1) as u32;
        let expiry = (expiry+rng.gen_range(-5..=10)).max(1) as u32;
        let value = ((income*expiry) as i32 + rng.gen_range(-70..-30)).max(10) as u32;
        Slave { name, income, expiry, value, owned: false }
    }
}

#[allow(dead_code)]
/// game internals
pub struct Game {
    state: Arc<Mutex<GameState>>,
    runtime: JoinHandle<()>,
    pub market: Vec<Slave> // this is a hack: main.rs needs access to this
}
/// stuff to keep on the mutex for multithreading purposes
struct GameState {
    money: u32,
    slaves: LinkedList<Slave>,
    graveyard: Vec<Slave>,
}
/// This is what you see at the top of the game UI
impl GameState {
    pub fn summary(&self) -> HashMap<String,u32> {
        let mut summary = HashMap::new();
        summary.insert("money".to_string(), self.money);
        summary.insert("slaves".to_string(), self.slaves.len() as u32);
        summary.insert("income".to_string(), self.slaves.iter().fold(0, |total,slave| total + slave.income));
        summary
    }
}
/// Various functions to run the game
impl Game {
    /// Creating a new game spawns a thread to tick forward game-time. Each tick runs callback().
    pub fn new(callback: impl Fn(HashMap<String,u32>) + std::marker::Send + 'static) -> Game {
        let state = Arc::new(Mutex::new(GameState {
                money: 0,
                slaves: LinkedList::new(),
                graveyard: Vec::new()
            }));
        let state_clone = Arc::clone(&state);
        Game { // the runtime attribute keeps the slaves working
            state, runtime: thread::spawn(move || {
                loop { // I would replace this with a time limit, but the docker container has a timeout anyway
                    let mut state = state_clone.lock().unwrap();

                    // run through slaves to figure out how much money to add
                    let mut cur = state.slaves.cursor_front_mut();
                    let mut add = 0;
                    let mut graveyard = vec![]; // i'd like to use state.graveyard directly, but borrow checker can't disambiguate between mutable references on different attributes of a struct and yada yada you don't really need to know this part to solve the challenge
                    while let Some(mut slave) = cur.current() {
                        if slave.expiry == 0 { // if one of them dies
                            if let Some(s) = cur.remove_current() {
                                graveyard.push(s);
                            }
                        } else {
                            slave.expiry -= 1;
                            add += slave.income;
                            cur.move_next();
                        }
                    }
                    state.money += add;
                    state.graveyard.append(&mut graveyard);

                    callback(state.summary()); // to dynamically update the UI
                    drop(state); // drop the lock for other usage
                    sleep_seconds!(1);
                }
            }),
            market: vec![ // hardcoded list of slaves; I'm kinda lazy
                Slave::new("Murky".to_string(), 0, 5),
                Slave::new("Cute Filly".to_string(), 2, 10),
                Slave::new("Troubleshoes".to_string(), 5, 50),
                Slave::new("Diana Pie".to_string(), 7, 40),
                Slave::new("Prissy Unicorn".to_string(), 2, 70),
            ]
        }
    }
    /// Create a thread to add a slave to the player's farm after a few seconds.
    pub fn add_slave(&self, mut slave: Slave) -> Result<(u64,JoinHandle<()>), Slave> {
        let state = self.state.lock().unwrap();
        if state.money < slave.value {
            Err(slave)
        } else { // simulate a transaction, taking between 0-1 days
            drop(state); // release this to let time pass in the runtime loop
            let state_clone = Arc::clone(&self.state);
            let duration = rand::thread_rng().gen_range(0..=1);
            Ok((duration, thread::spawn(move || {
                sleep_seconds!(duration);
                let mut state = state_clone.lock().unwrap();
                state.money -= slave.value;
                slave.owned = true;
                state.slaves.push_back(slave);
            })))
        }
    }
    /// This is what you want to succeed in for this challenge :)
    pub fn get_flag(&self) -> Option<String> {
        let state = self.state.lock().unwrap();
        if state.money < 10_10_2010_08 { None } 
        else {
            let res = Command::new("cat").arg("flag").output().unwrap();
            Some(if res.status.success() {
                String::from_utf8_lossy(&res.stdout).to_string()
            } else {
                format!("Something went wrong; please contact the CTF admins: {}",
                String::from_utf8_lossy(&res.stderr))
            })
        }
    }
    /// Manually increase money; 1/5 chance of getting nothing
    pub fn toss_rocks(&self) -> u32 {
        let income = rand::thread_rng().gen_range(0..50);
        let income = if income < 10 { 0 } else { income };
        let mut state = self.state.lock().unwrap();
        state.money += income;
        income
    }
    /// Wrapper over GameState.summary()
    pub fn summary(&self) -> HashMap<String,u32> {
        let state = self.state.lock().unwrap();
        state.summary()
    }
}
impl ToString for Game { // this is what shows up when you press S
    fn to_string(&self) -> String {
        let state = self.state.lock().unwrap();
        let mut s = String::from("===Ponies===\n");
        if state.slaves.is_empty() {
            s += "You have no ponies in your farm right now :(\n";
        } else {
            for slave in state.slaves.iter() {
                s += &slave.to_string();
                s += "\n";
            }
        }
        s += "\n";
        if !state.graveyard.is_empty() {
            s += "These ponies used to work with you, but have moved on to greener pastures:\n";
            for body in state.graveyard.iter() {
                s += &format!(" - {}\n", body.name);
            }
            s += "\n";
        }
        s += "===Items===\n";
        s += &format!("Money: ${}", state.money);
        s
    }
}
