import threading
import socket
from datetime import datetime as dt
from typing import Callable, Iterable, Any, Mapping


class Mp:
    ENC_TYPE = 'utf-8'

    def __init__(self, display_name: str) -> None:
        self.ftch_thread = FetchLoop(daemon=True, display_name=display_name)
        self.display_name = display_name

    def _fetch_loop() -> None:
        pass

    def now() -> str:
        return dt.now().strftime("%H:%M")
    # now()

    def req(self, mtype: str, recip: str, body: str = None) -> str:
        return mtype + " " +\
            self.now() + " " +\
            recip + " " +\
            self.display_name + "\n" +\
            body
    # req()

    def res(self, mtype: str, code: int, recip: str, body: str = None) -> str:
        return mtype + " " +\
            code + " " +\
            recip + " " +\
            self.display_name + "\n" +\
            body
    # res()

    def send(self, room: socket.socket, recip: str, body: str = None) -> None:
        room.send(self.req("SEND", recip, body))

    def join(self, room: socket.socket, recip: str) -> None:
        room.send(self.req("JOIN", recip))

    def disconnect(self, room: socket.socket, recip: str, body: str) -> None:
        room.send(self.req("DISCONNECT", recip, body))

    def fetch() -> None:
        pass
        # impliment latter

    def invite(self, conn: socket.socket, recip: str) -> None:
        conn.send(self.res("INVITE", 200, recip))

    def recieve(self, conn: socket.socket, recip: str) -> None:
        conn.send(self.res("RECIEVE", 200, recip))

    def catch() -> None:
        pass
        # impliment with fetch

    def decline(self, conn: socket.socket, recip: str, code: int) -> None:
        conn.send(self.res("DECLINE", code, recip))


class FetchLoop(threading.Thread):

    def __init__(self, group: None = ..., target: Callable[..., object] | None = ...,
                 name: str | None = ..., args: Iterable[Any] = ...,
                 kwargs: Mapping[str, Any] | None = ..., *, daemon: bool | None = ...,
                 display_name: str) -> None:
        self.display_name = display_name
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def run(self):
        cache = {}
        while True:
            if self.request is not None:
                ip = cache.get(self.request)
                if ip is not None:
                    # reset timer
                    self.request = None
                    self.socket = None
                else:
                    request = 'FETCH ' +\
                        Mp.now() + " " +\
                        self.request + " " +\
                        self.display_name + "\n"

                    self.socket.send(request.encode(Mp.ENC_TYPE))

    def request(self, display_name: str, socket: socket.socket) -> None:
        self.request = display_name
        self.socket = socket
