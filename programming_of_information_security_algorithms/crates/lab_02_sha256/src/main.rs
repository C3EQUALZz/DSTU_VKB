use std::process::ExitCode;

use clap::Parser;
use color_eyre::Result;

use lab_02_sha256::presentation::{Cli, run};

fn main() -> Result<ExitCode> {
    shared::logging::init()?;
    let cli = Cli::parse();
    run(cli)
}
