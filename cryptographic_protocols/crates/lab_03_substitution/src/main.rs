use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_03_substitution::presentation::cli::run()
}
