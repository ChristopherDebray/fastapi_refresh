from fastapi.routing import APIRoute


class PublicAPIRoute(APIRoute):
    """Mark a route as publicly accessible (no authentication required)."""

    public = True
