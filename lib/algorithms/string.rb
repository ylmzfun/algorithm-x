# encoding: utf-8
# String Matching Algorithms Collection
#
# Overview:
# String matching algorithms locate occurrences of a pattern within text.
# Different algorithms suit different scenarios: brute force for short patterns,
# KMP uses prefix information to avoid backtracking, Rabin-Karp uses hashing.
#
# Applications:
# 1. Text editors: find-and-replace functionality
# 2. Search engines: web content indexing
# 3. Bioinformatics: DNA sequence alignment
# 4. Intrusion detection: malicious code scanning

module StringAlgorithms
  # Brute Force string matching
  # Time: O(n*m)
  def self.brute_force(text, pattern)
    n = text.length
    m = pattern.length
    positions = []

    (0..n - m).each do |i|
      j = 0
      j += 1 while j < m && text[i + j] == pattern[j]
      positions << i if j == m
    end
    positions
  end

  # KMP (Knuth-Morris-Pratt) algorithm
  # Uses LPS (Longest Proper Prefix which is also Suffix) array
  # Time: O(n + m)
  def self.kmp_search(text, pattern)
    return [0] if pattern.empty?
    return [] if text.empty?

    n = text.length
    m = pattern.length
    lps = compute_lps(pattern)
    positions = []
    i = 0
    j = 0

    while i < n
      if text[i] == pattern[j]
        i += 1
        j += 1
      end

      if j == m
        positions << i - j
        j = lps[j - 1]
      elsif i < n && text[i] != pattern[j]
        if j != 0
          j = lps[j - 1]
        else
          i += 1
        end
      end
    end
    positions
  end

  # Rabin-Karp algorithm
  # Uses rolling hash for fast substring comparison
  # Time: average O(n + m), worst O(n*m)
  def self.rabin_karp(text, pattern, base = 256, mod = 10**9 + 7)
    return [0] if pattern.empty?
    return [] if text.empty? || pattern.length > text.length

    n = text.length
    m = pattern.length
    positions = []

    h = 1
    (m - 1).times { h = (h * base) % mod }

    pattern_hash = 0
    window_hash = 0
    m.times do |i|
      pattern_hash = (pattern_hash * base + pattern[i].ord) % mod
      window_hash = (window_hash * base + text[i].ord) % mod
    end

    (0..n - m).each do |i|
      if window_hash == pattern_hash
        positions << i if text[i, m] == pattern
      end

      if i < n - m
        window_hash = (window_hash - text[i].ord * h) % mod
        window_hash = (window_hash * base + text[i + m].ord) % mod
        window_hash = (window_hash + mod) % mod
      end
    end
    positions
  end

  # Boyer-Moore algorithm (simplified, bad character rule only)
  # Time: average O(n/m), worst O(n*m)
  def self.boyer_moore(text, pattern)
    return [0] if pattern.empty?
    return [] if text.empty? || pattern.length > text.length

    n = text.length
    m = pattern.length
    positions = []

    bad_char = {}
    pattern.each_char.with_index { |c, i| bad_char[c] = i }

    i = 0
    while i <= n - m
      j = m - 1

      while j >= 0 && pattern[j] == text[i + j]
        j -= 1
      end

      if j < 0
        positions << i
        i += (i + m < n) ? m - (bad_char[text[i + m]] || -1) : 1
      else
        shift = bad_char[text[i + j]]
        shift = shift ? [1, j - shift].max : j + 1
        i += shift
      end
    end
    positions
  end

  # Z-Algorithm: compute Z array (LCP of suffix with original string)
  # Time: O(n)
  def self.z_algorithm(str)
    n = str.length
    z = Array.new(n, 0)
    l = r = 0

    (1...n).each do |i|
      if i <= r
        z[i] = [r - i + 1, z[i - l]].min
      end

      while i + z[i] < n && str[z[i]] == str[i + z[i]]
        z[i] += 1
      end

      if i + z[i] - 1 > r
        l = i
        r = i + z[i] - 1
      end
    end
    z
  end

  # Pattern matching using Z-Algorithm
  def self.z_search(text, pattern)
    return [0] if pattern.empty?
    return [] if text.empty?

    combined = pattern + "$" + text
    z = z_algorithm(combined)
    m = pattern.length
    positions = []

    (m + 1...combined.length).each do |i|
      positions << (i - m - 1) if z[i] == m
    end
    positions
  end

  # Longest Common Substring
  # Time: O(n*m)
  def self.longest_common_substring(str1, str2)
    n = str1.length
    m = str2.length
    dp = Array.new(n + 1) { Array.new(m + 1, 0) }
    max_len = 0
    end_pos = 0

    (1..n).each do |i|
      (1..m).each do |j|
        if str1[i - 1] == str2[j - 1]
          dp[i][j] = dp[i - 1][j - 1] + 1
          if dp[i][j] > max_len
            max_len = dp[i][j]
            end_pos = i
          end
        end
      end
    end

    max_len > 0 ? str1[end_pos - max_len, max_len] : ""
  end

  # Edit Distance (Levenshtein Distance)
  # Time: O(n*m)
  def self.edit_distance(str1, str2)
    n = str1.length
    m = str2.length
    dp = Array.new(n + 1) { Array.new(m + 1, 0) }

    (0..n).each { |i| dp[i][0] = i }
    (0..m).each { |j| dp[0][j] = j }

    (1..n).each do |i|
      (1..m).each do |j|
        cost = str1[i - 1] == str2[j - 1] ? 0 : 1
        dp[i][j] = [
          dp[i - 1][j] + 1,
          dp[i][j - 1] + 1,
          dp[i - 1][j - 1] + cost
        ].min
      end
    end
    dp[n][m]
  end

  # Longest Palindromic Substring (Manacher's Algorithm)
  # Time: O(n)
  def self.longest_palindrome(str)
    return "" if str.empty?

    t = "^#" + str.chars.join('#') + "#\$"
    n = t.length
    p = Array.new(n, 0)
    center = right = 0

    (1...n - 1).each do |i|
      mirror = 2 * center - i
      p[i] = [right - i, p[mirror]].min if i < right

      while t[i + p[i] + 1] == t[i - p[i] - 1]
        p[i] += 1
      end

      if i + p[i] > right
        center = i
        right = i + p[i]
      end
    end

    max_len = p.max
    center_idx = p.index(max_len)
    start = (center_idx - max_len) / 2
    str[start, max_len]
  end

  # Check if string is palindrome
  def self.palindrome?(str)
    left = 0
    right = str.length - 1
    while left < right
      return false if str[left] != str[right]
      left += 1
      right -= 1
    end
    true
  end

  # Compute LPS (Longest Proper Prefix which is also Suffix) array for KMP
  def self.compute_lps(pattern)
    m = pattern.length
    lps = Array.new(m, 0)
    len = 0
    i = 1

    while i < m
      if pattern[i] == pattern[len]
        len += 1
        lps[i] = len
        i += 1
      elsif len != 0
        len = lps[len - 1]
      else
        lps[i] = 0
        i += 1
      end
    end
    lps
  end

  # All substrings of a string
  def self.all_substrings(str)
    result = []
    (0...str.length).each do |i|
      (i...str.length).each do |j|
        result << str[i..j]
      end
    end
    result
  end

  # Benchmark all string matching algorithms
  def self.benchmark(text, pattern)
    puts "String Matching Benchmark"
    puts "Text length: #{text.length}, Pattern length: #{pattern.length}"
    puts "-" * 50

    algorithms = {
      "BruteForce" => :brute_force,
      "KMP" => :kmp_search,
      "RabinKarp" => :rabin_karp,
      "BoyerMoore" => :boyer_moore,
      "Z-Algorithm" => :z_search
    }

    algorithms.each do |name, method|
      start = Time.now
      100.times { send(method, text, pattern) }
      elapsed = (Time.now - start) * 1000
      result = send(method, text, pattern)
      puts "#{name.ljust(12)}: #{elapsed.round(4)}ms, #{result.length} matches"
    end
  end
