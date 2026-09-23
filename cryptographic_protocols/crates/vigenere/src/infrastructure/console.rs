use std::io::{self, Write};

use crate::application::Output;

pub struct Console;

impl Output for Console {
    fn write(&mut self, text: &str) -> io::Result<()> {
        writeln!(io::stdout().lock(), "{text}")
    }
}
