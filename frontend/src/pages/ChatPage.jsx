import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, BookOpen, Trash2 } from "lucide-react";
import { chatWithBot, resetSystem } from "../services/api";
import { cn } from "../utils/cn";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am your RAG AI Assistant. Ask me anything about your uploaded documents." }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const [expandedSources, setExpandedSources] = useState({});
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => scrollToBottom(), [messages, isTyping]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMsg = input.trim();
    setInput("");
    setError(null);
    
    // Optimistic UI update
    const newMessages = [...messages, { role: "user", content: userMsg }];
    setMessages(newMessages);
    setIsTyping(true);

    try {
      const response = await chatWithBot(userMsg, newMessages);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
        page_numbers: response.page_numbers,
        confidence: response.confidence
      }]);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to fetch response.");
    } finally {
      setIsTyping(false);
    }
  };

  const handleClearChat = async () => {
    if (!confirm("Are you sure you want to reset the system? This will delete all uploaded documents, vector databases, and clear this chat.")) return;
    
    try {
      await resetSystem();
      setMessages([{ role: "assistant", content: "System reset successful. The database is now empty. Please upload new documents." }]);
      setExpandedSources({});
      setError(null);
    } catch (err) {
      setError("Failed to reset system: " + (err.response?.data?.detail || err.message));
    }
  };

  const toggleSources = (index) => {
    setExpandedSources(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto px-4 py-6 relative">
      {/* Header Actions */}
      <div className="flex justify-end mb-4">
        <button
          onClick={handleClearChat}
          className="flex items-center px-3 py-1.5 text-xs font-medium text-destructive hover:bg-destructive/10 rounded-md transition-colors border border-destructive/20"
        >
          <Trash2 className="w-3.5 h-3.5 mr-1.5" />
          Reset System
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 glass-dark rounded-2xl border border-border/50 overflow-hidden flex flex-col shadow-sm">
        
        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={cn("flex w-full animate-fade-in", msg.role === "user" ? "justify-end" : "justify-start")}>
              
              {/* Avatar for AI */}
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mr-3 shrink-0 mt-1">
                  <Bot className="w-4 h-4 text-primary" />
                </div>
              )}

              <div className={cn(
                "max-w-[85%] rounded-2xl px-5 py-3.5",
                msg.role === "user" 
                  ? "bg-primary text-primary-foreground rounded-tr-sm shadow-md" 
                  : "bg-muted/50 border border-border/50 rounded-tl-sm text-foreground"
              )}>
                <div className="prose prose-sm dark:prose-invert max-w-none break-words">
                  {msg.content}
                </div>

                {/* Sources Viewer Component */}
                {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-border/50">
                    <button 
                      onClick={() => toggleSources(idx)}
                      className="flex items-center text-xs font-medium text-muted-foreground hover:text-primary transition-colors"
                    >
                      <BookOpen className="w-3.5 h-3.5 mr-1.5" />
                      {expandedSources[idx] ? "Hide Sources" : `View ${msg.sources.length} Sources`}
                    </button>
                    
                    {expandedSources[idx] && (
                      <div className="mt-2 space-y-2 animate-accordion-down overflow-hidden">
                        {msg.sources.map((source, sIdx) => {
                          const fileName = source.split('/').pop() || source.split('\\').pop();
                          return (
                            <div key={sIdx} className="bg-background rounded p-2 text-xs border border-border/40 flex justify-between items-center">
                              <span className="font-medium text-primary truncate mr-2" title={source}>{fileName}</span>
                              {msg.page_numbers && msg.page_numbers.length > 0 && (
                                <span className="bg-muted px-1.5 py-0.5 rounded text-[10px] whitespace-nowrap">
                                  Page {msg.page_numbers.join(", ")}
                                </span>
                              )}
                            </div>
                          )
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Avatar for User */}
              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center ml-3 shrink-0 mt-1 border border-border/50">
                  <User className="w-4 h-4 text-secondary-foreground" />
                </div>
              )}
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex w-full justify-start animate-fade-in">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mr-3 shrink-0 mt-1">
                <Bot className="w-4 h-4 text-primary" />
              </div>
              <div className="bg-muted/50 border border-border/50 rounded-2xl rounded-tl-sm px-5 py-4 flex items-center space-x-1">
                <div className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <div className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <div className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce" />
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="px-6 py-2 bg-destructive/10 text-destructive text-xs font-medium border-t border-destructive/20 text-center">
            {error}
          </div>
        )}

        {/* Input Area */}
        <div className="p-4 border-t border-border/50 bg-background/50">
          <form onSubmit={handleSend} className="relative flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your documents..."
              disabled={isTyping}
              className="w-full bg-muted/30 border border-border/60 rounded-full pl-5 pr-12 py-3.5 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 text-sm"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="absolute right-2 p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-transform disabled:opacity-50 disabled:hover:bg-primary disabled:scale-100 hover:scale-105"
            >
              {isTyping ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" /> }
            </button>
          </form>
          <div className="text-center mt-2">
            <p className="text-[10px] text-muted-foreground">AI can make mistakes. Check important info from the provided sources.</p>
          </div>
        </div>
        
      </div>
    </div>
  );
}
