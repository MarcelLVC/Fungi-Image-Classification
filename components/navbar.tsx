"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Menu, X, Microscope } from "lucide-react"

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2 group">
            <span className="font-semibold text-lg text-foreground">FungiScope</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              href="#detection"
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 text-sm font-medium"
            >
              Detection
            </Link>
            <Link
              href="#features"
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 text-sm font-medium"
            >
              Features
            </Link>
            <Link
              href="#about"
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 text-sm font-medium"
            >
              About
            </Link>
            <Button
              size="sm"
              className="bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:scale-105"
            >
              Get Started
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-md hover:bg-muted transition-colors"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="h-5 w-5 text-foreground" /> : <Menu className="h-5 w-5 text-foreground" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-border animate-in slide-in-from-top-2 duration-200">
            <div className="flex flex-col gap-4">
              <Link
                href="#detection"
                className="text-muted-foreground hover:text-foreground transition-colors px-2 py-1"
                onClick={() => setIsOpen(false)}
              >
                Detection
              </Link>
              <Link
                href="#features"
                className="text-muted-foreground hover:text-foreground transition-colors px-2 py-1"
                onClick={() => setIsOpen(false)}
              >
                Features
              </Link>
              <Link
                href="#about"
                className="text-muted-foreground hover:text-foreground transition-colors px-2 py-1"
                onClick={() => setIsOpen(false)}
              >
                About
              </Link>
              <Button size="sm" className="w-fit bg-primary hover:bg-primary/90 text-primary-foreground">
                Get Started
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
