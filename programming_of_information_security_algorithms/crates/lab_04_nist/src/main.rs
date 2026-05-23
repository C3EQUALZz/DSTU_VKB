use std::process::ExitCode;

use clap::Parser;
use color_eyre::Result;

use lab_04_nist::presentation::{Cli, run};

fn main() -> Result<ExitCode> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
