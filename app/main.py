from __future__ import annotations

from litestar import Litestar, get
from litestar.contrib.prometheus import PrometheusConfig, PrometheusController
from litestar.openapi import OpenAPIConfig

from app.controller.risiko_controller import RisikoController
from app.errors import EXCEPTION_HANDLERS
from app.seed import seed_risiken


@get("/")
async def index() -> dict[str, str]:
    return {
        "name": "Risikoerfassung",
        "docs": "/schema/swagger",
        "metrics": "/metrics",
    }


async def on_startup() -> None:
    seed_risiken()


# Prometheus: erfasst Request-Anzahl, -Dauer und In-Flight pro Route/Methode/Status.
prometheus_config = PrometheusConfig(
    app_name="risikoerfassung",
    prefix="risikoerfassung",
    group_path=True,
    excluded_http_methods=None,
)


app = Litestar(
    route_handlers=[index, RisikoController, PrometheusController],
    openapi_config=OpenAPIConfig(title="Risikoerfassung API", version="0.1.0"),
    on_startup=[on_startup],
    middleware=[prometheus_config.middleware],
    exception_handlers=EXCEPTION_HANDLERS,
)
