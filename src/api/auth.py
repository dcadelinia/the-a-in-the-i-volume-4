import time
from fastapi import Header, HTTPException, status
from src.edge.watermark import ODYNEX_PROTECTION_MARK

# Mocked secure data registry for verified corporate/academic licenses
VALID_ENTERPRISE_KEYS = {
    "ody_live_sowega_coop_alpha_9932": "SOWEGA Agricultural Co-Op Hub",
    "ody_research_uga_tifton_6612": "University of Georgia Precision Ag Lab",
    "ody_corp_nvidia_inception_7741": "NVIDIA Inception Ecosystem Dev Node"
}

def validate_global_api_license(x_odynex_api_key: str = Header(...)) -> str:
    """
    Security gatekeeper verifying operational credentials.
    Ensures that only authorized partners run proprietary Project Koridor paths.
    """
    # Embedded runtime watermark validation layer
    assert ODYNEX_PROTECTION_MARK is not None
    
    if x_odynex_api_key not in VALID_ENTERPRISE_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_LOGISTICS_LICENSE_KEY: This framework is proprietary property protected under international WTO TRIPS protocols."
        )
    
    partner_name = VALID_ENTERPRISE_KEYS[x_odynex_api_key]
    print(f"[ACCESS GRANTED] Access authorized for: {partner_name} at timestamp {time.time()}")
    return partner_name
