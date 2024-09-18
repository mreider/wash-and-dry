import os
import json
import time
from datetime import datetime

TRACE_FILE_PATH = "/var/log/otel-traces.json"
WATERFALL_FILE_PATH = "/var/log/waterfall/waterfall-view.txt"

def read_traces():
    if not os.path.exists(TRACE_FILE_PATH):
        return []
    with open(TRACE_FILE_PATH, 'r') as file:
        traces = json.load(file)
    return traces.get('resourceSpans', [])

def create_waterfall_view(traces):
    span_dict = {}
    for resource_span in traces:
        for il_span in resource_span.get('instrumentationLibrarySpans', []):
            for span in il_span.get('spans', []):
                trace_id = span.get('traceId')
                span_id = span.get('spanId')
                parent_span_id = span.get('parentSpanId')
                name = span.get('name')
                start_time = span.get('startTimeUnixNano')
                end_time = span.get('endTimeUnixNano')
                service_name = resource_span.get('resource', {}).get('attributes', [{}])[0].get('value', {}).get('stringValue', 'unknown')
                span_dict[span_id] = {
                    'trace_id': trace_id,
                    'span_id': span_id,
                    'parent_span_id': parent_span_id,
                    'name': name,
                    'start_time': start_time,
                    'end_time': end_time,
                    'service_name': service_name
                }
    
    waterfall_view = []
    for span_id, span in span_dict.items():
        parent_span_id = span['parent_span_id']
        if parent_span_id and parent_span_id in span_dict:
            parent_span = span_dict[parent_span_id]
            indent = '\t' * (len(parent_span_id) // 2)
            waterfall_view.append(f"{indent}{span['service_name']} - {span['name']} (Trace ID: {span['trace_id']}, Span ID: {span['span_id']})")
        else:
            waterfall_view.append(f"{span['service_name']} - {span['name']} (Trace ID: {span['trace_id']}, Span ID: {span['span_id']})")
    
    return waterfall_view

def write_waterfall_view(waterfall_view):
    os.makedirs(os.path.dirname(WATERFALL_FILE_PATH), exist_ok=True)
    with open(WATERFALL_FILE_PATH, 'w') as file:
        for line in waterfall_view:
            file.write(line + "\n")

def main():
    while True:
        traces = read_traces()
        waterfall_view = create_waterfall_view(traces)
        write_waterfall_view(waterfall_view)
        time.sleep(60)

if __name__ == "__main__":
    main()
