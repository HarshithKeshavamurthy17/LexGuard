"""File-based storage for contracts."""

import json
import logging
from pathlib import Path
from typing import List, Optional

from lexguard.config import settings
from lexguard.models.contract import Contract
from lexguard.storage.schema import ContractMetadata

logger = logging.getLogger(__name__)


def save_contract(contract: Contract) -> None:
    """
    Save a contract to file storage.

    Args:
        contract: Contract to save
    """
    contracts_dir = settings.data_dir / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)

    file_path = contracts_dir / f"{contract.id}.json"

    try:
        # Convert to dict for JSON serialization
        contract_dict = contract.model_dump(mode="json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(contract_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved contract {contract.id} to {file_path}")

    except Exception as e:
        logger.error(f"Error saving contract {contract.id}: {e}")
        raise


def load_contract(contract_id: str) -> Optional[Contract]:
    """
    Load a contract from file storage.

    Args:
        contract_id: ID of the contract to load

    Returns:
        Contract object or None if not found
    """
    contracts_dir = settings.data_dir / "contracts"
    file_path = contracts_dir / f"{contract_id}.json"

    if not file_path.exists():
        logger.warning(f"Contract {contract_id} not found")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            contract_dict = json.load(f)

        contract = Contract(**contract_dict)
        logger.info(f"Loaded contract {contract_id}")
        return contract

    except Exception as e:
        logger.error(f"Error loading contract {contract_id}: {e}")
        raise


def list_contracts() -> List[ContractMetadata]:
    """
    List all stored contracts with metadata.

    Returns:
        List of contract metadata
    """
    contracts_dir = settings.data_dir / "contracts"

    if not contracts_dir.exists():
        return []

    metadata_list = []

    for file_path in contracts_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                contract_dict = json.load(f)

            # Count risk levels
            clauses = contract_dict.get("clauses", [])
            risk_counts = {"high": 0, "medium": 0, "low": 0}

            for clause in clauses:
                risk_level = clause.get("risk_level")
                if risk_level in risk_counts:
                    risk_counts[risk_level] += 1

            metadata = ContractMetadata(
                id=contract_dict["id"],
                title=contract_dict["title"],
                uploaded_at=contract_dict["uploaded_at"],
                original_filename=contract_dict["original_filename"],
                clause_count=len(clauses),
                high_risk_count=risk_counts["high"],
                medium_risk_count=risk_counts["medium"],
                low_risk_count=risk_counts["low"],
            )

            metadata_list.append(metadata)

        except Exception as e:
            logger.warning(f"Error reading contract metadata from {file_path}: {e}")
            continue

    # Sort by upload date (newest first)
    metadata_list.sort(key=lambda x: x.uploaded_at, reverse=True)

    return metadata_list


def delete_contract(contract_id: str) -> bool:
    """
    Delete a contract from storage.

    Args:
        contract_id: ID of the contract to delete

    Returns:
        True if deleted, False if not found
    """
    contracts_dir = settings.data_dir / "contracts"
    file_path = contracts_dir / f"{contract_id}.json"

    if not file_path.exists():
        return False

    try:
        file_path.unlink()
        logger.info(f"Deleted contract {contract_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting contract {contract_id}: {e}")
        raise


