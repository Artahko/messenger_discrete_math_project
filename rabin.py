
def rabin_karp(text, pattern, base, mod):
    n = len(text)
    m = len(pattern)
    results = []

    if m > n:
        return results

    h = pow(base, m - 1, mod)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        window_hash  = (base * window_hash  + ord(text[i]))    % mod

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                results.append(i)

        if i < n - m:
            window_hash = (base * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if window_hash < 0:
                window_hash += mod

    return results