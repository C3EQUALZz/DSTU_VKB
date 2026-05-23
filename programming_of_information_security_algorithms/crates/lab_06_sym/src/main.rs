use clap::Parser;
use color_eyre::Result;

use lab_06_sym::presentation::{Cli, run};

fn main() -> Result<()> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
