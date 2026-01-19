import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()
    
    const apiUrl = process.env.NODE_ENV === 'development' 
      ? "http://127.0.0.1:5000/classify" 
      : `${process.env.NEXT_PUBLIC_VERCEL_URL || ''}/api/classify-py`; 

    const response = await fetch(new URL('/api/classify-py', request.url), {
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
      { error: "Failed to connect to classification server." }, 
      { status: 500 }
    )
  }
}
