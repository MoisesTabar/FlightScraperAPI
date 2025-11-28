# Voice Input Structured Output Template

This file defines the structure of the output that the voice recognition endpoint should return after processing audio input.

## Output Format

When a user sends audio to the voice endpoint, the AI will:
1. Transcribe the audio using OpenAI Whisper
2. Extract structured information from the transcription
3. Return data in the following format:

```json
{
  "transcription": "Full text of what the user said",
  "summary": "Brief summary of the user's request",
  "extracted_data": {
    "departure": "Departure airport code or city",
    "destination": "Destination airport code or city",
    "departure_date": "Date in YYYY-MM-DD format",
    "return_date": "Return date in YYYY-MM-DD format (if mentioned)",
    "ticket_type": "One Way, Round Trip, or Multi-City",
    "flight_type": "Economy, Premium Economy, Business, or First",
    "passengers": {
      "Adult": 1,
      "Children": 0,
      "Infants In Seat": 0,
      "Infants On Lap": 0
    }
  },
  "confidence": "high/medium/low",
  "missing_fields": ["List of required fields that couldn't be extracted"]
}
```

## Field Descriptions

### `transcription`
- The complete, verbatim transcription of the audio input
- Type: `string`

### `summary`
- A concise summary of the user's flight search request
- Type: `string`
- Example: "User wants to book a round trip flight from New York to London for 2 adults in business class"

### `extracted_data`
- Structured flight search parameters extracted from the voice input
- This should match the `SearchParams` model structure where possible
- Fields:
  - **departure**: Airport code or city name (will be normalized)
  - **destination**: Airport code or city name (will be normalized)
  - **departure_date**: Date in YYYY-MM-DD format
  - **return_date**: Optional, only if round trip is mentioned
  - **ticket_type**: "One Way", "Round Trip", or "Multi-City"
  - **flight_type**: "Economy", "Premium Economy", "Business", or "First"
  - **passengers**: Object with passenger counts by type

### `confidence`
- AI's confidence level in the extraction accuracy
- Values: `"high"`, `"medium"`, `"low"`
- Based on clarity of audio and completeness of information

### `missing_fields`
- Array of field names that are required but couldn't be extracted from the audio
- Type: `array of strings`
- Example: `["return_date", "passengers"]`

## Example User Voice Inputs

### Example 1: Simple One-Way Flight
**User says:** "I need a flight from JFK to London on March 15th, 2026 for one person"

**Expected Output:**
```json
{
  "transcription": "I need a flight from JFK to London on March 15th, 2026 for one person",
  "summary": "One-way flight from JFK to London on March 15, 2026 for 1 adult",
  "extracted_data": {
    "departure": "JFK",
    "destination": "London",
    "departure_date": "2026-03-15",
    "ticket_type": "One Way",
    "flight_type": "Economy",
    "passengers": {
      "Adult": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 2: Round Trip with Multiple Passengers
**User says:** "Book a round trip from Miami to Paris, leaving May 1st and returning May 15th for two adults and one child in business class"

**Expected Output:**
```json
{
  "transcription": "Book a round trip from Miami to Paris, leaving May 1st and returning May 15th for two adults and one child in business class",
  "summary": "Round trip from Miami to Paris (May 1-15, 2026) for 2 adults and 1 child in business class",
  "extracted_data": {
    "departure": "Miami",
    "destination": "Paris",
    "departure_date": "2026-05-01",
    "return_date": "2026-05-15",
    "ticket_type": "Round Trip",
    "flight_type": "Business",
    "passengers": {
      "Adult": 2,
      "Children": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 3: Incomplete Information
**User says:** "I want to fly to Tokyo sometime next month"

**Expected Output:**
```json
{
  "transcription": "I want to fly to Tokyo sometime next month",
  "summary": "Flight to Tokyo, specific dates and departure location not specified",
  "extracted_data": {
    "destination": "Tokyo",
    "ticket_type": "One Way",
    "flight_type": "Economy",
    "passengers": {
      "Adult": 1
    }
  },
  "confidence": "low",
  "missing_fields": ["departure", "departure_date"]
}
```

### Example 4: Multi-City
**User says:** "I want to fly to Tokyo and then to Paris for two adults, one child and one infant on lap in premium economy class on the 15th of March to the 25th of March"

**Expected Output:**
```json
{
  "transcription": "I want to fly to Tokyo and then to Paris for two adults, one child and one infant on lap in premium economy class on the 15th of March to the 25th of March",
  "summary": "Flight to Tokyo and then to Paris for two adults, one child and one infant in lap in premium economy class on the 15th of March to the 25th of March",
  "extracted_data": {
    "departure": ["Tokyo", "Paris"],
    "destination": ["Paris", "Tokyo"],
    "departure_date": ["2026-03-15", "2026-03-25"],
    "ticket_type": "Multi-City",
    "flight_type": "Premium Economy",
    "city_amount": 1,
    "passengers": {
        "Adult": 2,
        "Children": 1,
        "Infants On Lap": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

---

## Customization Instructions

You can modify this template to change:
1. **Output fields**: Add or remove fields from `extracted_data`
2. **Field types**: Change data types or add validation rules
3. **Examples**: Add more examples to guide the AI's extraction logic
4. **Confidence criteria**: Define what constitutes high/medium/low confidence
5. **Passenger types**: If provided with "Infants_In_Lap" or "Infants_In_Seat", convert to "Infants In Lap" or "Infants In Seat" in the output JSON  

Save this file and the voice endpoint will use it as a reference for structuring the AI's output.
