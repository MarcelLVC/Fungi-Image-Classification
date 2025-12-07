import { Layers, Scan, BarChart3, Cpu } from "lucide-react"

const features = [
  {
    icon: Layers,
    title: "GLCM Analysis",
    description:
      "Gray Level Co-occurrence Matrix extracts texture features including contrast, homogeneity, energy, and correlation.",
  },
  {
    icon: Scan,
    title: "LBP Extraction",
    description:
      "Local Binary Pattern captures local texture information invariant to rotation and illumination changes.",
  },
  {
    icon: BarChart3,
    title: "HSV Histograms",
    description: "Color histogram analysis in HSV space captures hue, saturation, and value distributions.",
  },
  {
    icon: Cpu,
    title: "Random Forest",
    description:
      "Ensemble machine learning model trained on combined features for accurate multi-class classification.",
  },
]

export function FeaturesSection() {
  return (
    <section id="features" className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">How It Works</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Our system combines multiple feature extraction techniques with machine learning for accurate fungi
            classification.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="group p-6 rounded-xl bg-card border border-border hover:border-primary/30 hover:shadow-lg transition-all duration-300 animate-in fade-in slide-in-from-bottom-4"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="p-3 rounded-lg bg-primary/10 w-fit mb-4 group-hover:bg-primary/20 group-hover:scale-110 transition-all duration-300">
                <feature.icon className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
