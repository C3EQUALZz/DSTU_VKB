use clap::Parser;
use color_eyre::Result;

use lab_07_asym::presentation::{Cli, run};

fn main() -> Result<()> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
