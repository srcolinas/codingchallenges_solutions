import itertools

from src import huffman


def create_payload(source: str, table: dict[str, str]) -> bytes:
    def bits():
        for character in source:
            code = table[character]
            for bit in code:
                yield bit

    def bit_groups():
        group = ""
        for bit in bits():
            group += bit
            if len(group) == 8:
                yield group
                group = ""
        yield "1" + group

    def bytes_():
        for group in bit_groups():
            yield int(group, 2).to_bytes(1, signed=False)

    all_bytes = list(bytes_())
    last = all_bytes.pop()
    payload = last + b"".join(all_bytes)
    return payload


def restore_payload(payload: bytes, tree: huffman.HuffmanTree) -> str:
    def generate_bits():
        iterator = iter(payload)
        last = next(iterator)
        for p in iterator:
            code = bin(p)[2:]
            code = code.rjust(8, "0")
            for c in code:
                yield c

        code = bin(last)[3:]  # ignore 0b and first bit
        yield from code

    root, content = tree, []
    for direction in generate_bits():
        if root.children is not None:
            left, right = root.children
            if direction == "0":
                root = left
            else:
                root = right
        if root.key is not None:
            content.append(root.key)
            root = tree
    return "".join(content)


def create_header(frequencies: dict[str, int]) -> bytes:
    result = b""
    for k, v in frequencies.items():
        key = k.encode("utf-8")
        value = v.to_bytes((v.bit_length() - 1) // 8 + 1, signed=False)
        result += key + b"-" + value + b","
    result = result.removesuffix(b",")
    result += b"\n**\n"
    return result


def restore_frequencies(header: bytes) -> dict[str, int]:
    result: dict[str, int] = {}
    buffer: list[int] = []
    for c in header:
        if c == 45 and buffer:
            key_bytes = bytes(buffer)
            key = key_bytes.decode("utf-8")
            buffer = []
            continue
        if c == 44 and buffer:
            result[key] = int.from_bytes(buffer, signed=False)
            buffer = []
            continue
        buffer.append(c)
    result[key] = int.from_bytes(buffer, signed=False)
    return result
