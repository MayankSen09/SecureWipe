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
    Calcule le score de confiance de l'effacement de 0 à 100.
    - Effacement firmware / crypto réussi : +50
    - Échantillonnage de vérification réussi : +30
    - HPA non détectée ou effacée : +20
    """
    score = 0
    if ata_success or nvme_success or crypto_erase:
        score += 50
    if sampling_pass:
        score += 30
    if not hpa_detected or hpa_wiped:
        score += 20
    return min(100, max(0, score))
