class ProxyParser:

    @staticmethod
    def parse(proxy_line: str):
        clean_proxy = proxy_line.replace("http://", "").replace("https://", "").strip()
        proxy_settings = {}
        proxy_display = clean_proxy

        if "@" in clean_proxy:
            auth, server = clean_proxy.split("@", 1)
            user, password = auth.split(":", 1)
            proxy_settings = {"server": f"http://{server}", "username": user, "password": password}
            proxy_display = server
        else:
            parts = clean_proxy.split(':')
            if len(parts) == 4:
                proxy_settings = {
                    "server": f"http://{parts[0]}:{parts[1]}",
                    "username": parts[2],
                    "password": parts[3]
                }
                proxy_display = f"{parts[0]}:{parts[1]}"
            else:
                proxy_settings = {"server": f"http://{clean_proxy}"}

        return proxy_settings, proxy_display