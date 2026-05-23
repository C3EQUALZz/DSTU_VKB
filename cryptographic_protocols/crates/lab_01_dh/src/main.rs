use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_01_dh::presentation::cli::run()
}
