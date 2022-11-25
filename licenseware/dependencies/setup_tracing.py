# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config


def setup_tracing(app, config: Config):
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import SERVICE_NAME
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: config.APP_ID})
    )
    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)

    jaeger_exporter = JaegerExporter(
        agent_host_name=config.OPEN_TELEMETRY_HOST,
        agent_port=config.OPEN_TELEMETRY_PORT,
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
