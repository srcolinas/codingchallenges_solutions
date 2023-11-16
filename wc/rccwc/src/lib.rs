use std::io;

#[derive(PartialEq, Debug)]
pub struct FileCounts {
    chars: usize,
    lines: usize,
    words: usize,
    bytes: usize,
}

pub fn process_lines(lines: impl Iterator<Item = Result<String, io::Error>>) -> FileCounts {
    let mut counts = FileCounts {
        chars: 0,
        lines: 0,
        words: 0,
        bytes: 0,
    };

    for line_result in lines {
        match line_result {
            Ok(line) => {
                if !line.is_empty() {
                    counts.lines += 1;
                }
                counts.bytes += line.len();
                counts.words += line.split_whitespace().count();
                counts.chars += line.chars().count();
            }
            Err(e) => eprint!("Error reading line {}", e),
        }
    }
    counts
}

pub fn format_counts(
    counts: &FileCounts,
    add_chars: bool,
    add_lines: bool,
    add_words: bool,
    add_bytes: bool,
    filename: &str,
) -> String {
    let mut result = String::from("\t");
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

    result.push_str(" ");
    result.push_str(filename);
    result
}

#[cfg(test)]
mod tests_process_lines {
    use super::*;

    #[test]
    fn lines() {
        let expected = String::from("\t 0 ");
        assert_eq!(
            expected,
            format_counts(
                &FileCounts {
                    chars: 0,
                    lines: 0,
                    words: 0,
                    bytes: 0,
                },
                true,
                false,
                false,
                false,
                ""
            )
        );
    }
}

#[cfg(test)]
mod tests_format_counts {
    use super::*;

    #[test]
    fn emtpy_file() {
        let lines = vec![Result::Ok(String::from(""))];
        let expected = FileCounts {
            chars: 0,
            lines: 0,
            words: 0,
            bytes: 0,
        };
        assert_eq!(expected, process_lines(lines.into_iter()));
    }

    #[test]
    fn arbitrary_file() {
        let lines = vec![
            Ok(String::from("Hi there!")),
            Ok(String::from("桜の花abc")),
            Ok(String::from("\x01\x02")),
        ];
        let expected = FileCounts {
            chars: 17,
            lines: 3,
            words: 4,
            bytes: 23,
        };
        assert_eq!(expected, process_lines(lines.into_iter()));
    }
}
