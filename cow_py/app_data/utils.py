from re import T
from typing import Any, Dict
import httpx
from multiformats import CID

import json

from cow_py.app_data.consts import DEFAULT_IPFS_READ_URI

# CID uses multibase to self-describe the encoding used (See https://github.com/multiformats/multibase)
#   - Most reference implementations (multiformats/cid or Pinata, etc) use base58btc encoding
#   - However, the backend uses base16 encoding (See https://github.com/cowprotocol/services/blob/main/crates/app-data-hash/src/lib.rs#L64)
MULTIBASE_BASE16 = "f"


def extract_digest(cid_str: str) -> str:
    # TODO: Verify this
    cid = CID.decode(cid_str)
    if cid_str[0] == MULTIBASE_BASE16:
        return "0x" + cid.digest.hex()[4:]

    return "0x" + cid.set(base="base58btc").digest.hex()[4:]


def stringify_deterministic(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


async def fetch_doc_from_cid(
    cid: str, ipfs_uri: str = DEFAULT_IPFS_READ_URI
) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ipfs_uri}/{cid}")
        return response.json()
