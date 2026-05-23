use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_05_xor::presentation::cli::run()
}
