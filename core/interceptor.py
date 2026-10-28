from urllib.parse import urlparse

class TrafficInterceptor:

    BLOCKED_RESOURCE_TYPES = [
        "image", "media", "font", "stylesheet", "other",
        "websocket", "manifest", "ping", "beacon"
    ]

    BLOCKED_KEYWORDS = [
        "doubleclick", "googlesyndication", "adsystem", "adnxs", "rubiconproject",
        "pubmatic", "criteo", "taboola", "outbrain", "amazon-adsystem", "moatads",
        "quantserve", "scorecardresearch", "zedo", "mp4", "webm", "m3u8", "video",
        "jwplayer", "brightcove", "imasdk", "prebid", "pbjs", "sentry", "hotjar",
        "facebook.net", "tiktok", "pinterest", "clarity.ms", "recaptcha", "analytics"
    ]

    def __init__(self, target_url: str):
        self.target_domain = urlparse(target_url).netloc.replace("www.", "")

    async def strict_traffic_saver(self, route):
        req = route.request
        req_url = req.url.lower()
        res_type = req.resource_type

        if res_type in self.BLOCKED_RESOURCE_TYPES:
            await route.abort()
            return

        if any(k in req_url for k in self.BLOCKED_KEYWORDS):
            await route.abort()
            return

        if res_type in ["script", "xhr", "fetch", "sub_frame"]:
            if self.target_domain not in req_url:
                await route.abort()
                return

        await route.continue_()