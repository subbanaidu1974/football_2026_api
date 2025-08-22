from fastapi import FastAPI
from .db import lifespan
from .routers import api
from .routers import (
    cities, venues, competitions, seasons, stages, teams, matches,
    pages, page_blocks, affiliate_partners, affiliate_offers,
    outbound_clicks, email_subscribers, alert_subscriptions
)

app = FastAPI(title="SportsHub API", version="1.0.0", lifespan=lifespan)

# mount routers
for r in [
    cities.router, venues.router, competitions.router, seasons.router, stages.router,
    teams.router, matches.router, pages.router, page_blocks.router,
    affiliate_partners.router, affiliate_offers.router, outbound_clicks.router,
    email_subscribers.router, alert_subscriptions.router,
]:
    app.include_router(r)

@app.get("/")
async def root():
    return {"ok": True, "service": "sportshub"}
