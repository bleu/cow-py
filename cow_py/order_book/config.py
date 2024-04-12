from cow_py.common.api.api_base import APIConfig
from cow_py.common.config import CowEnv, SupportedChainId

ORDER_BOOK_PROD_CONFIG = {
    SupportedChainId.MAINNET: "https://api.cow.fi/mainnet",
    SupportedChainId.GNOSIS_CHAIN: "https://api.cow.fi/xdai",
    SupportedChainId.SEPOLIA: "https://api.cow.fi/sepolia",
}

ORDER_BOOK_STAGING_CONFIG = {
    SupportedChainId.MAINNET: "https://barn.api.cow.fi/mainnet",
    SupportedChainId.GNOSIS_CHAIN: "https://barn.api.cow.fi/xdai",
    SupportedChainId.SEPOLIA: "https://barn.api.cow.fi/sepolia",
}


class ProdAPIConfig(APIConfig):
    def get_base_url(self):
        return ORDER_BOOK_PROD_CONFIG.get(
            self.chain_id, "default URL if chain_id is not found"
        )

    def get_context(self):
        return {
            "base_url": self.get_base_url(),
            **self.context,
        }


class StagingAPIConfig(APIConfig):
    def get_base_url(self):
        return ORDER_BOOK_STAGING_CONFIG.get(
            self.chain_id, "default URL if chain_id is not found"
        )

    def get_context(self):
        return {
            "base_url": self.get_base_url(),
            **self.context,
        }


class WithCoWConfig:
    @staticmethod
    def get_config(context) -> APIConfig:
        env = context.get("env", CowEnv.PROD)
        chain_id = context.get("chain_id", SupportedChainId.MAINNET)

        if env == CowEnv.PROD:
            return ProdAPIConfig(chain_id, context)
        elif env == CowEnv.STAGING:
            return StagingAPIConfig(chain_id, context)
        else:
            raise ValueError("Unknown environment")
