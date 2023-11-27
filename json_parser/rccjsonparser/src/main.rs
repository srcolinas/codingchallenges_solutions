use std::fs;
use std::process::ExitCode;

use clap::Parser;

#[derive(Parser)]
struct Cli {
    #[arg(value_name = "FILE")]
    file: std::path::PathBuf,
}

fn main() -> ExitCode {
    let args = Cli::parse();
    match fs::read_to_string(args.file) {
        Ok(source) => match rccjsonparser::parse(&source) {
            Ok(_) => ExitCode::from(0),
            Err(_) => ExitCode::from(2),
        },
        Err(_) => ExitCode::from(1),
    }
}
