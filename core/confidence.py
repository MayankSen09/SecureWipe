"""
SecureWipe — core/confidence.py
Module for computing the wipe confidence score (0–100).
Author: TEAM SOLUTION
"""

def compute_score(
    ata_success: bool = False,
    nvme_success: bool = False,
    hpa_detected: bool = False,
    hpa_wiped: bool = False,
    sampling_pass: bool = False,
    crypto_erase: bool = False,
) -> int:
    """
    Computes the wipe confidence score from 0 to 100.
    - Firmware wipe / crypto erase successful: +50
    - Verification sampling passed: +30
    - HPA not detected or wiped: +20
    """
    score = 0
    if ata_success or nvme_success or crypto_erase:
        score += 50
    if sampling_pass:
        score += 30
    if not hpa_detected or hpa_wiped:
        score += 20
    return min(100, max(0, score))
