from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

ISS_API_URL = "http://api.open-notify.org/iss-now.json"

@app.get("/")
async def get_iss_location():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ISS_API_URL)
            response.raise_for_status()
            data = response.json()

        # Validate the response structure
        if data.get("message") != "success":
            raise HTTPException(status_code=500, detail="API did not return success message")

        iss_position = data.get("iss_position")
        timestamp = data.get("timestamp")

        if not timestamp or not iss_position:
            raise HTTPException(status_code=500, detail="Invalid API response")

        latitude = iss_position.get("latitude")
        longitude = iss_position.get("longitude")

        if latitude is None or longitude is None:
            raise HTTPException(status_code=500, detail="Incomplete position data")

        return {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the ISS API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
