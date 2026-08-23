"""
SecureWipe — core/confidence.py
Module pour le calcul du score de confiance de l'effacement (0–100).
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
    Computes the erasure confidence score on a scale from 0 to 100.

    Weighted breakdown:
    - Firmware / Cryptographic Sanitization success: +50 pts
    - Verification sampling pass: +30 pts
    - HPA/DCO hidden sector check passed or wiped: +20 pts

    Returns:
        int: Sanitization confidence score bounded between 0 and 100.
    """
    score = 0
    if ata_success or nvme_success or crypto_erase:
        score += 50
    if sampling_pass:
        score += 30
    if not hpa_detected or hpa_wiped:
        score += 20
    return min(100, max(0, score))


def get_confidence_level(score: int) -> str:
    """
    Returns a human-readable confidence rating label based on score.

    Args:
        score (int): Confidence score (0-100).

    Returns:
        str: 'HIGH' (>=90), 'MEDIUM' (>=70), or 'LOW' (<70).
    """
    bounded_score = min(100, max(0, score))
    if bounded_score >= 90:
        return "HIGH"
    elif bounded_score >= 70:
        return "MEDIUM"
    return "LOW"

