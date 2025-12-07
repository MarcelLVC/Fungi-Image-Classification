import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { DetectionSection } from "@/components/detection-section"
import { FeaturesSection } from "@/components/features-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Navbar />
      <HeroSection />
      <DetectionSection />
      <FeaturesSection />
      <Footer />
    </main>
  )
}
