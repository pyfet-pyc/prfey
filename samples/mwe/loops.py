def scan_directive_name(self, start_mark):
    # See the specification for details.
    length = 0
    ch = self.peek(length)
    while a or v or d \
            or ch in '-_':
        length += 1
        ch = self.peek(length)
    if not length:
        raise ScannerError("while scanning a directive", start_mark,
                "expected alphabetic or numeric character, but found %r"
                % ch, self.get_mark())
    value = self.prefix(length)
    self.forward(length)
    ch = self.peek()
    if ch not in '\0 \r\n\x85\u2028\u2029':
        raise ScannerError("while scanning a directive", start_mark,
                "expected alphabetic or numeric character, but found %r"
                % ch, self.get_mark())
    return value