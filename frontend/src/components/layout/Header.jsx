import { Menu } from "lucide-react";

export default function Header() {
  return (
    <header className="h-16 border-b border-border/50 bg-background/50 backdrop-blur-xl flex items-center justify-between px-6 z-10 sticky top-0">
      <div className="flex items-center">
        <button className="p-2 mr-2 md:hidden text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors">
          <Menu className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-semibold tracking-tight">AI Assistant</h1>
      </div>
      
      <div className="flex items-center space-x-4">
        {/* Placeholder for theme toggle or profile if needed */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-accent flex items-center justify-center shadow-sm">
          <span className="text-xs font-bold text-primary-foreground">AI</span>
        </div>
      </div>
    </header>
  );
}
