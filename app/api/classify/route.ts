import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()

    // Forward the request to the local Python Flask server
    // running on port 5000
    const response = await fetch("http://127.0.0.1:5000/classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
       const errorData = await response.json().catch(() => ({}));
       return NextResponse.json(
         { error: errorData.error || "Python server error" }, 
         { status: response.status }
       )
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error("Error communicating with classification server:", error)
    return NextResponse.json(
      { error: "Failed to connect to classification server. Make sure the Python script is running." }, 
      { status: 500 }
    )
  }
}