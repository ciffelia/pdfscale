def _mm_to_pixels_at_72ppi(mm: float) -> float:
    """Convert millimeters to pixels at 72 ppi."""

    return mm * 72 / 25.4


a4_height = _mm_to_pixels_at_72ppi(297)
b5_height = _mm_to_pixels_at_72ppi(257)
