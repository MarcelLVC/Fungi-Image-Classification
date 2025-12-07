import { Button } from "@/components/ui/button"
import { ArrowDown, Sparkles, Shield, Zap } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-background py-20 sm:py-32">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-[0.03]">
        <svg className="h-full w-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
              <circle cx="1" cy="1" r="1" fill="currentColor" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Sparkles className="h-4 w-4" />
            AI-Powered Analysis
          </div>

          {/* Heading */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-foreground mb-6 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-100 text-balance">
            Microscopic Fungi
            <span className="block text-primary">Detection System</span>
          </h1>

          {/* Description */}
          <p className="max-w-2xl mx-auto text-lg text-muted-foreground mb-10 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-200 text-pretty">
            Advanced machine learning classification for microscopic fungal images. Upload your sample and get instant,
            accurate species identification using GLCM, LBP, and HSV feature extraction.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-in fade-in slide-in-from-bottom-4 duration-500 delay-300">
            <Button
              size="lg"
              className="bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:scale-105 hover:shadow-lg"
              asChild
            >
              <a href="#detection">
                Start Analysis
                <ArrowDown className="ml-2 h-4 w-4" />
              </a>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-border hover:bg-muted transition-all duration-200 bg-transparent"
            >
              Learn More
            </Button>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500 delay-400">
            <div className="flex flex-col items-center p-6 rounded-xl bg-card border border-border hover:border-primary/30 transition-colors duration-300">
              <div className="p-3 rounded-lg bg-primary/10 mb-3">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <span className="text-2xl font-bold text-foreground">Fast</span>
              <span className="text-sm text-muted-foreground">Instant Results</span>
            </div>
            <div className="flex flex-col items-center p-6 rounded-xl bg-card border border-border hover:border-primary/30 transition-colors duration-300">
              <div className="p-3 rounded-lg bg-primary/10 mb-3">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <span className="text-2xl font-bold text-foreground">Accurate</span>
              <span className="text-sm text-muted-foreground">ML-Based</span>
            </div>
            <div className="flex flex-col items-center p-6 rounded-xl bg-card border border-border hover:border-primary/30 transition-colors duration-300">
              <div className="p-3 rounded-lg bg-primary/10 mb-3">
                <Sparkles className="h-6 w-6 text-primary" />
              </div>
              <span className="text-2xl font-bold text-foreground">Simple</span>
              <span className="text-sm text-muted-foreground">Easy to Use</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
