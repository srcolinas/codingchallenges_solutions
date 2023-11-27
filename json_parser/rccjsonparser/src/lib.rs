use std::collections::HashMap;

#[derive(PartialEq, Debug)]
pub struct InvalidJson;

#[derive(PartialEq, Debug)]
pub enum Json<'a> {
    Null,
    Bool(bool),
    Number(f64),
    String(&'a str),
    Array(Vec<Json<'a>>),
    Object(HashMap<&'a str, Json<'a>>),
}

pub fn parse(source: &str) -> Result<Json, InvalidJson> {
    if source.starts_with('"') && source.ends_with('"') {
        let value = source.strip_prefix('"').unwrap().strip_suffix('"').unwrap();
        Ok(Json::String(value))
    } else if source == "true" {
        Ok(Json::Bool(true))
    } else if source == "false" {
        Ok(Json::Bool(false))
    } else if source == "null" {
        Ok(Json::Null)
    } else if source.starts_with('{') && source.ends_with('}') {
        parse_object(source)
    } else if source.starts_with('[') && source.ends_with(']') {
        parse_array(source)
    } else {
        match source.parse::<f64>() {
            Err(_) => Err(InvalidJson),
            Ok(value) => Ok(Json::Number(value)),
        }
    }
}

fn parse_object(source: &str) -> Result<Json, InvalidJson> {
    let result = HashMap::new();
    Ok(Json::Object(result))
}

fn parse_array(source: &str) -> Result<Json, InvalidJson> {
    let result = vec![];
    Ok(Json::Array(result))
}

#[cfg(test)]
mod test_parser {
    use super::*;

    #[test]
    fn valid_cases() -> Result<(), InvalidJson> {
        let cases = vec![
            ("{}", Json::Object(HashMap::new())),
            ("[]", Json::Array(vec![])),
            (
                "{\"key\": \"value\"}",
                Json::Object(HashMap::from([("key", Json::String("value"))])),
            ),
        ];
        for (c, r) in cases.iter() {
            let result = parse(c)?;
            assert_eq!(r, &result)
        }
        Ok(())
    }

    #[test]
    fn invalid_cases() {
        let cases = vec!["", "{\"key\": \"value\",}"];
        for c in cases.into_iter() {
            let result = parse(c);
            assert_eq!(result, Err(InvalidJson))
        }
    }
}
