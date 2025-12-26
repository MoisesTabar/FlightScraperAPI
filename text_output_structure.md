# Text Input Structured Output Template

This file defines the structure of the output that the text recognition endpoint should return after processing text input.

## Output Format

When a user sends text to the text endpoint, the AI will:
1. Parse the text describing the desired flight
2. Extract structured information from the text
3. Return data in the following format:

```json
{
  "input_text": "Full text of what the user wrote",
  "summary": "Brief summary of the user's request",
  "extracted_data": {
    "departure": "Departure airport code or city",
    "destination": "Destination airport code or city",
    "departure_date": "Date in YYYY-MM-DD format",
    "return_date": "Return date in YYYY-MM-DD format (if mentioned)",
    "ticket_type": "One Way, Round Trip, or Multi-City",
    "flight_type": "Economy, Premium Economy, Business, or First",
    "city_amount": "Number of cities in the trip (Multi-City only) spawns one when there are more than 2 cities",
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

### `input_text`
- The complete, verbatim text input provided by the user
- Type: `string`

### `summary`
- A concise summary of the user's flight search request
- Type: `string`
- Example: "User wants to book a round trip flight from New York to London for 2 adults in business class"

### `extracted_data`
- Structured flight search parameters extracted from the text input
- This should match the `SearchParams` model structure where possible
- Fields:
  - **departure**: Airport code or city name (will be normalized)
  - **destination**: Airport code or city name (will be normalized)
  - **departure_date**: Date in YYYY-MM-DD format
  - **return_date**: Optional, only if round trip is mentioned
  - **ticket_type**: "One Way", "Round Trip", or "Multi-City"
  - **flight_type**: "Economy", "Premium Economy", "Business", or "First"
  - **passengers**: Object with passenger counts by type
  - **city_amount**: Number of cities in the trip (Multi-City only) Google Flights spawns 2 selectors when multi-city is selected so it will spawn one when there are more than 2 cities, and it will spawn two when there are more than 3 cities so on and so forth.

### `confidence`
- AI's confidence level in the extraction accuracy
- Values: `"high"`, `"medium"`, `"low"`
- Based on clarity of text and completeness of information

### `missing_fields`
- Array of field names that are required but couldn't be extracted from the text
- Type: `array of strings`
- Example: `["return_date", "passengers"]`

## Example User Text Inputs

### Example 1: Simple Round Trip
**User writes:** "Round Trip Flight from Santiago de los Caballeros to New York from December 27th to January 10th"

**Expected Output:**
```json
{
  "input_text": "Round Trip Flight from Santiago de los Caballeros to New York from December 27th to January 10th",
  "summary": "Round trip from Santiago de los Caballeros to New York (December 27, 2025 - January 10, 2026) for 1 adult",
  "extracted_data": {
    "departure": "Santiago de los Caballeros",
    "destination": "New York",
    "departure_date": "2025-12-27",
    "return_date": "2026-01-10",
    "ticket_type": "Round Trip",
    "flight_type": "Economy",
    "passengers": {
      "Adult": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 2: One-Way with Specific Class
**User writes:** "One way flight from Miami to Los Angeles on March 20th 2026 in business class for two adults"

**Expected Output:**
```json
{
  "input_text": "One way flight from Miami to Los Angeles on March 20th 2026 in business class for two adults",
  "summary": "One-way flight from Miami to Los Angeles on March 20, 2026 for 2 adults in business class",
  "extracted_data": {
    "departure": "Miami",
    "destination": "Los Angeles",
    "departure_date": "2026-03-20",
    "ticket_type": "One Way",
    "flight_type": "Business",
    "passengers": {
      "Adult": 2
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 3: Round Trip with Multiple Passengers
**User writes:** "Round trip Chicago to Tokyo May 5 to May 20 for 2 adults and 3 children in premium economy"

**Expected Output:**
```json
{
  "input_text": "Round trip Chicago to Tokyo May 5 to May 20 for 2 adults and 3 children in premium economy",
  "summary": "Round trip from Chicago to Tokyo (May 5-20, 2026) for 2 adults and 3 children in premium economy",
  "extracted_data": {
    "departure": "Chicago",
    "destination": "Tokyo",
    "departure_date": "2026-05-05",
    "return_date": "2026-05-20",
    "ticket_type": "Round Trip",
    "flight_type": "Premium Economy",
    "passengers": {
      "Adult": 2,
      "Children": 3
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 4: Incomplete Information
**User writes:** "Flight to Paris next week"

**Expected Output:**
```json
{
  "input_text": "Flight to Paris next week",
  "summary": "Flight to Paris, specific dates and departure location not specified",
  "extracted_data": {
    "destination": "Paris",
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

### Example 5: Multi-City Trip
**User writes:** "Multi-city flight from New York to London to Dubai, one adult and one child in first class from June 1st, June 8th, June 15th 2026"

**Expected Output:**
```json
{
  "input_text": "Multi-city flight from New York to London to Dubai, one adult and one child in first class from June 1st, June 8th, June 15th 2026",
  "summary": "Multi-city flight from New York to London to Dubai for 1 adult and 1 child in first class on June 1, 8, and 15, 2026",
  "extracted_data": {
    "departure": ["New York", "London", "Dubai"],
    "destination": ["London", "Dubai", "New York"],
    "departure_date": ["2026-06-01", "2026-06-08", "2026-06-15"],
    "ticket_type": "Multi-City",
    "flight_type": "First",
    "city_amount": 1,
    "passengers": {
      "Adult": 1,
      "Children": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 6: Round Trip with Infants
**User writes:** "Round trip from Boston to Barcelona July 10 to July 24 for 2 adults, 1 child, and 1 infant on lap in economy"

**Expected Output:**
```json
{
  "input_text": "Round trip from Boston to Barcelona July 10 to July 24 for 2 adults, 1 child, and 1 infant on lap in economy",
  "summary": "Round trip from Boston to Barcelona (July 10-24, 2026) for 2 adults, 1 child, and 1 infant on lap in economy",
  "extracted_data": {
    "departure": "Boston",
    "destination": "Barcelona",
    "departure_date": "2026-07-10",
    "return_date": "2026-07-24",
    "ticket_type": "Round Trip",
    "flight_type": "Economy",
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

### Example 7: Multi-City with Multiple Stops
**User writes:** "Multi-city from San Francisco to Rome to Amsterdam to San Francisco, 3 adults in business, departing April 1, April 10, April 20, 2026"

**Expected Output:**
```json
{
  "input_text": "Multi-city from San Francisco to Rome to Amsterdam to San Francisco, 3 adults in business, departing April 1, April 10, April 20, 2026",
  "summary": "Multi-city flight from San Francisco to Rome to Amsterdam to San Francisco for 3 adults in business class on April 1, 10, and 20, 2026",
  "extracted_data": {
    "departure": ["San Francisco", "Rome", "Amsterdam", "San Francisco"],
    "destination": ["Rome", "Amsterdam", "San Francisco", "Rome"],
    "departure_date": ["2026-04-01", "2026-04-10", "2026-04-20"],
    "ticket_type": "Multi-City",
    "flight_type": "Business",
    "city_amount": 2,
    "passengers": {
      "Adult": 3
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
6. **Children specification**: If provided with "Children In / On Lap" or "Children In / On Seat", convert to "Infants On Lap" or "Infants In Seat" in the output JSON

Save this file and the text endpoint will use it as a reference for structuring the AI's output.