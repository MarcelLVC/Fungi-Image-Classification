"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Upload, X, Loader2, CheckCircle, AlertCircle, ImageIcon } from "lucide-react"
import Image from "next/image"

interface PredictionResult {
  class: string
  confidence: number
  features: {
    glcm: number[]
    lbp: number[]
    hsv: number[]
  }
}

export function DetectionSection() {
  const [image, setImage] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setFileName(file.name)
      setResult(null)
      setError(null)
      const reader = new FileReader()
      reader.onload = (e) => {
        setImage(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"],
    },
    multiple: false,
  })

  const handleAnalyze = async () => {
    if (!image) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/classify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
      })

      if (!response.ok) {
        throw new Error("Classification failed")
      }

      const data = await response.json()
      setResult(data)
    } catch {
      setError("Failed to classify image. Please ensure the model server is running.")
    } finally {
      setIsLoading(false)
    }
  }

  const clearImage = () => {
    setImage(null)
    setFileName("")
    setResult(null)
    setError(null)
  }

  return (
    <section id="detection" className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">Analyze Your Sample</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Upload a microscopic image of fungi and our AI model will classify the species using advanced feature
            extraction techniques.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Upload Area */}
          <Card className="border-border bg-card overflow-hidden">
            <CardContent className="p-6">
              <h3 className="font-semibold text-foreground mb-4 flex items-center gap-2">
                <Upload className="h-5 w-5 text-primary" />
                Upload Image
              </h3>

              {!image ? (
                <div
                  {...getRootProps()}
                  className={`
                    border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
                    transition-all duration-300 ease-out
                    ${
                      isDragActive
                        ? "border-primary bg-primary/5 scale-[1.02]"
                        : "border-border hover:border-primary/50 hover:bg-muted/50"
                    }
                  `}
                >
                  <input {...getInputProps()} />
                  <div className="flex flex-col items-center gap-4">
                    <div
                      className={`
                      p-4 rounded-full bg-primary/10 
                      transition-transform duration-300
                      ${isDragActive ? "scale-110" : ""}
                    `}
                    >
                      <ImageIcon className="h-8 w-8 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium text-foreground mb-1">
                        {isDragActive ? "Drop your image here" : "Drag & drop your image"}
                      </p>
                      <p className="text-sm text-muted-foreground">or click to browse files</p>
                    </div>
                    <p className="text-xs text-muted-foreground">Supports PNG, JPG, TIFF, BMP</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative aspect-square rounded-xl overflow-hidden bg-muted">
                    <Image
                      src={image || "/placeholder.svg"}
                      alt="Uploaded microscopic image"
                      fill
                      className="object-contain"
                    />
                    <button
                      onClick={clearImage}
                      className="absolute top-2 right-2 p-2 rounded-full bg-background/80 hover:bg-background transition-colors"
                    >
                      <X className="h-4 w-4 text-foreground" />
                    </button>
                  </div>
                  <p className="text-sm text-muted-foreground truncate">{fileName}</p>
                  <Button
                    onClick={handleAnalyze}
                    disabled={isLoading}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:scale-[1.02]"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Sparkles className="mr-2 h-4 w-4" />
                        Analyze Image
                      </>
                    )}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Area */}
          <Card className="border-border bg-card">
            <CardContent className="p-6">
              <h3 className="font-semibold text-foreground mb-4 flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-primary" />
                Classification Results
              </h3>

              {!result && !error && !isLoading && (
                <div className="flex flex-col items-center justify-center h-64 text-center">
                  <div className="p-4 rounded-full bg-muted mb-4">
                    <ImageIcon className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <p className="text-muted-foreground">Upload and analyze an image to see results</p>
                </div>
              )}

              {isLoading && (
                <div className="flex flex-col items-center justify-center h-64">
                  <Loader2 className="h-12 w-12 text-primary animate-spin mb-4" />
                  <p className="text-muted-foreground">Processing image...</p>
                  <p className="text-sm text-muted-foreground mt-2">Extracting GLCM, LBP, and HSV features</p>
                </div>
              )}

              {error && (
                <div className="flex flex-col items-center justify-center h-64 text-center">
                  <div className="p-4 rounded-full bg-destructive/10 mb-4">
                    <AlertCircle className="h-8 w-8 text-destructive" />
                  </div>
                  <p className="text-destructive font-medium mb-2">Analysis Failed</p>
                  <p className="text-sm text-muted-foreground max-w-xs">{error}</p>
                </div>
              )}

              {result && (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
                  <div className="p-6 rounded-xl bg-primary/5 border border-primary/20">
                    <p className="text-sm text-muted-foreground mb-2">Detected Species</p>
                    <p className="text-2xl font-bold text-foreground">{result.class}</p>
                    <div className="mt-4">
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-muted-foreground">Confidence</span>
                        <span className="font-medium text-foreground">{(result.confidence * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-2 rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full bg-primary rounded-full transition-all duration-500"
                          style={{ width: `${result.confidence * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <h4 className="font-medium text-foreground text-sm">Extracted Features</h4>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="p-3 rounded-lg bg-muted/50 text-center">
                        <p className="text-xs text-muted-foreground mb-1">GLCM</p>
                        <p className="text-sm font-medium text-foreground">{result.features.glcm.length} features</p>
                      </div>
                      <div className="p-3 rounded-lg bg-muted/50 text-center">
                        <p className="text-xs text-muted-foreground mb-1">LBP</p>
                        <p className="text-sm font-medium text-foreground">{result.features.lbp.length} features</p>
                      </div>
                      <div className="p-3 rounded-lg bg-muted/50 text-center">
                        <p className="text-xs text-muted-foreground mb-1">HSV</p>
                        <p className="text-sm font-medium text-foreground">{result.features.hsv.length} features</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

function Sparkles(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
      <path d="M5 3v4" />
      <path d="M19 17v4" />
      <path d="M3 5h4" />
      <path d="M17 19h4" />
    </svg>
  )
}
