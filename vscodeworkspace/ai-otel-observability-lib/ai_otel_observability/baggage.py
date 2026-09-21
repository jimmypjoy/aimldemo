from opentelemetry import baggage
from opentelemetry.context import attach
from opentelemetry.sdk.trace import SpanProcessor


class BaggageSpanProcessor(SpanProcessor):
    """Promotes every OTel Baggage entry onto each span as it starts.

    Baggage travels across process boundaries automatically (via the W3C
    `baggage` header) but is otherwise invisible to search -- it never
    becomes a Tempo-queryable span attribute unless something copies it on
    start, since by on_end the span is a read-only ReadableSpan. `setup()`
    registers this on every service's TracerProvider automatically.
    """

    def on_start(self, span, parent_context=None) -> None:
        for key, value in baggage.get_all(parent_context).items():
            span.set_attribute(key, value)


def set_business_context(key: str, value: str) -> None:
    """Attaches one key/value pair to OTel Baggage on the current context.

    Once attached, the value propagates automatically to every downstream
    HTTP call made from this point in the current request/task (via the W3C
    baggage header), and -- once it reaches a service where `setup()` has
    registered a BaggageSpanProcessor -- becomes a searchable span attribute
    and log field there too, with no further code needed on the receiving
    end.

    Call this as early as possible once the value is known (e.g. a case id,
    order id, or session id), since it only affects spans/calls created
    after this point, not ones already in flight. Safe to call multiple
    times with different keys in the same request; each call layers onto
    whatever baggage already exists in the current context.

    Args:
        key: A namespaced attribute name (e.g. "review.key", "case.id") --
            namespaced to avoid colliding with OTel semantic-convention
            attribute names or another team's key on shared infrastructure.
        value: The value to attach. Keep it short: baggage travels on every
            outgoing request in this context, including calls to external
            third-party APIs, so avoid large payloads or sensitive data.
    """
    attach(baggage.set_baggage(key, value))
