from winevt import EventLog

query = EventLog.Query("Application","Event/System/Provider[@Name='Windows Error Reporting']")

for event in query:
    for item in event.EventData.Data:
        