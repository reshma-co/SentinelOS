from fastapi import APIRouter, HTTPException
from app.mission.commander import get_mission_status, run_mission
from app.mission.schemas import CreateMissionInput, UnifiedMissionResponse
from app.utils.logger import logger

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.post("/start", response_model=UnifiedMissionResponse)
@router.post("/run", response_model=UnifiedMissionResponse)
async def start_mission(mission_input: CreateMissionInput):
    logger.info(
        f"Received mission start request for location: {mission_input.location}"
    )
    try:
        response = await run_mission(mission_input)
        logger.info(
            f"Mission {response.mission_id} completed successfully with status: {response.status}"
        )
        return response
    except Exception as exc:
        logger.error(f"Error executing mission: {str(exc)}")
        raise HTTPException(
            status_code=500, detail=f"Mission execution failed: {str(exc)}"
        )


@router.get("/{mission_id}/status")
def get_status(mission_id: str):
    logger.info(f"Fetching status for mission: {mission_id}")
    try:
        return get_mission_status(mission_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
