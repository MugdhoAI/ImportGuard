"""Small in-process sliding-window limits for the local single-server app."""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class RateLimitExceeded(RuntimeError):
    """Raised when a bounded request budget is exhausted."""

    def __init__(self, retry_after: int):
        super().__init__("Rate limit reached; try again shortly.")
        self.retry_after = max(1, retry_after)


class SlidingWindowLimiter:
    def __init__(self):
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> None:
        now = monotonic()
        cutoff = now - max(1, window_seconds)
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= max(1, limit):
                retry_after = int(events[0] + window_seconds - now) + 1
                raise RateLimitExceeded(retry_after)
            events.append(now)

    def clear(self) -> None:
        with self._lock:
            self._events.clear()


api_limiter = SlidingWindowLimiter()
