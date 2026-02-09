aviation-mcp-client git:(main) uv run python -m src.client --test --mcp-url http://localhost:8000/sse
Connecting to MCP server at http://localhost:8000/sse...

  [FAIL] Flight lookup at BDL
  [FAIL] Flight by number
  [FAIL] Unknown airport returns empty
  [FAIL] Gates at JFK
  [FAIL] Specific gate
  [FAIL] Unknown gate returns empty
  [FAIL] Weather at LAX
  [FAIL] Unknown airport weather

Results: 0/8 passed


======
log output

aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Setting up SSE connection
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Setting up SSE connection
aviation-mcp-1   | Setting up SSE connection
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Created new session with ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Created new session with ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Created new session with ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Starting SSE response task
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Starting SSE response task
aviation-mcp-1   | Starting SSE response task
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Yielding read and write streams
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Yielding read and write streams
aviation-mcp-1   | Yielding read and write streams
aviation-mcp-1   | INFO:     172.22.0.1:42170 - "GET /sse HTTP/1.1" 200 OK
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Starting SSE writer
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Starting SSE writer
aviation-mcp-1   | Starting SSE writer
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sent endpoint event: /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sent endpoint event: /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c
aviation-mcp-1   | Sent endpoint event: /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mcp","version":"0.1.0"}},"jsonrpc":"2.0","id":0}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mcp","version":"0.1.0"}},"jsonrpc":"2.0","id":0}'
aviation-mcp-1   | Received JSON: b'{"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mcp","version":"0.1.0"}},"jsonrpc":"2.0","id":0}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e490>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e490>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e490>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=0, result={'protocolVersion': '2025-11-25', 'capabilities': {'experimental': {}, 'prompts': {'listChanged': False}, 'resources': {'subscribe': False, 'listChanged': False}, 'tools': {'listChanged': False}}, 'serverInfo': {'name': 'aviation-mcp', 'version': '1.26.0'}})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=0, result={'protocolVersion': '2025-11-25', 'capabilities': {'experimental': {}, 'prompts': {'listChanged': False}, 'resources': {'subscribe': False, 'listChanged': False}, 'tools': {'listChanged': False}}, 'serverInfo': {'name': 'aviation-mcp', 'version': '1.26.0'}})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=0, result={'protocolVersion': '2025-11-25', 'capabilities': {'experimental': {}, 'prompts': {'listChanged': False}, 'resources': {'subscribe': False, 'listChanged': False}, 'tools': {'listChanged': False}}, 'serverInfo': {'name': 'aviation-mcp', 'version': '1.26.0'}})), metadata=None)
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"notifications/initialized","jsonrpc":"2.0"}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"notifications/initialized","jsonrpc":"2.0"}'
aviation-mcp-1   | Received JSON: b'{"method":"notifications/initialized","jsonrpc":"2.0"}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | Validated client message: root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ead0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ead0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ead0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: root=InitializedNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: root=InitializedNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | Received message: root=InitializedNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL"}},"jsonrpc":"2.0","id":1}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL"}},"jsonrpc":"2.0","id":1}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL"}},"jsonrpc":"2.0","id":1}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ea30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ea30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL'}}, jsonrpc='2.0', id=1)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ea30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e7b0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e7b0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e7b0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://flight-status:5001/api/flights?airport=BDL "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://flight-status:5001/api/flights?airport=BDL "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=1, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=1, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=1, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12\nFlight UA567 (United): BDL -> ORD, Status: On Time, Gate: B3\nFlight AA890 (American): BDL -> DFW, Status: Delayed, Gate: A8\nFlight SW321 (Southwest): BDL -> BWI, Status: On Time, Gate: B1'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/list","jsonrpc":"2.0","id":2}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/list","jsonrpc":"2.0","id":2}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/list","jsonrpc":"2.0","id":2}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e990>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e990>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=2)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e990>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e490>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e490>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e490>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type ListToolsRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type ListToolsRequest
aviation-mcp-1   | Processing request of type ListToolsRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type ListToolsRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type ListToolsRequest
aviation-mcp-1   | Dispatching request of type ListToolsRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=2, result={'tools': [{'name': 'get_flight_status', 'description': 'Get flight status information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    flight_number: Flight number (e.g., DL1234)\n    time: Departure time filter (ISO 8601 prefix)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'flight_number': {'default': '', 'title': 'Flight Number', 'type': 'string'}, 'time': {'default': '', 'title': 'Time', 'type': 'string'}}, 'title': 'get_flight_statusArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_flight_statusOutput', 'type': 'object'}}, {'name': 'get_gate_info', 'description': 'Get gate information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    gate_number: Gate identifier (e.g., A1, B12)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'gate_number': {'default': '', 'title': 'Gate Number', 'type': 'string'}}, 'title': 'get_gate_infoArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_gate_infoOutput', 'type': 'object'}}, {'name': 'get_weather', 'description': 'Get current weather conditions for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}}, 'title': 'get_weatherArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_weatherOutput', 'type': 'object'}}]})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=2, result={'tools': [{'name': 'get_flight_status', 'description': 'Get flight status information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    flight_number: Flight number (e.g., DL1234)\n    time: Departure time filter (ISO 8601 prefix)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'flight_number': {'default': '', 'title': 'Flight Number', 'type': 'string'}, 'time': {'default': '', 'title': 'Time', 'type': 'string'}}, 'title': 'get_flight_statusArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_flight_statusOutput', 'type': 'object'}}, {'name': 'get_gate_info', 'description': 'Get gate information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    gate_number: Gate identifier (e.g., A1, B12)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'gate_number': {'default': '', 'title': 'Gate Number', 'type': 'string'}}, 'title': 'get_gate_infoArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_gate_infoOutput', 'type': 'object'}}, {'name': 'get_weather', 'description': 'Get current weather conditions for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}}, 'title': 'get_weatherArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_weatherOutput', 'type': 'object'}}]})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=2, result={'tools': [{'name': 'get_flight_status', 'description': 'Get flight status information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    flight_number: Flight number (e.g., DL1234)\n    time: Departure time filter (ISO 8601 prefix)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'flight_number': {'default': '', 'title': 'Flight Number', 'type': 'string'}, 'time': {'default': '', 'title': 'Time', 'type': 'string'}}, 'title': 'get_flight_statusArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_flight_statusOutput', 'type': 'object'}}, {'name': 'get_gate_info', 'description': 'Get gate information for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n    gate_number: Gate identifier (e.g., A1, B12)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}, 'gate_number': {'default': '', 'title': 'Gate Number', 'type': 'string'}}, 'title': 'get_gate_infoArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_gate_infoOutput', 'type': 'object'}}, {'name': 'get_weather', 'description': 'Get current weather conditions for an airport.\n\nArgs:\n    airport: IATA airport code (e.g., BDL, JFK)\n', 'inputSchema': {'properties': {'airport': {'default': '', 'title': 'Airport', 'type': 'string'}}, 'title': 'get_weatherArguments', 'type': 'object'}, 'outputSchema': {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'get_weatherOutput', 'type': 'object'}}]})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL","flight_number":"DL1234"}},"jsonrpc":"2.0","id":3}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL","flight_number":"DL1234"}},"jsonrpc":"2.0","id":3}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"BDL","flight_number":"DL1234"}},"jsonrpc":"2.0","id":3}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e530>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e530>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'BDL', 'flight_number': 'DL1234'}}, jsonrpc='2.0', id=3)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873e530>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873d130>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873d130>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873d130>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://flight-status:5001/api/flights?airport=BDL&flightNumber=DL1234 "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://flight-status:5001/api/flights?airport=BDL&flightNumber=DL1234 "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=3, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=3, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=3, result={'content': [{'type': 'text', 'text': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}], 'structuredContent': {'result': 'Flight DL1234 (Delta): BDL -> ATL, Status: On Time, Gate: A12'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":4}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":4}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_flight_status","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":4}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c190>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c190>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_flight_status', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=4)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c190>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e990>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e990>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e990>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://flight-status:5001/api/flights?airport=XXX "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://flight-status:5001/api/flights?airport=XXX "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=4, result={'content': [{'type': 'text', 'text': 'No flights found matching the criteria.'}], 'structuredContent': {'result': 'No flights found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=4, result={'content': [{'type': 'text', 'text': 'No flights found matching the criteria.'}], 'structuredContent': {'result': 'No flights found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=4, result={'content': [{'type': 'text', 'text': 'No flights found matching the criteria.'}], 'structuredContent': {'result': 'No flights found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK"}},"jsonrpc":"2.0","id":5}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK"}},"jsonrpc":"2.0","id":5}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK"}},"jsonrpc":"2.0","id":5}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c7d0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c7d0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK'}}, jsonrpc='2.0', id=5)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c7d0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873efd0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873efd0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873efd0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://gate-info:5002/api/gates?airport=JFK "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://gate-info:5002/api/gates?airport=JFK "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=5, result={'content': [{'type': 'text', 'text': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}], 'structuredContent': {'result': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=5, result={'content': [{'type': 'text', 'text': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}], 'structuredContent': {'result': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=5, result={'content': [{'type': 'text', 'text': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}], 'structuredContent': {'result': 'Gate C22 (Terminal 4): Status: Boarding, Flight: DL400, Airline: Delta\nGate D7 (Terminal 7): Status: Open, Flight: BA178, Airline: British Airways\nGate B14 (Terminal 8): Status: Boarding, Flight: AA100, Airline: American'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"BDL","gate_number":"A1"}},"jsonrpc":"2.0","id":6}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"BDL","gate_number":"A1"}},"jsonrpc":"2.0","id":6}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"BDL","gate_number":"A1"}},"jsonrpc":"2.0","id":6}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c050>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c050>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'BDL', 'gate_number': 'A1'}}, jsonrpc='2.0', id=6)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873c050>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873ecb0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873ecb0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873ecb0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://gate-info:5002/api/gates?airport=BDL&gateNumber=A1 "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://gate-info:5002/api/gates?airport=BDL&gateNumber=A1 "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=6, result={'content': [{'type': 'text', 'text': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}], 'structuredContent': {'result': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=6, result={'content': [{'type': 'text', 'text': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}], 'structuredContent': {'result': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=6, result={'content': [{'type': 'text', 'text': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}], 'structuredContent': {'result': 'Gate A1 (Terminal A): Status: Boarding, Flight: DL1234, Airline: Delta'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK","gate_number":"Z99"}},"jsonrpc":"2.0","id":7}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK","gate_number":"Z99"}},"jsonrpc":"2.0","id":7}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_gate_info","arguments":{"airport":"JFK","gate_number":"Z99"}},"jsonrpc":"2.0","id":7}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ef30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ef30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_gate_info', 'arguments': {'airport': 'JFK', 'gate_number': 'Z99'}}, jsonrpc='2.0', id=7)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873ef30>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f4d0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f4d0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f4d0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://gate-info:5002/api/gates?airport=JFK&gateNumber=Z99 "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://gate-info:5002/api/gates?airport=JFK&gateNumber=Z99 "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=7, result={'content': [{'type': 'text', 'text': 'No gate information found matching the criteria.'}], 'structuredContent': {'result': 'No gate information found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=7, result={'content': [{'type': 'text', 'text': 'No gate information found matching the criteria.'}], 'structuredContent': {'result': 'No gate information found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=7, result={'content': [{'type': 'text', 'text': 'No gate information found matching the criteria.'}], 'structuredContent': {'result': 'No gate information found matching the criteria.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"LAX"}},"jsonrpc":"2.0","id":8}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"LAX"}},"jsonrpc":"2.0","id":8}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"LAX"}},"jsonrpc":"2.0","id":8}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f390>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f390>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'LAX'}}, jsonrpc='2.0', id=8)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f390>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e3f0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e3f0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873e3f0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://weather:5003/api/weather?airport=LAX "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://weather:5003/api/weather?airport=LAX "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=8, result={'content': [{'type': 'text', 'text': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}], 'structuredContent': {'result': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=8, result={'content': [{'type': 'text', 'text': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}], 'structuredContent': {'result': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=8, result={'content': [{'type': 'text', 'text': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}], 'structuredContent': {'result': 'LAX: Clear, 68.0°F / 20.0°C, Wind: 5 mph W, Visibility: 10 miles, Humidity: 40%'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Handling POST message
aviation-mcp-1   | Handling POST message
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | Parsed session ID: d0eb279b-f642-458a-ae9e-cb48b3bbd63c
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":9}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":9}'
aviation-mcp-1   | Received JSON: b'{"method":"tools/call","params":{"name":"get_weather","arguments":{"airport":"XXX"}},"jsonrpc":"2.0","id":9}'
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)
aviation-mcp-1   | INFO:     172.22.0.1:42178 - "POST /messages/?session_id=d0eb279bf642458aae9ecb48b3bbd63c HTTP/1.1" 202 Accepted
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)
aviation-mcp-1   | Validated client message: root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f2f0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f2f0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | Sending session message to writer: SessionMessage(message=JSONRPCMessage(root=JSONRPCRequest(method='tools/call', params={'name': 'get_weather', 'arguments': {'airport': 'XXX'}}, jsonrpc='2.0', id=9)), metadata=ServerMessageMetadata(related_request_id=None, request_context=<starlette.requests.Request object at 0x7f373873f2f0>, close_sse_stream=None, close_standalone_sse_stream=None))
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f9d0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f9d0>
aviation-mcp-1   | Received message: <mcp.shared.session.RequestResponder object at 0x7f373873f9d0>
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] INFO: Processing request of type CallToolRequest
aviation-mcp-1   | Processing request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Dispatching request of type CallToolRequest
aviation-mcp-1   | Dispatching request of type CallToolRequest
aviation-mcp-1   | 2026-02-09 21:02:06 [httpx] INFO: HTTP Request: GET http://weather:5003/api/weather?airport=XXX "HTTP/1.1 200 OK"
aviation-mcp-1   | HTTP Request: GET http://weather:5003/api/weather?airport=XXX "HTTP/1.1 200 OK"
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.lowlevel.server] DEBUG: Response sent
aviation-mcp-1   | Response sent
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=9, result={'content': [{'type': 'text', 'text': 'No weather data found for the specified airport.'}], 'structuredContent': {'result': 'No weather data found for the specified airport.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | 2026-02-09 21:02:06 [mcp.server.sse] DEBUG: Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=9, result={'content': [{'type': 'text', 'text': 'No weather data found for the specified airport.'}], 'structuredContent': {'result': 'No weather data found for the specified airport.'}, 'isError': False})), metadata=None)
aviation-mcp-1   | Sending message via SSE: SessionMessage(message=JSONRPCMessage(root=JSONRPCResponse(jsonrpc='2.0', id=9, result={'content': [{'type': 'text', 'text': 'No weather data found for the specified airport.'}], 'structuredContent': {'result': 'No weather data found for the specified airport.'}, 'isError': False})), metadata=None)