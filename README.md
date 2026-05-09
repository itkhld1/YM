# Real-Time Log Processing System (Microservices)

This project is a containerized microservices architecture built in Python. It simulates a real-time data streaming environment where a Producer application generates sensitive log data, and a Consumer application securely processes, enriches, and formats that data.

## 🏗 System Architecture

The system consists of two separate applications running in isolated Docker containers, communicating over a private Docker network (`pipeline_network`).

1. **Producer (Veri Üretecek):** Generates randomized mock logs including sensitive PII (Personally Identifiable Information) like passwords and credit card numbers.
2. **Consumer (Veriyi Alıp İşleyecek):** Receives the raw logs via HTTP POST requests and runs them through a multi-stage processing pipeline.

## ⚙️ Processing Pipeline (The Consumer)

The Consumer processes incoming data in three distinct stages, fulfilling the assignment requirements:

* **1. Filtre (KVKK/GDPR & Performans):** 
  * **Privacy:** Detects sensitive fields (passwords, credit cards) and anonymizes/masks them.
  * **Performance:** Drops low-priority logs (e.g., `DEBUG` level) entirely to save processing power and storage.
* **2. Zenginleştirme (Enrichment):** Analyzes the incoming data and adds new value. In this system, it calculates and appends a geographical `region` based on the user's ID.
* **3. Biçimlendirme (Formatting):** Dynamically outputs the finalized data into different formats depending on the requesting department (Developer -> JSON, Security -> CSV, SysAdmin -> HTML).

## 🧩 Software Design Patterns Used

To ensure clean, scalable, and maintainable code, this project heavily relies on three specific software design patterns:

### 1. Builder Pattern (Creational)
* **Location:** `producer.py` (`LogBuilder` class)
* **Purpose:** Used to cleanly construct complex, randomized log objects step-by-step. Since logs have many optional and required fields (base info, security info, personal info), the Builder pattern prevents massive, messy constructors.

### 2. Chain of Responsibility Pattern (Behavioral)
* **Location:** `consumer.py` (`AbstractHandler` class)
* **Purpose:** Used to build the core processing pipeline. Instead of a single monolithic function, the data passes through linked handlers (`KVKKFilterHandler -> EnrichmentHandler -> FormattingHandler`). This allows the chain to be broken early (e.g., dropping a `DEBUG` log for performance) without executing the rest of the logic.

### 3. Strategy Pattern (Behavioral)
* **Location:** `consumer.py` (`FormatterStrategy` class)
* **Purpose:** Used to fulfill the "Biçimlendirme" requirement. Instead of hardcoding `if/else` statements for formatting, the system dynamically swaps out algorithms (`JsonFormatter`, `CsvFormatter`, `HtmlFormatter`) based on which department requested the data.

## 🚀 How to Run

Ensure Docker and Docker Compose are installed and running on your machine.

1. Open a terminal in the project root directory.
2. Build and start the containers using the following command:
   ```bash
   docker-compose up --build

3. To run the containers in the background, append -d:
   ```bash
   docker-compose up --build -d

4. To view the clean output logs of the Consumer, run:
   ```bash
   docker-compose logs -f consumer

