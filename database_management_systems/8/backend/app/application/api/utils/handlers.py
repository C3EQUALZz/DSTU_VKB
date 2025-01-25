from fastapi import APIRouter, status
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=["utils"]
)

@router.get(
    path="/",
    response_class=RedirectResponse,
    name="homepage",
    status_code=status.HTTP_303_SEE_OTHER
)
async def homepage():
    return RedirectResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        url="api/docs"
    )