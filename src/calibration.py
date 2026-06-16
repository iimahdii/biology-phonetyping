"""Basic hyperspectral calibration helpers."""

import numpy as np


def radiometric_correction(raw: np.ndarray, dark: np.ndarray, white: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Convert raw hyperspectral intensity to reflectance.

    Reflectance = (Raw - Dark) / (White - Dark)

    Parameters
    ----------
    raw : np.ndarray
        Raw hyperspectral cube with shape [height, width, bands].
    dark : np.ndarray
        Dark reference cube or spectrum.
    white : np.ndarray
        White reference cube or spectrum.
    eps : float
        Small value to avoid division by zero.

    Returns
    -------
    np.ndarray
        Reflectance cube clipped to [0, 1].
    """
    reflectance = (raw.astype(np.float32) - dark.astype(np.float32)) / (white.astype(np.float32) - dark.astype(np.float32) + eps)
    return np.clip(reflectance, 0.0, 1.0)
