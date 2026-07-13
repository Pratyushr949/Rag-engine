import { NavLink } from "react-router-dom";
import { MessageSquare, UploadCloud, FileText } from "lucide-react";
import { cn } from "../../utils/cn";

export default function Sidebar() {
  const navItems = [
    { name: "Chat", path: "/chat", icon: MessageSquare },
    { name: "Upload Documents", path: "/upload", icon: UploadCloud },
  ];

  return (
    <aside className="w-64 h-full border-r border-border/50 bg-background/50 backdrop-blur-xl flex flex-col hidden md:flex">
      <div className="h-16 flex items-center px-6 border-b border-border/50">
        <FileText className="w-6 h-6 text-primary mr-2" />
        <span className="font-bold text-lg tracking-tight">RAG Engine</span>
      </div>
      
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <p className="px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">
          Menu
        </p>
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-primary/10 text-primary shadow-sm"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )
            }
          >
            <item.icon className="w-4 h-4 mr-3" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-border/50">
        <div className="flex items-center px-3 py-2 rounded-lg bg-muted/50 border border-border/50">
          <div className="w-2 h-2 rounded-full bg-green-500 mr-3 animate-pulse"></div>
          <span className="text-xs font-medium text-muted-foreground">System Online</span>
        </div>
      </div>
    </aside>
  );
}
