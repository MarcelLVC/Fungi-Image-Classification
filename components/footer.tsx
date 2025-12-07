
export function Footer() {
  return (
    <footer id="about" className="bg-card border-t border-border py-12 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-foreground">FungiScope</span>
          </div>

          <p className="text-sm text-muted-foreground text-center">
            AI-powered microscopic fungi detection using GLCM, LBP, and HSV feature extraction 
          </p>

          <p className="text-sm text-muted-foreground">© {new Date().getFullYear()} FungiScope. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
