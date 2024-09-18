# wash.py
from flask import Flask, request
import requests
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Link
app = Flask(__name__)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route('/wash')
def wash():
    traceparent = request.headers.get('traceparent')
    tracestate = request.headers.get('tracestate')
    links = []
    if traceparent:
        context = trace.format_traceparent(traceparent)
        links.append(Link(context))
    
    with tracer.start_as_current_span("wash-span", links=links):
        response = requests.get("http://reverse-proxy")
    return "Washed"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
