use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::io::BufReader;

use clap::Parser;

#[derive(Parser)]
struct Cli {
    #[arg(value_name = "FILE")]
    file: Option<std::path::PathBuf>,

    #[arg(short = 'c', long = "bytes")]
    count_bytes: bool,

    #[arg(short = 'l', long = "lines")]
    count_lines: bool,

    #[arg(short = 'w', long = "words")]
    count_words: bool,

    #[arg(short = 'm', long = "chars")]
    count_chars: bool,
}

fn main() {
    let args = Cli::parse();

    match args.file {
        None => {
            let lines = BufReader::new(io::stdin()).lines();
            let counts = process_lines(lines);
            let result = format_counts(
                &counts,
                args.count_chars,
                args.count_lines,
                args.count_words,
                args.count_bytes,
                "",
            );
            println!("{}", result);
        }
        Some(value) => {
            let filename = value.to_string_lossy().to_string();
            let lines = match File::open(value) {
                Ok(file) => BufReader::new(file).lines(),
                Err(e) => {
                    eprintln!("Error opening file: {}", e);
                    std::process::exit(1);
                }
            };
            let counts = process_lines(lines);
            let result = format_counts(
                &counts,
                args.count_chars,
                args.count_lines,
                args.count_words,
                args.count_bytes,
                &filename,
            );
            println!("{}", result)
        }
    };
}

struct FileCounts {
    chars: usize,
    lines: usize,
    words: usize,
    bytes: usize,
}

fn process_lines(lines: impl Iterator<Item = Result<String, io::Error>>) -> FileCounts {
    let mut counts = FileCounts {
        chars: 0,
        lines: 0,
        words: 0,
        bytes: 0,
    };

    for line_result in lines {
        match line_result {
            Ok(line) => {
                counts.lines += 1;
                counts.bytes += line.len() + 1;
                counts.words += line.split_whitespace().count();
                counts.chars += line.chars().count();
            }
            Err(e) => eprint!("Error reading line {}", e),
        }
    }
    counts
}

fn format_counts(
    counts: &FileCounts,
    add_chars: bool,
    add_lines: bool,
    add_words: bool,
    add_bytes: bool,
    filename: &str,
) -> String {
    let mut result = String::from("  ");
    let default = !add_lines & !add_bytes & !add_chars & !add_words;
    if add_lines | default {
        result.push_str(counts.lines.to_string().as_str());
    }
    if add_words | default {
        result.push_str(" ");
        result.push_str(counts.words.to_string().as_str());
    }
    if add_chars {
        result.push_str(" ");
        result.push_str(counts.chars.to_string().as_str());
    }
    if add_bytes | default {
        result.push_str(" ");
        result.push_str(counts.bytes.to_string().as_str());
    }

    result.push_str(filename);
    result
}
