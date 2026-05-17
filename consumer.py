import json
import random

import flask
from flask import Flask, request

#DESIGN PATTERN 2: CHAIN OF RESPONSIBILITY

# The base class that links our pipeline together
class AbstractHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler # Returning the handler allows us to chain them: a.set_next(b).set_next(c)

    def handle(self, request_data):
        if self.next_handler:
            return self.next_handler.handle(request_data)
        return request_data

# DESIGN PATTERN 3: STRATEGY PATTERN

# The "Protocol" (Base Strategy)
class formatterStrategy:
    def format(self, data):
        pass

# Strategy 1: For Developers
class JSONFormatterStrategy(formatterStrategy):
    def format(self, data):
        return json.dumps(data, indent=2)

# Strategy 2: For Security
class CsvFormatterStrategy(formatterStrategy):
    def format(self, data):
        headers = ",".join(data.keys())
        values = ",".join(str(v) for v in data.values())
        return f"{headers}\n{values}"

# Strategy 3: For SysAdmins
class HtmlFormatterStrategy(formatterStrategy):
    def format(self, data):
        html = "<ul>\n"
        for key, value in data.items():
            html += f"<li><strong>{key}:</strong> {value}</li>\n"
        html += "</ul>"
        return html

# Stage 1: KVKK / GDPR Anonymization (Security)
class KVKKFilterHandler(AbstractHandler):
    def handle(self, request_data):
        print("Stage 1: KVKK Anonymization....")

        # PRIVACY: Mask the credit card
        if request_data.get('credit_card'):
            request_data['credit_card'] = "****-****-****-" + request_data['credit_card'][-4:]

        # PRIVACY: Mask the password
        if request_data.get('password'):
            request_data['password'] = "********"

        # PRIVACY: Mask the email
        if request_data.get('email'):
            parts = request_data['email'].split('@')
            if len(parts) == 2:
                request_data['email'] = parts[0][0] + "***@" + parts[1]

        # PRIVACY: Mask user_id (TC Kimlik No simulation)
        if request_data.get('user_id'):
            request_data['user_id'] = "ID-***" + str(request_data['user_id'])[-2:]

        return super().handle(request_data)

# Stage 2: Enrichment (Zenginleştirme)
class EnrichmentHandler(AbstractHandler):
    def handle(self, request_data):
        print("Stage 2: Data Enrichment...")

        # Adding mandatory tags for microservices
        request_data['sender_id'] = request_data.get('user_id')
        request_data['transaction_no'] = request_data.get('token')
        request_data['status'] = "CRITICAL" if request_data.get('level') == "ERROR" else "NORMAL"
        request_data['message'] = f"Processed log for {request_data.get('user_id')}"
        request_data['debug_info'] = f"Level: {request_data.get('level')}, Time: {request_data.get('transaction_time')}"

        return super().handle(request_data)

# Stage 3: Formatting (Biçimlendirme)
class FormattingHandler(AbstractHandler):
    def handle(self, request_data):
        print("Stage 3: Applying Strategy Pattern for Formatting...")

        # Simulate a request coming from one of the three departments
        target_department = random.choice(["DEV", "GÜV", "SYS YÖN"])

        # Dynamically choose the strategy based on the department
        if target_department == "DEV":
            strategy = JSONFormatterStrategy()
        elif target_department == "GÜV":
            strategy = CsvFormatterStrategy()
        else:
            strategy = HtmlFormatterStrategy()

        # Execute the chosen strategy
        final_output = strategy.format(request_data)

        print(f"\n✅ FINAL OUTPUT DELIVERED TO [{target_department}]:")
        print(final_output)
        print("-" * 40)

        # We don't call super().handle() here because this is the end of the chain!
        return request_data


# THE SERVER (Receives data from Container 1)
app = Flask(__name__)

# Build the chain!
pipeline_start = KVKKFilterHandler()
pipeline_start.set_next(EnrichmentHandler()).set_next(FormattingHandler())


@app.route('/ingest', methods=['POST'])
def ingest_log():
    raw_log = request.json
    print(f"\n--- Incoming Log for User {raw_log.get('user_id')} ---")

    # Push the raw log into the start of our pipeline
    processed_log = pipeline_start.handle(raw_log)

    if processed_log:
        print(f"Final Output: {json.dumps(processed_log, indent=2)}")
        return {"status": "success"}, 200
    else:
        return {"status": "dropped"}, 200

if __name__ == '__main__':
    print("Consumer listening on port 5001...")
    app.run(host="0.0.0.0", port=5001)