use clap::Parser;
use color_eyre::Result;

use practice_01::presentation::{cli::Cli, run};

fn main() -> Result<()> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
