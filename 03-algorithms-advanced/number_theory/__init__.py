"""Number theory algorithms package."""

from .primes import (
    sieve_of_eratosthenes,
    segmented_sieve,
    miller_rabin,
    trial_division_factorization,
    pollards_rho,
)
from .gcd_lcm import gcd, lcm, extended_gcd, mod_inverse, solve_linear_diophantine, chinese_remainder
from .modular_arithmetic import mod_pow, ncr_mod, ncr_mod_lucas
from .number_theory_applications import (
    count_primes_in_range,
    all_factors,
    euler_totient,
    mobius_function,
    linear_sieve,
)

__all__ = [
    # primes
    "sieve_of_eratosthenes",
    "segmented_sieve",
    "miller_rabin",
    "trial_division_factorization",
    "pollards_rho",
    # gcd_lcm
    "gcd",
    "lcm",
    "extended_gcd",
    "mod_inverse",
    "solve_linear_diophantine",
    "chinese_remainder",
    # modular_arithmetic
    "mod_pow",
    "ncr_mod",
    "ncr_mod_lucas",
    # number_theory_applications
    "count_primes_in_range",
    "all_factors",
    "euler_totient",
    "mobius_function",
    "linear_sieve",
]
