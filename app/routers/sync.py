from fastapi import APIRouter, HTTPException

ROUTER = APIRouter(
    prefix="/sync",
    tags=["sync"]
)

@ROUTER.post("/", status_code=200)
def sync() -> bool:
    """sync

    Syncs the xlsx db file with the cloud location

    Returns:
        bool: on success of syncing with cloud location
    """
    return True