end

# Usage examples and tests
if __FILE__ == $0
  puts "=== String Matching Algorithms Demo ==="

  text = "ABABDABACDABABCABAB"
  pattern = "ABABCABAB"

  puts "Text: #{text}"
  puts "Pattern: #{pattern}"
  puts

  {
    "BruteForce" => StringAlgorithms.brute_force(text, pattern),
    "KMP" => StringAlgorithms.kmp_search(text, pattern),
    "RabinKarp" => StringAlgorithms.rabin_karp(text, pattern),
    "BoyerMoore" => StringAlgorithms.boyer_moore(text, pattern),
    "Z-Algorithm" => StringAlgorithms.z_search(text, pattern)
  }.each { |name, pos| puts "#{name.ljust(12)}: position #{pos}" }

  puts "\n=== Z-Algorithm ==="
  puts "Z array for 'aabcaabxaaaz': #{StringAlgorithms.z_algorithm('aabcaabxaaaz')}"

  puts "\n=== String Operations ==="
  puts "LCS of ('abcdef', 'zbcde'): #{StringAlgorithms.longest_common_substring('abcdef', 'zbcde')}"
  puts "Edit distance ('kitten', 'sitting'): #{StringAlgorithms.edit_distance('kitten', 'sitting')}"
  puts "Longest palindrome in 'babad': #{StringAlgorithms.longest_palindrome('babad')}"
  puts "Is 'racecar' palindrome?: #{StringAlgorithms.palindrome?('racecar')}"
  puts "Is 'hello' palindrome?: #{StringAlgorithms.palindrome?('hello')}"

  puts "\n=== Large-scale Benchmark ==="
  large_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 1000
  StringAlgorithms.benchmark(large_text, "XYZABC")
end
