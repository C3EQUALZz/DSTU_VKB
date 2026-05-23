use clap::Parser;
use color_eyre::Result;

use lab_03_prng::presentation::{Cli, run};

fn main() -> Result<()> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
