use clap::Parser;
use color_eyre::Result;
use practice_02::presentation::{Cli, run};

fn main() -> Result<()> {
    shared::logging::init()?;
    run(Cli::parse())
}
